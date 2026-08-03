#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Point every internal link at the URL the server actually serves.

Azure Static Web Apps serves /about and 301-redirects /about.html to it. Every
link on the site used the .html form, so each click cost a redirect hop and each
crawl spent budget confirming the same thing 87 times.

Also renames tokenization-03A -> tokenization (an internal draft filename that
leaked into a public URL) and keeps a 301 for the old one.

  python3 tools/urls_fix.py [--check]
"""
import io, os, re, sys, glob, json, subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seo_data import RENAMES, NOTES_DIR

CHECK = "--check" in sys.argv


def read(p):
    return io.open(p, encoding="utf-8").read()


def write(p, s):
    io.open(p, "w", encoding="utf-8").write(s)


def targets():
    return (sorted(glob.glob("*.html")) + sorted(glob.glob("explorables/*.html"))
            + sorted(glob.glob("%s/*.html" % NOTES_DIR)) + sorted(glob.glob("assets/*.js")))


def rewrite(s):
    # /foo.html -> /foo, /index.html -> /  ... only for root-relative hrefs, so
    # external links and anything with a query string are left alone.
    s = re.sub(r'(href=")(/(?:[\w./-]*/)?)index\.html(")', r"\1\2\3", s)
    s = re.sub(r'(href=")(/[\w./-]+?)\.html(["#?])', r"\1\2\3", s)
    for old, new in RENAMES.items():
        s = s.replace("/explorables/%s" % old, "/explorables/%s" % new)
    # a bare medium.com in sameAs/footer resolves to nobody; a wrong entity link
    # is worse than a missing one
    s = s.replace('href="https://medium.com/"', 'href="https://medium.com/@ritesh.modi"')
    return s


def main():
    if not os.path.exists("explorables.html"):
        sys.exit("run me from the site root")

    changed = []

    # 1. rename on disk, preserving history
    for old, new in RENAMES.items():
        op, np_ = "explorables/%s.html" % old, "explorables/%s.html" % new
        if os.path.exists(op) and not os.path.exists(np_):
            if CHECK:
                changed.append("rename %s -> %s" % (op, np_))
            else:
                try:
                    subprocess.check_call(["git", "mv", op, np_])
                except Exception:
                    os.rename(op, np_)
                changed.append("renamed %s -> %s" % (op, np_))

    # 2. links
    for p in targets():
        s = read(p)
        out = rewrite(s)
        if out != s:
            changed.append(p)
            if not CHECK:
                write(p, out)

    # 3. a permanent 301 for the old slug, since it has been public
    cfg_p = "staticwebapp.config.json"
    cfg = json.loads(read(cfg_p))
    routes = cfg.setdefault("routes", [])
    want = [{"route": "/explorables/%s" % old,
             "redirect": "/explorables/%s" % new, "statusCode": 301}
            for old, new in RENAMES.items()]
    # tools/ lives in the repo because the sitemap and OG images must be
    # regenerated on every new explorable, but it is not part of the website
    want.append({"route": "/tools/*", "statusCode": 404})
    for w in want:
        if not any(r.get("route") == w["route"] for r in routes):
            routes.append(w)
            changed.append("route %s" % w["route"])
    body = json.dumps(cfg, indent=2, ensure_ascii=False) + "\n"
    if body != read(cfg_p):
        if not CHECK:
            write(cfg_p, body)

    if CHECK:
        if changed:
            print("URL DRIFT (%d):" % len(changed))
            for c in changed:
                print("   " + c)
            sys.exit(1)
        print("urls_fix --check: clean")
    else:
        print("urls_fix: %d change(s)" % len(changed))
        for c in changed:
            print("   " + c)


if __name__ == "__main__":
    main()
