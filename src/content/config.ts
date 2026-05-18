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
  }),
});

export const collections = { noticias };
