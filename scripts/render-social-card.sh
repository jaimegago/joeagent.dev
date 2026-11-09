#!/usr/bin/env bash
#
# render-social-card.sh — regenerate static/images/joe-social.png from
# scripts/social-card.svg. Invoked by `make social-card`.
#
# Renders with rsvg-convert (librsvg; `brew install librsvg`). Text is set in
# the brand faces, which are resolved from brand/fonts/ through a private
# fontconfig so the output does not depend on what the machine has installed.
# PANGOCAIRO_BACKEND forces pango onto fontconfig: on macOS it defaults to
# CoreText, which ignores FONTCONFIG_FILE and silently substitutes a system
# sans. Same librsvg, same fonts → byte-identical PNG; `--check` verifies it.
#
# Pass --check to render to a temp file and compare it with the committed PNG
# instead of overwriting it (exit 1 on a difference).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/scripts/social-card.svg"
OUT="$ROOT/static/images/joe-social.png"
WIDTH=1200
HEIGHT=630

command -v rsvg-convert >/dev/null || { echo "rsvg-convert not found (brew install librsvg)" >&2; exit 1; }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# Fontconfig that sees only brand/fonts, so a missing face fails loudly
# (falls back to another brand face) rather than silently to a system font.
cat > "$TMP/fonts.conf" <<CONF
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <dir>$ROOT/brand/fonts</dir>
  <cachedir>$TMP/cache</cachedir>
</fontconfig>
CONF

TARGET="$OUT"
[ "${1:-}" = "--check" ] && TARGET="$TMP/joe-social.png"

PANGOCAIRO_BACKEND=fontconfig FONTCONFIG_FILE="$TMP/fonts.conf" rsvg-convert \
  --width "$WIDTH" --height "$HEIGHT" --format png \
  --output "$TARGET" "$SRC"

if [ "${1:-}" = "--check" ]; then
  if cmp -s "$TARGET" "$OUT"; then
    echo "ok: $OUT matches $SRC"
  else
    echo "DIFFERS: $OUT is not what $SRC renders to; run make social-card" >&2
    exit 1
  fi
else
  echo "wrote $OUT ($(wc -c < "$OUT" | tr -d ' ') bytes)"
fi
