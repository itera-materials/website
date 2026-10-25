# website

Public bilingual site for Itera Materials at https://iteramaterials.com: Astro, static output,
deployed to GitHub Pages by `.github/workflows/deploy.yml`. This repo is **public**: never add
confidential material, partner names, figures or patent details unless Vanessa has approved them.

Workspace context, decisions and approvals: the `workspace` repo (`CLAUDE.md`, `docs/`).

- Text lives in `src/content/home/{en,fr}.yaml`, same keys in both (the schema in
  `src/content.config.ts` fails the build otherwise). French: non-breaking space before `: ; ! ?`.
- Style comes only from `vendor/design-system/` (synced from a tagged release, never edited here);
  no colour literals in `src/`. A missing component belongs in the design-system repo.
- No cookies, web fonts or third-party requests; the only scripts are the Organization JSON-LD and
  the pinned GoatCounter script set in `src/analytics.ts` (D022). The privacy notice must match what runs.
- New pages go into `src/pages/sitemap.xml.ts` and `PAGES` in `scripts/check_site.py`.
- `just test` before every commit; `just serve` to preview at http://localhost:4321.
