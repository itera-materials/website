"""Checks on the built site (dist/) and the sources. Stdlib only; run after `npm run build`.

EN/FR completeness is enforced by the content schemas at build time (src/content.config.ts);
this script checks what the schemas cannot: every page exists with the right language and
alternates, the custom domain is set, the only scripts are JSON-LD and (when switched on)
Plausible (D021), there are no other third-party URLs (D005), the sitemap, robots.txt and preview
images are in place, and the sources contain no colour literals (style comes only from the
design system).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
DOMAIN = "iteramaterials.com"
PAGES = [
    ("en", "index.html"),
    ("fr", "fr/index.html"),
    ("en", "privacy/index.html"),
    ("fr", "fr/confidentialite/index.html"),
]
PLAUSIBLE_SRC = re.compile(r"^https://plausible\.io/js/pa-[A-Za-z0-9_-]+\.js$")
ALLOWED_URL = re.compile(
    rf"^https://{re.escape(DOMAIN)}/|^http://www\.w3\.org/2000/svg$|^https://schema\.org$|^https://plausible\.io/js/pa-[A-Za-z0-9_-]+\.js$"
)
URL = re.compile(r"""(?:https?:)?//[^\s"'<>)]+""")
SCRIPT = re.compile(r"<script(?P<attrs>[^>]*)>(?P<body>.*?)</script>", re.S)
COLOUR_LITERAL = re.compile(r"#[0-9a-fA-F]{3,8}\b|\b(rgba?|hsla?|oklch)\(")
MAX_PAGE_BYTES = 60_000


def plausible_init(root: Path) -> str:
    """The exact inline init line src/analytics.ts allows."""
    text = (root / "src/analytics.ts").read_text(encoding="utf-8")
    match = re.search(r'PLAUSIBLE_INIT =\s*"([^"]+)"', text)
    return match.group(1) if match else ""


def script_problems(page: str, html: str, init: str) -> list[str]:
    problems = []
    for script in SCRIPT.finditer(html):
        attrs, body = script.group("attrs"), script.group("body").strip()
        src = re.search(r'src="([^"]+)"', attrs)
        if 'type="application/ld+json"' in attrs:
            try:
                json.loads(body)
            except json.JSONDecodeError as error:
                problems.append(f"dist/{page}: JSON-LD does not parse ({error})")
        elif src and PLAUSIBLE_SRC.match(src.group(1)) and not body:
            continue
        elif not src and init and body == init:
            continue
        else:
            problems.append(f"dist/{page}: script not allowed ({attrs.strip() or body[:40]}); only JSON-LD and Plausible")
    return problems


def check(dist: Path = DIST, root: Path = ROOT) -> list[str]:
    problems = []
    if (dist / "CNAME").read_text(encoding="utf-8").strip() != DOMAIN if (dist / "CNAME").is_file() else True:
        problems.append(f"dist/CNAME must contain exactly {DOMAIN} (public/CNAME)")
    init = plausible_init(root)
    for lang, page in PAGES:
        path = dist / page
        if not path.is_file():
            problems.append(f"dist/{page} missing")
            continue
        html = path.read_text(encoding="utf-8")
        if f'<html lang="{lang}"' not in html:
            problems.append(f"dist/{page}: <html lang> is not {lang}")
        if 'name="robots" content="noindex' in html:
            problems.append(f"dist/{page}: must not carry robots noindex")
        for alt in ("en", "fr"):
            if f'hreflang="{alt}"' not in html:
                problems.append(f"dist/{page}: no hreflang alternate for {alt}")
        if 'type="application/ld+json"' not in html:
            problems.append(f"dist/{page}: no Organization JSON-LD")
        if 'property="og:image"' not in html:
            problems.append(f"dist/{page}: no og:image")
        problems += script_problems(page, html, init)
        if len(html.encode()) > MAX_PAGE_BYTES:
            problems.append(f"dist/{page}: {len(html.encode())} bytes, over the {MAX_PAGE_BYTES} budget")
    sitemap = dist / "sitemap.xml"
    if not sitemap.is_file():
        problems.append("dist/sitemap.xml missing")
    else:
        text = sitemap.read_text(encoding="utf-8")
        for _, page in PAGES:
            loc = f"https://{DOMAIN}/" + page.removesuffix("index.html")
            if f"<loc>{loc}</loc>" not in text:
                problems.append(f"dist/sitemap.xml: no entry for {loc}")
    robots = dist / "robots.txt"
    if not robots.is_file() or f"Sitemap: https://{DOMAIN}/sitemap.xml" not in robots.read_text(encoding="utf-8"):
        problems.append("dist/robots.txt must point to the sitemap")
    for image in ("og.png", "logo.png"):
        if not (dist / image).is_file():
            problems.append(f"dist/{image} missing (public/{image})")
    for path in sorted(p for p in dist.rglob("*") if p.suffix in {".html", ".css", ".js"}):
        text = path.read_text(encoding="utf-8")
        for url in sorted(set(URL.findall(text))):
            if url.startswith("//") or not ALLOWED_URL.match(url):
                problems.append(f"{path.relative_to(dist.parent)}: third-party URL {url}")
    for path in sorted((root / "src").rglob("*")):
        if path.suffix in {".astro", ".css", ".ts"} and COLOUR_LITERAL.search(path.read_text(encoding="utf-8")):
            problems.append(f"{path.relative_to(root)}: colour literal; colours come from the design system")
    return problems


def main() -> int:
    problems = check()
    for problem in problems:
        print(f"  ✗ {problem}")
    if not problems:
        sizes = ", ".join(f"{page} {(DIST / page).stat().st_size // 1024} KB" for _, page in PAGES)
        print(f"  ✓ pages, alternates, CNAME, sitemap, robots, JSON-LD, preview images, allowed scripts only ({sizes})")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
