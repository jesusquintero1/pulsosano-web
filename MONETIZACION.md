# Monetización — estado y plan (actualizado 2026-09-05)

Fuente de verdad del estado de monetización de PulsoSano. Complementa
[`RESCATE-CALIDAD.md`](RESCATE-CALIDAD.md).

## Estado

- **AdSense:** cuenta creada, pub ID `ca-pub-8849534484285084` en secret, `ads.txt`,
  meta y script en cada página. Última revisión: **rechazada por "contenido de poco
  valor"** (julio 2026). Hay que **re-solicitar revisión** tras el saneamiento de
  2026-09-05 (ver checklist abajo).
- **Newsletter propia:** operativa. `POST /api/newsletter` → KV `pulsosano-newsletter`.
  Es el segundo activo monetizable (patrocinios, tráfico recurrente sin depender de
  Google). Exportar lista: `npx wrangler@4 kv key list --binding NEWSLETTER --prefix sub:`.
- **Ingresos actuales:** $0.

## Lo que ya quedó armado en código (2026-09-05)

| Palanca | Estado |
|---|---|
| Auto Ads por `?client=` en el script (sin doble init) | ✅ |
| Anuncios no personalizados por defecto; personalizados al aceptar cookies | ✅ |
| Sin navegación SPA (cada página carga completa → cada vista cuenta) | ✅ |
| 6 posiciones de unidades manuales listas en `src/adSlots.ts` (vacías) | ✅ |
| Páginas de confianza: Sobre, Metodología, Equipo, Aviso médico, Privacidad, Contacto | ✅ |
| Buzón de contacto operativo (`contacto@`) | ✅ |
| Sitio visible = ~290 artículos de 900+ palabras con FAQs; 1.202 finos en `noindex` | ✅ |
| Sitemap con `lastmod` real, sin páginas contradictorias | ✅ |

## Checklist para re-solicitar AdSense (hacer en este orden)

1. **Esperar 2-3 semanas** desde el deploy del 2026-09-05 para que Google re-rastree
   (verificar en GSC → Indexación que las URLs `noindex` salen y las nuevas entran).
2. Comprobar en GSC que las impresiones diarias dejan de caer.
3. En el dashboard de AdSense → **Privacidad y mensajes** → activar el mensaje de
   consentimiento GDPR de Google (cubre tráfico de España/UE; el banner propio del
   sitio no es un CMP certificado).
4. AdSense → Sitios → pulsosano.com → **Solicitar revisión**.
5. Si aprueban: en 24-48 h deben verse anuncios. Si no, AdSense → Anuncios → Por sitio
   → activar **Auto Ads** (toggle único).
6. Después de aprobado: crear las 6 unidades manuales y pegar sus IDs en
   `src/adSlots.ts` (mejor RPM que solo Auto Ads).

**Riesgo:** un segundo rechazo endurece la siguiente revisión. No re-solicitar antes
del paso 2.

## Plan de ingresos por etapas

| Etapa | Fuente | Requisito |
|---|---|---|
| 1 | AdSense (display + in-article) | Aprobación (checklist arriba) |
| 2 | Patrocinio de newsletter | ≥ 1.000 suscriptores; envío semanal (pendiente elegir herramienta de envío: Cloudflare Email Service o Brevo/Resend con la lista exportada de KV) |
| 3 | Contenido evergreen de alto RPM (guías GLP-1/obesidad, salud mental) | Ya hay 6 artículos expandidos; seguir el plan de `RESCATE-CALIDAD.md` |
| 4 | Clon en portugués (Brasil) | Stack reutilizable ~90 %; solo tras estabilizar 1-3 |

## Riesgos operativos que NO se automatizan por código

- **Créditos de Anthropic.** Si se agotan, el pipeline se detiene (pasó may-jun 2026).
  Activar auto-reload en console.anthropic.com. El CI falla en rojo (exit 3) y GitHub
  avisa por email.
- **Cambios de la SDK.** Ya pasó (ago-2026, 16 días sin publicar). La versión está
  fijada a `>=1,<2`; revisar el CHANGELOG antes de subir de mayor.
- **Feeds que bloquean IPs de GitHub** (Gaceta Médica 403, EFE Salud 429 intermitentes).
  No rompen el run; solo reducen candidatos.
- **Correo.** Solo existe la regla `contacto@` en Cloudflare Email Routing. Si se
  quieren más buzones, crearlos ahí antes de publicarlos.
