# website

Public one-page site for Itera Materials at https://iteramaterials.com, served by GitHub Pages from
`main`. This repo is **public**: never add confidential material, partner names, figures or patent
details unless Vanessa has approved them.

Workspace context, decisions and approvals: the `workspace` repo (`CLAUDE.md`, `docs/`).

- Everything is in `index.html`; no build step, no dependencies.
- Every visible text exists as an adjacent pair: `<span lang="en">…</span><span lang="fr">…</span>`.
- No cookies, analytics, web fonts or third-party requests.
- `just test` before every commit; `just serve` to preview at http://localhost:8000.
