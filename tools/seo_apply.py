#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write canonical / description / OG / Twitter / JSON-LD into every page.

Everything this script emits lives between <!-- seo:begin --> and <!-- seo:end -->,
so running it twice replaces the block instead of stacking a second copy. Any
canonical, description, og:* or twitter:* tag found OUTSIDE the block is deleted
first - those are the hand-written ones this replaces, and two canonicals is worse
than none because the crawler picks for you.

  python3 tools/seo_apply.py          # apply
  python3 tools/seo_apply.py --check  # report drift, change nothing, exit 1 if any

Run from the site root.
"""
import io, json, os, re, sys, glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seo_data import (SITE, AUTHOR, PAGES, EXPLORABLES, PERSON, RENAMES,
                      NOTES, NOTES_DIR)

BEGIN, END = "<!-- seo:begin -->", "<!-- seo:end -->"
CHECK = "--check" in sys.argv

# The five GRC/atlas pages were authored as bare fragments: they open with <style>
# and have no doctype, no <head> and no viewport. Browsers cope by inferring all
# three, but the inferred document is in quirks mode and has no mobile viewport,
# which is a real ranking and rendering problem rather than a cosmetic one.
FRAGMENTS = set()


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def read(p):
    return io.open(p, encoding="utf-8").read()


def write(p, s):
    io.open(p, "w", encoding="utf-8").write(s)


def cards():
    """Date, topic, level and title per explorable, straight from the listing page."""
    s = read("explorables.html")
    out = {}
    for m in re.finditer(r'<a class="card"([^>]*)>(.*?)</a>', s, re.S):
        attrs, body = m.group(1), m.group(2)
        g = lambda k: (re.search(k + r'="([^"]*)"', attrs) or [None, ""])[1]
        href = g("href")
        # Placeholder cards are class="card soon", which the pattern above already
        # excludes. Do NOT substring-test attrs for "soon": data-q holds the whole
        # search haystack, so any page whose prose contains the word disappears.
        if not href.startswith("/explorables/"):
            continue
        slug = href.rsplit("/", 1)[-1].replace(".html", "")
        slug = RENAMES.get(slug, slug)
        h3 = re.search(r"<h3[^>]*>(.*?)</h3>", body, re.S)
        out[slug] = dict(
            date=g("data-date") or "",
            topic=g("data-topic") or "",
            level=g("data-level") or "",
            card_title=re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h3.group(1))).strip() if h3 else "",
        )
    return out


def page_title(s):
    m = re.search(r"<title>(.*?)</title>", s, re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def strip_unmanaged(head):
    """Remove the hand-written tags this script now owns, leaving charset/viewport/title."""
    pats = [
        r'\s*<link[^>]+rel=["\']canonical["\'][^>]*>',
        r'\s*<meta[^>]+name=["\']description["\'][^>]*>',
        r'\s*<meta[^>]+property=["\']og:[^"\']*["\'][^>]*>',
        r'\s*<meta[^>]+name=["\']twitter:[^"\']*["\'][^>]*>',
        r'\s*<script[^>]+type=["\']application/ld\+json["\'][^>]*>.*?</script>',
    ]
    for p in pats:
        head = re.sub(p, "", head, flags=re.I | re.S)
    return head


def block(url, title, desc, short, image, ld, ART=False):
    """The managed head block. og:image is absolute because scrapers do not resolve
    relative URLs - a relative og:image is the single most common reason a share
    card renders blank."""
    L = [BEGIN,
         '<meta name="description" content="%s">' % esc(desc),
         '<link rel="canonical" href="%s">' % url,
         '<link rel="alternate" type="application/atom+xml" title="%s — Explorables" href="%s/feed.xml">'
         % (esc(AUTHOR), SITE),
         '<meta property="og:type" content="%s">' % ("article" if ART else "website"),
         '<meta property="og:site_name" content="%s">' % esc(AUTHOR),
         '<meta property="og:locale" content="en_GB">',
         '<meta property="og:title" content="%s">' % esc(title),
         '<meta property="og:description" content="%s">' % esc(short),
         '<meta property="og:url" content="%s">' % url,
         '<meta property="og:image" content="%s">' % image,
         '<meta property="og:image:width" content="1200">',
         '<meta property="og:image:height" content="630">',
         '<meta property="og:image:alt" content="%s">' % esc(title),
         '<meta name="twitter:card" content="summary_large_image">',
         '<meta name="twitter:title" content="%s">' % esc(title),
         '<meta name="twitter:description" content="%s">' % esc(short),
         '<meta name="twitter:image" content="%s">' % image,
         ]
    for obj in ld:
        L.append('<script type="application/ld+json">%s</script>'
                 % json.dumps(obj, ensure_ascii=False, separators=(",", ":")))
    L.append(END)
    return "\n  ".join(L)


def wrap_fragment(s, title):
    """Give a bare fragment a real document: doctype, lang, charset, viewport."""
    s = re.sub(r"<title>.*?</title>\s*", "", s, count=1, flags=re.S)
    return ('<!DOCTYPE html>\n<html lang="en">\n<head>\n'
            '  <meta charset="utf-8">\n'
            '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '  <title>%s</title>\n'
            '</head>\n<body>\n%s\n</body>\n</html>\n' % (esc(title), s.strip()))


def apply_page(path, slug, url, meta, info, drift):
    s = read(path)
    orig = s

    # 1. fragments first, so everything below can assume a real <head>.
    # Test for the CLOSING tag: "<head" is a substring of "<header>", which these
    # pages do have, so an opening-tag test calls a fragment a full document and
    # the splice below lands at index -1 - metadata at the end of <body>, where a
    # canonical is ignored outright.
    if "</head>" not in s.lower():
        FRAGMENTS.add(path)
        s = wrap_fragment(s, page_title(s) or info.get("card_title") or slug)

    title = page_title(s) or info.get("card_title") or slug
    desc = meta["desc"]
    short = meta.get("short", desc)
    image = "%s/og/%s.png" % (SITE, slug)

    # 2. structured data
    ld = []
    is_note = ("/%s/" % NOTES_DIR) in url
    is_article = ("/explorables/" in url) or is_note
    if is_article:
        date = info.get("date") or "2026-07-26"
        ld.append({
            "@context": "https://schema.org",
            "@type": ["Article", "LearningResource"],
            "headline": title[:110],
            "description": desc,
            "url": url,
            "image": image,
            "datePublished": date,
            "dateModified": date,
            "inLanguage": "en",
            "author": {"@type": "Person", "name": AUTHOR, "url": SITE + "/about"},
            "publisher": {"@type": "Person", "name": AUTHOR, "url": SITE + "/"},
            "learningResourceType": "Interactive explorable",
            "educationalLevel": "Beginner" if info.get("level") == "beginner" else "Intermediate",
            "isAccessibleForFree": True,
            "about": {"@type": "Thing", "name": meta["about"]},
        })
        ld.append({
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2,
                 "name": "Notes" if is_note else "Explorables",
                 "item": SITE + ("/" + NOTES_DIR if is_note else "/explorables")},
                {"@type": "ListItem", "position": 3,
                 "name": info.get("card_title") or title},
            ],
        })
    if slug in ("index", "about"):
        ld.append(PERSON)

    if slug == "explorables":
        # the listing is the collection's front door; without an ItemList a crawler
        # sees 28 undifferentiated links and no statement that they belong together
        items = sorted(cards().items(), key=lambda kv: kv[1].get("date", ""), reverse=True)
        ld.append({
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": "Explorables",
            "description": desc,
            "url": url,
            "isPartOf": {"@type": "WebSite", "name": AUTHOR, "url": SITE + "/"},
            "mainEntity": {
                "@type": "ItemList",
                "numberOfItems": len(items),
                "itemListElement": [
                    {"@type": "ListItem", "position": i + 1,
                     "url": "%s/explorables/%s" % (SITE, s),
                     "name": v.get("card_title") or s}
                    for i, (s, v) in enumerate(items)],
            },
        })

    blk = block(url, title, desc, short, image, ld, ART=is_article)

    # 3. splice into head
    head_end = s.lower().find("</head>")
    if head_end < 0:
        raise SystemExit("%s: no </head> even after wrapping - refusing to splice" % path)
    head, rest = s[:head_end], s[head_end:]
    head = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), "", head, flags=re.S)
    head = strip_unmanaged(head)
    head = head.rstrip() + "\n  " + blk + "\n"
    s = head + rest

    if s != orig:
        drift.append(path)
        if not CHECK:
            write(path, s)


def main():
    if not os.path.exists("explorables.html"):
        sys.exit("run me from the site root")

    info_all = cards()
    drift = []

    for slug, meta in PAGES.items():
        p = slug + ".html"
        if os.path.exists(p):
            url = SITE + ("/" if slug == "index" else "/" + slug)
            apply_page(p, slug, url, meta, {}, drift)

    for slug, meta in EXPLORABLES.items():
        p = "explorables/%s.html" % slug
        if not os.path.exists(p):
            print("  ! missing %s" % p)
            continue
        apply_page(p, slug, "%s/explorables/%s" % (SITE, slug), meta,
                   info_all.get(slug, {}), drift)

    for slug, meta in NOTES.items():
        p = "%s/%s.html" % (NOTES_DIR, slug)
        if not os.path.exists(p):
            print("  ! missing %s" % p)
            continue
        apply_page(p, slug, "%s/%s/%s" % (SITE, NOTES_DIR, slug), meta, {}, drift)

    have = {os.path.basename(f)[:-5] for f in glob.glob("explorables/*.html")}
    for extra in sorted(have - set(EXPLORABLES)):
        print("  ! no metadata authored for explorables/%s.html" % extra)
    have_n = {os.path.basename(f)[:-5] for f in glob.glob("%s/*.html" % NOTES_DIR)}
    for extra in sorted(have_n - set(NOTES)):
        print("  ! no metadata authored for %s/%s.html — add it to NOTES in seo_data.py"
              % (NOTES_DIR, extra))

    if CHECK:
        if drift:
            print("SEO DRIFT in %d file(s):" % len(drift))
            for d in drift:
                print("   " + d)
            sys.exit(1)
        print("seo_apply --check: clean")
    else:
        print("updated %d file(s)" % len(drift))
        if FRAGMENTS:
            print("wrapped %d fragment(s) in a real document:" % len(FRAGMENTS))
            for f in sorted(FRAGMENTS):
                print("   " + f)


if __name__ == "__main__":
    main()
