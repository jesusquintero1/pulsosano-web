// @ts-check
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';
import rehypeSlug from 'rehype-slug';
import rehypeAutolinkHeadings from 'rehype-autolink-headings';
import fs from 'node:fs';
import path from 'node:path';

const SITE = process.env.SITE_URL || 'https://PulsoSano.com';

// Poda de calidad: URLs con `noindex: true` en su frontmatter quedan fuera del
// sitemap principal (rescate calidad 2026-07). Se leen los .md en build time.
const NOTICIAS_DIR = path.resolve('./src/content/noticias');
const noindexSlugs = new Set(
  fs.existsSync(NOTICIAS_DIR)
    ? fs.readdirSync(NOTICIAS_DIR)
        .filter((f) => f.endsWith('.md'))
        .filter((f) => {
          const fm = fs.readFileSync(path.join(NOTICIAS_DIR, f), 'utf8').split(/^---\s*$/m)[1] || '';
          return /^noindex:\s*true\s*$/m.test(fm);
        })
        .map((f) => f.replace(/\.md$/, ''))
    : []
);

export default defineConfig({
  site: SITE,
  output: 'static',
  trailingSlash: 'ignore',
  integrations: [
    tailwind({ applyBaseStyles: false }),
    sitemap({
      changefreq: 'daily',
      priority: 0.7,
      lastmod: new Date(),
      filter: (page) => {
        const m = page.match(/\/noticia\/([^/]+)\/?$/);
        return !(m && noindexSlugs.has(decodeURIComponent(m[1])));
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
