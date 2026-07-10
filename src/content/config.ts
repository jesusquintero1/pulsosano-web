import { defineCollection, z } from 'astro:content';

export const CATEGORIAS = [
  'Investigación Clínica',
  'Avances Médicos',
  'Nutrición y Dieta',
  'Salud Mental',
  'Fitness y Ejercicio',
  'Medicina Preventiva',
  'Enfermedades y Tratamientos',
  'Estilo de Vida Saludable',
  'Salud Pública y Política',
] as const;

const noticias = defineCollection({
  type: 'content',
  schema: z.object({
    titulo: z.string().min(5).max(140),
    resumen: z.string().min(20).max(400),
    porQueImporta: z.string().min(10).max(400).optional(),
    categoria: z.enum(CATEGORIAS),
    fuente: z.object({
      nombre: z.string(),
      url: z.string().url(),
    }),
    fecha: z.coerce.date(),
    tags: z.array(z.string()).default([]),
    imagen: z.string().url().optional(),
    autorIA: z.string().default('claude-haiku-4-5'),
    // Poda de calidad: excluye el artículo de sitemaps/RSS y emite meta robots
    // noindex. Para artículos débiles/off-topic/duplicados (rescate calidad 2026-07).
    noindex: z.boolean().default(false),
    // SEO: FAQ para rich results / "Otras preguntas" (artículos nuevos). Opcional:
    // los 1.170 históricos no lo tienen y deben seguir validando.
    faqs: z.array(z.object({
      pregunta: z.string().min(5).max(200),
      respuesta: z.string().min(10).max(700),
    })).default([]),
    // SEO: entidades médicas canónicas para el Knowledge Graph (sameAs a Wikipedia).
    entidades: z.array(z.object({
      nombre: z.string().min(2).max(120),
      tipo: z.string().max(60).optional(),
      wikipedia: z.string().url().optional(),
    })).default([]),
  }),
});

export const collections = { noticias };
