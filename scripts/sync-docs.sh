#!/usr/bin/env bash
#
# sync-docs.sh — single-source the documentation tree.
#
# The Hextra docs tree under content/docs/ is GENERATED, never committed. This
# script is the one sync step: it copies documentation from a configurable source
# into content/docs/ and adapts front matter so Hextra's sidebar auto-generates.
# It runs in BOTH local development (`make sync` / `make dev`) and the deploy
# workflow (before `hugo`).
#
# ===========================================================================
#  THE SOURCE SWITCH — this is the ONE place to point at Joe's real docs.
# ===========================================================================
#  The real, permanent source is the **docs/public** tree inside Joe's own
#  repository — a curated, reader-facing product-docs tree, NOT Joe's broader
#  internal docs directory (decision records, investigations, prompts, specs).
#
#  Until Joe is a public repository, CI cannot check Joe's repo out, so this
#  defaults to a **locally-seeded copy** of docs/public committed in THIS repo
#  ($ROOT/docs/public) — labeled-placeholder stubs that keep the build green and
#  render the sidebar today.
#
#  >>> THE ONE FLIP STEP (when Joe is public): change DOCS_SOURCE to a checkout
#  >>> of Joe's public repository's docs/public — e.g. clone joe in CI and set
#  >>> DOCS_SOURCE=<joe-checkout>/docs/public. Nothing else here changes; the
#  >>> seeded $ROOT/docs/public copy is then retired.
#
#  >>> NOTE (curation lives upstream): because the real source is the curated
#  >>> docs/public tree (not Joe's raw docs dir), no curation filter is needed
#  >>> in this script. The front-matter normalization below stays as a safety
#  >>> net for any file that arrives without front matter.
# ===========================================================================
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# The source switch. Default: the locally-seeded docs/public copy.
# Flip (Joe public): DOCS_SOURCE=<joe-checkout>/docs/public make sync
DOCS_SOURCE="${DOCS_SOURCE:-$ROOT/docs/public}"

# The generated, gitignored target.
TARGET="$ROOT/content/docs"

if [ ! -d "$DOCS_SOURCE" ]; then
  echo "sync-docs: source not found: $DOCS_SOURCE" >&2
  exit 1
fi

echo "sync-docs: source = $DOCS_SOURCE"
echo "sync-docs: target = $TARGET"

# Clean and recreate the generated tree.
rm -rf "$TARGET"
mkdir -p "$TARGET"

# Copy the documentation tree verbatim.
cp -R "$DOCS_SOURCE"/. "$TARGET"/

# Front-matter adaptation seam: any .md WITHOUT YAML front matter gets a minimal
# title derived from its filename, so Hextra can place it in the sidebar. The
# placeholder source already carries front matter, so this is a no-op today; it
# is the hook that makes raw Joe docs (which may carry none) render once the
# source switches. Real curation/normalization belongs in the TODO above.
while IFS= read -r -d '' f; do
  first_line="$(head -n 1 "$f" 2>/dev/null || true)"
  if [ "$first_line" != "---" ]; then
    base="$(basename "$f" .md)"
    title="$(echo "$base" | tr '-_' '  ')"
    tmp="$(mktemp)"
    {
      echo "---"
      echo "title: \"${title}\""
      echo "---"
      echo ""
      cat "$f"
    } > "$tmp"
    mv "$tmp" "$f"
    echo "sync-docs: injected front matter -> ${f#$ROOT/}"
  fi
done < <(find "$TARGET" -name '*.md' -print0)

count="$(find "$TARGET" -name '*.md' | wc -l | tr -d ' ')"
echo "sync-docs: wrote $count markdown file(s) into content/docs/"
