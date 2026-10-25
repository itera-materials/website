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

# Copy design-system release vVERSION (dist) into vendor/FOLDER (D019: `design-system` for the
# industrial version, `design-system-classic` for the classic one)
sync-design-system VERSION FOLDER="design-system":
    git -C ../design-system rev-parse -q --verify "refs/tags/v{{VERSION}}" >/dev/null || { echo "design-system has no tag v{{VERSION}}"; exit 1; }
    rm -rf vendor/{{FOLDER}} && mkdir -p vendor/{{FOLDER}}
    git -C ../design-system archive "v{{VERSION}}" dist | tar -x -C vendor/{{FOLDER}}
    echo "{{VERSION}}" > vendor/{{FOLDER}}/VERSION
    @echo "vendor/{{FOLDER}} = design-system {{VERSION}}. Set release.{{FOLDER}}: {{VERSION}} in the workspace repos.yaml."
