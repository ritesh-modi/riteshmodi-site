#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regenerate sitemap.xml with final, 200-status URLs.

Two things the old sitemap got wrong:

  * every <loc> used the .html form, which 301s. A sitemap is a list of the URLs
    you want indexed, so listing a redirect asks the crawler to discard all 32.
  * <priority> on every entry. Google has ignored it for years; it is noise.

<lastmod> is taken from git, skipping commits whose subject starts with "seo:" -
otherwise this metadata pass would stamp today's date on all 34 pages and the
field would mean nothing, which is worse than omitting it.

  python3 tools/build_sitemap.py [--check]
"""
import io, os, re, sys, glob, subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seo_data import SITE

CHECK = "--check" in sys.argv
SKIP_SUBJECTS = ("seo:", "untrack")


def read(p):
    return io.open(p, encoding="utf-8").read()


def git_date(path):
    """Last commit that changed this file for a reason a reader would notice."""
    try:
        out = subprocess.check_output(
            ["git", "log", "--format=%cs\t%s", "--", path],
            stderr=subprocess.DEVNULL).decode("utf-8", "replace")
    except Exception:
        return None
    for line in out.splitlines():
        if "\t" not in line:
            continue
        date, subject = line.split("\t", 1)
        if not subject.lower().startswith(SKIP_SUBJECTS):
            return date
    return None


def card_dates():
    s = read("explorables.html")
    out = {}
    for m in re.finditer(r'<a class="card"([^>]*)>', s):
        a = m.group(1)
        g = lambda k: (re.search(k + r'="([^"]*)"', a) or [None, ""])[1]
        href = g("href")
        if href:
            out[href.rsplit("/", 1)[-1].replace(".html", "")] = g("data-date")
    return out


def main():
    if not os.path.exists("explorables.html"):
        sys.exit("run me from the site root")

    cd = card_dates()
    urls = []

    for f in sorted(glob.glob("*.html")):
        slug = f[:-5]
        if slug == "404":
            continue
        urls.append((SITE + ("/" if slug == "index" else "/" + slug),
                     git_date(f) or "2026-07-26"))

    # For explorables the card's data-date wins over git. git records the last time
    # any byte moved - a domain migration or a metadata sweep touches all 28 files
    # on one day and flattens every lastmod to that date. The card date is
    # maintained by hand and tracks the writing, which is what lastmod is for.
    for f in sorted(glob.glob("explorables/*.html")):
        slug = os.path.basename(f)[:-5]
        urls.append((SITE + "/explorables/" + slug,
                     cd.get(slug) or git_date(f) or "2026-07-26"))

    body = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, mod in urls:
        body += ["  <url>", "    <loc>%s</loc>" % loc,
                 "    <lastmod>%s</lastmod>" % mod, "  </url>"]
    body.append("</urlset>")
    out = "\n".join(body) + "\n"

    if CHECK:
        cur = read("sitemap.xml") if os.path.exists("sitemap.xml") else ""
        if cur != out:
            print("SITEMAP DRIFT - run tools/build_sitemap.py")
            sys.exit(1)
        print("build_sitemap --check: clean")
    else:
        io.open("sitemap.xml", "w", encoding="utf-8").write(out)
        print("sitemap.xml: %d urls, no .html, no <priority>" % len(urls))


if __name__ == "__main__":
    main()
