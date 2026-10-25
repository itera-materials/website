// Two versions of the home page (D019): `home` (classic, live at / and /fr/) and
// `homeIndustrial` (preview at /preview/industrial/). One entry per language in each; every key is
// required, so the build fails when a text exists in one language only.
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
const audience = z.strictObject({
  title: z.string(),
  body: z.string(),
  items: z.array(z.string()).min(1),
  note: z.string(),
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
    footer: z.strictObject({ hosting: z.string() }),
  }),
});

const homeIndustrial = defineCollection({
  loader: glob({ pattern: "*.yaml", base: "src/content/home-industrial" }),
  schema: z.strictObject({
    meta,
    skipLink: z.string(),
    nav: z.strictObject({
      label: z.string(),
      process: z.string(),
      work: z.string(),
      contact: z.string(),
      languages: z.string(),
    }),
    hero,
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

export const collections = { home, homeIndustrial };
