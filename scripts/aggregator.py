#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SaludLatAm — Agregador automático de noticias médicas.

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
# No editar sin tener consciencia de la invalidación del prompt cache.
SYSTEM_PROMPT = """Eres editor médico y traductor especializado en divulgación de salud para el público
latinoamericano. Tu trabajo es producir contenido ORIGINAL en español a partir del
titular y resumen de una fuente médica autorizada, sin copiar texto literal.

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
5. Si la fuente menciona estadísticas, conserva las cifras exactas.
6. Cita la fuente original con enlace nofollow.

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
  "titulo": "Titular en español, informativo, sin clickbait, máximo 90 caracteres",
  "resumen": "Resumen original de 2-3 frases (max 280 caracteres). Qué y por qué.",
  "categoria": "Una de las 9 permitidas",
  "porQueImporta": "1-2 frases sobre relevancia para el lector latinoamericano.",
  "cuerpo": "Artículo en markdown de 500-700 palabras. Usa ## para 4 secciones: contexto, hallazgos, qué significa en general (NO consejo individual), limitaciones del estudio. Cierra con un párrafo recordando consultar a un profesional sanitario. NO uses tablas ni HTML.",
  "tags": ["3-5", "palabras", "clave", "lowercase", "sin-tildes"]
}

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


def clean_text(html: str) -> str:
    soup = BeautifulSoup(html or "", "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    text = soup.get_text(" ", strip=True)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def call_anthropic(client: Anthropic, model: str, user_prompt: str, verbose: bool) -> dict:
    last_err: Optional[Exception] = None
    for attempt in range(3):
        try:
            resp = client.messages.create(
                model=model,
                max_tokens=2200,
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
                     title: str, summary: str) -> str:
    return f"""Reescribe la siguiente noticia médica para el público latinoamericano en español neutro,
siguiendo TODAS las reglas del system prompt.

Fuente original: {source_name}
URL original: {source_url}
Idioma original: {lang}

Titular original:
{title}

Resumen / extracto original:
{summary}

Recuerda: responde SOLO con el JSON pedido, sin texto antes ni después."""


def write_article(data: dict, *, source_name: str, source_url: str,
                  fecha_iso: str, image: Optional[str]) -> Path:
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

    front_lines = [
        "---",
        f"titulo: {yq(titulo)}",
        f"resumen: {yq(data['resumen'].strip())}",
    ]
    if data.get("porQueImporta"):
        front_lines.append(f"porQueImporta: {yq(data['porQueImporta'].strip())}")
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
    if image:
        front_lines.append(f"imagen: {yq(image)}")
    front_lines.append('autorIA: "claude-haiku-4-5"')
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
    user_agent = cfg.get("user_agent", "Mozilla/5.0 SaludLatAm/1.0")

    state = load_state()
    processed_hashes = set(state.get("processed_urls", []))

    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    client = None if args.dry_run else Anthropic(api_key=api_key)

    headers = {"User-Agent": user_agent}
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

    candidates.sort(key=lambda c: (-c["peso"], c["fecha_iso"]), reverse=False)
    candidates.sort(key=lambda c: c["peso"], reverse=True)
    candidates = candidates[: max_total * 2]
    random.shuffle(candidates)
    candidates = candidates[:max_total]

    print(f"[plan] Se procesarán {len(candidates)} noticia(s) (max_total={max_total})")

    if args.dry_run:
        for c in candidates:
            print(f"  - [{c['source_name']}] {c['title'][:90]}")
        return 0

    written = 0
    for i, c in enumerate(candidates, 1):
        try:
            print(f"[{i}/{len(candidates)}] {c['source_name']}: {c['title'][:80]}")
            user_prompt = make_user_prompt(
                source_name=c["source_name"],
                source_url=c["source_url"],
                lang=c["lang"],
                title=c["title"],
                summary=c["summary"],
            )
            data = call_anthropic(client, model, user_prompt, verbose=args.verbose)
            path = write_article(
                data,
                source_name=c["source_name"],
                source_url=c["source_url"],
                fecha_iso=c["fecha_iso"],
                image=c["image"],
            )
            print(f"    -> {path.relative_to(ROOT)}")
            processed_hashes.add(c["hash"])
            written += 1
        except Exception as e:
            print(f"    [error] {e}", file=sys.stderr)

    state["processed_urls"] = list(processed_hashes)
    state.setdefault("stats", {})
    state["stats"]["total_processed"] = state["stats"].get("total_processed", 0) + written
    state["stats"]["last_run"] = datetime.now(timezone.utc).isoformat()
    save_state(state)

    print(f"[ok] {written} artículo(s) escritos. Total histórico: {state['stats']['total_processed']}.")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="SaludLatAm — agregador de noticias médicas")
    p.add_argument("--dry-run", action="store_true", help="No llama al modelo; solo muestra candidatos.")
    p.add_argument("--verbose", "-v", action="store_true", help="Logs detallados.")
    p.add_argument("--limit", type=int, default=0, help="Forzar máximo de noticias en esta corrida.")
    args = p.parse_args()
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
