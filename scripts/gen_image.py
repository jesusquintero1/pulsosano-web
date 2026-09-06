#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PulsoSano — generador de imágenes editoriales propias (1200×630) para cada artículo.

Sustituye el hotlink de imágenes de terceros (riesgo de copyright y de imágenes
rotas) por una tarjeta con identidad de marca: color por categoría, motivo gráfico
determinista derivado del slug (línea de pulso + partículas), titular tipografiado,
fuente citada y dominio. Sin APIs externas: solo Pillow y las fuentes OFL de
scripts/assets/fonts/.

Uso:
    py scripts/gen_image.py --all            # artículos visibles (noindex != true) sin tarjeta
    py scripts/gen_image.py --all --force    # regenera todas
    py scripts/gen_image.py --slug <slug>    # una sola
    py scripts/gen_image.py --preview        # 3 muestras en scratch (no toca el repo)

Desde el agregador:
    from gen_image import generate_card
    generate_card(slug, titulo, categoria, fuente)  -> "/img/noticias/<slug>.jpg"
"""
from __future__ import annotations

import argparse
import hashlib
import math
import random
import re
import sys
from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "scripts" / "assets" / "fonts"
CONTENT_DIR = ROOT / "src" / "content" / "noticias"
OUT_DIR = ROOT / "public" / "img" / "noticias"
URL_PREFIX = "/img/noticias/"

W, H = 1200, 630
SCALE = 2  # se dibuja a 2× y se reduce con LANCZOS (antialiasing)

# Paleta por categoría: (fondo oscuro, acento claro). Una familia cromática por sección
# para que el lector reconozca la categoría de un vistazo en portada.
PALETTE = {
    "Investigación Clínica":       ("#0b3b3c", "#5eead4"),
    "Avances Médicos":             ("#1c1a4d", "#a5b4fc"),
    "Nutrición y Dieta":           ("#3b2a0a", "#fcd34d"),
    "Salud Mental":                ("#2c1260", "#c4b5fd"),
    "Fitness y Ejercicio":         ("#43160a", "#fdba74"),
    "Medicina Preventiva":         ("#064e3b", "#6ee7b7"),
    "Enfermedades y Tratamientos": ("#1c2740", "#93c5fd"),
    "Estilo de Vida Saludable":    ("#421b22", "#fda4af"),
    "Salud Pública y Política":    ("#0b2846", "#7dd3fc"),
}
DEFAULT_PALETTE = ("#0f172a", "#10b981")


def _hex(c: str) -> tuple[int, int, int]:
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def _lighten(rgb, f):
    return tuple(min(255, int(v + (255 - v) * f)) for v in rgb)


def _font(name: str, size: int) -> ImageFont.FreeTypeFont:
    p = FONTS / name
    if not p.exists():
        raise FileNotFoundError(f"Fuente no encontrada: {p}")
    return ImageFont.truetype(str(p), size)


def _wrap(text: str, font: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        t = (cur + " " + w).strip()
        if font.getlength(t) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _fit_title(text: str, max_w: int, max_h: int):
    """Mayor tamaño de fuente con el que el titular cabe en max_w × max_h (≤ 4 líneas)."""
    for size in (66, 60, 54, 48, 44, 40, 36):
        f = _font("SourceSerif4-Bold.ttf", size * SCALE)
        lines = _wrap(text, f, max_w * SCALE)
        lh = int(size * 1.14) * SCALE
        if len(lines) <= 4 and len(lines) * lh <= max_h * SCALE:
            return f, lines, lh
    f = _font("SourceSerif4-Bold.ttf", 34 * SCALE)
    lines = _wrap(text, f, max_w * SCALE)[:4]
    if len(lines) == 4:
        lines[-1] = lines[-1].rstrip(".,;:") + "…"
    return f, lines, int(34 * 1.14) * SCALE


def _background(bg, accent, rng: random.Random) -> Image.Image:
    w, h = W * SCALE, H * SCALE
    top = _lighten(bg, 0.10)
    grad = Image.linear_gradient("L").resize((w, h))
    img = Image.composite(Image.new("RGB", (w, h), bg), Image.new("RGB", (w, h), top), grad)

    # Halo de acento difuso (arriba-derecha) — profundidad sin ruido.
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    cx, cy = int(w * (0.78 + rng.uniform(-0.06, 0.06))), int(h * (0.18 + rng.uniform(-0.08, 0.08)))
    r = int(h * 0.55)
    gd.ellipse((cx - r, cy - r, cx + r, cy + r), fill=accent + (70,))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=110 * SCALE // 2))
    img = Image.alpha_composite(img.convert("RGBA"), glow)

    # Partículas: círculos translúcidos, más densos a la derecha (el titular vive a la izquierda).
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for _ in range(rng.randint(14, 22)):
        x = int(w * (0.50 + 0.50 * rng.random() ** 0.6))
        y = int(h * rng.random())
        rad = int(rng.choice([4, 6, 8, 12, 18, 26, 40, 58]) * SCALE)
        a = rng.randint(14, 42)
        if rng.random() < 0.35:
            ld.ellipse((x - rad, y - rad, x + rad, y + rad), outline=accent + (a + 30,), width=2 * SCALE)
        else:
            ld.ellipse((x - rad, y - rad, x + rad, y + rad), fill=accent + (a,))
    img = Image.alpha_composite(img, layer)

    # Línea de pulso (ECG) determinista: identidad de marca, banda inferior.
    pulse = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pd = ImageDraw.Draw(pulse)
    base_y = int(h * 0.80)
    pts = []
    x = 0
    while x < w:
        seg = rng.randint(60, 140) * SCALE
        pts.append((x, base_y + rng.randint(-3, 3) * SCALE))
        x += seg
        if x < w and rng.random() < 0.55:
            amp = rng.randint(28, 70) * SCALE
            pts += [(x, base_y), (x + 10 * SCALE, base_y - amp), (x + 22 * SCALE, base_y + amp // 2),
                    (x + 34 * SCALE, base_y)]
            x += 40 * SCALE
    pts.append((w, base_y))
    pd.line(pts, fill=accent + (150,), width=3 * SCALE, joint="curve")
    soft = pulse.filter(ImageFilter.GaussianBlur(radius=6 * SCALE))
    img = Image.alpha_composite(img, soft)
    img = Image.alpha_composite(img, pulse)
    return img


def render_card(titulo: str, categoria: str, fuente: str, slug: str) -> Image.Image:
    bg_hex, ac_hex = PALETTE.get(categoria, DEFAULT_PALETTE)
    bg, accent = _hex(bg_hex), _hex(ac_hex)
    seed = int(hashlib.sha256(slug.encode("utf-8")).hexdigest()[:8], 16)
    rng = random.Random(seed)

    img = _background(bg, accent, rng)
    d = ImageDraw.Draw(img)
    S = SCALE
    M = 56 * S  # margen

    # --- Marca (arriba-izquierda) ---
    box = 44 * S
    d.rounded_rectangle((M, M - 4 * S, M + box, M - 4 * S + box), radius=10 * S, fill=accent)
    cx, cy = M + box // 2, M - 4 * S + box // 2
    arm, thick = 13 * S, 7 * S
    d.rectangle((cx - thick // 2, cy - arm, cx + thick // 2, cy + arm), fill=bg)
    d.rectangle((cx - arm, cy - thick // 2, cx + arm, cy + thick // 2), fill=bg)
    f_brand = _font("Inter-Bold.ttf", 30 * S)
    f_tag = _font("Inter-Medium.ttf", 13 * S)
    tx = M + box + 14 * S
    d.text((tx, M - 6 * S), "PulsoSano", font=f_brand, fill=(255, 255, 255))
    d.text((tx, M + 30 * S), "S A L U D  ·  E V I D E N C I A  ·  L A T A M", font=f_tag, fill=accent)

    # --- Categoría (arriba-derecha) ---
    f_cat = _font("Inter-SemiBold.ttf", 19 * S)
    label = categoria.upper()
    tw = f_cat.getlength(label)
    px, py = 22 * S, 11 * S
    x1 = W * S - M
    x0 = int(x1 - tw - 2 * px)
    y0 = M - 2 * S
    y1 = y0 + int(19 * S * 1.2) + 2 * py
    pill = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(pill).rounded_rectangle((x0, y0, x1, y1), radius=(y1 - y0) // 2, fill=accent + (46,),
                                           outline=accent + (120,), width=2 * S)
    img = Image.alpha_composite(img, pill)
    d = ImageDraw.Draw(img)
    d.text((x0 + px, y0 + py - 1 * S), label, font=f_cat, fill=accent)

    # --- Titular ---
    f_title, lines, lh = _fit_title(titulo, max_w=W - 2 * 56 - 40, max_h=270)
    ty = 178 * S
    for ln in lines:
        d.text((M, ty), ln, font=f_title, fill=(255, 255, 255))
        ty += lh

    # --- Pie: fuente y dominio ---
    f_src = _font("Inter-Medium.ttf", 21 * S)
    src = f"Fuente: {fuente}"
    while f_src.getlength(src) > (W - 2 * 56 - 220) * S and len(src) > 20:
        src = src[:-2].rstrip() + "…"
    d.text((M, H * S - M - 18 * S), src, font=f_src, fill=_lighten(bg, 0.72))
    f_dom = _font("Inter-SemiBold.ttf", 20 * S)
    dom = "pulsosano.com"
    d.text((W * S - M - f_dom.getlength(dom), H * S - M - 18 * S), dom, font=f_dom, fill=accent)

    return img.convert("RGB").resize((W, H), Image.LANCZOS)


def generate_card(slug: str, titulo: str, categoria: str, fuente: str,
                  out_dir: Path = OUT_DIR, force: bool = False) -> str:
    """Genera (si no existe) la tarjeta y devuelve la ruta pública (/img/noticias/<slug>.jpg)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / f"{slug}.jpg"
    if force or not target.exists():
        img = render_card(titulo, categoria, fuente, slug)
        img.save(str(target), "JPEG", quality=82, optimize=True, progressive=True)
    return URL_PREFIX + target.name


# ---------- Utilidades sobre el corpus ----------

RX_FIELD = {
    "titulo": re.compile(r'^titulo: "(.*)"\s*$', re.M),
    "categoria": re.compile(r'^categoria: "(.*)"\s*$', re.M),
    "fuente": re.compile(r'^  nombre: "(.*)"\s*$', re.M),
    "noindex": re.compile(r"^noindex: true\s*$", re.M),
    "imagen": re.compile(r'^imagen: "(.*)"\s*$', re.M),
}


def _read_meta(md: Path) -> dict:
    t = md.read_text(encoding="utf-8")
    fm = t.split("\n---\n", 1)[0]
    g = lambda k: (RX_FIELD[k].search(fm) or [None, ""])[1] if RX_FIELD[k].search(fm) else ""
    return {
        "slug": md.stem, "titulo": g("titulo").replace("'", "'"), "categoria": g("categoria"),
        "fuente": g("fuente"), "noindex": bool(RX_FIELD["noindex"].search(fm)),
        "imagen": g("imagen"), "text": t, "fm": fm,
    }


def _set_imagen(md: Path, meta: dict, url: str) -> bool:
    """Escribe/reemplaza la línea `imagen:` del frontmatter. Devuelve True si cambió."""
    t = meta["text"]
    fm = meta["fm"]
    line = f'imagen: "{url}"'
    if RX_FIELD["imagen"].search(fm):
        new_fm = RX_FIELD["imagen"].sub(line, fm, count=1)
    elif re.search(r"^autorIA:", fm, re.M):
        new_fm = re.sub(r"^(autorIA:)", line + "\n\\1", fm, count=1, flags=re.M)
    else:
        new_fm = fm + "\n" + line
    if new_fm == fm:
        return False
    md.write_text(new_fm + t[len(fm):], encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="Tarjetas editoriales PulsoSano")
    ap.add_argument("--all", action="store_true", help="Todos los artículos visibles (noindex != true)")
    ap.add_argument("--include-noindex", action="store_true", help="Con --all: también los noindex")
    ap.add_argument("--slug", help="Un solo artículo")
    ap.add_argument("--force", action="store_true", help="Regenerar aunque exista")
    ap.add_argument("--preview", action="store_true", help="3 muestras en --out sin tocar frontmatter")
    ap.add_argument("--out", help="Directorio de salida (por defecto public/img/noticias)")
    a = ap.parse_args()

    out_dir = Path(a.out) if a.out else OUT_DIR
    mds = sorted(CONTENT_DIR.glob("*.md"))
    if a.slug:
        mds = [CONTENT_DIR / f"{a.slug}.md"]
    metas = [_read_meta(m) for m in mds if m.exists()]
    if a.all and not a.include_noindex:
        metas = [m for m in metas if not m["noindex"]]
    if a.preview:
        rng = random.Random(7)
        metas = rng.sample(metas, min(3, len(metas)))

    done = upd = 0
    for m in metas:
        if not (a.all or a.slug or a.preview):
            break
        url = generate_card(m["slug"], m["titulo"], m["categoria"], m["fuente"], out_dir=out_dir, force=a.force)
        done += 1
        if not a.preview and _set_imagen(CONTENT_DIR / f"{m['slug']}.md", m, url):
            upd += 1
    print(f"[gen_image] tarjetas: {done} · frontmatter actualizado: {upd} · dir: {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
