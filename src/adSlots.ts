/**
 * Slot IDs de las unidades de anuncio manuales de Google AdSense.
 * ÚNICO lugar donde se configuran — actívalos aquí tras la aprobación de AdSense.
 *
 * ESTADO: sin configurar (todos ''). Mientras estén vacíos, NO se renderiza ninguna
 * unidad manual y Auto Ads (activado en el dashboard de AdSense) coloca los anuncios.
 * Un slot vacío nunca produce un <ins> roto.
 *
 * ─────────────────────────────────────────────────────────────────────────────
 * CÓMO ACTIVAR LAS UNIDADES MANUALES (mayor control/RPM que solo Auto Ads):
 *
 * 1. En AdSense → Anuncios → Por unidad de anuncio → "Crear unidad de anuncio".
 * 2. Crea estas 6 unidades (tipo y formato sugeridos):
 *      - homeTop        → Display, horizontal (responsive)
 *      - homeMid        → Display, horizontal (responsive)
 *      - articleTop     → Display, horizontal (responsive)
 *      - articleInline  → In-article (in-feed/in-article)
 *      - articleSidebar → Display, vertical 300×600
 *      - categoryGrid   → Display, horizontal (responsive)
 * 3. Cada unidad creada da un "data-ad-slot" de 10 dígitos. Pégalo abajo (entre comillas).
 * 4. Commit + push. Las unidades manuales se encienden solas (el resto sigue con Auto Ads).
 *
 * No hace falta tocar ningún otro archivo: las páginas leen estos valores.
 * ─────────────────────────────────────────────────────────────────────────────
 */
export const AD_SLOTS = {
  homeTop: '',
  homeMid: '',
  articleTop: '',
  articleInline: '',
  articleSidebar: '',
  categoryGrid: '',
} as const;
