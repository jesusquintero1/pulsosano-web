# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project at a glance

**PulsoSano** — agregador automático de noticias y avances en salud, en español
neutro para LatAm, monetizado con Google AdSense. Nicho YMYL (Your Money Your Life).

- **Producción:** https://pulsosano.com (HTTPS · Cloudflare Workers)
- **Defensa marca:** https://pulsosano.org → 301 a `.com` (preserva path + query)
- **Repo:** https://github.com/jesusquintero1/pulsosano-web
- **CI/CD:** GitHub Actions cron `0 */2 * * *` (12 deploys/día)

## Common commands

```powershell
# Dev local
npm install                                    # primera vez
npm run dev                                    # dev server, http://localhost:4321
npm run build                                  # build estático -> dist/

# Aggregator (genera noticias con Claude Haiku)
py scripts/aggregator.py --dry-run --verbose   # no llama API, solo lista candidatos
py scripts/aggregator.py --limit 5             # genera 5 artículos
py scripts/aggregator.py                       # corrida normal (usa max_noticias_por_run de sources.yml)

# IndexNow (Bing/Yandex)
py scripts/indexnow_submit.py                  # submit todas las URLs al endpoint indexnow

# Deploy manual (solo si hay urgencia — normalmente GitHub Actions lo hace)
npx wrangler@4 deploy                          # principal
npx wrangler@4 deploy --config redirect/wrangler.jsonc  # worker redirect

# Lanzar workflow desde local
gh workflow run "Agregador de noticias" --repo jesusquintero1/pulsosano-web

# Ver logs del último run
gh run list --repo jesusquintero1/pulsosano-web --workflow "Agregador de noticias" --limit 5
gh run view <ID> --repo jesusquintero1/pulsosano-web --log
```

> **Nota Windows**: usar `py`, NO `python` (la Microsoft Store intercepta `python`).
> Para git: el repo tiene `core.autocrlf` activo y bash via `Bash` tool funciona;
> PowerShell falla con paths que contienen corchetes (`[...slug].astro`) — usar
> `Edit`/`Read` tools en vez de PowerShell cmdlets para esos archivos.

## Architecture (big picture)

Hay **3 procesos independientes** que se sincronizan vía git:

```
┌──────────────────────────────────────────────────────────────────┐
│                    GitHub Actions (cron 2h)                       │
│                                                                  │
│  1. checkout → 2. aggregator.py → 3. commit nuevas .md →         │
│  4. astro build → 5. wrangler deploy (principal + redirect)      │
│  6. IndexNow + Google sitemap ping                                │
└──────────────────────────────────────────────────────────────────┘
            │                          │
            ▼                          ▼
   src/content/noticias/         dist/ (static HTML)
   (Markdown frontmatter)              │
            │                          ▼
            │                  Cloudflare Workers
            │                  ├── pulsosano-web        (assets ./dist)
            │                  │   └── pulsosano.com, www.pulsosano.com
            │                  └── pulsosano-redirect   (./redirect/index.js)
            │                      └── pulsosano.org → 301 → .com
            ▼
   src/content/config.ts (Zod schema valida cada .md al build time)
```

**Pieza 1 — Frontend Astro (`src/`, `astro.config.mjs`)**
- `output: 'static'`, sin adapter Cloudflare (eso rompe deploys solo-assets).
- `Base.astro` inyecta SEO completo en cada página: `hreflang` × 21 LatAm,
  `NewsMediaOrganization` JSON-LD, `WebSite` con `SearchAction`, View Transitions,
  preconnect a fonts + AdSense, `max-image-preview:large`.
- `noticia/[...slug].astro` usa schema híbrido `NewsArticle` + `MedicalScholarlyArticle`
  (cuando categoría es Investigación o Avances), añade `Speakable`, autor
  `Organization`, TOC sticky en aside, AdSlot vertical 300×600.
- Las URL siguen el patrón `/noticia/<slug>/`, `/categoria/<slug-cat>/`, `/[1..N]`.
- Slugs de categoría: `[áéíóúñ] → ascii`, luego `[^a-z0-9]+ → -`.

**Pieza 2 — Aggregator Python (`scripts/aggregator.py`)**
- Lee `scripts/sources.yml` (22 fuentes RSS activas), dedupe via SHA256 del URL en
  `scripts/state/processed.json` (commiteado por el bot del CI).
- Envía cada candidato a `claude-haiku-4-5` con un **SYSTEM_PROMPT congelado**
  (cualquier cambio invalida prompt cache de Anthropic → +50% costo). Marca el
  system prompt con `cache_control: ephemeral`.
- Valida con `check_compliance()`: regex `FORBIDDEN_PATTERNS`, cifras médicas sin
  contexto de estudio, similitud Jaccard ≤ 0.40 con el resumen RSS (anti-plagio).
- Si la validación falla 2 veces, marca la noticia como procesada y la salta.
- Escribe Markdown con frontmatter Zod-compatible en `src/content/noticias/<slug>.md`.

**Pieza 3 — Deploy Cloudflare (`wrangler.jsonc` + `redirect/wrangler.jsonc`)**
- Son **DOS Workers separados**:
  - `pulsosano-web` (raíz): static assets `./dist/`, custom domains `pulsosano.com` y `www.pulsosano.com`.
  - `pulsosano-redirect` (`redirect/`): worker JS de 1 función que hace `Response.redirect(target, 301)`. Custom domains `pulsosano.org` y `www.pulsosano.org`.
- El workflow ejecuta `wrangler deploy` dos veces con `workingDirectory` distinto.

## Pitfalls (NO repetir)

1. **`cloudflare/wrangler-action@v3` con wrangler 3 falla en deploys solo-assets**
   con "Missing entry-point". Forzar `wranglerVersion: "4"` en el workflow.
2. **`PowerShell -replace` es case-insensitive por defecto.** Usa `-creplace` para
   reemplazos case-sensitive (crítico durante el rebrand: lowercase URLs vs
   PascalCase brand).
3. **`Get-Content -Raw -Encoding UTF8` falla** en algunas versiones de PowerShell.
   Usar `[System.IO.File]::ReadAllText($path, [System.Text.UTF8Encoding]::new($false))`.
4. **Paths con corchetes `[...slug].astro`** rompen muchos cmdlets de PowerShell
   (`Resolve-Path`, `Get-ChildItem` con wildcards). Para editar esos archivos,
   usar la herramienta `Edit` directamente.
5. **Astro `getStaticPaths`** corre en contexto aislado. Declarar helpers
   (`slugify`, etc.) **dentro** de la función, no en el frontmatter superior.
6. **`SYSTEM_PROMPT` en `aggregator.py` está congelado.** Cualquier cambio (incluso
   un espacio) invalida el prompt cache de Anthropic, lo que sube el costo ~3x
   los siguientes 5 minutos. NO editarlo sin tener consciencia.
7. **NUNCA usar `output: 'server'` ni `@astrojs/cloudflare`** — rompe Workers Static
   Assets. Solo `static`.
8. **NUNCA usar Cloudflare Pages** — siempre Workers (`wrangler deploy`). Pages
   ignora la config de `routes` con `custom_domain: true`.
9. **NUNCA copiar texto literal de las fuentes.** El SYSTEM_PROMPT + validador
   Jaccard ≤ 0.40 lo aseguran.
10. **NUNCA publicar consejos individuales** (dosis, "tomá X", "cura Y"). Esto
    bloquea AdSense en revisión YMYL automáticamente.
11. **El bot del CI hace commits.** Al trabajar local, hacer `git pull --rebase`
    antes de cualquier push; el bot puede haber pusheado en el ínterin.
12. **Si haces rebase y `--no-edit` no existe** en `git rebase`, no usarlo. Usa
    `git commit --amend --no-edit` para el último commit, o cherry-pick.
13. **Cloudflare cache** tarda 2-5 min en propagar tras deploy. Si verificas
    cambios con `curl https://pulsosano.com/`, bustea con `?v=<timestamp>`.
14. **Verificación CAA en Windows**: `Resolve-DnsName -Type CAA` NO existe en
    Windows DNS client. Usar Cloudflare DNS-over-HTTPS:
    `Invoke-RestMethod "https://cloudflare-dns.com/dns-query?name=X&type=CAA" -Headers @{Accept='application/dns-json'}`.

## YMYL E-E-A-T (reglas editoriales obligatorias)

El sitio es categoría YMYL — Google es 5x más estricto en salud que en otros
nichos. Estas reglas están codificadas en `SYSTEM_PROMPT`:

- Lenguaje informativo y diferido: "según el estudio…", "los investigadores observaron…".
- Cada artículo cierra recordando consultar con un profesional sanitario.
- Disclaimer visible en home, categorías y cada noticia (`MedicalDisclaimer.astro`).
- Página dedicada `/aviso-medico` con disclaimer extendido.
- Cada noticia cita la fuente original con `rel="nofollow noopener"`.
- Solo fuentes autorizadas (peer-review, agencias gubernamentales, hospitales reconocidos).
- Prohibido en código y en contenido: "tomar X mg", "dosis recomendada",
  "cura X", "100% efectivo", "milagroso", imperativos médicos personales.

## RSS sources (`scripts/sources.yml`)

22 fuentes activas, peso 5 = autoridad máxima:
- **Peer-review (5):** Nature Medicine, BMJ Open, PLOS Medicine
- **Agencias (5):** WHO, OPS/PAHO (es+en), MedlinePlus (NIH), CDC Newsroom
- **Periodismo médico (4-5):** STAT News, Diario Médico, Reuters Health, BBC Health, NYT Health
- **Divulgación (3-4):** ScienceDaily (3 secciones), Cuídate Plus, El Mundo Salud, Healthline, PsyPost, ScienceAlert
- **Generalista (2):** 20Minutos Salud

**Inactivas (bot bloqueado por user-agent):** Harvard Health, Mayo Clinic,
Cleveland Clinic, Medical News Today, The Lancet, Infosalus, EFE Salud.
Marcadas `activa: false` con fecha. Reintentar trimestralmente.

## Categorías permitidas (NO agregar ni renombrar)

Definidas en `src/content/config.ts`:

1. Investigación Clínica
2. Avances Médicos
3. Nutrición y Dieta
4. Salud Mental
5. Fitness y Ejercicio
6. Medicina Preventiva
7. Enfermedades y Tratamientos
8. Estilo de Vida Saludable
9. Salud Pública y Política

Renombrar una categoría rompe todas las URLs `/categoria/<slug>/` indexadas.

## File structure (high signal)

```
src/
  layouts/Base.astro               head SEO completo (hreflang × 21, NewsArticle/MedicalScholarlyArticle JSON-LD, ViewTransitions, AdSense pausado hasta consentimiento)
  components/
    Header.astro                   logo + nav 7 items
    Footer.astro                   newsletter (Formspree) + enlaces legales
    ArticleCard.astro              variantes: default | featured | compact
    AdSlot.astro                   variant: horizontal | vertical | square | fluid; lazy opcional
    CookieBanner.astro             GDPR consent + pauseAdRequests
    MedicalDisclaimer.astro        variant: box | inline | compact
  pages/
    [...page].astro                home paginado pageSize=12, ItemList JSON-LD
    categoria/[cat].astro          9 categorías; ItemList JSON-LD
    noticia/[...slug].astro        NewsArticle + MedicalScholarlyArticle + Breadcrumb + Speakable + TOC
    sobre.astro privacidad.astro contacto.astro aviso-medico.astro 404.astro
    rss.xml.js news-sitemap.xml.js
  content/
    config.ts                      Zod schema (titulo, resumen, categoria enum, fuente, fecha, tags, imagen)
    noticias/*.md
scripts/
  aggregator.py                    SYSTEM_PROMPT congelado, validadores compliance, prompt cache ephemeral
  sources.yml                      22 activas + 7 inactivas
  indexnow_submit.py               ping a Bing/Yandex post-deploy
  requirements.txt
redirect/                          worker separado pulsosano.org → 301 .com
  index.js                         1 función Response.redirect()
  wrangler.jsonc                   custom_domain pulsosano.org + www.pulsosano.org
.github/workflows/aggregate.yml    cron 2h + push trigger + workflow_dispatch
public/
  robots.txt                       allow Googlebot-News/Image, block AhrefsBot/SemrushBot
  manifest.webmanifest             PWA con 3 shortcuts
  ads.txt                          pub-__PENDIENTE__ hasta tener AdSense aprobado
  og-default.png                   1200×630, generado con System.Drawing
  logo-square.png                  1024×1024 para Google Publisher Center
  favicon.svg                      cruz médica verde esmeralda
  <indexnow-key>.txt               UUID verificación IndexNow
wrangler.jsonc                     worker principal: assets ./dist, custom domain .com
astro.config.mjs                   rehype-slug + rehype-autolink-headings, sitemap
tailwind.config.mjs                paleta verde esmeralda (brand-500: #10b981) + azul ciencia
```

## SEO setup ya aplicado

Búsquedas frecuentes que pueden hacerse (no las repitas analizando, ya están):
- 21 `hreflang` LatAm + `x-default` en `Base.astro` (es-MX, es-AR, es-CO, etc.)
- `NewsArticle` JSON-LD para Google Discover/News, `MedicalScholarlyArticle`
  para Investigación Clínica/Avances Médicos.
- `Speakable` Schema con selectores `h1`, `header p`, `.prose-medical p:first-of-type`.
- Google News Sitemap separado en `/news-sitemap.xml` (últimas 48h).
- IndexNow integrado al workflow → Bing/Yandex indexan en segundos.
- View Transitions Astro (SPA-like, CLS = 0 entre páginas).
- `max-snippet:-1`, `max-image-preview:large` para CTR alto en SERP.
- `NewsMediaOrganization` Schema con `ethicsPolicy` + `correctionsPolicy`.
- `WebSite` con `SearchAction` → habilita Sitelinks Search Box en SERP.

## DNS / Seguridad (Cloudflare)

Configurado en la zona `pulsosano.com`:
- **CAA** × 6 (visible: 4 + 2 wildcards): letsencrypt.org, pki.goog, sectigo.com,
  digicert.com (+ comodoca.com y ssl.com añadidos automáticamente por CF).
- **SPF**: `v=spf1 -all` (no enviamos email).
- **DMARC**: `v=DMARC1; p=reject; rua=mailto:jdqf19992025@gmail.com`.

## Estado actual del roadmap (snapshot 2026-05-19)

Ya completado:
- Día 1: dominio + repo + Cloudflare deploy + redirect .org + 22 RSS verificadas.
- Día 2: DNS hardening (CAA/SPF/DMARC) + Google Search Console verificado +
  sitemaps enviados (`/sitemap-index.xml`, `/news-sitemap.xml`) + Bing Webmaster
  importado desde GSC.

Pendiente (orden cronológico):
- **Día 7-10:** crear publicación en Google Publisher Center cuando haya ≥1000
  artículos (rechaza por "insufficient content" antes).
- **Día 30+:** solicitar AdSense (ver `public/ads.txt` con placeholder).
  Cuando Google dé `ca-pub-XXXXXXXXXXXXXXXX`, actualizarlo en:
  - GitHub Secret `PUBLIC_ADSENSE_CLIENT`
  - `public/ads.txt` (sin prefijo `ca-`)
- **Mes 6+:** considerar clonar el stack a Portugués (Brasil) — mismo código,
  traducir SYSTEM_PROMPT, cambiar feeds RSS. Stack reutilizable al 90%.

## GitHub Secrets requeridos

| Secret | Origen |
|---|---|
| `ANTHROPIC_API_KEY` | console.anthropic.com (reutilizada de AutomatizacionLatAm) |
| `CLOUDFLARE_API_TOKEN` | Plantilla "Edit Cloudflare Workers" |
| `CLOUDFLARE_ACCOUNT_ID` | Dashboard de Cloudflare |
| `PUBLIC_ADSENSE_CLIENT` | Pendiente — se añade tras aprobación AdSense (Día 30+) |
