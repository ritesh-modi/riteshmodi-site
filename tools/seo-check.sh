#!/usr/bin/env bash
# SEO gate. Run from the site root:  bash tools/seo-check.sh
#
# The generators above are idempotent, so "--check" means "would running this
# change anything?" - which catches a page added by hand without metadata. The
# assertions after that are independent of the generators, because a generator
# checking its own output only proves it is consistent, not that it is correct.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

fail=0
say() { printf '%s\n' "$*"; }
step() { printf '\n\033[1m%s\033[0m\n' "$*"; }

step "1. generators are up to date"
for c in "tools/seo_apply.py --check" "tools/urls_fix.py --check" \
         "tools/build_sitemap.py --check" "tools/build_feed.py --check" "tools/gen_og.py --check"; do
  if python3 $c >/dev/null 2>&1; then
    say "   ok   $c"
  else
    say "   FAIL $c"
    python3 $c 2>&1 | sed 's/^/        /' | head -12
    fail=1
  fi
done

step "2. independent assertions"
python3 - <<'PY' || fail=1
import glob, io, json, os, re, sys
sys.path.insert(0, "tools")
from seo_data import NOTES_DIR

SITE = "https://www.loopingly.com"
bad = []
pages = (sorted(glob.glob("*.html")) + sorted(glob.glob("explorables/*.html"))
         + sorted(glob.glob("%s/*.html" % NOTES_DIR)))
descs = {}

for p in pages:
    s = io.open(p, encoding="utf-8", errors="replace").read()
    name = p
    if p == "404.html":
        continue
    head = s[:s.lower().find("</head>")] if "</head>" in s.lower() else ""

    if not head:
        bad.append("%s: no <head> - metadata cannot be seen by a crawler" % name)
        continue

    # exactly one canonical, and it must not be a redirecting URL
    cans = [m[1] for m in re.findall(r'<link[^>]+rel=["\']canonical["\'][^>]+href=(["\'])(.*?)\1', head, re.I)]
    if len(cans) != 1:
        bad.append("%s: %d canonical tags (want exactly 1)" % (name, len(cans)))
    elif cans[0].endswith(".html"):
        bad.append("%s: canonical points at a redirecting .html URL" % name)

    # the canonical must be the page's own final URL, not a neighbour's
    slug = os.path.basename(p)[:-5]
    if slug == "index":
        want = SITE + "/"
    elif p.startswith("explorables/"):
        want = SITE + "/explorables/" + slug
    elif p.startswith(NOTES_DIR + "/"):
        want = SITE + "/" + NOTES_DIR + "/" + slug
    else:
        want = SITE + "/" + slug
    if cans and cans[0] != want:
        bad.append("%s: canonical is %s, expected %s" % (name, cans[0], want))

    d = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=(["\'])(.*?)\1', head, re.I)
    if not d:
        bad.append("%s: no meta description" % name)
    else:
        t = d.group(2)
        descs.setdefault(t, []).append(name)
        if not (110 <= len(t) <= 175):
            bad.append("%s: description is %d chars (want 110-175)" % (name, len(t)))

    for need, label in [("og:title", "og:title"), ("og:image", "og:image"),
                        ("og:url", "og:url"), ("twitter:card", "twitter:card")]:
        if need not in head:
            bad.append("%s: missing %s" % (name, label))

    if 'name="twitter:card" content="summary_large_image"' not in head:
        bad.append("%s: twitter:card is not summary_large_image" % name)

    # og:image must be absolute AND actually exist - scrapers do not resolve
    # relative URLs, and a 404 image renders a blank card
    for img in [m[1] for m in re.findall(r'property=["\']og:image["\'][^>]+content=(["\'])(.*?)\1', head)]:
        if not img.startswith("http"):
            bad.append("%s: og:image is relative" % name)
        elif not os.path.exists(img.replace(SITE + "/", "")):
            bad.append("%s: og:image file missing (%s)" % (name, img))

    for blob in re.findall(r'type=["\']application/ld\+json["\']>(.*?)</script>', head, re.S):
        try:
            json.loads(blob)
        except Exception as e:
            bad.append("%s: JSON-LD does not parse (%s)" % (name, e))

for t, where in descs.items():
    if len(where) > 1:
        bad.append("duplicate description on: %s" % ", ".join(where))

# no internal link may point at a redirecting URL
for p in pages + sorted(glob.glob("assets/*.js")):
    s = io.open(p, encoding="utf-8", errors="replace").read()
    for h in re.findall(r'href="(/[^"]*\.html)"', s):
        bad.append("%s: internal link to %s (301s)" % (p, h))

# every sitemap URL must correspond to a real file
sm = io.open("sitemap.xml", encoding="utf-8").read()
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
for loc in locs:
    rel = loc.replace(SITE, "").strip("/")
    f = "index.html" if rel == "" else rel + ".html"
    if not os.path.exists(f):
        bad.append("sitemap lists %s but %s does not exist" % (loc, f))
if "<priority>" in sm:
    bad.append("sitemap still has <priority> (ignored by Google)")
if ".html<" in sm:
    bad.append("sitemap still lists .html URLs")

# the search index is keyed by card href; a mismatch kills full-text search silently
try:
    idx = json.load(io.open("assets/search-index.json", encoding="utf-8"))
    listing = io.open("explorables.html", encoding="utf-8").read()
    for h in re.findall(r'<a class="card"[^>]*href="(/explorables/[^"]+)"', listing):
        if h not in idx:
            bad.append("search index has no entry for %s" % h)
except FileNotFoundError:
    bad.append("assets/search-index.json missing")

# Unlisted must actually be unlisted. These pages are reachable by URL and crawlable,
# but a card or a search-index entry would defeat the entire point, and both are added
# by tools that run on every publish.
notes = sorted(glob.glob("%s/*.html" % NOTES_DIR))
if notes:
    listing = io.open("explorables.html", encoding="utf-8").read()
    try:
        idx = json.load(io.open("assets/search-index.json", encoding="utf-8"))
    except Exception:
        idx = {}
    feed = io.open("feed.xml", encoding="utf-8").read() if os.path.exists("feed.xml") else ""
    for f in notes:
        slug = os.path.basename(f)[:-5]
        if slug in listing:
            bad.append("%s is unlisted but appears on explorables.html" % f)
        if any(slug in k for k in idx):
            bad.append("%s is unlisted but is in the site search index" % f)
        if slug in feed:
            bad.append("%s is unlisted but is in feed.xml" % f)
    sm = io.open("sitemap.xml", encoding="utf-8").read()
    for f in notes:
        slug = os.path.basename(f)[:-5]
        if "/%s/%s<" % (NOTES_DIR, slug) not in sm:
            bad.append("%s is missing from sitemap.xml (unlisted, but meant to be crawlable)" % f)

if bad:
    print("   %d problem(s):" % len(bad))
    for b in bad:
        print("      " + b)
    sys.exit(1)
print("   ok   %d pages: canonical, description, OG, Twitter, JSON-LD, links, sitemap" % (len(pages) - 1))
PY

step "result"
if [ "$fail" -eq 0 ]; then
  say "PASS"
else
  say "FAIL"
fi
exit $fail
