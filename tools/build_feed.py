#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate /feed.xml (Atom).

The audience for explorables - the Distill / Observable / Bret Victor corner - is
unusually RSS-heavy, and feeds get pulled into newsletters that link back. There
was no feed at all, so none of that could happen.

Atom rather than RSS 2.0: dates are unambiguous (RFC 3339) and every reader
supports it.

  python3 tools/build_feed.py [--check]
"""
import io, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seo_data import SITE, AUTHOR, EXPLORABLES

CHECK = "--check" in sys.argv


def read(p):
    return io.open(p, encoding="utf-8").read()


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def main():
    if not os.path.exists("explorables.html"):
        sys.exit("run me from the site root")

    s = read("explorables.html")
    items = []
    for m in re.finditer(r'<a class="card"([^>]*)>(.*?)</a>', s, re.S):
        attrs, body = m.group(1), m.group(2)
        g = lambda k: (re.search(k + r'="([^"]*)"', attrs) or [None, ""])[1]
        href = g("href")
        # see the note in seo_apply.cards(): "soon" occurs inside data-q
        if not href.startswith("/explorables/"):
            continue
        slug = href.rsplit("/", 1)[-1]
        h3 = re.search(r"<h3[^>]*>(.*?)</h3>", body, re.S)
        title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h3.group(1))).strip() if h3 else slug
        meta = EXPLORABLES.get(slug, {})
        items.append((g("data-date") or "2026-07-26", slug, title,
                      meta.get("desc", "")))

    items.sort(reverse=True)
    updated = (items[0][0] if items else "2026-07-26") + "T00:00:00Z"

    L = ['<?xml version="1.0" encoding="utf-8"?>',
         '<feed xmlns="http://www.w3.org/2005/Atom">',
         "  <title>%s — Explorables</title>" % esc(AUTHOR),
         "  <subtitle>Interactive explainers you learn by messing with.</subtitle>",
         '  <link href="%s/feed.xml" rel="self"/>' % SITE,
         '  <link href="%s/explorables"/>' % SITE,
         "  <id>%s/</id>" % SITE,
         "  <updated>%s</updated>" % updated,
         "  <author><name>%s</name><uri>%s/about</uri></author>" % (esc(AUTHOR), SITE)]
    for date, slug, title, desc in items:
        u = "%s/explorables/%s" % (SITE, slug)
        L += ["  <entry>",
              "    <title>%s</title>" % esc(title),
              '    <link href="%s"/>' % u,
              "    <id>%s</id>" % u,
              "    <updated>%sT00:00:00Z</updated>" % date,
              "    <published>%sT00:00:00Z</published>" % date,
              "    <summary>%s</summary>" % esc(desc),
              "  </entry>"]
    L.append("</feed>")
    out = "\n".join(L) + "\n"

    if CHECK:
        cur = read("feed.xml") if os.path.exists("feed.xml") else ""
        if cur != out:
            print("FEED DRIFT - run tools/build_feed.py")
            sys.exit(1)
        print("build_feed --check: clean")
    else:
        io.open("feed.xml", "w", encoding="utf-8").write(out)
        print("feed.xml: %d entries" % len(items))


if __name__ == "__main__":
    main()
