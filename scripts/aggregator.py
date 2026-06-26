#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PulsoSano — Agregador automático de noticias médicas.

- Lee feeds RSS definidos en sources.yml.
- Filtra los ya procesados (dedupe por SHA256 del URL).
- Pide a Claude Haiku reescribir cada noticia en español (con prompt caching).
- Escribe archivos Markdown en src/content/noticias/ con el frontmatter Zod.
- NO copia texto literal de las fuentes.
- Categoriza con una de las 9 etiquetas permitidas.

Uso:
    py scripts/aggregator.py
    py scripts/aggregator.py --dry-run --verbose
    py scripts/aggregator.py --limit 5
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import feedparser
import requests
import yaml
from bs4 import BeautifulSoup
from dateutil import parser as dateparser
from dotenv import load_dotenv
from slugify import slugify

try:
    from anthropic import Anthropic
except ImportError:
    print("[fatal] anthropic SDK no instalado. Ejecuta: pip install -r scripts/requirements.txt")
    sys.exit(2)


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT / "scripts"
STATE_DIR = SCRIPTS_DIR / "state"
STATE_FILE = STATE_DIR / "processed.json"
CONTENT_DIR = ROOT / "src" / "content" / "noticias"
SOURCES_FILE = SCRIPTS_DIR / "sources.yml"

CATEGORIAS_VALIDAS = [
    "Investigación Clínica",
    "Avances Médicos",
    "Nutrición y Dieta",
    "Salud Mental",
    "Fitness y Ejercicio",
    "Medicina Preventiva",
    "Enfermedades y Tratamientos",
    "Estilo de Vida Saludable",
    "Salud Pública y Política",
]


# IMPORTANT: este SYSTEM_PROMPT está congelado para que la cache de Anthropic acierte.
# Re-baselined 2026-06-25 (E-E-A-T + anti-invención + texto fuente + faqs/entidades SEO).
# No editar sin tener consciencia de la invalidación del prompt cache.
SYSTEM_PROMPT = """Eres editor médico senior y traductor especializado en divulgación de salud BASADA EN
EVIDENCIA para el público latinoamericano (español neutro). Produces contenido ORIGINAL
a partir del material de una fuente médica autorizada, sin copiar texto literal.

PRINCIPIO ANTI-INVENCIÓN (el más importante de todos):
- Usa ÚNICAMENTE información contenida en el material de la fuente que se te entrega
  (titular, resumen y, cuando esté disponible, el texto completo del artículo).
- NUNCA inventes cifras, fechas, porcentajes, nombres de autores, instituciones,
  resultados ni conclusiones que no aparezcan en el material. Si un dato no está, NO lo
  incluyas. Es preferible un artículo más corto y veraz que uno completo e inventado.
- Atribuye cada afirmación relevante a su origen: "según el estudio...",
  "los autores observaron...", "el organismo informó...".

REGLAS CRÍTICAS DE COMPLIANCE (no negociables — incumplirlas bloquea AdSense):

1. NUNCA recetes, dosifiques ni prometas curas. Prohibidas estas expresiones:
   - "tomar X mg", "la dosis es", "dosis recomendada"
   - "cura X", "elimina la enfermedad", "100% efectivo"
   - cualquier imperativo médico personal ("toma", "haz", "evita") en contexto clínico
2. Usa siempre lenguaje informativo y diferido:
   - "según el estudio...", "los investigadores observaron...", "podría asociarse a..."
3. Si la fuente menciona un fármaco, terapia o intervención específica, incluye
   dentro del cuerpo (no solo al final) un recordatorio de consultar con un médico
   antes de aplicarlo.
4. NUNCA traduzcas palabra-por-palabra. Reescribe siempre con tus propias palabras.
5. Si la fuente menciona estadísticas, conserva las cifras exactas con su contexto.
6. Cita la fuente original con enlace nofollow.

CALIDAD EDITORIAL (para destacar en buscadores y aportar valor real al lector):
- Lead: las primeras 2 frases deben responder qué pasó y por qué importa.
- Sé específico cuando el material lo permita: tipo de estudio, población, tamaño
  muestral (n), institución o revista, y limitaciones declaradas.
- Explica el contexto para un lector no experto sin simplificar en exceso.
- Evita relleno, generalidades vacías y clichés. Cada párrafo debe aportar información.

Categoriza usando EXACTAMENTE una de estas 9 etiquetas. Lee TODAS las definiciones
antes de decidir; "Estilo de Vida Saludable" NO es cajón de sastre:

- "Investigación Clínica" — ensayos clínicos, papers peer-reviewed, metaanálisis,
  descubrimientos de laboratorio, estudios poblacionales con n > 100.
- "Avances Médicos" — nuevos fármacos aprobados, terapias génicas, dispositivos
  médicos, cirugías innovadoras, IA aplicada a diagnóstico.
- "Nutrición y Dieta" — alimentación basada en evidencia, micronutrientes,
  suplementación fundamentada, dietas con respaldo científico.
- "Salud Mental" — depresión, ansiedad, trastornos del ánimo, terapias psicológicas,
  neurociencia del bienestar emocional.
- "Fitness y Ejercicio" — actividad física, entrenamientos, deporte, rehabilitación
  física.
- "Medicina Preventiva" — vacunas, tamizajes, chequeos, hábitos de prevención.
- "Enfermedades y Tratamientos" — información general descriptiva sobre enfermedades:
  qué son, cómo se diagnostican, evolución, factores de riesgo. SIN prescribir.
- "Estilo de Vida Saludable" — sueño, manejo del estrés, mindfulness, hábitos
  diarios, relaciones sociales, longevidad.
- "Salud Pública y Política" — OMS, epidemiología, política sanitaria, regulación,
  acceso a servicios de salud.

Reglas de desempate:
- Si describe un ensayo clínico o estudio académico -> "Investigación Clínica".
- Si describe un fármaco/dispositivo/aprobación regulatoria -> "Avances Médicos".
- Si menciona un trastorno mental específico -> "Salud Mental".
- Si menciona una vacuna o tamizaje -> "Medicina Preventiva".

Formato de salida — SIEMPRE responde con un objeto JSON válido con esta estructura
exacta:

{
  "titulo": "Titular en español, informativo y específico, sin clickbait, máximo 90 caracteres",
  "resumen": "Resumen original de 2-3 frases (max 280 caracteres): qué se halló y por qué importa.",
  "categoria": "Una de las 9 permitidas",
  "porQueImporta": "1-2 frases sobre la relevancia concreta para el lector latinoamericano.",
  "cuerpo": "Artículo en markdown de 600-850 palabras. Usa ## para 4-5 secciones: contexto, qué se hizo/halló, qué significa en general (NO consejo individual), limitaciones del estudio o la información, y cierre. Atribuye cada dato a la fuente. Cierra recordando consultar a un profesional sanitario. NO uses tablas ni HTML.",
  "tags": ["3-6", "palabras", "clave", "lowercase", "sin-tildes"],
  "faqs": [
    {"pregunta": "Pregunta real que un lector buscaría en Google sobre este tema (lenguaje natural).",
     "respuesta": "Respuesta de 1-3 frases, informativa y diferida, RESPONDIBLE solo con el material de la fuente. Aplica las mismas reglas de compliance (sin dosis, sin imperativos médicos, sin promesas de cura)."}
  ],
  "entidades": [
    {"nombre": "Concepto médico canónico del artículo (enfermedad, fármaco, organismo, procedimiento).",
     "tipo": "Uno de: MedicalCondition, Drug, MedicalProcedure, AnatomicalStructure, Organization, Thing.",
     "wikipedia": "URL EXACTA en español https://es.wikipedia.org/wiki/... SOLO si estás muy seguro. Ante la duda, OMITE el campo o la entidad."}
  ]
}

Sobre "faqs": incluye 3-4 preguntas frecuentes y útiles que la gente realmente busca
(qué es, por qué ocurre, a quién afecta, qué sigue). Deben poder responderse con el
material; si no hay base, genera menos preguntas o ninguna. NUNCA inventes respuestas.

Sobre "entidades": incluye 1-3 conceptos médicos centrales. El enlace de Wikipedia es
OPCIONAL y solo para conceptos canónicos inequívocos; ante la menor duda, omítelo. Es
preferible una entidad sin enlace que un enlace equivocado. Si no hay entidades claras,
devuelve [].

No agregues texto antes ni después del JSON. No envuelvas el JSON en fences."""


def log(msg: str, *, verbose: bool = False, force: bool = False) -> None:
    if force or verbose:
        print(msg, flush=True)


def load_sources() -> dict:
    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_state() -> dict:
    if not STATE_FILE.exists():
        return {"processed_urls": [], "stats": {"total_processed": 0}}
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"processed_urls": [], "stats": {"total_processed": 0}}


def save_state(state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def url_hash(url: str) -> str:
    return hashlib.sha256(url.strip().lower().encode("utf-8")).hexdigest()


def extract_image(entry: Any) -> Optional[str]:
    # 1) media:content
    for key in ("media_content", "media_thumbnail"):
        media = entry.get(key) or []
        for item in media:
            if isinstance(item, dict) and item.get("url"):
                return item["url"]
    # 2) enclosure
    for link in entry.get("links", []):
        if link.get("rel") == "enclosure" and link.get("type", "").startswith("image"):
            return link.get("href")
    # 3) primera <img> en summary o content
    html_blobs = []
    if entry.get("summary"):
        html_blobs.append(entry["summary"])
    for c in entry.get("content") or []:
        if isinstance(c, dict) and c.get("value"):
            html_blobs.append(c["value"])
    for html in html_blobs:
        soup = BeautifulSoup(html, "html.parser")
        img = soup.find("img")
        if img and img.get("src"):
            return img["src"]
    return None


# ---------- Validadores de compliance YMYL ----------

# Frases médicamente peligrosas para AdSense. Si el modelo las produce,
# rechazamos el artículo y reintentamos.
FORBIDDEN_PATTERNS = [
    r"\btoma(r)?\s+\d+\s*(mg|g|ml|mcg|μg|ui|unidades)\b",
    r"\bla dosis (es|recomendada|debe)\b",
    r"\bdosis (recomendada|sugerida|óptima)\b",
    r"\bcura(r|do|n)?\s+(el|la|los|las)\b",
    r"\belimina\s+(la enfermedad|el cáncer|la diabetes)\b",
    r"\b100\s*%\s*(efectivo|seguro|garantizado)\b",
    r"\bmilagroso\b",
    r"\bremedio (casero|definitivo|infalible) para\b",
    r"\b(debe|debes|deberías) tomar\b.*\b(mg|g|ml|mcg)\b",
]

# Cifras sospechosas: número seguido de unidad médica sin contexto de estudio.
# (Si la cifra está, debe estar respaldada por palabras como 'estudio', 'según', 'investigadores'.)
NUMERIC_CLAIM_RX = re.compile(
    r"\b\d+([,.]\d+)?\s*(mg|mg/kg|g/dl|mmol|μg|ug|ng|kcal|ui)\b",
    flags=re.IGNORECASE,
)
EVIDENCE_WORDS = re.compile(
    r"\b(según|estudio|estudios|ensayo|investigadores|investigación|publicad[oa]|"
    r"revista|journal|reportad[oa]|datos|análisis|metaanálisis)\b",
    flags=re.IGNORECASE,
)


def _tokens(text: str) -> set:
    return {t.lower() for t in re.findall(r"[a-záéíóúñ]{4,}", text, flags=re.IGNORECASE)}


def jaccard_similarity(a: str, b: str) -> float:
    """Similitud de tokens — para detectar plagio del resumen RSS."""
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def check_compliance(data: dict, source_summary: str) -> tuple[bool, list[str]]:
    """Devuelve (es_válido, lista_de_problemas)."""
    problems: list[str] = []
    faq_text = " ".join(
        f"{q.get('pregunta','')} {q.get('respuesta','')}"
        for q in (data.get("faqs") or []) if isinstance(q, dict)
    )
    body_full = " ".join([
        data.get("titulo", ""),
        data.get("resumen", ""),
        data.get("porQueImporta", ""),
        data.get("cuerpo", ""),
        faq_text,
    ])

    # 1) Frases prohibidas
    for pat in FORBIDDEN_PATTERNS:
        if re.search(pat, body_full, flags=re.IGNORECASE):
            problems.append(f"frase prohibida: {pat}")

    # 2) Cifras médicas sin contexto de estudio
    for m in NUMERIC_CLAIM_RX.finditer(body_full):
        start = max(0, m.start() - 200)
        ctx = body_full[start:m.end() + 200]
        if not EVIDENCE_WORDS.search(ctx):
            problems.append(f"cifra médica sin contexto de estudio: '{m.group(0)}'")
            break  # con uno basta para rechazar

    # 3) Plagio frente al resumen RSS de la fuente
    sim = jaccard_similarity(data.get("cuerpo", ""), source_summary or "")
    if sim > 0.4:
        problems.append(f"similitud {sim:.2f} > 0.40 con resumen original (posible plagio)")

    return (len(problems) == 0, problems)


# ---------- Limpieza HTML ----------

def clean_text(html: str) -> str:
    soup = BeautifulSoup(html or "", "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    text = soup.get_text(" ", strip=True)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def fetch_article_text(url: str, headers: dict, max_chars: int, verbose: bool = False) -> str:
    """Descarga el artículo de la fuente y extrae el cuerpo principal en texto plano.

    Recorta a max_chars (en límite de palabra) para acotar el costo en tokens.
    Devuelve "" ante cualquier fallo: el llamador hace fallback al resumen RSS.
    Esto es lo que permite que el modelo escriba desde sustancia real y no desde un
    stub de 1500 caracteres — clave para calidad y anti-alucinación.
    """
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code != 200 or "html" not in r.headers.get("content-type", ""):
            return ""
        soup = BeautifulSoup(r.content, "html.parser")
        # Quitar ruido estructural que no es el artículo.
        for tag in soup(["script", "style", "nav", "header", "footer", "aside",
                         "form", "figure", "figcaption", "noscript", "iframe"]):
            tag.decompose()
        # Preferir el contenedor semántico del artículo si existe.
        container = (soup.find("article") or soup.find("main")
                     or soup.find(attrs={"role": "main"}) or soup.body or soup)
        paras = [clean_text(p.get_text(" ", strip=True)) for p in container.find_all("p")]
        paras = [p for p in paras if len(p) >= 40]  # descarta pies/menús/avisos cortos
        text = "\n\n".join(paras).strip()
        if len(text) < 200:  # extracción demasiado pobre: no aporta sobre el resumen
            return ""
        if len(text) > max_chars:
            # Recorte inteligente: 70% del inicio (contexto/métodos) + 30% del final
            # (conclusiones/limitaciones, donde está el valor E-E-A-T). Mejor calidad
            # por token que truncar solo el inicio.
            head_n = int(max_chars * 0.7)
            tail_n = max_chars - head_n
            head = text[:head_n]
            hsp = head.rfind(" ")
            if hsp > head_n * 0.6:
                head = head[:hsp]
            tail = text[-tail_n:]
            tsp = tail.find(" ")
            if 0 <= tsp < tail_n * 0.4:
                tail = tail[tsp + 1:]
            text = head.rstrip() + "\n\n[…]\n\n" + tail.lstrip()
        return text
    except Exception as e:
        log(f"    [fulltext] no disponible ({type(e).__name__}); uso resumen RSS", verbose=verbose)
        return ""


def call_anthropic(client: Anthropic, model: str, user_prompt: str, verbose: bool,
                   usage_acc: Optional[dict] = None) -> dict:
    last_err: Optional[Exception] = None
    for attempt in range(3):
        try:
            resp = client.messages.create(
                model=model,
                max_tokens=3000,
                temperature=0.4,
                system=[
                    {
                        "type": "text",
                        "text": SYSTEM_PROMPT,
                        "cache_control": {"type": "ephemeral"},
                    }
                ],
                messages=[{"role": "user", "content": user_prompt}],
            )
            # Telemetría de tokens (se facturan aunque falle el parseo posterior).
            if usage_acc is not None and getattr(resp, "usage", None):
                u = resp.usage
                usage_acc["calls"] = usage_acc.get("calls", 0) + 1
                usage_acc["input"] = usage_acc.get("input", 0) + (getattr(u, "input_tokens", 0) or 0)
                usage_acc["output"] = usage_acc.get("output", 0) + (getattr(u, "output_tokens", 0) or 0)
                usage_acc["cache_write"] = usage_acc.get("cache_write", 0) + (getattr(u, "cache_creation_input_tokens", 0) or 0)
                usage_acc["cache_read"] = usage_acc.get("cache_read", 0) + (getattr(u, "cache_read_input_tokens", 0) or 0)
            raw = "".join(
                block.text for block in resp.content if getattr(block, "type", None) == "text"
            ).strip()

            # Remover fences si el modelo los puso por error
            if raw.startswith("```"):
                raw = re.sub(r"^```(?:json)?\s*", "", raw)
                raw = re.sub(r"\s*```$", "", raw)

            data = json.loads(raw)

            # Validar campos
            for key in ("titulo", "resumen", "categoria", "cuerpo", "tags"):
                if key not in data:
                    raise ValueError(f"falta campo '{key}' en respuesta del modelo")
            if data["categoria"] not in CATEGORIAS_VALIDAS:
                raise ValueError(f"categoría inválida: {data['categoria']!r}")
            if not isinstance(data["tags"], list):
                raise ValueError("tags no es lista")
            return data
        except (json.JSONDecodeError, ValueError) as e:
            last_err = e
            log(f"    [retry {attempt+1}/3] parseo: {e}", verbose=verbose)
        except Exception as e:
            last_err = e
            log(f"    [retry {attempt+1}/3] api: {e}", verbose=verbose)
        time.sleep((2 ** attempt) + random.random())
    raise RuntimeError(f"Falló la llamada a Anthropic tras 3 intentos: {last_err}")


def make_user_prompt(*, source_name: str, source_url: str, lang: str,
                     title: str, summary: str, fulltext: str = "") -> str:
    if fulltext:
        material = f"""Texto completo del artículo original (BASA tu reescritura ÚNICAMENTE en este
material; no agregues datos que no estén aquí):
\"\"\"
{fulltext}
\"\"\""""
    else:
        material = f"""Resumen / extracto original (es el ÚNICO material disponible; no inventes datos
que no estén aquí; si es escaso, escribe un artículo más breve pero veraz):
{summary}"""

    return f"""Reescribe la siguiente noticia médica para el público latinoamericano en español neutro,
siguiendo TODAS las reglas del system prompt.

Fuente original: {source_name}
URL original: {source_url}
Idioma original: {lang}

Titular original:
{title}

{material}

Recuerda: responde SOLO con el JSON pedido, sin texto antes ni después."""


def _clamp(s: str, max_len: int) -> str:
    """Trunca s a max_len caracteres respetando el limite del schema Zod.

    Si excede, corta en la ultima palabra completa antes del limite y
    agrega elipsis. Garantiza que el resultado tenga <= max_len chars.
    """
    s = (s or "").strip()
    if len(s) <= max_len:
        return s
    # Reservar 1 char para la elipsis
    cut = s[: max_len - 1].rstrip()
    # Intentar cortar en el ultimo espacio dentro del rango
    last_space = cut.rfind(" ")
    if last_space > max_len * 0.6:  # solo si no perdemos demasiado
        cut = cut[:last_space].rstrip()
    # Quitar puntuacion final repetida antes de la elipsis
    cut = cut.rstrip(",;:.- ")
    result = cut + "…"
    # Sanity: asegurar limite estricto
    return result[:max_len]


def write_article(data: dict, *, source_name: str, source_url: str,
                  fecha_iso: str, image: Optional[str],
                  modelo: str = "claude-haiku-4-5") -> Path:
    titulo = data["titulo"].strip()
    slug = slugify(titulo, lowercase=True, max_length=80, word_boundary=True, save_order=True)
    if not slug:
        slug = url_hash(source_url)[:16]

    target = CONTENT_DIR / f"{slug}.md"
    suffix = 2
    while target.exists():
        target = CONTENT_DIR / f"{slug}-{suffix}.md"
        suffix += 1

    tags_clean = []
    for t in (data.get("tags") or []):
        if isinstance(t, str):
            t2 = slugify(t, lowercase=True, max_length=30)
            if t2 and t2 not in tags_clean:
                tags_clean.append(t2)
        if len(tags_clean) >= 6:
            break

    # YAML-safe quoting (sustituye comillas dobles internas por comillas simples)
    def yq(s: str) -> str:
        return '"' + str(s).replace('"', "'").replace("\\", "\\\\") + '"'

    # Clamp DURO a los limites del schema Zod (src/content/config.ts):
    #   titulo:        min 5,  max 140
    #   resumen:       min 20, max 400
    #   porQueImporta: min 10, max 400
    # Sin esto, si Claude excede los limites (ya paso), el build de Astro
    # falla con InvalidContentEntryDataError y se rompe el deploy.
    titulo = _clamp(titulo, 140)
    resumen = _clamp(data["resumen"], 400)
    porque = _clamp(data.get("porQueImporta") or "", 400) if data.get("porQueImporta") else ""

    front_lines = [
        "---",
        f"titulo: {yq(titulo)}",
        f"resumen: {yq(resumen)}",
    ]
    if porque:
        front_lines.append(f"porQueImporta: {yq(porque)}")
    front_lines.extend([
        f"categoria: {yq(data['categoria'])}",
        "fuente:",
        f"  nombre: {yq(source_name)}",
        f"  url: {yq(source_url)}",
        f"fecha: {fecha_iso}",
        "tags:",
    ])
    for t in tags_clean:
        front_lines.append(f"  - {yq(t)}")

    # FAQ (SEO rich results). Clamp a los límites del schema Zod (pregunta<=200,
    # respuesta<=700). Solo se emite la clave si hay al menos una FAQ válida.
    faqs_clean = []
    for q in (data.get("faqs") or []):
        if not isinstance(q, dict):
            continue
        preg = _clamp(str(q.get("pregunta", "")).strip(), 200)
        resp = _clamp(str(q.get("respuesta", "")).strip(), 700)
        if len(preg) >= 5 and len(resp) >= 10:
            faqs_clean.append((preg, resp))
        if len(faqs_clean) >= 5:
            break
    if faqs_clean:
        front_lines.append("faqs:")
        for preg, resp in faqs_clean:
            front_lines.append(f"  - pregunta: {yq(preg)}")
            front_lines.append(f"    respuesta: {yq(resp)}")

    # Entidades médicas (Knowledge Graph). wikipedia solo si es URL http(s) válida.
    ents_clean = []
    for e in (data.get("entidades") or []):
        if not isinstance(e, dict):
            continue
        nombre = _clamp(str(e.get("nombre", "")).strip(), 120)
        if len(nombre) < 2:
            continue
        tipo = _clamp(str(e.get("tipo", "")).strip(), 60)
        wiki = str(e.get("wikipedia", "")).strip()
        wiki = wiki if wiki.startswith(("http://", "https://")) else ""
        ents_clean.append((nombre, tipo, wiki))
        if len(ents_clean) >= 3:
            break
    if ents_clean:
        front_lines.append("entidades:")
        for nombre, tipo, wiki in ents_clean:
            front_lines.append(f"  - nombre: {yq(nombre)}")
            if tipo:
                front_lines.append(f"    tipo: {yq(tipo)}")
            if wiki:
                front_lines.append(f"    wikipedia: {yq(wiki)}")

    if image:
        front_lines.append(f"imagen: {yq(image)}")
    front_lines.append(f'autorIA: {yq(modelo)}')
    front_lines.append("---")
    front_lines.append("")
    front_lines.append(data["cuerpo"].strip())
    front_lines.append("")

    target.write_text("\n".join(front_lines), encoding="utf-8")
    return target


def run(args: argparse.Namespace) -> int:
    load_dotenv(ROOT / ".env")
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not args.dry_run and (not api_key or api_key == "__PENDIENTE__"):
        print("[fatal] ANTHROPIC_API_KEY no configurada en .env o en el entorno.", file=sys.stderr)
        return 2

    sources_cfg = load_sources()
    cfg = sources_cfg.get("config", {}) or {}
    max_total = args.limit or int(cfg.get("max_noticias_por_run", 12))
    max_por_fuente = int(cfg.get("max_por_fuente", 2))
    model = cfg.get("modelo", "claude-haiku-4-5")
    model_premium = cfg.get("modelo_premium", model)
    peso_premium_min = int(cfg.get("peso_premium_min", 99))  # 99 = nunca, salvo config
    fetch_fulltext = bool(cfg.get("fetch_fulltext", False))
    fulltext_max_chars = int(cfg.get("fulltext_max_chars", 4000))
    fulltext_skip_if_summary = int(cfg.get("fulltext_skip_if_summary_chars", 0))
    user_agent = cfg.get("user_agent", "Mozilla/5.0 PulsoSano/1.0")
    # Temas prioritarios: boost de SELECCIÓN (data-driven desde Google Search Console).
    # NO afecta el SYSTEM_PROMPT ni la generación — solo qué candidatos se eligen.
    temas_cfg = cfg.get("temas_prioritarios", {}) or {}
    temas_keywords = [k.lower() for k in (temas_cfg.get("keywords") or [])]
    temas_reserva_frac = float(temas_cfg.get("reserva_frac", 0.0))

    state = load_state()
    processed_hashes = set(state.get("processed_urls", []))

    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    client = None if args.dry_run else Anthropic(api_key=api_key)

    headers = {
        "User-Agent": user_agent,
        "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, text/html, */*",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    }
    candidates = []

    for fuente in sources_cfg.get("fuentes", []):
        if not fuente.get("activa", True):
            log(f"[skip] {fuente['nombre']}: marcada inactiva", verbose=args.verbose)
            continue
        log(f"[feed] {fuente['nombre']} ({fuente['url']})", verbose=args.verbose, force=True)
        try:
            resp = requests.get(fuente["url"], headers=headers, timeout=20)
            resp.raise_for_status()
            parsed = feedparser.parse(resp.content)
        except Exception as e:
            log(f"    error: {e}", verbose=args.verbose, force=True)
            continue

        nuevos = 0
        for entry in parsed.entries:
            if nuevos >= max_por_fuente:
                break
            link = (entry.get("link") or "").strip()
            if not link:
                continue
            h = url_hash(link)
            if h in processed_hashes:
                continue
            title = clean_text(entry.get("title") or "")
            summary_html = entry.get("summary") or ""
            if not summary_html and entry.get("content"):
                for c in entry["content"]:
                    if isinstance(c, dict) and c.get("value"):
                        summary_html = c["value"]
                        break
            summary = clean_text(summary_html)
            if not title or not summary or len(summary) < 60:
                continue
            try:
                pub = entry.get("published") or entry.get("updated") or ""
                fecha_dt = dateparser.parse(pub) if pub else datetime.now(timezone.utc)
            except Exception:
                fecha_dt = datetime.now(timezone.utc)
            image = extract_image(entry)

            candidates.append({
                "source_name": fuente["nombre"],
                "source_url": link,
                "lang": fuente.get("idioma", "en"),
                "title": title,
                "summary": summary[:1500],
                "fecha_iso": fecha_dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00"),
                "image": image,
                "peso": int(fuente.get("peso", 3)),
                "hash": h,
            })
            nuevos += 1
        log(f"    -> {nuevos} candidatos nuevos", verbose=args.verbose, force=True)

    if not candidates:
        print("[ok] No hay candidatos nuevos.")
        return 0

    candidates.sort(key=lambda c: (c["peso"], c["fecha_iso"]), reverse=True)

    # Boost por temas prioritarios: reserva una fracción de los slots para
    # candidatos cuyo título/resumen matcheen las keywords (p.ej. GLP-1, que ya
    # rankea página 1 en GSC). Los reservados van al frente -> sobreviven el corte.
    # Si no hay candidatos prioritarios en este run, cae al comportamiento normal.
    def _es_prioritario(c):
        if not temas_keywords:
            return False
        txt = (c["title"] + " " + c["summary"]).lower()
        return any(kw in txt for kw in temas_keywords)

    pool = candidates[: max_total * 3]
    random.shuffle(pool)
    prioritarios = [c for c in pool if _es_prioritario(c)]
    resto = [c for c in pool if not _es_prioritario(c)]
    n_reserva = min(len(prioritarios), round(max_total * temas_reserva_frac)) if temas_keywords else 0
    candidates = (prioritarios[:n_reserva] + resto + prioritarios[n_reserva:])[:max_total]
    random.shuffle(candidates)  # orden de procesamiento (no afecta la selección)
    for c in candidates:
        c["prioritario"] = _es_prioritario(c)
    if n_reserva:
        print(f"[boost] {n_reserva} slot(s) reservado(s) a temas prioritarios "
              f"({len(prioritarios)} candidato(s) prioritario(s) encontrado(s))")

    print(f"[plan] Se procesarán {len(candidates)} noticia(s) (max_total={max_total})")

    if args.dry_run:
        for c in candidates:
            mark = "⚡" if c.get("prioritario") else " "
            print(f"  - {mark}[{c['source_name']}] {c['title'][:90]}")
        return 0

    written = 0
    api_errors = 0
    usage = {}
    fetched = 0
    for i, c in enumerate(candidates, 1):
        try:
            # Ruteo de modelo por autoridad de la fuente: las de peso alto
            # (peer-review, agencias) usan el modelo premium; el resto, el base.
            modelo_usado = model_premium if c["peso"] >= peso_premium_min else model

            # Texto completo de la fuente (mayor calidad / menos alucinación).
            # Optimización de tokens: si el resumen RSS ya es suficientemente rico
            # (p.ej. abstracts estructurados de journals), saltamos el fetch — no
            # aporta sobre lo que ya tenemos y ahorra tokens de entrada + una descarga.
            # Si falla, fulltext="" y el prompt cae al resumen RSS.
            fulltext = ""
            if fetch_fulltext and len(c["summary"]) < (fulltext_skip_if_summary or 10**9):
                fulltext = fetch_article_text(c["source_url"], headers,
                                              fulltext_max_chars, verbose=args.verbose)
                if fulltext:
                    fetched += 1

            marca = "★" if modelo_usado == model_premium else " "
            pri = "⚡" if c.get("prioritario") else ""
            ft_tag = f"+texto({len(fulltext)}c)" if fulltext else "solo-resumen"
            print(f"[{i}/{len(candidates)}] {marca}{pri}{c['source_name']}: {c['title'][:70]} [{ft_tag}]")

            user_prompt = make_user_prompt(
                source_name=c["source_name"],
                source_url=c["source_url"],
                lang=c["lang"],
                title=c["title"],
                summary=c["summary"],
                fulltext=fulltext,
            )

            # Generación con validación de compliance.
            data = None
            for compliance_attempt in range(2):
                candidate = call_anthropic(client, modelo_usado, user_prompt,
                                           verbose=args.verbose, usage_acc=usage)
                ok, problems = check_compliance(candidate, c["summary"])
                if ok:
                    data = candidate
                    break
                print(f"    [compliance] intento {compliance_attempt+1}: {', '.join(problems)}", file=sys.stderr)
            if data is None:
                print("    [skip] compliance falló dos veces; se omite esta noticia.", file=sys.stderr)
                processed_hashes.add(c["hash"])  # no reintentar la misma noticia mañana
                continue

            path = write_article(
                data,
                source_name=c["source_name"],
                source_url=c["source_url"],
                fecha_iso=c["fecha_iso"],
                image=c["image"],
                modelo=modelo_usado,
            )
            print(f"    -> {path.relative_to(ROOT)}")
            processed_hashes.add(c["hash"])
            written += 1
        except Exception as e:
            print(f"    [error] {e}", file=sys.stderr)
            api_errors += 1

    state["processed_urls"] = list(processed_hashes)
    state.setdefault("stats", {})
    state["stats"]["total_processed"] = state["stats"].get("total_processed", 0) + written
    state["stats"]["last_run"] = datetime.now(timezone.utc).isoformat()
    save_state(state)

    print(f"[ok] {written} artículo(s) escritos. Total histórico: {state['stats']['total_processed']}.")

    # Telemetría de tokens — visibilidad para optimizar costo. cache_read se
    # factura a 0.1x y cache_write a 1.25x; un cache_read alto = prompt cache
    # acertando (bueno). fetched = cuántos artículos usaron texto fuente completo.
    if usage:
        calls = usage.get("calls", 0)
        inp = usage.get("input", 0); out = usage.get("output", 0)
        cw = usage.get("cache_write", 0); cr = usage.get("cache_read", 0)
        billed_in = inp + cw + cr
        per_art = (billed_in + out) // max(written, 1)
        print(f"[tokens] {calls} llamadas | entrada: {inp} fresh + {cr} cache-read + {cw} cache-write "
              f"| salida: {out} | fulltext usado: {fetched}/{len(candidates)} "
              f"| ~{per_art} tok/artículo")

    # Alerta: hubo candidatos pero NINGUNO se pudo generar por errores de
    # generación (típicamente saldo de API agotado o caída de Anthropic).
    # Salir con código != 0 hace que el run de CI falle visiblemente, en vez
    # de reportar `success` en falso mientras el sitio se congela. El caso
    # legítimo de "0 candidatos nuevos" sale antes (return 0) y no llega aquí.
    if written == 0 and api_errors > 0:
        print(
            f"[fallo] 0 artículos escritos pero {api_errors} fallo(s) de generación. "
            "Posible saldo de API agotado o caída del proveedor. Revisa los [error] arriba.",
            file=sys.stderr,
        )
        return 3

    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="PulsoSano — agregador de noticias médicas")
    p.add_argument("--dry-run", action="store_true", help="No llama al modelo; solo muestra candidatos.")
    p.add_argument("--verbose", "-v", action="store_true", help="Logs detallados.")
    p.add_argument("--limit", type=int, default=0, help="Forzar máximo de noticias en esta corrida.")
    args = p.parse_args()
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
