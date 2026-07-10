import { getCollection } from 'astro:content';

function escape(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

export async function GET(context) {
  const SITE = (import.meta.env.SITE_URL || context.site?.toString() || 'https://pulsosano.com').replace(/\/$/, '');
  const items = (await getCollection('noticias'))
    .filter((n) => n.data.noindex !== true)
    .sort((a, b) => new Date(b.data.fecha).getTime() - new Date(a.data.fecha).getTime())
    .slice(0, 50);

  const itemsXml = items.map((entry) => {
    const link = `${SITE}/noticia/${entry.slug}/`;
    const pub = new Date(entry.data.fecha).toUTCString();
    return `    <item>
      <title>${escape(entry.data.titulo)}</title>
      <link>${link}</link>
      <guid isPermaLink="true">${link}</guid>
      <pubDate>${pub}</pubDate>
      <category>${escape(entry.data.categoria)}</category>
      <description>${escape(entry.data.resumen)}</description>
    </item>`;
  }).join('\n');

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>PulsoSano — Noticias y avances en salud</title>
    <link>${SITE}</link>
    <atom:link href="${SITE}/rss.xml" rel="self" type="application/rss+xml" />
    <description>Resúmenes en español de noticias médicas y avances científicos, citando la fuente original.</description>
    <language>es</language>
${itemsXml}
  </channel>
</rss>`;

  return new Response(xml, {
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
      'Cache-Control': 'public, max-age=900',
    },
  });
}
