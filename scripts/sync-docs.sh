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
#
# ===========================================================================
#  SEED MODE — refresh the committed copy AND stamp it, in one operation.
# ===========================================================================
#  Usage: ./scripts/sync-docs.sh --seed-from /path/to/joe
#
#  Replaces $ROOT/docs/public from <joe-checkout>/docs/public and, in the SAME
#  operation, writes $ROOT/data/joe.yaml describing the exact joe commit the
#  copy came from. Stamping at seed time is what makes the rendered claim true
#  by construction: the data file and the seeded copy are produced together and
#  committed together, so they cannot disagree. CI never checks joe out and
#  never regenerates the stamp — it only reads what was committed here.
#
#  Without --seed-from the script behaves exactly as before (copy + adapt), so
#  the CI invocation and `make sync` / `make dev` / `make build` are unaffected.
# ===========================================================================
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# --- Argument parsing -------------------------------------------------------
# Default (no args) is the pre-existing behavior, byte for byte.
SEED_FROM=""
while [ $# -gt 0 ]; do
  case "$1" in
    --seed-from)
      [ $# -ge 2 ] || { echo "sync-docs: --seed-from requires a path" >&2; exit 1; }
      SEED_FROM="$2"
      shift 2
      ;;
    --seed-from=*)
      SEED_FROM="${1#--seed-from=}"
      shift
      ;;
    -h|--help)
      echo "usage: sync-docs.sh [--seed-from <joe-checkout>]"
      exit 0
      ;;
    *)
      echo "sync-docs: unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

# --- Seed mode --------------------------------------------------------------
# Every check runs BEFORE anything is written, and the stamp is assembled in
# full before it is moved into place: a failure here leaves the tree untouched
# rather than half-seeded or carrying an empty stamp.
if [ -n "$SEED_FROM" ]; then
  if [ ! -d "$SEED_FROM" ]; then
    echo "sync-docs: seed source not found: $SEED_FROM" >&2
    exit 1
  fi
  SEED_ROOT="$(cd "$SEED_FROM" && pwd)"

  if ! git -C "$SEED_ROOT" rev-parse --git-dir >/dev/null 2>&1; then
    echo "sync-docs: not a git checkout (no readable git metadata): $SEED_ROOT" >&2
    exit 1
  fi

  SEED_DOCS="$SEED_ROOT/docs/public"
  if [ ! -d "$SEED_DOCS" ]; then
    echo "sync-docs: seed checkout has no docs/public: $SEED_DOCS" >&2
    exit 1
  fi

  # Full SHA. Required — a stamp without it is not a stamp.
  JOE_COMMIT="$(git -C "$SEED_ROOT" rev-parse HEAD 2>/dev/null || true)"
  if [ -z "$JOE_COMMIT" ]; then
    echo "sync-docs: could not read HEAD commit from $SEED_ROOT" >&2
    exit 1
  fi
  JOE_COMMIT_SHORT="$(git -C "$SEED_ROOT" rev-parse --short HEAD)"

  # Version. `git describe --tags` exits NON-ZERO (128, not 1) on a repo with no
  # tags, so branch on any non-zero exit, not on a specific code. No tags yet is
  # the expected state today, not an error: fall back to the pre-release marker.
  if JOE_VERSION="$(git -C "$SEED_ROOT" describe --tags 2>/dev/null)" && [ -n "$JOE_VERSION" ]; then
    echo "sync-docs: seed version from git describe = $JOE_VERSION"
  else
    JOE_VERSION="pre-release"
    echo "sync-docs: no tags in $SEED_ROOT — version falls back to $JOE_VERSION"
  fi

  SEEDED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

  echo "sync-docs: seeding docs/public from $SEED_DOCS"
  rm -rf "$ROOT/docs/public"
  mkdir -p "$ROOT/docs/public"
  cp -R "$SEED_DOCS"/. "$ROOT/docs/public"/

  # Write the stamp only once every field is known non-empty, via a temp file so
  # a partial write can never land as data/joe.yaml.
  mkdir -p "$ROOT/data"
  stamp_tmp="$(mktemp)"
  {
    echo "# GENERATED by scripts/sync-docs.sh --seed-from — do not edit by hand."
    echo "# Describes the joe checkout that the committed docs/public copy was"
    echo "# seeded from. Committed (not gitignored) because it documents committed"
    echo "# content: CI never checks joe out and cannot regenerate this."
    echo "version: \"${JOE_VERSION}\""
    echo "commit: \"${JOE_COMMIT}\""
    echo "commit_short: \"${JOE_COMMIT_SHORT}\""
    echo "seeded_at: \"${SEEDED_AT}\""
  } > "$stamp_tmp"
  mv "$stamp_tmp" "$ROOT/data/joe.yaml"
  echo "sync-docs: wrote stamp -> data/joe.yaml (version=$JOE_VERSION commit=$JOE_COMMIT_SHORT)"
fi

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

# Duplicate-H1 adaptation seam: Hextra renders the front-matter `title` AS the
# page's <h1>. Source files that ALSO open their body with a `# Heading` matching
# that title therefore render the title twice. Strip that leading body H1 (and one
# blank line after it) when — and only when — it duplicates the title. A body H1
# that differs from the title is left untouched. This keeps docs/public valid for
# standalone viewing (GitHub etc. show the H1) while the site avoids the doubling.
while IFS= read -r -d '' f; do
  tmp="$(mktemp)"
  if awk '
    BEGIN { state = "fm_start" }
    state == "fm_start" {
      if ($0 == "---") { print; state = "fm"; next }
      state = "body_pre"
    }
    state == "fm" {
      print
      if ($0 ~ /^title:/) {
        t = $0; sub(/^title:[ \t]*/, "", t); sub(/[ \t]+$/, "", t)
        gsub(/^["'\'']|["'\'']$/, "", t); title = t
      }
      if ($0 == "---") { state = "body_pre" }
      next
    }
    state == "body_pre" {
      if ($0 ~ /^[ \t]*$/) { print; next }   # keep blank lines before content
      if ($0 ~ /^# /) {
        h = $0; sub(/^# +/, "", h); sub(/[ \t]+$/, "", h)
        if (title != "" && h == title) { stripped = 1; state = "after_h1"; next }
      }
      state = "body"; print; next
    }
    state == "after_h1" {                     # drop one blank line after the H1
      state = "body"; if ($0 ~ /^[ \t]*$/) next
      print; next
    }
    state == "body" { print }
    END { exit (stripped ? 0 : 1) }
  ' "$f" > "$tmp"; then
    mv "$tmp" "$f"
    echo "sync-docs: stripped duplicate H1 -> ${f#$ROOT/}"
  else
    rm -f "$tmp"
  fi
done < <(find "$TARGET" -name '*.md' -print0)

count="$(find "$TARGET" -name '*.md' | wc -l | tr -d ' ')"
echo "sync-docs: wrote $count markdown file(s) into content/docs/"
