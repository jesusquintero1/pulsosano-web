# Monetización — estado y activación

Fuente de verdad del estado de monetización de PulsoSano. Resumen: **el sistema está
configurado para activarse SOLO al aprobarse AdSense, sin cambios de código ni deploys.**

## Estado actual (2026-06-26)

- AdSense: **en revisión** ("Preparando"). Ingresos = $0 hasta aprobación.
- Pub ID configurado en todos lados: `ca-pub-8849534484285084`
  - GitHub Secret `PUBLIC_ADSENSE_CLIENT` ✅
  - `public/ads.txt` ✅ (`google.com, pub-8849534484285084, DIRECT, f08c47fec0942fa0`)
  - Meta `google-adsense-account` + script `adsbygoogle.js` en cada página ✅

## Qué pasa AUTOMÁTICAMENTE cuando Google apruebe (cero intervención)

En cuanto la cuenta pase a "Listo", **sin tocar nada**:

1. **Los anuncios empiezan a servirse solos.** El script de AdSense ya está en cada
   página, `pauseAdRequests = 0` (no se ahogan) y `enable_page_level_ads: true` pide
   activar **Auto Ads por código**. Google coloca los anuncios automáticamente.
2. **El contenido sigue publicándose** cada 12h (cron GitHub Actions) → más páginas =
   más inventario de anuncios, sin intervención.
3. **Los deploys siguen automáticos** (CI) → cada artículo nuevo queda monetizado.
4. **ads.txt ya verificado** con el pub ID real.

> No se requiere ningún cambio de código, commit ni deploy del propietario tras la
> aprobación. El sistema ya está "armado".

## El ÚNICO punto que vive en Google (no automatizable por código)

Auto Ads se controla desde el dashboard de AdSense y **no existe API pública** para
activarlo. Dos escenarios:

- **Caso común:** en las aprobaciones nuevas, Auto Ads suele venir **activado por
  defecto** → los anuncios aparecen solos (gracias también al flag del código).
- **Si no aparecieran tras ~24-48h de aprobado:** ir a AdSense → Anuncios → "Por
  sitio" → `pulsosano.com` → activar **Auto Ads**. Es un toggle de 30 segundos, una
  sola vez. No requiere tocar el repo.

## Opcional — más ingresos (NO requerido)

Auto Ads funciona solo, pero las unidades manuales en posiciones premium suelen rendir
más. Para activarlas: crear 6 ad units en AdSense y pegar sus slot IDs reales en
[`src/adSlots.ts`](src/adSlots.ts) (un solo archivo, autodocumentado) → commit. Las
unidades se encienden solas; mientras los slots estén vacíos, Auto Ads las cubre.

## El único riesgo recurrente a la automatización: créditos de Anthropic

El contenido se genera con la API de Anthropic. Si el saldo se agota, el pipeline deja
de producir artículos (pasó may-jun 2026). **No es automatizable por código** (es
facturación en console.anthropic.com).

- **Acción única recomendada:** activar **auto-reload de créditos** en la consola de
  Anthropic. Con eso, el contenido nunca se detiene sin intervención.
- **Red de seguridad ya implementada:** si un run genera 0 artículos por error de API,
  el CI **falla en rojo** (exit 3) y GitHub **envía un email** al propietario. No hay
  fallos silenciosos.

## Resumen en una línea

Todo lo automatizable ya está armado: al aprobarse AdSense, los anuncios se sirven
solos. Lo único fuera de mi alcance: el toggle de Auto Ads (si Google no lo deja por
defecto) y el auto-reload de créditos — ambos, acciones únicas de 30 segundos en sus
dashboards.
