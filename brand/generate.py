#!/usr/bin/env python3
"""joe brand asset generator.

Regenerates every brand asset from code: marks, favicon, lockups,
palette card, typography specimen, and the brand reference one-pager.

Usage:
    pip install cairosvg pillow
    python3 generate.py [output_dir]     # default: directory of this script

Fonts (Zilla Slab, Source Sans 3, IBM Plex Mono) are downloaded from the
google/fonts GitHub repo into ./fonts/ on first run. All OFL-licensed.
"""

import math
import os
import sys
import urllib.request

import cairosvg
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- palette
INK = "#211D19"
RUST = "#C05F2E"
RUST_ON_DARK = "#D97B4A"
BRASS = "#D9A441"
CREAM = "#F5F0E4"
SLATE = "#4A6670"
GRAY = "#6B6459"        # muted text on cream (derived, not a brand color)
HAIRLINE = "#D8D2C4"    # borders on cream (derived, not a brand color)

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(OUT, "fonts")

FONT_FILES = {
    "ZillaSlab-Bold.ttf": "ofl/zillaslab/ZillaSlab-Bold.ttf",
    "ZillaSlab-SemiBold.ttf": "ofl/zillaslab/ZillaSlab-SemiBold.ttf",
    "SourceSans3.ttf": "ofl/sourcesans3/SourceSans3%5Bwght%5D.ttf",
    "IBMPlexMono-Regular.ttf": "ofl/ibmplexmono/IBMPlexMono-Regular.ttf",
    "IBMPlexMono-Medium.ttf": "ofl/ibmplexmono/IBMPlexMono-Medium.ttf",
}


def ensure_fonts():
    os.makedirs(FONT_DIR, exist_ok=True)
    base = "https://raw.githubusercontent.com/google/fonts/main/"
    for local, remote in FONT_FILES.items():
        path = os.path.join(FONT_DIR, local)
        if not os.path.exists(path):
            print(f"fetching {local}")
            urllib.request.urlretrieve(base + remote, path)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


# ------------------------------------------------------------------ marks
def mark_body(ink, rust, sw=10, pr=11, br=16, spw=12, bh=12):
    """Flyball governor in a 140x140 box. Spindle overlaps 6 units into the
    base so the rounded corners weld instead of pinching."""
    return f'''
  <circle cx="70" cy="12" r="{pr}" fill="{ink}"/>
  <line x1="70" y1="16" x2="22" y2="70" stroke="{ink}" stroke-width="{sw}" stroke-linecap="round"/>
  <line x1="70" y1="16" x2="118" y2="70" stroke="{ink}" stroke-width="{sw}" stroke-linecap="round"/>
  <circle cx="22" cy="79" r="{br}" fill="{rust}"/>
  <circle cx="118" cy="79" r="{br}" fill="{rust}"/>
  <rect x="{70 - spw / 2}" y="16" width="{spw}" height="{124 - 16 - bh + 6}" rx="4" fill="{ink}"/>
  <rect x="28" y="{124 - bh}" width="84" height="{bh}" rx="4" fill="{ink}"/>'''


def write_svg(body, viewbox, name):
    doc = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}">{body}\n</svg>'
    with open(os.path.join(OUT, f"{name}.svg"), "w") as f:
        f.write(doc)


def wordmark(ink, sw=13):
    """Drawn lowercase 'joe'. Baseline 100, x-height top 36. o and e carry
    ~2 units of optical overshoot past both lines."""
    parts = []
    jx = 16
    parts.append(f'<circle cx="{jx}" cy="15" r="8.5" fill="{ink}"/>')
    parts.append(
        f'<path d="M {jx} 36 L {jx} 106 A 19 19 0 0 1 {jx - 34} 110" '
        f'fill="none" stroke="{ink}" stroke-width="{sw}" stroke-linecap="round"/>')
    ox, oy, orad = 71, 68, 27.5
    parts.append(f'<circle cx="{ox}" cy="{oy}" r="{orad}" fill="none" stroke="{ink}" stroke-width="{sw}"/>')
    ex, ey, er = 152, 68, 27.5
    a = math.radians(42)
    endx, endy = ex + er * math.cos(a), ey + er * math.sin(a)
    parts.append(
        f'<path d="M {ex - er} {ey} H {ex + er} A {er} {er} 0 1 0 {endx:.1f} {endy:.1f}" '
        f'fill="none" stroke="{ink}" stroke-width="{sw}" stroke-linecap="round"/>')
    return "\n".join(parts)


def lockup(ink, rust, name):
    body = f"<g>{mark_body(ink, rust)}</g>"
    body += f'<g transform="translate(195,10)">{wordmark(ink)}</g>'
    write_svg(body, "-10 -8 404 156", name)


def render_png(name, width, bg=None):
    cairosvg.svg2png(url=os.path.join(OUT, f"{name}.svg"),
                     write_to=os.path.join(OUT, f"{name}.png"),
                     output_width=width, background_color=bg)


def raster(name, width, bg=None):
    tmp = os.path.join(OUT, "_tmp.png")
    cairosvg.svg2png(url=os.path.join(OUT, f"{name}.svg"), write_to=tmp,
                     output_width=width, background_color=bg)
    img = Image.open(tmp).convert("RGBA")
    os.remove(tmp)
    return img


def make_marks():
    write_svg(mark_body(INK, RUST), "0 0 140 140", "joe-mark")
    write_svg(mark_body(CREAM, RUST), "0 0 140 140", "joe-mark-dark")
    write_svg(mark_body(INK, RUST, sw=14, pr=14, br=20, spw=16, bh=16),
              "-8 -12 156 156", "joe-favicon")
    lockup(INK, RUST, "joe-lockup")
    lockup(CREAM, RUST, "joe-lockup-dark")
    render_png("joe-mark", 280, CREAM)
    render_png("joe-mark-dark", 280, INK)
    render_png("joe-favicon", 32, CREAM)
    render_png("joe-lockup", 640, CREAM)
    render_png("joe-lockup-dark", 640, INK)


def make_contact_sheet():
    names = ["joe-mark", "joe-mark-dark", "joe-favicon", "joe-lockup", "joe-lockup-dark"]
    imgs = [Image.open(os.path.join(OUT, f"{n}.png")) for n in names]
    width, y = 700, 10
    height = sum(i.height + 16 for i in imgs) + 10
    sheet = Image.new("RGB", (width, height), "#888888")
    for i in imgs:
        sheet.paste(i, ((width - i.width) // 2, y))
        y += i.height + 16
    sheet.save(os.path.join(OUT, "contact.png"))


# ----------------------------------------------------------- palette card
SWATCHES = [
    ("Ink", INK, "Structure, text, dark ground"),
    ("Rust", RUST, "Primary accent - flyballs, CTAs"),
    ("Rust (on dark)", RUST_ON_DARK, "Lightened rust for text/links on Ink"),
    ("Brass", BRASS, "Secondary warm - editorial illustration only"),
    ("Cream", CREAM, "Light ground"),
    ("Slate", SLATE, "Cool foil - links, info, code accents"),
]


def make_palette_card():
    W, PAD, SH, GAPV = 760, 40, 100, 24
    rows, y = [], 110
    for name, hexv, role in SWATCHES:
        stroke = f' stroke="{HAIRLINE}" stroke-width="1"' if hexv == CREAM else ""
        rows.append(f'<rect x="{PAD}" y="{y}" width="100" height="{SH}" rx="12" fill="{hexv}"{stroke}/>')
        tx = PAD + 128
        rows.append(f'<text x="{tx}" y="{y + 38}" font-family="Helvetica, Arial, sans-serif" '
                    f'font-size="26" font-weight="700" fill="{INK}">{name}</text>')
        rows.append(f'<text x="{tx}" y="{y + 66}" font-family="Menlo, Consolas, monospace" '
                    f'font-size="20" fill="{RUST}">{hexv}</text>')
        rows.append(f'<text x="{tx}" y="{y + 90}" font-family="Helvetica, Arial, sans-serif" '
                    f'font-size="17" fill="{GRAY}">{role}</text>')
        y += SH + GAPV
    H = y + PAD - GAPV
    header = (f'<rect width="{W}" height="{H}" fill="{CREAM}"/>'
              f'<text x="{PAD}" y="62" font-family="Helvetica, Arial, sans-serif" font-size="34" '
              f'font-weight="700" fill="{INK}">joe - brand palette</text>'
              f'<g transform="translate({W - 130},28) scale(0.5)">{mark_body(INK, RUST)}</g>')
    doc = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">{header}{"".join(rows)}</svg>'
    with open(os.path.join(OUT, "joe-palette.svg"), "w") as f:
        f.write(doc)
    cairosvg.svg2png(url=os.path.join(OUT, "joe-palette.svg"),
                     write_to=os.path.join(OUT, "joe-palette.png"), output_width=1520)


# ------------------------------------------------------ typography card
def make_typography_card():
    W, H = 1520, 1240
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    zb = font("ZillaSlab-Bold.ttf", 88)
    zsb = font("ZillaSlab-SemiBold.ttf", 54)
    ss = font("SourceSans3.ttf", 34)
    mono = font("IBMPlexMono-Regular.ttf", 30)
    monoM = font("IBMPlexMono-Medium.ttf", 26)
    lab = font("SourceSans3.ttf", 24)

    y = 60
    d.text((80, y), "joe - typography", font=zsb, fill=INK); y += 110
    d.text((80, y), "DISPLAY / HEADINGS - Zilla Slab Bold & SemiBold", font=lab, fill=GRAY); y += 44
    d.text((80, y), "Governed autonomy.", font=zb, fill=INK); y += 108
    d.text((80, y), "Joe is running, so Joe is governed", font=zsb, fill=RUST); y += 110
    d.text((80, y), "BODY - Source Sans 3", font=lab, fill=GRAY); y += 44
    for line in ["Joe is a self-hosted agent for infrastructure operations. Every tool",
                 "call is classified as read or mutate before it runs, and mutations",
                 "pass through a governed gate. Unknown tools are denied by default."]:
        d.text((80, y), line, font=ss, fill=INK); y += 46
    y += 28
    d.text((80, y), "MONO - IBM Plex Mono (code, CLI, identifiers)", font=lab, fill=GRAY); y += 44
    d.rounded_rectangle((80, y, W - 80, y + 150), radius=16, fill=INK)
    d.text((110, y + 26), "$ joe serve --config joe.yaml", font=mono, fill=CREAM)
    d.text((110, y + 76), "write_floor: observation   # boot-resolved, fail-closed",
           font=mono, fill=RUST_ON_DARK)
    y += 190
    d.text((80, y), "SCALE & ROLES", font=lab, fill=GRAY); y += 50
    for text, color in [
        ("H1  Zilla Slab Bold        clamp(2.4-3.4rem)", INK),
        ("H2  Zilla Slab SemiBold    1.8rem", INK),
        ("Body  Source Sans 3 Regular  1.0-1.06rem / 1.6", GRAY),
        ("Caption/label  Source Sans 3  0.85rem, tracked +2%", GRAY),
        ("Code  IBM Plex Mono Regular  0.92em of body", SLATE),
    ]:
        d.text((80, y), text, font=monoM, fill=color); y += 44
    img.save(os.path.join(OUT, "joe-typography.png"))


# -------------------------------------------------------- brand one-pager
def make_brand_sheet():
    W, H = 1600, 2263
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    zb = font("ZillaSlab-Bold.ttf", 64)
    zsb = font("ZillaSlab-SemiBold.ttf", 40)
    ss = font("SourceSans3.ttf", 28)
    ssl = font("SourceSans3.ttf", 23)
    ss26 = font("SourceSans3.ttf", 26)
    ss20 = font("SourceSans3.ttf", 20)
    ss24 = font("SourceSans3.ttf", 24)
    mono = font("IBMPlexMono-Regular.ttf", 24)
    monoS = font("IBMPlexMono-Regular.ttf", 20)

    def sect(y, label):
        d.text((90, y), label.upper(), font=ss24, fill=RUST)
        d.line((90, y + 40, W - 90, y + 40), fill=HAIRLINE, width=2)
        return y + 70

    lk = raster("joe-lockup", 460)
    img.paste(lk, (90, 70), lk)
    d.text((W - 90, 100), "Brand reference", font=zsb, fill=INK, anchor="ra")
    d.text((W - 90, 160), "v1 - July 2026", font=ssl, fill=GRAY, anchor="ra")

    y = sect(280, "The mark")
    m = raster("joe-mark", 200)
    img.paste(m, (140, y + 50), m)
    d.rounded_rectangle((90, y, 390, y + 300), radius=18, outline=HAIRLINE, width=2)
    d.rounded_rectangle((420, y, 720, y + 300), radius=18, fill=INK)
    md = raster("joe-mark-dark", 200)
    img.paste(md, (470, y + 50), md)
    for w, yy in [(64, 40), (32, 130), (16, 190)]:
        fv = raster("joe-favicon", w, CREAM)
        img.paste(fv, (770, y + yy))
    d.text((860, y + 50), "Watt flyball governor, reduced.", font=ss, fill=INK)
    for i, line in enumerate([
        "Ink structure, rust flyballs - rust is never recolored.",
        "Clearspace: one flyball diameter on all sides.",
        "Minimum size 16px; use joe-favicon.svg below 48px.",
        "Dark surfaces: joe-mark-dark.svg (cream structure).",
    ]):
        d.text((860, y + 92 + i * 38), line, font=ssl, fill=GRAY)
    y += 360

    y = sect(y, "Palette")
    short_roles = ["structure, text", "primary accent", "links on Ink",
                   "editorial only", "light ground", "cool foil"]
    x = 90
    for (name, hexv, _), role in zip(SWATCHES, short_roles):
        d.rounded_rectangle((x, y, x + 215, y + 110), radius=14, fill=hexv,
                            outline=HAIRLINE if hexv == CREAM else None, width=2)
        d.text((x, y + 124), name.replace(" (on dark)", " on dark"), font=ss26, fill=INK)
        d.text((x, y + 156), hexv, font=monoS, fill=RUST)
        d.text((x, y + 186), role, font=ss20, fill=GRAY)
        x += 238
    y += 270

    y = sect(y, "Typography")
    d.text((90, y), "Zilla Slab", font=zb, fill=INK)
    d.text((480, y + 24), "Display & headings - Bold / SemiBold", font=ssl, fill=GRAY)
    y += 90
    d.text((90, y), "Source Sans 3 - body and interface text, regular and semibold.", font=ss, fill=INK)
    d.text((90, y + 40), "Body 1.0-1.06rem / 1.6 line height. Captions 0.85rem tracked.", font=ssl, fill=GRAY)
    y += 100
    d.text((90, y), "IBM Plex Mono - code, CLI, identifiers, hex values.", font=mono, fill=SLATE)
    d.text((90, y + 40), "All three OFL-licensed, self-hosted woff2. Wordmark is drawn paths, never typed.",
           font=ssl, fill=GRAY)
    y += 110

    y = sect(y, "Verbal identity")
    d.text((90, y), "joe - Joe Operates Everything", font=zsb, fill=INK)
    d.text((90, y + 58), "Recursive backronym, GNU tradition. Secondary placement only: README first line,",
           font=ssl, fill=GRAY)
    d.text((90, y + 92), "docs opener, site footer, man-page NAME line. Never inside or beside the mark.",
           font=ssl, fill=GRAY)
    y += 150
    d.text((90, y), "Joe is a self-hosted, open-source AI agent for your infrastructure.", font=ss, fill=INK)
    d.text((90, y + 40), "Primary positioning line. Leads on high-stakes surfaces; the backronym is the wink.",
           font=ssl, fill=GRAY)
    y += 100
    d.text((90, y), "Named for the centrifugal governor - the first machine that governed a machine.",
           font=ss, fill=RUST)
    d.text((90, y + 40), "Origin story, one line. The backronym is the reach; the mark is the restraint.",
           font=ssl, fill=GRAY)
    y += 110

    y = sect(y, "Rules")
    for rule in [
        "Do use the lockup on first appearance per surface; the bare mark thereafter.",
        "Do keep dark variants on transparent backgrounds - never bake in a ground.",
        "Don't recolor the flyballs, add words to the mark, or typeset the wordmark in a font.",
        "Don't place the backronym as the sole positioning statement on a landing surface.",
    ]:
        d.ellipse((94, y + 10, 106, y + 22), fill=RUST)
        d.text((124, y), rule, font=ss, fill=INK)
        y += 48

    img.save(os.path.join(OUT, "joe-brand-sheet.png"))
    img.save(os.path.join(OUT, "joe-brand-sheet.pdf"), resolution=140)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    ensure_fonts()
    make_marks()
    make_contact_sheet()
    make_palette_card()
    make_typography_card()
    make_brand_sheet()
    print(f"assets written to {OUT}")
