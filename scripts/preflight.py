#!/usr/bin/env python3
"""Pre-launch checks for flipsolar.com (static site). Run from the repo root:

    python3 scripts/preflight.py

Exits non-zero if anything that should block a launch is found.
Use --allow-placeholders to skip the {{TOKEN}} check while you are still drafting.
"""
import re, sys, pathlib
from html.parser import HTMLParser
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
ALLOW_PLACEHOLDERS = "--allow-placeholders" in sys.argv
SITE = "https://flipsolar.com"
errors, warnings = [], []

pages = sorted(p for p in ROOT.rglob("*.html") if ".git" not in p.parts)

class Collector(HTMLParser):
    def __init__(self):
        super().__init__(); self.refs = []; self.ids = set(); self.meta = {}; self.title = False; self.has_title = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"): self.ids.add(a["id"])
        if tag == "a" and a.get("href"): self.refs.append(("href", a["href"]))
        if tag == "link" and a.get("href") and a.get("rel") in ("stylesheet", "icon") and not a["href"].startswith("data:"): self.refs.append(("href", a["href"]))
        if tag in ("img", "script", "iframe") and a.get("src"): self.refs.append(("src", a["src"]))
        if tag == "meta":
            k = a.get("name") or a.get("property")
            if k: self.meta[k] = a.get("content", "")
        if tag == "link" and a.get("rel") == "canonical": self.meta["canonical"] = a.get("href", "")
        if tag == "title": self.title = True
    def handle_data(self, d):
        if self.title and d.strip(): self.has_title = True
    def handle_endtag(self, tag):
        if tag == "title": self.title = False

parsed = {}
for p in pages:
    c = Collector(); c.feed(p.read_text(encoding="utf-8")); parsed[p] = c

def resolve(page, ref):
    """Map an internal URL to a local file (or None if external/ignored)."""
    if ref.startswith(("mailto:", "tel:", "data:", "javascript:")): return "skip", None
    u = urlparse(ref)
    if u.scheme in ("http", "https"):
        if u.netloc.replace("www.", "") != "flipsolar.com": return "skip", None
        path = u.path
    elif u.scheme: return "skip", None
    else:
        path = u.path
    if not path:  # same-page anchor
        return page, u.fragment
    if path.startswith("/"): target = ROOT / path.lstrip("/")
    else: target = (page.parent / path)
    target = target.resolve()
    if path.endswith("/") or target.is_dir(): target = target / "index.html"
    return target, u.fragment

for p, c in parsed.items():
    rel = p.relative_to(ROOT)
    for kind, ref in c.refs:
        target, frag = resolve(p, ref)
        if target == "skip": continue
        if not pathlib.Path(target).exists():
            errors.append(f"{rel}: broken link -> {ref}")
            continue
        if frag and str(target).endswith(".html"):
            ids = parsed.get(pathlib.Path(target)).ids if pathlib.Path(target) in parsed else set()
            if frag not in ids: errors.append(f"{rel}: missing anchor #{frag} in {pathlib.Path(target).relative_to(ROOT)} (from {ref})")

    noindex = "noindex" in c.meta.get("robots", "")
    if not c.has_title: errors.append(f"{rel}: missing <title>")
    if not c.meta.get("description"): errors.append(f"{rel}: missing meta description")
    if not noindex and not c.meta.get("canonical"): errors.append(f"{rel}: missing canonical")
    for k in ("og:image", "twitter:image"):
        v = c.meta.get(k)
        if v:
            t, _ = resolve(p, v)
            if t != "skip" and not pathlib.Path(t).exists(): errors.append(f"{rel}: {k} points to a missing file: {v}")
    # (logo URL inside JSON-LD)
text_all = {p: p.read_text(encoding="utf-8") for p in pages}
for p, t in text_all.items():
    rel = p.relative_to(ROOT)
    for m in re.findall(r'https://flipsolar\.com/(images/[^"\s]+)', t):
        if not (ROOT / m).exists(): errors.append(f"{rel}: references missing file /{m}")
    if not ALLOW_PLACEHOLDERS and "{{" in t:
        errors.append(f"{rel}: unfilled placeholders: {sorted(set(re.findall(r'{{[A-Z_]+}}', t)))}  -> run scripts/fill_legal.py")
    for pat, why in [(r"YOUR_AFFILIATE_TAG", "placeholder affiliate tag"),
                     (r"solar-pool-heater-florida-2025", "stale link to renamed pool guide"),
                     (r"through 2032", "outdated ITC claim"),
                     (r"\b(vetted|verified) (local |commercial )?installers", "unsubstantiated installer-vetting claim"),
                     (r"Loading quote form", None)]:
        if why and re.search(pat, t): errors.append(f"{rel}: {why} ({pat})")
    for m in re.findall(r'amazon\.com/[^"\s]*', t):
        if "tag=flipsolar-20" not in m: errors.append(f"{rel}: Amazon link without affiliate tag: {m}")
    if re.search(r"\$\d[\d,]*\s*<span>on Amazon", t): errors.append(f"{rel}: hard-coded Amazon price (Associates policy risk)")

# sitemap entries must exist
sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
for loc in re.findall(r"<loc>([^<]+)</loc>", sm):
    path = urlparse(loc).path.lstrip("/") or "index.html"
    if not (ROOT / path).exists(): errors.append(f"sitemap.xml: {loc} does not exist")
for p in pages:
    rel = p.relative_to(ROOT).as_posix()
    if rel in ("404.html", "thank-you.html"): continue
    url = f"{SITE}/{'' if rel == 'index.html' else rel}"
    if url not in sm: warnings.append(f"{rel}: not listed in sitemap.xml")

for w in warnings: print("WARN ", w)
for e in errors: print("FAIL ", e)
print(f"\n{len(pages)} pages checked: {len(errors)} failure(s), {len(warnings)} warning(s)")
sys.exit(1 if errors else 0)
