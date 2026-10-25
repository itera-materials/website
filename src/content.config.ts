// One entry per language (src/content/home/en.yaml, fr.yaml). Every key is required, so the
// build fails when a text exists in one language only.
import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "astro/zod";

const block = z.object({ title: z.string(), body: z.string() });
const meta = z.strictObject({ title: z.string(), description: z.string(), ogDescription: z.string() });
const hero = z.strictObject({
  eyebrow: z.string(),
  title: z.string(),
  lead: z.string(),
  primary: z.string(),
  secondary: z.string(),
});

const home = defineCollection({
  loader: glob({ pattern: "*.yaml", base: "src/content/home" }),
  schema: z.strictObject({
    meta,
    skipLink: z.string(),
    nav: z.strictObject({
      label: z.string(),
      approach: z.string(),
      partners: z.string(),
      contact: z.string(),
      languages: z.string(),
    }),
    hero,
    problem: z.strictObject({ title: z.string(), body: z.string(), callout: z.string() }),
    approach: z.strictObject({ title: z.string(), intro: z.string(), steps: z.array(block).length(3) }),
    partners: z.strictObject({ title: z.string(), intro: z.string(), groups: z.array(block).length(2) }),
    contact: z.strictObject({ title: z.string(), body: z.string() }),
    footer: z.strictObject({ note: z.string(), privacy: z.string() }),
  }),
});

// Privacy notice (D021): sections marked `analytics: true` show only while Plausible is on.
const privacy = defineCollection({
  loader: glob({ pattern: "*.yaml", base: "src/content/privacy" }),
  schema: z.strictObject({
    meta,
    title: z.string(),
    updated: z.string(),
    sections: z.array(z.strictObject({ title: z.string(), body: z.string(), analytics: z.boolean().default(false) })).min(1),
  }),
});

export const collections = { home, privacy };
