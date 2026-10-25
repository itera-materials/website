"""Site checks: every English text has a French twin, and the custom domain is set. Stdlib only."""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "iteramaterials.com"


class LangSpans(HTMLParser):
    """Collects the sequence of lang="en"/"fr" elements below <body>, with their line numbers."""

    def __init__(self) -> None:
        super().__init__()
        self.in_body = False
        self.spans: list[tuple[str, int]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "body":
            self.in_body = True
        lang = dict(attrs).get("lang")
        if self.in_body and lang in ("en", "fr"):
            self.spans.append((lang, self.getpos()[0]))


def check(root: Path = ROOT) -> list[str]:
    problems = []
    parser = LangSpans()
    parser.feed((root / "index.html").read_text(encoding="utf-8"))
    spans = parser.spans
    i = 0
    while i < len(spans):
        lang, line = spans[i]
        if lang == "en" and i + 1 < len(spans) and spans[i + 1][0] == "fr":
            i += 2
            continue
        problems.append(f"index.html:{line}: lang=\"{lang}\" text without its {'fr' if lang == 'en' else 'en'} twin right after it")
        i += 1
    cname = root / "CNAME"
    if not cname.is_file() or cname.read_text(encoding="utf-8").strip() != DOMAIN:
        problems.append(f"CNAME must contain exactly {DOMAIN}")
    if not spans:
        problems.append("index.html: no lang=\"en\"/\"fr\" texts found")
    return problems


def main() -> int:
    problems = check()
    for problem in problems:
        print(f"  ✗ {problem}")
    if not problems:
        print("  ✓ EN/FR pairs complete, CNAME set")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
