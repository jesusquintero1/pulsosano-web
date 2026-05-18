# CLAUDE.md — PulsoSano

Sitio agregador automático de noticias y avances en salud, en español neutro,
monetizado con Google AdSense. Nicho YMYL (Your Money Your Life).

## Resumen técnico

- Frontend: **Astro 5 estático** + Tailwind CSS + @astrojs/sitemap.
- Aggregator: **Python 3.12** (`feedparser`, `bs4`, `anthropic>=0.34`).
- Modelo IA: **claude-haiku-4-5** con prompt caching (`cache_control: ephemeral`).
- Hosting: **Cloudflare Workers Static Assets** (NO Pages, NO adapter).
- CI/CD: **GitHub Actions**, cron `0 */2 * * *`.
- Dominio sugerido: `pulsosano.com`.

## Comandos

```powershell
npm run dev       # dev server (Astro)
npm run build     # build estático en dist/
py scripts/aggregator.py --dry-run --verbose
py scripts/aggregator.py --limit 5
```

## Pitfalls ya conocidos — NO repetir

1. **Wrangler 3 falla** en deploys solo-assets con "Missing entry-point".
   El workflow fuerza `wranglerVersion: "4"` en `cloudflare/wrangler-action@v3`.
2. **`.env` con SITE_URL incorrecto** sobreescribe el build. Verificar tras cada
   deploy: `curl https://pulsosano.com/ | grep canonical`.
3. **Cloudflare cache** tarda 2-5 minutos en propagar. Bustear con `?v=$(date +%s)`.
4. **Astro `getStaticPaths`** corre en contexto aislado: declarar helpers DENTRO
   de la función, no en el frontmatter superior.
5. **Slugify simple `\s+` falla** con puntos y símbolos. Usar el pipeline
   `[áéíóúñ]→` luego `[^a-z0-9]+ → -`.
6. **Prompt cache de Anthropic** se invalida con cualquier byte volátil en el
   system prompt (timestamps, IDs dinámicos). El `SYSTEM_PROMPT` en
   `scripts/aggregator.py` está congelado — NO editarlo sin tener consciencia
   de la invalidación del cache.
7. **No usar adapter Cloudflare** ni `output: 'server'`. Solo Static Assets.
8. **No usar Pages** — siempre Workers (`wrangler deploy`).
9. **No copiar texto literal** de las fuentes — todo reescrito por Claude.
10. **No publicar consejos individuales** ni dosis, ni cura, ni imperativos médicos.
    Compliance YMYL bloquearía AdSense.

## Reglas editoriales obligatorias (E-E-A-T)

- Lenguaje informativo y diferido: "según el estudio…", "los investigadores observaron…".
- Cada artículo cierra recordando consultar con un profesional sanitario.
- Disclaimer visible en home, en categorías y en cada noticia (componente
  `MedicalDisclaimer.astro`).
- Página dedicada `/aviso-medico` con el disclaimer extendido.
- Cada noticia cita la fuente original con `rel="nofollow noopener"`.
- Sólo fuentes autorizadas (NIH, OMS, Mayo Clinic, Harvard, Diario Médico, etc.).

## Fuentes RSS

Definidas en `scripts/sources.yml`. Cada fuente tiene `peso` (5 = autoridad alta).
Si una empieza a fallar (HTTP 403/404/429), marcar `activa: false` y dejar
comentario con la fecha.

Verificadas funcionando el 2026-05-18 (22 activas):
- Peer-review: Nature Medicine, BMJ Open, PLOS Medicine
- Agencias: WHO, OPS/PAHO (es+en), MedlinePlus, CDC Newsroom
- Periodismo médico: STAT News, Diario Médico, Reuters Health
- Calidad: BBC Health, NYT Health
- Divulgación: ScienceDaily (3), Cuídate Plus, El Mundo Salud
- Complementaria: Healthline, PsyPost, ScienceAlert, 20Minutos

Bloqueadas al user-agent del bot:
Harvard Health, Mayo Clinic, Cleveland Clinic, Medical News Today,
The Lancet, Infosalus, EFE Salud (marcadas `activa:false`).

## Validadores de compliance YMYL

`scripts/aggregator.py` aplica tras cada generación:
1. **FORBIDDEN_PATTERNS** — frases prohibidas (dosis, cura, milagroso…).
2. **NUMERIC_CLAIM_RX** — cifras `mg/g/ml/mcg/UI` sin contexto de estudio.
3. **jaccard_similarity** — si > 0.40 con el resumen RSS, rechaza por plagio.
Si falla 2 veces consecutivas, marca la noticia como procesada y la salta.

## Estructura de archivos

```
src/
  layouts/Base.astro              # head/CMP/JSON-LD organización + AdSense pausado
  components/
    Header.astro                  # logo cruz médica + nav 7 items
    Footer.astro                  # newsletter + enlaces legales
    ArticleCard.astro             # default/featured/compact
    AdSlot.astro                  # responsivo, placeholder si no hay client
    CookieBanner.astro            # GDPR/CCPA con pauseAdRequests
    MedicalDisclaimer.astro       # box/inline/compact
  pages/
    [...page].astro               # home con paginate(12)
    categoria/[cat].astro         # 9 categorías médicas
    noticia/[...slug].astro       # JSON-LD MedicalScholarlyArticle + BreadcrumbList
    sobre.astro privacidad.astro contacto.astro aviso-medico.astro
    rss.xml.js
  content/
    config.ts                     # Zod schema (titulo, resumen, categoria, ...)
    noticias/*.md
scripts/
  aggregator.py                   # SYSTEM_PROMPT congelado, dedupe SHA256
  sources.yml
  requirements.txt
.github/workflows/aggregate.yml   # cron 2h, wranglerVersion:4
public/ ads.txt robots.txt og-default.png favicon.svg
wrangler.jsonc
```

## Categorías permitidas (no agregar ni renombrar)

1. Investigación Clínica
2. Avances Médicos
3. Nutrición y Dieta
4. Salud Mental
5. Fitness y Ejercicio
6. Medicina Preventiva
7. Enfermedades y Tratamientos
8. Estilo de Vida Saludable
9. Salud Pública y Política
