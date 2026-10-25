# iteramaterials.com

One-page bilingual (EN/FR) website for Itera Materials, served free by GitHub Pages at https://iteramaterials.com.

## Editing

Everything is in `index.html`; there is no build step. Each piece of text appears twice, once per language:

```html
<span lang="en">English text</span><span lang="fr">Texte français</span>
```

Change both, commit, and push to `main`. GitHub Pages republishes within a minute or two.

To preview locally, open `index.html` in a browser.

## Hosting

- GitHub Pages, deployed from the `main` branch root. `CNAME` holds the custom domain.
- DNS is at GoDaddy: four `A` records for `@` pointing at GitHub Pages, and `www` as a `CNAME` to `itera-materials.github.io`.
- Email (Google Workspace MX records) is separate and must not be changed when editing website DNS.
- No cookies, analytics or third-party requests, so no cookie banner is needed.
