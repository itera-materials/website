# Website commands.

set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

# EN/FR pairs complete and CNAME set
test:
    python3 scripts/check_site.py

# Serve the site locally at http://localhost:8000
serve:
    python3 -m http.server 8000
