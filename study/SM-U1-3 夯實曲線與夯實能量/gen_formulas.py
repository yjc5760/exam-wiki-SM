#!/usr/bin/env python3
"""TEMPLATE — copy this file into your job's working directory and fill in FORMULAS below
with every formula used across all decks in this batch (one shared dict/manifest, reused by
every deckN.js via lib.js's mathImg()).

Renders each formula as true LaTeX typesetting via matplotlib's mathtext engine — this gives
proper math typesetting (fractions, subscripts, square roots, Greek letters, etc.) without
needing a full TeX/LaTeX install. Writes transparent PNGs + a manifest.json mapping
id -> {file, ar (aspect ratio = width/height)} that lib.js's formulaSlide/cheatSheetSlide
read to size and place the image.

Run with: python3 gen_formulas.py    (produces formula_imgs/*.png + formula_manifest.json)
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import json, os

OUT_DIR = "formula_imgs"
os.makedirs(OUT_DIR, exist_ok=True)

NAVY = "#1B2A41"   # match lib.js's C.navy so formula images blend with the deck's ink color
DPI = 400
FONTSIZE = 30

# matplotlib mathtext (mathtext.fontset='cm') renders proper LaTeX-typeset math without
# requiring a full TeX install. Gotcha: mathtext supports a subset of real LaTeX — commands
# like \textstyle, \begin{aligned}, or anything requiring a package will throw a
# ParseSyntaxException. Stick to: \frac, \sqrt, super/subscripts (^ _), \sum, \left/\right,
# Greek letters (\lambda, \phi, \pi...), \leq/\geq/\times/\cdot, and plain multi-part strings
# joined with \quad for "formula, with a side condition" layouts.
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["text.color"] = NAVY

# ---------------------------------------------------------------------------------------
# Fill this in. Use one short mnemonic id per formula (e.g. "d1_f1_1" = deck 1, formula
# group 1, item 1) — deckN.js will reference these ids by name in formulaSlide/cheatSheetSlide
# calls, so keep them stable once you start wiring up the decks.
#
# Wrap every entry in raw-string $...$ so backslashes aren't mangled by Python, e.g.:
#   "example_1": r"$F_{cr} = \left(0.658^{\lambda_c^2}\right) F_y$",
# ---------------------------------------------------------------------------------------
FORMULAS = {
    "gd": r"$\gamma_d = \frac{\gamma}{1+w} \quad , \quad \gamma = \frac{M g}{V}$",
    "zav": r"$\gamma_{zav} = \frac{G_s \gamma_w}{1 + w G_s} \quad (S = 1,\ e_{min} = w G_s)$",
    "sline": r"$\gamma_d = \frac{G_s \gamma_w}{1 + \frac{w G_s}{S}} \quad (Se = w G_s)$",
    "E": r"$E = \frac{W \cdot h \cdot N \cdot L}{V}$",
    "Estd": r"$E_{std} = \frac{24.5 \times 0.305 \times 25 \times 3}{944 \times 10^{-6}} = 594\ \mathrm{kJ/m^3}$",
    "Emod": r"$E_{mod} = \frac{44.5 \times 0.457 \times 25 \times 5}{944 \times 10^{-6}} = 2693\ \mathrm{kJ/m^3}$",
    "RC": r"$R_C = \frac{\gamma_{d,field}}{\gamma_{d,max}} \times 100\% = \frac{16.80}{17.50} = 96.0\%$",
    "check": r"$\gamma_d \leq \gamma_{zav}(w) \quad \Rightarrow \quad 20.29 > 17.51\ \mathrm{(error)}$",
}

manifest = {}
errors = []
for fid, latex in FORMULAS.items():
    fig = plt.figure(figsize=(0.1, 0.1), dpi=DPI)
    try:
        fig.text(0, 0, latex, fontsize=FONTSIZE, color=NAVY)
        path = os.path.join(OUT_DIR, f"{fid}.png")
        # pad_inches gives a small safety margin — formulas with sqrt/fraction stacks can
        # clip at the top/bottom if this is too tight (0.08 has proven safe in practice).
        fig.savefig(path, dpi=DPI, transparent=True, bbox_inches="tight", pad_inches=0.08)
        plt.close(fig)
        from PIL import Image
        im = Image.open(path)
        w, h = im.size
        manifest[fid] = {"file": path, "ar": w / h}
    except Exception as e:
        errors.append((fid, str(e)))
        plt.close(fig)

with open("formula_manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print(f"Rendered {len(manifest)} formulas, {len(errors)} errors")
for fid, err in errors:
    print("ERROR", fid, err)
