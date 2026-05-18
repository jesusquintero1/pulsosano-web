"""Submit all current article URLs to IndexNow (Bing + Yandex) for instant indexing."""
from __future__ import annotations
import os, sys, json, re
from pathlib import Path
import requests
import yaml

ROOT = Path(__file__).resolve().parent.parent
SITE = os.environ.get("SITE_URL", "https://saludlatam.com").rstrip("/")
KEY_FILE = ROOT / "public" / "indexnow-key.txt"

def collect_urls() -> list[str]:
    urls: list[str] = [SITE + "/"]
    content_dir = ROOT / "src" / "content" / "noticias"
    for md in content_dir.glob("*.md"):
        slug = md.stem
        urls.append(f"{SITE}/noticia/{slug}/")
    # categorías
    cats = [
        "investigacion-clinica", "avances-medicos", "nutricion-y-dieta",
        "salud-mental", "fitness-y-ejercicio", "medicina-preventiva",
        "enfermedades-y-tratamientos", "estilo-de-vida-saludable",
        "salud-publica-y-politica",
    ]
    for c in cats:
        urls.append(f"{SITE}/categoria/{c}/")
    return urls

def main() -> int:
    if not KEY_FILE.exists():
        print("[skip] No hay indexnow-key.txt; saltando IndexNow.", file=sys.stderr)
        return 0
    key = KEY_FILE.read_text(encoding="ascii").strip()
    if not key:
        print("[skip] indexnow-key.txt vacío.", file=sys.stderr)
        return 0

    host = re.sub(r"^https?://", "", SITE).split("/")[0]
    urls = collect_urls()
    payload = {
        "host": host,
        "key": key,
        "keyLocation": f"{SITE}/{key}.txt",
        "urlList": urls[:10000],
    }
    print(f"[indexnow] submitting {len(payload['urlList'])} URLs to api.indexnow.org")
    try:
        r = requests.post(
            "https://api.indexnow.org/IndexNow",
            json=payload,
            timeout=20,
            headers={"Content-Type": "application/json; charset=utf-8"},
        )
        print(f"[indexnow] status={r.status_code} body={r.text[:200]}")
        return 0 if r.status_code in (200, 202) else 1
    except Exception as e:
        print(f"[indexnow] error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
