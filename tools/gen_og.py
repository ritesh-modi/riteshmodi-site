#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render a 1200x630 share card per page.

The site had no og:image at all, so every LinkedIn and Slack share rendered as a
grey text stub. These cards are generated rather than screenshotted: a screenshot
of an interactive figure is unreadable at card size, and half the explorables open
on a near-empty canvas that only fills in once you touch it.

Each card borrows the palette of its own page. The CSS custom properties are named
differently across the collection (--accent, --ac, --ink-accent, --paper, --bg...),
so colours are picked by measurement instead of by name: lightest swatch is the
paper, darkest is the ink, most saturated is the accent. That holds for pages that
have not been written yet.

  python3 tools/gen_og.py [--check] [--force]
"""
import io, os, re, sys, glob, colorsys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seo_data import PAGES, EXPLORABLES

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
OUT = "og"
CHECK = "--check" in sys.argv
FORCE = "--force" in sys.argv

F_TITLE = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
F_KICK = "/System/Library/Fonts/Supplemental/Futura.ttc"
F_BODY = "/System/Library/Fonts/Supplemental/Georgia.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def hex2rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lum(c):
    return (0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]) / 255.0


def sat(c):
    return colorsys.rgb_to_hls(*[x / 255.0 for x in c])[2]


def palette(path):
    """lightest / darkest / most saturated of whatever the page declares."""
    s = io.open(path, encoding="utf-8", errors="replace").read()
    hexes = re.findall(r"--[\w-]+\s*:\s*(#[0-9A-Fa-f]{3,6})\b", s[:14000])
    cols = []
    for h in hexes:
        try:
            cols.append(hex2rgb(h))
        except Exception:
            pass
    if not cols:
        return (246, 243, 239), (26, 26, 26), (156, 58, 95)
    paper = max(cols, key=lum)
    ink = min(cols, key=lum)
    cand = [c for c in cols if 0.18 < lum(c) < 0.72]
    accent = max(cand or cols, key=sat)
    if lum(paper) < 0.80:
        paper = (246, 243, 239)
    if lum(ink) > 0.35:
        ink = (26, 26, 26)
    return paper, ink, darken_to_contrast(accent, paper)


def contrast(a, b):
    la, lb = lum(a) + 0.05, lum(b) + 0.05
    return max(la, lb) / min(la, lb)


def darken_to_contrast(accent, paper, want=3.2):
    """Several pages declare their accent as a pale tint intended for fills, not
    for text. Picked as-is it produces a kicker you cannot read on a light card,
    so walk the lightness down until it clears a legible ratio."""
    h, l, s = colorsys.rgb_to_hls(*[c / 255.0 for c in accent])
    for _ in range(24):
        c = tuple(int(round(v * 255)) for v in colorsys.hls_to_rgb(h, l, s))
        if contrast(c, paper) >= want:
            return c
        l = max(0.0, l - 0.04)
    return tuple(int(round(v * 255)) for v in colorsys.hls_to_rgb(h, l, s))


def wrap(draw, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def title_of(path, fallback):
    s = io.open(path, encoding="utf-8", errors="replace").read()
    m = re.search(r"<title>(.*?)</title>", s, re.S)
    if not m:
        return fallback
    t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()
    # titles are written "Subject: the angle" - the card has room for the subject
    return t


def card(path, slug, kicker, out_png):
    paper, ink, accent = palette(path)
    img = Image.new("RGB", (W, H), paper)
    d = ImageDraw.Draw(img)

    # a broad accent band down the left, and a hairline rule under the kicker:
    # enough structure that the card reads as designed at thumbnail size
    d.rectangle([0, 0, 18, H], fill=accent)

    pad_l, pad_r = 86, 80
    maxw = W - pad_l - pad_r

    fk = font(F_KICK, 25)
    kick = kicker.upper()
    # Futura.ttc has no built-in tracking; fake it so the kicker reads as a label
    x = pad_l
    for ch in kick:
        d.text((x, 74), ch, font=fk, fill=accent)
        x += d.textlength(ch, font=fk) + 3.0

    d.line([pad_l, 122, W - pad_r, 122], fill=accent, width=2)

    size = 74
    ft = font(F_TITLE, size)
    lines = wrap(d, title_of(path, slug), ft, maxw)
    while len(lines) > 3 and size > 44:
        size -= 5
        ft = font(F_TITLE, size)
        lines = wrap(d, title_of(path, slug), ft, maxw)
    lines = lines[:3]

    # centre the title in the space between the rule and the footer, so a two-line
    # headline does not float with a hole under it
    step = int(size * 1.24)
    top, bot = 150, H - 120
    y = top + max(0, ((bot - top) - len(lines) * step) // 2)
    for ln in lines:
        d.text((pad_l, y), ln, font=ft, fill=ink)
        y += step

    fb = font(F_BODY, 27)
    d.text((pad_l, H - 92), "loopingly.com", font=fb, fill=ink)
    tag = "Ritesh Modi"
    d.text((W - pad_r - d.textlength(tag, font=fb), H - 92), tag, font=fb, fill=accent)

    img.save(out_png, "PNG", optimize=True)


def main():
    if not os.path.exists("explorables.html"):
        sys.exit("run me from the site root")
    if not os.path.exists(OUT):
        os.makedirs(OUT)

    # the footer already says "Ritesh Modi"; the kicker should say what the page is
    KICK = {"index": "Interactive explorables", "explorables": "The explorables",
            "about": "About", "books": "Books", "talks": "Talks & recognition"}
    jobs = [(s + ".html", s, KICK.get(s, "Ritesh Modi")) for s in PAGES]
    jobs += [("explorables/%s.html" % s, s, "Interactive explorable") for s in EXPLORABLES]

    missing, made = [], 0
    for src, slug, kick in jobs:
        if not os.path.exists(src):
            continue
        dst = os.path.join(OUT, slug + ".png")
        if CHECK:
            if not os.path.exists(dst):
                missing.append(dst)
            continue
        if os.path.exists(dst) and not FORCE:
            continue
        card(src, slug, kick, dst)
        made += 1

    if CHECK:
        if missing:
            print("MISSING OG IMAGES (%d):" % len(missing))
            for m in missing:
                print("   " + m)
            sys.exit(1)
        print("gen_og --check: all present")
    else:
        print("og: wrote %d card(s) to %s/" % (made, OUT))


if __name__ == "__main__":
    main()
