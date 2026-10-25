// One entry per language (src/content/home/en.yaml, fr.yaml). Every key is required, so the
// build fails when a text exists in one language only.
import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "astro/zod";

const block = z.object({ title: z.string(), body: z.string() });
const audience = z.strictObject({
  title: z.string(),
  body: z.string(),
  items: z.array(z.string()).min(1),
  note: z.string(),
});

const home = defineCollection({
  loader: glob({ pattern: "*.yaml", base: "src/content/home" }),
  schema: z.strictObject({
    meta: z.strictObject({ title: z.string(), description: z.string(), ogDescription: z.string() }),
    skipLink: z.string(),
    nav: z.strictObject({
      label: z.string(),
      process: z.string(),
      work: z.string(),
      contact: z.string(),
      languages: z.string(),
    }),
    hero: z.strictObject({
      eyebrow: z.string(),
      title: z.string(),
      lead: z.string(),
      primary: z.string(),
      secondary: z.string(),
    }),
    why: z.strictObject({
      label: z.string(),
      items: z.array(z.strictObject({ value: z.string(), label: z.string() })).length(4),
    }),
    problem: z.strictObject({ title: z.string(), body: z.string(), callout: z.string() }),
    approach: z.strictObject({ title: z.string(), intro: z.string(), steps: z.array(block).length(3) }),
    partners: z.strictObject({ title: z.string(), intro: z.string(), waste: audience, fibre: audience }),
    contact: z.strictObject({ title: z.string(), body: z.string() }),
    footer: z.strictObject({ hosting: z.string() }),
  }),
});

export const collections = { home };
