"""Checks on the built site (dist/) and the sources. Stdlib only; run after `npm run build`.

EN/FR completeness is enforced by the content schema at build time (src/content.config.ts);
this script checks what the schema cannot: both pages exist with the right language and
alternates, the custom domain is set, the output has no scripts and no third-party URLs (D005),
and the sources contain no colour literals (style comes only from the design system).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
DOMAIN = "iteramaterials.com"
PAGES = {"en": "index.html", "fr": "fr/index.html"}
ALLOWED_URL = re.compile(rf"^https://{re.escape(DOMAIN)}/|^http://www\.w3\.org/2000/svg$")
URL = re.compile(r"""(?:https?:)?//[^\s"'<>)]+""")
COLOUR_LITERAL = re.compile(r"#[0-9a-fA-F]{3,8}\b|\b(rgba?|hsla?|oklch)\(")
MAX_PAGE_BYTES = 60_000


def check(dist: Path = DIST, root: Path = ROOT) -> list[str]:
    problems = []
    if (dist / "CNAME").read_text(encoding="utf-8").strip() != DOMAIN if (dist / "CNAME").is_file() else True:
        problems.append(f"dist/CNAME must contain exactly {DOMAIN} (public/CNAME)")
    for lang, page in PAGES.items():
        path = dist / page
        if not path.is_file():
            problems.append(f"dist/{page} missing")
            continue
        html = path.read_text(encoding="utf-8")
        if f'<html lang="{lang}"' not in html:
            problems.append(f"dist/{page}: <html lang> is not {lang}")
        for alt in PAGES:
            if f'hreflang="{alt}"' not in html:
                problems.append(f"dist/{page}: no hreflang alternate for {alt}")
        if "<script" in html:
            problems.append(f"dist/{page}: contains a <script>; the site ships no JavaScript")
        if len(html.encode()) > MAX_PAGE_BYTES:
            problems.append(f"dist/{page}: {len(html.encode())} bytes, over the {MAX_PAGE_BYTES} budget")
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
        sizes = ", ".join(f"{page} {(DIST / page).stat().st_size // 1024} KB" for page in PAGES.values())
        print(f"  ✓ both languages, alternates, CNAME, no scripts, no third-party URLs ({sizes})")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
