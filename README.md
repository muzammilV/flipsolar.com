# Pre-launch checklist (do these before pointing DNS / announcing)

1. **Fill the legal pages** (privacy / terms / contact contain `{{TOKENS}}` until you do):
   ```
   python3 scripts/fill_legal.py --legal-name "Your LLC" --state Texas \
       --address "Street, City, ST ZIP" --email you@flipsolar.com --date "Month D, 2026"
   ```
2. **Run the checker** — it must report 0 failures: `python3 scripts/preflight.py`
   (checks placeholders, broken links/anchors, sitemap, OG images, stale claims, Amazon tags).
3. **Tally settings** (not in this repo): set *After submission → Redirect* to `https://flipsolar.com/thank-you.html`;
   add a required consent checkbox mirroring the Privacy/Terms text; if installers will **text** leads,
   add TCPA-style SMS consent wording (and get legal review) and update privacy.html.
4. **Submit a real test lead** from phone and desktop and confirm it arrives where installers' leads should go.
5. **Have a lawyer review** privacy.html, terms.html and the tax/incentive wording.
6. Re-verify time-sensitive claims (federal ITC deadlines, Florida incentives) before each content refresh.

---

# FlipSolar.com — GitHub Pages Site

Solar lead gen + affiliate site targeting small business owners in Texas & Florida.

## 📁 File Structure

```
flipsolar/
├── index.html                              ← Homepage + lead form
├── CNAME                                   ← Custom domain (flipsolar.com)
├── sitemap.xml                             ← Submit to Google Search Console
├── robots.txt                              ← Search engine instructions
├── css/
│   └── style.css                          ← All styling
└── blog/
    ├── solar-panels-restaurants-texas.html ← Article 1 (done)
    ├── solar-pool-heater-florida-2026.html ← Article 2 (done)
    └── solar-savings-small-business.html  ← Article 3 (done)
```

## 🚀 Deploy to GitHub Pages

1. Create a new public GitHub repo named `flipsolar` (or your username.github.io)
2. Push all these files to the repo
3. Go to Settings → Pages → Source: Deploy from branch → main → / (root)
4. Add custom domain: `flipsolar.com`
5. Check "Enforce HTTPS"

## 🌐 Point Dynadot DNS to GitHub Pages

In Dynadot DNS settings, add these A records:
```
@ A 185.199.108.153
@ A 185.199.109.153
@ A 185.199.110.153
@ A 185.199.111.153
www CNAME yourusername.github.io
```

## ✏️ What to Customise (do these before going live)

### 1. Tally Form
- Go to tally.so → create your lead form
- Fields: Business type, monthly bill, state, name, email, phone
- Click Share → Embed → copy the script
- Replace `<div class="tally-embed-placeholder">` blocks in both HTML files

### 2. Amazon Affiliate Links
- Affiliate tag in use: `flipsolar-20`. Click every Amazon link and confirm each ASIN matches the product named next to it (B0B8ZLZ53M is labeled differently on the homepage and the restaurant guide).
- Do not hard-code prices (Amazon Associates policy); the site links to Amazon for current price.
- Verify the ASINs are current:
  - EcoFlow DELTA Pro: B09STZTLGN
  - Jackery SolarSaga 200W: B09SJMGHL4
  - Bluetti AC200MAX: B09NCJPBMT

### 3. After deploy — submit to Google
- Go to search.google.com/search-console
- Add property: flipsolar.com
- Verify ownership (HTML tag method works with GitHub Pages)
- Submit sitemap: https://flipsolar.com/sitemap.xml

## 📝 Adding New Articles

Ask Claude: "Write a complete SEO HTML page about [topic] for flipsolar.com.
Use the same CSS file at ../css/style.css. Include meta tags, article schema,
H1, H2s, and a Tally form embed placeholder."

Save as blog/your-article-name.html, push to GitHub, add URL to sitemap.xml.

## 💰 Revenue Streams Built In

1. **Lead gen** — Tally form → you forward submissions to installer partners
2. **Amazon affiliate** — 3 product cards on homepage + 2 in blog article
3. **Display ads** — Add Ezoic script to <head> when you get traffic

## 📊 Update sitemap.xml when adding articles

Add each new article URL to sitemap.xml with today's date.
