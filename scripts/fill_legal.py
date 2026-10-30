#!/usr/bin/env python3
"""Fill the {{TOKENS}} in privacy.html / terms.html / contact.html.

    python3 scripts/fill_legal.py --legal-name "Acme Solar LLC" --state Texas \
        --address "123 Main St, Houston, TX 77002" --email hello@flipsolar.com \
        --date "November 1, 2026"
"""
import argparse, html, pathlib
ap = argparse.ArgumentParser()
for k in ("legal-name", "state", "address", "email", "date"): ap.add_argument("--" + k, required=True)
a = ap.parse_args()
vals = {"{{LEGAL_NAME}}": a.legal_name, "{{STATE}}": a.state, "{{ADDRESS}}": a.address,
        "{{EMAIL}}": a.email, "{{EFFECTIVE_DATE}}": a.date}
root = pathlib.Path(__file__).resolve().parent.parent
for name in ("privacy.html", "terms.html", "contact.html"):
    p = root / name; t = p.read_text(encoding="utf-8")
    for k, v in vals.items(): t = t.replace(k, html.escape(v, quote=False))
    p.write_text(t, encoding="utf-8"); print("filled", name)
