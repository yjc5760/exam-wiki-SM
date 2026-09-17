#!/usr/bin/env python3
"""SM-U1-3 觀念講義 — 公式 PNG 渲染（matplotlib mathtext）

注意（踩過的坑）：
  * mathtext 只支援 LaTeX 子集：\\frac \\sqrt ^ _ \\sum \\left \\right 希臘字母
    \\leq \\geq \\times \\cdot \\quad；**不支援** \\le \\ge \\tfrac \\text \\begin。
  * `$...$` 內絕對不能放中文 —— cm 字型無 CJK 字面。中文一律寫在 deck.js 的
    label / note / insights。
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import json, os, re

OUT_DIR = "formula_imgs"
os.makedirs(OUT_DIR, exist_ok=True)

NAVY = "#1B2A41"
DPI, FONTSIZE = 400, 30
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["text.color"] = NAVY

FORMULAS = {
    # ── 萬用鑰匙（三相關係）──────────────────────────────
    "f_eps":   r"$\varepsilon_v = \frac{\Delta H}{H_0} = \frac{\Delta e}{1 + e_0}$",
    "f_gd":    r"$\gamma_d = \frac{G_s \gamma_w}{1 + e} = \frac{\gamma}{1 + w}$",
    "f_se":    r"$S \, e = w \, G_s$",
    "f_sce":   r"$S_c = \frac{\Delta e}{1 + e_0} \, H$",
    # ── 夯實 ────────────────────────────────────────────
    "f_zav":   r"$\gamma_{zav} = \frac{G_s \gamma_w}{1 + w G_s} \qquad (S = 100\%)$",
    "f_energy": r"$E = \frac{W \cdot h \cdot N \cdot L}{V}$",
    "f_rc":    r"$RC = \frac{\gamma_{d,field}}{\gamma_{d,max}} \times 100\%$",
    "f_dr":    r"$D_r = \frac{e_{max} - e}{e_{max} - e_{min}} \times 100\%$",
    "f_ws":    r"$W_s = \gamma_{d,fill} \, V_{fill} = \gamma_{d,borrow} \, V_{borrow}$",
    "f_water": r"$W_w = W_s \, (w_{target} - w_{nat})$",
    # ── 應力歷史 ────────────────────────────────────────
    "f_p0":    r"$p_0' = \sum \gamma_i h_i - u = \sum \gamma_i' h_i$",
    "f_ocr":   r"$OCR = \frac{p_c'}{p_0'} \qquad OCR = 1 : NC \; , \; OCR > 1 : OC$",
    "f_cc":    r"$C_c = \frac{e_1 - e_2}{\log (p_2' / p_1')} \quad , \quad C_c / C_r \approx 5 \sim 10$",
    # ── 壓密沉陷量 ──────────────────────────────────────
    "f_caseA": r"$S_c = \frac{C_c H}{1 + e_0} \, \log \frac{p_0' + \Delta \sigma}{p_0'}$",
    "f_caseB": r"$S_c = \frac{C_r H}{1 + e_0} \, \log \frac{p_0' + \Delta \sigma}{p_0'}$",
    "f_caseC": r"$S_c = \frac{C_r H}{1 + e_0} \log \frac{p_c'}{p_0'} + \frac{C_c H}{1 + e_0} \log \frac{p_0' + \Delta \sigma}{p_c'}$",
    # ── 應力增量 ────────────────────────────────────────
    "f_21":    r"$\Delta \sigma = \frac{Q}{(B + z)(L + z)} \qquad (z \; \mathrm{from \; base})$",
    "f_wide":  r"$\Delta \sigma (z) = \Delta \sigma_0 = \mathrm{const.}$",
    # ── 壓密速率 ────────────────────────────────────────
    "f_tv":    r"$T_v = \frac{c_v \, t}{H_{dr}^{\,2}}$",
    "f_hdr":   r"$H_{dr} = H/2 \;\; (\mathrm{double}) \quad ; \quad H_{dr} = H \;\; (\mathrm{single})$",
    "f_u60a":  r"$T_v = \frac{\pi}{4} U^2 \qquad (U < 60\%)$",
    "f_u60b":  r"$T_v = 1.781 - 0.933 \log (100 - U\%) \qquad (U \geq 60\%)$",
    "f_tratio": r"$\frac{t_1}{t_2} = \left( \frac{H_{dr,1}}{H_{dr,2}} \right)^{2}$",
    "f_cv":    r"$c_v = \frac{k}{m_v \gamma_w} \quad , \quad m_v = \frac{a_v}{1 + e_0} = \frac{-\Delta e / \Delta p'}{1 + e_0}$",
    # ── 預壓工法 ────────────────────────────────────────
    "f_pre":   r"$U_{req} = \frac{S_c}{S_{cf}} < 100\% \qquad (S_{cf} > S_c)$",
}

CJK = re.compile(r"[　-〿一-鿿＀-￯]")
bad = {k: v for k, v in FORMULAS.items() if CJK.search(v)}
if bad:
    raise SystemExit(f"CJK leaked into mathtext: {list(bad)}")
for k, v in FORMULAS.items():
    if re.search(r"\\le[^qf]|\\ge[^q]|\\tfrac", v):
        raise SystemExit(f"unsupported macro in {k}: {v}")

manifest, errors = {}, []
for fid, latex in FORMULAS.items():
    fig = plt.figure(figsize=(0.1, 0.1), dpi=DPI)
    try:
        fig.text(0, 0, latex, fontsize=FONTSIZE, color=NAVY)
        path = os.path.join(OUT_DIR, f"{fid}.png")
        fig.savefig(path, dpi=DPI, transparent=True, bbox_inches="tight", pad_inches=0.08)
        plt.close(fig)
        from PIL import Image
        w, h = Image.open(path).size
        manifest[fid] = {"file": path, "ar": w / h}
    except Exception as e:
        errors.append((fid, str(e)))
        plt.close(fig)

with open("formula_manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print(f"Rendered {len(manifest)} formulas, {len(errors)} errors")
for fid, err in errors:
    print("ERROR", fid, err)
