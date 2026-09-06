# Rescate de calidad — PulsoSano (2026-07-09)

Registro del incidente de calidad y el plan de recuperación. Complementa
[`MONETIZACION.md`](MONETIZACION.md).

## Diagnóstico (2026-07-09, vía Google Search Console + AdSense)

Dos sistemas de Google emitieron el **mismo veredicto**: el sitio se clasifica
como **contenido escalado de poco valor**.

1. **Desindexación masiva (~2026-06-04).** Las páginas indexadas cayeron de
   ~1000+ a **509** (123 sin indexar; ~900 URLs "olvidadas"). Las impresiones
   colapsaron de ~75/día (pico 22-may a 1-jun, luna de miel post-lanzamiento) a
   **~1/día** desde el 3-jun. Sin recuperación en 5 semanas.
2. **AdSense: "Contenido de poco valor"** (estado *Requiere su atención*; el
   `ads.txt` figura *Autorizado*). El plan de auto-activación de MONETIZACION.md
   quedó **invalidado** — hay que mejorar y **re-solicitar revisión**.
3. **Sin acción manual** (verificado en GSC → Acciones manuales: sin problemas).
   Es reevaluación **algorítmica**, no penalización formal.
4. **Causa raíz:** patrón de content-farm. 1004 de 1366 artículos se volcaron en
   **may-2026**; **90% tiene <600 palabras** (0 llegan a las 850 que apunta el
   prompt). Muchos son churnalism hiperlocal, off-topic (astronomía, zoología) o
   duplicados exactos. Los sitemaps responden 200 y bien formados: **no es un
   problema técnico**.

## Acciones aplicadas (commit `89ae553`, 2026-07-09)

| Palanca | Antes | Ahora |
|---|---|---|
| Cron del agregador | 12h (2/día) | **24h (1/día)** |
| `max_noticias_por_run` | 5 | **3** |
| `max_por_fuente` | 2 | **1** |
| Artículos con `noindex` | 0 | **94** |

**Poda de calidad (94 artículos `noindex: true`):**
- 19 off-topic no-salud (astronomía, paleontología, zoología, física pura).
- ~60 finos (<400 palabras).
- ~14 copias duplicadas (sufijo `-2`/`-3`; se mantiene la copia base).
- **Excepción:** 2 artículos GLP-1/obesidad finos NO se ocultaron — son
  candidatos a **expandir** (tema que rankea, ver [GSC]).

Mecanismo: campo `noindex` en `src/content/config.ts`; excluye de
`sitemap` (astro.config.mjs `filter`), `news-sitemap.xml`, `rss.xml` y emite
`<meta name="robots" content="noindex, nofollow">` vía `Base.astro`.
`SYSTEM_PROMPT` **intacto** (no invalida el prompt cache).

## Checklist re-revisión AdSense (esperar 3-4 semanas → ~2026-08-01)

Antes de pulsar "Solicitar revisión" en el dashboard de AdSense:

- [ ] Confirmar en GSC que la desindexación **se estabilizó o revirtió** (páginas
      indexadas dejan de caer; idealmente suben). Reporte: Indexación → Páginas.
- [ ] Reenviar sitemaps en GSC si marcan error (news-sitemap tenía "Falta etiqueta
      XML", probablemente stale tras el deploy).
- [ ] Verificar que los 94 `noindex` NO aparecen en `sitemap-0.xml` en producción.
- [ ] **Expandir** los ganadores GLP-1/salud mental a 800-1000 palabras con
      contexto propio (no solo rewrite de la fuente) — diferenciación real.
- [ ] Revisar que home, categorías y artículos tengan el disclaimer YMYL visible.
- [ ] Solo entonces: AdSense → Sitios → pulsosano.com → **Solicitar revisión**.

**Riesgo:** un segundo rechazo endurece la siguiente revisión. No re-solicitar
sin haber movido la aguja de calidad de forma verificable.

## Segunda fase (2026-09-05) — poda completa del archivo

Diagnóstico con el corpus completo (1.492 artículos): mediana 487 palabras;
1.104 artículos visibles por debajo de 600 palabras; 31 URLs fuente duplicadas;
40 artículos con fecha RSS de 2019-2025. Además el CI llevaba 16 días caído
(SDK `anthropic` 1.x) y el sitio no publicaba nada desde el 20-ago.

| Palanca | Antes | Ahora |
|---|---|---|
| Artículos con `noindex` | 94 | **1.202** |
| Artículos visibles (portada/categorías/sitemap) | 1.398 | **~290** |
| Umbral | ad hoc | **< 600 palabras** o duplicado por URL fuente |
| Listados | mostraban `noindex` | los excluyen |
| Fechas fuera de ventana | 40 | 0 (y el agregador acota a 21 días) |

Los ~290 visibles son los generados desde julio (mediana 917 palabras, FAQs y
entidades) más los expandidos a mano. Todo artículo nuevo entra ya con ese
estándar. Reversible: quitar `noindex: true` del frontmatter.

Checklist de re-revisión AdSense actualizada en [`MONETIZACION.md`](MONETIZACION.md).

## Próximos pasos de fondo (más allá del parche)

1. **Elevar el piso de calidad del generador.** El prompt apunta a 600-850
   palabras pero la salida real es 450-599. Investigar por qué no alcanza el
   objetivo (¿fulltext insuficiente? ¿el modelo corta?). Diferenciación >
   volumen.
2. **Refresco de ganadores** (pendiente de la sesión anterior): profundizar las
   páginas pos 4-15 de GSC en vez de publicar noticias nuevas efímeras.
3. **Crecer Salud Mental** (desnutrida) con contenido evergreen, no noticioso.
