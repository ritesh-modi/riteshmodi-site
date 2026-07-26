# riteshmodi.com — static site

A fast, playful, fully-static personal site. **No build step** — plain HTML/CSS/JS, so it drops
straight onto **Azure Static Web Apps** and every interactive explorable runs untouched.

```
/                        index.html      home (ivory)
/explorables.html         the explorables, filterable (lavender)
/about.html              about (mint)
/books.html              books (periwinkle)
/talks.html              talks & recognition (rose)
/404.html                friendly not-found
/explorables/*.html       the self-contained interactive explorables (full JS)
/assets/styles.css       shared design system (light + dark)
/assets/site.js          shared behaviour (theme, blobs, tilt, filters)
/staticwebapp.config.json  Azure SWA routing, mime types, 404
```

## Preview locally
Any static server works, e.g.:
```
cd site
python3 -m http.server 8080     # then open http://localhost:8080
```

## Deploy to Azure Static Web Apps (Free tier — $0)

1. **Put these files in a GitHub repo** with `index.html` at the repo root
   (i.e., copy the *contents* of this `site/` folder to the root of a new repo, or keep the
   folder and set "App location" to `/site` in step 3).
2. In the **Azure Portal → Create a resource → Static Web App**:
   - Plan type: **Free**
   - Source: **GitHub** → authorize → pick your repo + branch (`main`)
   - Build presets: **Custom**
   - **App location:** `/`  (or `/site` if you kept the subfolder)
   - **Api location:** *(leave empty)*
   - **Output location:** *(leave empty — there's no build)*
3. Create. Azure adds a **GitHub Actions workflow** to your repo and deploys in ~1–2 min.
   Every push to `main` re-deploys automatically.
4. You get a URL like `https://<name>.azurestaticapps.net`. Open it — the site is live.

## Point riteshmodi.com at it
In the Static Web App → **Custom domains → Add**:
- Add `riteshmodi.com` and `www.riteshmodi.com`.
- Azure gives you a **CNAME/TXT** record to create at wherever your DNS lives (your registrar).
  Add them, wait for validation → Azure issues a **free managed SSL cert** automatically.
- (Your domain registration/renewal stays wherever it is; that's separate from Azure.)

## Add a new explorable (today's workflow)
1. Drop the self-contained `.html` file into `/explorables/` (e.g. `my-explorable.html`).
2. Add a card to `explorables.html` (copy an existing `<a class="card">…</a>`, point `href`
   at the new file, set `--ac` to an accent, write the title/blurb/tags).
3. Commit + push → live in ~1 minute.

## Later: the friendly admin (phase 2)
When you want the "fill-a-form, no code" admin, this site ports cleanly to **Astro + a Git-based
CMS** (Sveltia at `/admin`, or the hosted PagesCMS), still on Azure SWA Free. Adding an explorable
then becomes: upload the HTML + fill a form. The design system here carries over as-is.

## Content notes
- Bio lines (Principal Engineer, Gen AI @ Microsoft, AI/ML EMEA Community Lead, Microsoft Regional
  Director 2018–2020) are real. **Book titles, talk entries, and social links are placeholders** —
  swap in the real ones. Add your photo where the `RM` monogram sits (`.facepile` in `about.html`
  and `index.html`).
```
