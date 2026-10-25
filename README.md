# iteramaterials.com

Bilingual (EN/FR) website for Itera Materials, built with Astro and served free by GitHub Pages
at https://iteramaterials.com (English at `/`, French at `/fr/`).

## Editing text

All text is in `src/content/home/en.yaml` and `src/content/home/fr.yaml`, with the same keys in
both. Change both, run `just test`, commit and push to `main`; the deploy workflow publishes in a
minute or two. The build fails if a key exists in one language only.

## Editing style

Nothing here defines colours or type: the page uses the classes of the Itera design system,
copied into `vendor/design-system/` from a tagged release (`just sync-design-system X.Y.Z`).
Style changes happen in the `brand` and `design-system` repos.

## Commands

`just install` (once), `just serve` (live preview at http://localhost:4321), `just test` (build +
checks: both languages, no scripts, no third-party URLs, page size budget).

## Hosting

- GitHub Pages, deployed by `.github/workflows/deploy.yml` (Pages source: GitHub Actions).
  `public/CNAME` holds the custom domain.
- DNS is at GoDaddy: four `A` records for `@` pointing at GitHub Pages, and `www` as a `CNAME` to
  `itera-materials.github.io`.
- Email (Google Workspace MX records) is separate and must not be changed when editing website DNS.
- No cookies, analytics, client JavaScript or third-party requests, so no cookie banner is needed.
