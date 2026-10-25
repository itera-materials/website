# Website commands.

set shell := ["bash", "-euo", "pipefail", "-c"]

# Astro's anonymous usage telemetry stays off (D005: no third-party requests, not even at build).
export ASTRO_TELEMETRY_DISABLED := "1"

default:
    @just --list

# Install the locked dependencies
install:
    npm ci

# Build the static site into dist/
build:
    npm run build

# Build, then check the output: languages, links, no scripts, no third-party URLs, no colours
test: build
    python3 scripts/check_site.py

# Live preview while editing at http://localhost:4321
serve:
    npm run dev

# Copy design-system release vVERSION (dist) from ../design-system into vendor/design-system
sync-design-system VERSION:
    git -C ../design-system rev-parse -q --verify "refs/tags/v{{VERSION}}" >/dev/null || { echo "design-system has no tag v{{VERSION}}"; exit 1; }
    rm -rf vendor/design-system && mkdir -p vendor/design-system
    git -C ../design-system archive "v{{VERSION}}" dist | tar -x -C vendor/design-system
    echo "{{VERSION}}" > vendor/design-system/VERSION
    @echo "vendor/design-system = design-system {{VERSION}}. Set release.design-system: {{VERSION}} in the workspace repos.yaml."
