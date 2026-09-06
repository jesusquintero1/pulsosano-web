// @ts-check
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';
import rehypeSlug from 'rehype-slug';
import rehypeAutolinkHeadings from 'rehype-autolink-headings';
import fs from 'node:fs';
import path from 'node:path';

const SITE = process.env.SITE_URL || 'https://pulsosano.com';

// Poda de calidad: URLs con `noindex: true` en su frontmatter quedan fuera del
// sitemap principal (rescate calidad 2026-07). Se leen los .md en build time.
const NOTICIAS_DIR = path.resolve('./src/content/noticias');
const noindexSlugs = new Set();
// lastmod real por artículo (fecha del frontmatter). Un lastmod global igual a la
// hora del build hacía que Google ignorase la señal en las ~1.500 URLs.
const lastmodBySlug = new Map();
if (fs.existsSync(NOTICIAS_DIR)) {
  for (const f of fs.readdirSync(NOTICIAS_DIR)) {
    if (!f.endsWith('.md')) continue;
    const fm = fs.readFileSync(path.join(NOTICIAS_DIR, f), 'utf8').split(/^---\s*$/m)[1] || '';
    const slug = f.replace(/\.md$/, '');
    if (/^noindex:\s*true\s*$/m.test(fm)) noindexSlugs.add(slug);
    const m = fm.match(/^fecha:\s*(\S+)/m);
    if (m && !Number.isNaN(Date.parse(m[1]))) lastmodBySlug.set(slug, new Date(m[1]));
  }
}
const slugOf = (page) => {
  const m = String(page).match(/\/noticia\/([^/]+)\/?$/);
  return m ? decodeURIComponent(m[1]) : null;
};

export default defineConfig({
  site: SITE,
  output: 'static',
  trailingSlash: 'always',
  integrations: [
    tailwind({ applyBaseStyles: false }),
    sitemap({
      filter: (page) => {
        const slug = slugOf(page);
        return !(slug && noindexSlugs.has(slug));
      },
      serialize: (item) => {
        const slug = slugOf(item.url);
        if (slug) {
          const d = lastmodBySlug.get(slug);
          if (d) item.lastmod = d.toISOString();
          item.changefreq = 'monthly';
          item.priority = 0.7;
        } else {
          item.changefreq = 'daily';
          item.priority = item.url.replace(/\/$/, '') === SITE.replace(/\/$/, '') ? 1.0 : 0.6;
        }
        return item;
      },
      i18n: {
        defaultLocale: 'es',
        locales: {
          es: 'es',
        },
      },
    }),
  ],
  markdown: {
    rehypePlugins: [
      rehypeSlug,
      [rehypeAutolinkHeadings, {
        behavior: 'append',
        properties: { className: ['anchor-link'], 'aria-label': 'Enlace permanente' },
        content: { type: 'text', value: ' #' },
      }],
    ],
  },
  build: {
    inlineStylesheets: 'auto',
  },
});
