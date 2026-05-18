import { getCollection } from 'astro:content';

function escape(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

// Google News acepta artículos publicados en los últimos 2 días.
const NEWS_WINDOW_MS = 2 * 24 * 60 * 60 * 1000;

export async function GET(context) {
  const SITE = (import.meta.env.SITE_URL || context.site?.toString() || 'https://pulsosano.com').replace(/\/$/, '');
  const PUBLICATION_NAME = 'PulsoSano';
  const PUBLICATION_LANG = 'es';

  const cutoff = Date.now() - NEWS_WINDOW_MS;
  const items = (await getCollection('noticias'))
    .filter((n) => new Date(n.data.fecha).getTime() >= cutoff)
    .sort((a, b) => new Date(b.data.fecha).getTime() - new Date(a.data.fecha).getTime())
    .slice(0, 1000);

  const xmlItems = items.map((entry) => {
    const link = `${SITE}/noticia/${entry.slug}/`;
    const pub = new Date(entry.data.fecha).toISOString();
    const keywords = (entry.data.tags || []).join(', ');
    return `  <url>
    <loc>${link}</loc>
    <lastmod>${pub}</lastmod>
    <news:news>
      <news:publication>
        <news:name>${escape(PUBLICATION_NAME)}</news:name>
        <news:language>${PUBLICATION_LANG}</news:language>
      </news:publication>
      <news:publication_date>${pub}</news:publication_date>
      <news:title>${escape(entry.data.titulo)}</news:title>
      ${keywords ? `<news:keywords>${escape(keywords)}</news:keywords>` : ''}
    </news:news>
  </url>`;
  }).join('\n');

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">
${xmlItems}
</urlset>`;

  return new Response(xml, {
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
      'Cache-Control': 'public, max-age=600',
    },
  });
}
