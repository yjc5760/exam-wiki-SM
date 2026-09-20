# -*- coding: utf-8 -*-
"""
gen_SM-key.py — 「萬用鑰匙：固體顆粒體積不變」觀念講義向量圖
所有圖上數字由本檔頂端常數算出，改常數重跑即可。
"""
import sys, math, os
sys.path.insert(0, "/mnt/skills/user/struct-diagram/scripts")
from structdraw import Canvas, C, FONT, FONT_M, esc

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
PRE = "SM-key-fig"

# ══════════ 示範案例（全篇共用） ══════════
GW = 9.81                       # γw, kN/m³
# 案例 A：正常壓密黏土層（飽和）
GS_A, H0, E0 = 2.70, 4.00, 1.10
CC, P0, P1 = 0.50, 100.0, 200.0
DE   = CC * math.log10(P1 / P0)          # Δe
E1   = E0 - DE
EPS  = DE / (1 + E0)                     # εv
SC   = H0 * EPS                          # 正確沉陷量
SC_W = H0 * DE / (1 + E1)                # 錯誤分母
ERR  = SC_W / SC - 1
H1   = H0 - SC
GD0  = GS_A * GW / (1 + E0)
GD1  = GS_A * GW / (1 + E1)
W0, W1 = E0 / GS_A, E1 / GS_A            # 飽和 S=1 → w = e/Gs
# 案例 B：砂土（相對密度 vs 相對夯實度）
GS_B, EMAX, EMIN, DR = 2.65, 0.90, 0.45, 0.70
E_B   = EMAX - DR * (EMAX - EMIN)
GD_B  = GS_B * GW / (1 + E_B)
GDMAX = GS_B * GW / (1 + EMIN)
GDMIN = GS_B * GW / (1 + EMAX)
RC_B  = GD_B / GDMAX
RC_0  = GDMIN / GDMAX
# 案例 C：夯實土（部分飽和）
GS_C, E_C, W_C = 2.70, 0.60, 0.15
S_C   = W_C * GS_C / E_C
GD_C  = GS_C * GW / (1 + E_C)

GRAY_F = "#A7AEBA"; BLUE_F = "#C5D3F3"; AIR_F = "#FFFFFF"; WATER_F = "#8FB4EE"


class PX(Canvas):
    """SVG 像素座標（y 向下）的便利方法"""
    def __init__(s, w, h): super().__init__(w, h, 1, 0, 0, bg="#FFFFFF")
    def L(s, x0, y0, x1, y1, **k): s.line((x0, s.h - y0), (x1, s.h - y1), **k)
    def A(s, x0, y0, x1, y1, **k): s.arrow((x0, s.h - y0), (x1, s.h - y1), **k)
    def PL(s, pts, **k): s.poly([(x, s.h - y) for x, y in pts], **k)
    def PG(s, pts, fill, **k): s.polygon([(x, s.h - y) for x, y in pts], fill, **k)
    def R(s, x, y, w, h, fill, stroke=C["member"], sw=2, rx=0):
        s.rect_px(x, y, w, h, fill, rx, stroke, sw)
    def T(s, x, y, t, size=18, color=C["text"], anchor="middle", weight="400"):
        s.text_px(x, y, esc(t) if ("<" in t or "&" in t) else t, size, color, anchor, weight)
    def M(s, x, y, t, size=20, color=C["text"], anchor="middle", weight="400"):
        s.math_px(x, y, t, size, color, anchor, weight)
    def CI(s, x, y, r, fill, stroke=C["member"], sw=1.5):
        s.parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" '
                       f'stroke="{stroke}" stroke-width="{sw}"/>')


def save(cv, n, name):
    p = os.path.join(OUT, f"{PRE}-{n:02d}-{name}.svg"); cv.save(p); return p


def axes_plot(cv, x0, y0, w, h, xr, yr, xt, yt, xlabel, ylabel, fx="{:.1f}", fy="{:.0f}"):
    """回傳 (X, Y) 映射函式；畫軸與刻度"""
    X = lambda v: x0 + (v - xr[0]) / (xr[1] - xr[0]) * w
    Y = lambda v: y0 + h - (v - yr[0]) / (yr[1] - yr[0]) * h
    for t in yt:
        cv.L(x0, Y(t), x0 + w, Y(t), color=C["border"], w=1)
        cv.T(x0 - 10, Y(t), fy.format(t), 15, C["muted"], "end")
    for t in xt:
        cv.L(X(t), y0 + h, X(t), y0 + h + 6, color=C["member"], w=1.5)
        cv.T(X(t), y0 + h + 22, fx.format(t), 15, C["muted"])
    cv.L(x0, y0 + h, x0 + w, y0 + h, color=C["member"], w=2)
    cv.L(x0, y0, x0, y0 + h, color=C["member"], w=2)
    cv.T(x0 + w / 2, y0 + h + 50, xlabel, 17, C["text"])
    cv.parts.append(f'<text x="{x0-62}" y="{y0+h/2}" font-family="{FONT}" font-size="17" fill="{C["text"]}" '
                    f'text-anchor="middle" transform="rotate(-90 {x0-62} {y0+h/2})">{ylabel}</text>')
    return X, Y


# ─────────── 圖 1：萬用鑰匙地圖 ───────────
def fig_map():
    cv = PX(900, 560)
    cx, cy = 190, 280
    cv.R(40, 170, 300, 220, "#F1F3F7", C["member"], 2.5, 18)
    cv.T(cx, 212, "萬用鑰匙", 26, C["text"], weight="700")
    cv.M(cx, 268, "V_{s} = 1", 34)
    cv.T(cx, 318, "固體顆粒體積永遠不變", 18, C["muted"])
    cv.T(cx, 350, "孔隙體積 = e", 18, C["muted"])
    items = [("① 孔隙比 ⇄ 乾單位重", "γ_{d} = G_{s}γ_{w} / (1 + e)", C["load"], 95),
             ("② 含水量 ⇄ 飽和度", "S e = w G_{s}", C["deform"], 280),
             ("③ 孔隙比 ⇄ 沉陷量", "S_{c} = H_{0}·Δe / (1 + e_{0})", C["bmd"], 465)]
    for title, f, col, y in items:
        cv.A(340, cy, 470, y, color=col, w=3, head=13)
        cv.R(480, y - 62, 390, 124, "#FFFFFF", col, 2.5, 14)
        cv.T(500, y - 32, title, 19, col, "start", "700")
        cv.M(675, y + 20, f, 27)
    return save(cv, 1, "key-map")


# ─────────── 圖 2：三相圖（案例 C） ───────────
def fig_phase():
    cv = PX(820, 600)
    VW = W_C * GS_C; VA = E_C - VW; tot = 1 + E_C
    top, hh = 70, 440; k = hh / tot
    x, w = 290, 170
    yS = top + hh - 1 * k; yW = yS - VW * k; yA = top
    cv.R(x, yA, w, VA * k, AIR_F); cv.R(x, yW, w, VW * k, WATER_F); cv.R(x, yS, w, k, GRAY_F)
    cv.T(x + w / 2, yA + VA * k / 2, "空氣", 19); cv.T(x + w / 2, yW + VW * k / 2, "水", 19)
    cv.T(x + w / 2, yS + k / 2, "固體", 21, "#FFFFFF", weight="700")
    # 左側體積標註
    def brace(xl, y0, y1, lab, col, side=-1, math_=True):
        cv.L(xl, y0 + 2, xl, y1 - 2, color=col, w=2)
        cv.L(xl, y0 + 2, xl - 8 * side, y0 + 2, color=col, w=2); cv.L(xl, y1 - 2, xl - 8 * side, y1 - 2, color=col, w=2)
        (cv.M if math_ else cv.T)(xl + 16 * side, (y0 + y1) / 2, lab, 19, col, "end" if side < 0 else "start")
    brace(x - 20, yS, yS + k, "V_{s} = 1", C["member"])
    brace(x - 20, yW, yS, f"V_{{w}} = wG_{{s}} = {VW:.3f}", C["deform"])
    brace(x - 20, yA, yW, f"V_{{a}} = {VA:.3f}", C["muted"])
    brace(x + w + 20, yA, yS, f"V_{{v}} = e = {E_C:.2f}", C["deform"], 1)
    brace(x + w + 150, yA, yS + k, f"V = 1 + e = {tot:.2f}", C["text"], 1)
    cv.T(x + w + 20, yS + k / 2, "重量：", 16, C["muted"], "start")
    cv.M(x + w + 70, yS + k / 2, "W_{s} = G_{s}γ_{w}", 18, C["member"], "start")
    cv.T(410, 30, f"案例 C：夯實土  G_s = {GS_C:.2f}，e = {E_C:.2f}，w = {W_C*100:.0f}%", 18, C["text"], weight="700")
    cv.T(410, 560, f"飽和度 S = V_w / V_v = {VW:.3f} / {E_C:.2f} = {S_C*100:.1f}%", 18, C["accent"], weight="700")
    return save(cv, 2, "phase")


# ─────────── 圖 3：顆粒不變，孔隙變 ───────────
def fig_particles():
    cv = PX(900, 480)
    rs = [22, 18, 20, 16, 24, 19, 17, 21, 23, 18, 20, 16]
    def box(x0, H, title):
        y0 = 400 - H
        cv.R(x0, y0, 300, H, BLUE_F, C["deform"], 2, 8)
        cols, rows = 4, 3
        for i, r in enumerate(rs):
            c, rw = i % cols, i // cols
            cxp = x0 + 38 + c * 75 + (rw % 2) * 12
            cyp = 400 - 30 - rw * (H - 60) / (rows - 1)
            cv.CI(cxp, cyp, r, GRAY_F, C["member"], 2)
        cv.T(x0 + 150, y0 - 22, title, 19, C["text"], weight="700")
    box(60, 330, "受壓前"); box(540, 250, "受壓後")
    cv.A(390, 235, 515, 235, color=C["load"], w=3.5, head=14)
    cv.T(452, 205, "加壓", 18, C["load"], weight="700")
    cv.T(450, 445, "12 顆顆粒、每顆大小都相同 → V_s 不變；只有顆粒之間的孔隙（藍）被擠掉", 17, C["muted"])
    return save(cv, 3, "particles")


# ─────────── 圖 4：正規化柱 vs 實際土層（案例 A） ───────────
def fig_columns():
    cv = PX(1090, 660)
    k = 210; base = 580
    def col(x, e, lab, labc):
        cv.R(x, base - k, 130, k, GRAY_F); cv.R(x, base - k - e * k, 130, e * k, BLUE_F, C["deform"])
        cv.M(x + 65, base - k / 2, "V_{s} = 1", 20, "#FFFFFF")
        cv.M(x + 65, base - k - e * k / 2, f"e = {e:.3f}", 20, C["deform"])
        cv.M(x + 65, base - k - e * k - 22, lab, 20, labc)
    col(90, E0, f"1 + e_{{0}} = {1+E0:.3f}", C["text"])
    col(300, E1, f"1 + e = {1+E1:.3f}", C["text"])
    cv.L(60, base, 460, base, color=C["member"], w=2.5)
    yt0, yt1 = base - k * (1 + E0), base - k * (1 + E1)
    cv.L(220, yt0, 485, yt0, color=C["dim"], w=1.5, dash="6 5"); cv.L(430, yt1, 485, yt1, color=C["dim"], w=1.5, dash="6 5")
    cv.L(470, yt0, 470, yt1, color=C["load"], w=3)
    cv.M(480, (yt0 + yt1) / 2 + 30, f"Δe = {DE:.4f}", 19, C["load"], "start")
    cv.T(265, 30, "模型（每 1 份固體）", 20, C["text"], weight="700")
    cv.T(265, 630, "高度單位：「份」，不是公尺", 16, C["muted"])
    # 右：實際土層
    s = 95; xr = 640
    hA, hB = H0 * s, H1 * s
    cv.R(xr, base - hA, 110, hA, "#DCE3EE", C["member"], 2); cv.R(xr + 150, base - hB, 110, hB, "#DCE3EE", C["member"], 2)
    cv.L(610, base, 900, base, color=C["member"], w=2.5)
    cv.T(xr + 55, base - hA - 22, f"H_{{0}} = {H0:.2f} m", 18, C["text"], weight="700")
    cv.T(xr + 205, base - hB - 22, f"H = {H1:.3f} m", 18, C["text"], weight="700")
    cv.L(xr + 110, base - hA, xr + 285, base - hA, color=C["dim"], w=1.5, dash="6 5")
    cv.L(xr + 280, base - hA, xr + 280, base - hB, color=C["load"], w=3)
    cv.M(xr + 290, base - (hA + hB) / 2 - 4, f"S_{{c}} = {SC:.3f} m", 18, C["load"], "start")
    cv.T(760, 30, "現場土層", 20, C["text"], weight="700")
    cv.A(505, 330, 600, 330, color=C["accent"], w=3, head=13)
    cv.T(552, 290, "同比例放大", 17, C["accent"], weight="700")
    cv.T(552, 372, f"× {H0/(1+E0):.3f} m/份", 16, C["accent"])
    return save(cv, 4, "columns")


# ─────────── 圖 5：γd–e 曲線（案例 A） ───────────
def fig_gd_e():
    cv = PX(760, 560)
    X, Y = axes_plot(cv, 110, 50, 600, 390, (0.4, 1.4), (10, 20), [0.4, 0.6, 0.8, 1.0, 1.2, 1.4],
                     [10, 12, 14, 16, 18, 20], "孔隙比 e", "γd（kN/m³）")
    pts = [(X(e / 100), Y(GS_A * GW / (1 + e / 100))) for e in range(40, 141, 2)]
    cv.PL(pts, color=C["bmd"], w=3.5)
    for e, g, lab, dy in [(E0, GD0, "受壓前", -30), (E1, GD1, "受壓後", -30)]:
        cv.L(X(e), Y(10), X(e), Y(g), color=C["dim"], w=1.5, dash="5 5")
        cv.L(X(0.4), Y(g), X(e), Y(g), color=C["dim"], w=1.5, dash="5 5")
        cv.CI(X(e), Y(g), 7, C["load"], "#FFFFFF", 2)
        cv.T(X(e) + 12, Y(g) + dy, f"{lab} e={e:.3f}, γd={g:.2f}", 16, C["load"], "start", "700")
    cv.M(560, 110, "γ_{d} = G_{s}γ_{w} / (1 + e)", 22, C["bmd"])
    cv.T(560, 145, f"G_s = {GS_A:.2f}", 16, C["muted"])
    return save(cv, 5, "gd-e")


# ─────────── 圖 6：RC vs Dr 刻度對照（案例 B） ───────────
def fig_rc_dr():
    cv = PX(1000, 470)
    x0, x1 = 160, 900
    Xe = lambda e: x0 + (EMAX - e) / (EMAX - EMIN) * (x1 - x0)
    rows = [(90, "孔隙比 e"), (190, "相對密度 Dr"), (290, "乾單位重 γd"), (390, "相對夯實度 RC")]
    for y, lab in rows:
        cv.L(x0, y, x1, y, color=C["member"], w=2.5)
        cv.T(x0 - 20, y, lab, 18, C["text"], "end", "700")
    for e in [0.90, 0.80, 0.70, 0.50, 0.45]:
        xx = Xe(e); dr = (EMAX - e) / (EMAX - EMIN); gd = GS_B * GW / (1 + e)
        for y in (90, 190, 290, 390): cv.L(xx, y - 6, xx, y + 6, color=C["member"], w=1.5)
        cv.T(xx, 90 - 22, f"{e:.2f}", 15, C["muted"])
        cv.T(xx, 190 - 22, f"{dr*100:.0f}%", 15, C["muted"])
        cv.T(xx, 290 - 22, f"{gd:.2f}", 15, C["muted"])
        cv.T(xx, 390 - 22, f"{gd/GDMAX*100:.1f}%", 15, C["muted"])
    xb = Xe(E_B)
    cv.L(xb, 60, xb, 420, color=C["load"], w=3)
    for y, t in [(90, f"e = {E_B:.3f}"), (190, f"Dr = {DR*100:.0f}%"), (290, f"γd = {GD_B:.2f}"), (390, f"RC = {RC_B*100:.1f}%")]:
        cv.CI(xb, y, 7, C["load"], "#FFFFFF", 2)
        cv.T(xb + 12, y + 20, t, 16, C["load"], "start", "700")
    cv.T(500, 452, f"Dr = 0% 時 RC 已是 {RC_0*100:.1f}%：兩把尺的起點不同，百分比不能直接對接", 17, C["accent"], weight="700")
    return save(cv, 6, "rc-dr")


# ─────────── 圖 7：固定 e，改變含水量 ───────────
def fig_sat():
    cv = PX(900, 570)
    k = 230; base = 470; tot = 1 + E_C
    for i, S in enumerate([0.5, 0.8, 1.0]):
        x = 90 + i * 270; w = 150
        vw = S * E_C; va = E_C - vw
        cv.R(x, base - k, w, k, GRAY_F)
        cv.R(x, base - k - vw * k, w, vw * k, WATER_F)
        if va > 1e-6: cv.R(x, base - k - E_C * k, w, va * k, AIR_F)
        cv.T(x + w / 2, base - k / 2, "固體 1", 18, "#FFFFFF", weight="700")
        cv.M(x + w / 2, base - k - vw * k / 2, f"V_{{w}} = {vw:.2f}", 18, C["text"])
        cv.T(x + w / 2, 40, f"S = {S*100:.0f}%", 20, C["deform"], weight="700")
        cv.T(x + w / 2, 505, f"w = Se/G_s = {S*E_C/GS_C*100:.1f}%", 17, C["text"])
    cv.L(60, base, 860, base, color=C["member"], w=2.5)
    cv.L(60, base - k * tot, 860, base - k * tot, color=C["dim"], w=1.5, dash="6 5")
    cv.T(860, base - k * tot - 16, f"總體積 1 + e = {tot:.2f} 不變", 16, C["muted"], "end")
    cv.T(450, 545, f"e = {E_C:.2f}、G_s = {GS_C:.2f} 固定：水越多，w 與 S 同步上升，兩者被 Se = wGs 綁在一起", 16, C["muted"])
    return save(cv, 7, "saturation")


# ─────────── 圖 8：夯實平面與 ZAVC ───────────
def fig_zav():
    cv = PX(800, 580)
    X, Y = axes_plot(cv, 110, 50, 620, 410, (8, 32), (13, 21), [8, 12, 16, 20, 24, 28, 32],
                     [13, 15, 17, 19, 21], "含水量 w（%）", "γd（kN/m³）", "{:.0f}", "{:.0f}")
    for S, col, dash in [(1.0, C["deform"], None), (0.9, C["sfd"], "8 6"), (0.8, C["accent"], "3 5")]:
        pts = []
        for w in range(8, 33):
            g = GS_C * GW / (1 + w / 100 * GS_C / S)
            if 13 <= g <= 21: pts.append((X(w), Y(g)))
        cv.PL(pts, color=col, w=3.2, dash=dash)
        w_lab = 29 if S == 1 else (30 if S == 0.9 else 31)
        g_lab = GS_C * GW / (1 + w_lab / 100 * GS_C / S)
        cv.T(X(w_lab), Y(g_lab) - 18, "ZAVC (S=100%)" if S == 1 else f"S={S*100:.0f}%", 15, col, "middle", "700")
    cv.CI(X(W_C * 100), Y(GD_C), 7, C["load"], "#FFFFFF", 2)
    cv.T(X(8.6), Y(14.6), f"案例 C：w={W_C*100:.0f}%, γd={GD_C:.2f}", 16, C["load"], "start", "700")
    cv.T(X(8.6), Y(14.6) + 26, f"S={S_C*100:.1f}%（在 S=80% 線下方）", 16, C["load"], "start", "700")
    cv.L(X(W_C*100), Y(GD_C) + 8, X(12.5), Y(14.6) - 14, color=C["load"], w=1.5)
    cv.M(520, 95, "γ_{d} = G_{s}γ_{w} / (1 + wG_{s}/S)", 21, C["text"])
    cv.T(520, 128, "所有夯實點都必須在 ZAVC 左下方", 16, C["muted"])
    return save(cv, 8, "zavc")


# ─────────── 圖 9：e-log p' → 沉陷量 ───────────
def fig_elogp():
    cv = PX(1000, 560)
    lx = lambda p: math.log10(p)
    X, Y = axes_plot(cv, 110, 50, 520, 400, (lx(50), lx(400)), (0.85, 1.25), [], [0.85, 0.95, 1.05, 1.15, 1.25],
                     "有效應力 p'（kPa，對數刻度）", "孔隙比 e", fy="{:.2f}")
    for p in [50, 100, 200, 400]:
        cv.L(X(lx(p)), 450, X(lx(p)), 456, color=C["member"], w=1.5); cv.T(X(lx(p)), 472, f"{p}", 15, C["muted"])
    e_of = lambda p: E0 - CC * math.log10(p / P0)
    cv.PL([(X(lx(p)), Y(e_of(p))) for p in [50 * 1.05 ** i for i in range(0, 43)] if e_of(p) >= 0.85], color=C["bmd"], w=3.5)
    for p, e in [(P0, E0), (P1, E1)]:
        cv.L(X(lx(p)), Y(e), X(lx(p)), 450, color=C["dim"], w=1.5, dash="5 5")
        cv.L(110, Y(e), X(lx(p)), Y(e), color=C["dim"], w=1.5, dash="5 5")
        cv.CI(X(lx(p)), Y(e), 7, C["load"], "#FFFFFF", 2)
    cv.L(125, Y(E0), 125, Y(E1), color=C["load"], w=3.5)
    cv.M(135, (Y(E0) + Y(E1)) / 2, f"Δe = {DE:.4f}", 18, C["load"], "start")
    cv.T(X(lx(P0)) + 10, Y(E0) - 18, f"p'_{{0}}={P0:.0f}, e_{{0}}={E0:.2f}", 15, C["text"], "start")
    cv.T(X(lx(P1)) + 10, Y(E1) - 18, f"p'={P1:.0f}, e={E1:.3f}", 15, C["text"], "start")
    cv.M(470, 90, f"C_{{c}} = {CC:.2f}", 20, C["bmd"])
    # 右：換成厚度
    cv.A(650, 270, 720, 270, color=C["accent"], w=3, head=13)
    cv.T(685, 240, "÷(1+e_{0})×H_{0}", 15, C["accent"], weight="700")
    s = 85; base = 470; xr = 740
    cv.R(xr, base - H0 * s, 120, H0 * s, "#DCE3EE", C["member"], 2)
    cv.R(xr, base - H0 * s, 120, SC * s, "#F6D5D1", C["load"], 2)
    cv.T(xr + 60, base - H0 * s - 22, f"H_{{0}} = {H0:.2f} m", 17, C["text"], weight="700")
    cv.T(xr + 130, base - H0 * s + SC * s / 2, f"Sc = {SC*100:.1f} cm", 18, C["load"], "start", "700")
    cv.T(xr + 60, base + 30, f"εv = {EPS*100:.2f}%", 16, C["muted"])
    return save(cv, 9, "elogp")


# ─────────── 圖 10：分母錯誤的代價 ───────────
def fig_error():
    cv = PX(1000, 520)
    # 左：兩根長條
    base = 440; s = 11
    for i, (v, lab, col) in enumerate([(SC * 100, "分母 1+e_{0}（正確）", C["bmd"]), (SC_W * 100, "分母 1+e（錯誤）", C["load"])]):
        x = 90 + i * 170
        cv.R(x, base - v * s, 110, v * s, col, col, 1, 4)
        cv.T(x + 55, base - v * s - 20, f"{v:.1f} cm", 19, col, weight="700")
        cv.T(x + 55, base + 26, lab, 16, C["text"])
    cv.L(60, base, 400, base, color=C["member"], w=2.5)
    cv.T(230, 40, f"案例 A：高估 {ERR*100:.1f}%", 20, C["text"], weight="700")
    # 右：誤差 vs εv
    X, Y = axes_plot(cv, 560, 60, 380, 330, (0, 0.30), (0, 45), [0, 0.1, 0.2, 0.3], [0, 15, 30, 45],
                     "體積應變 εv", "高估比例（%）", "{:.1f}", "{:.0f}")
    cv.PL([(X(e / 100), Y(100 * (e / 100) / (1 - e / 100))) for e in range(0, 31)], color=C["load"], w=3.5)
    cv.CI(X(EPS), Y(ERR * 100), 7, C["load"], "#FFFFFF", 2)
    cv.T(X(EPS) + 12, Y(ERR * 100) - 16, "案例 A", 15, C["load"], "start", "700")
    cv.T(640, 95, "誤差 =", 18, C["text"], "start")
    cv.M(700, 95, "ε_{v} / (1 − ε_{v})", 20, C["text"], "start")
    cv.T(750, 505, "壓縮越大，錯得越多", 16, C["muted"])
    return save(cv, 10, "error")


# ─────────── 圖 11：乾土重守恆對帳 ───────────
def fig_check():
    cv = PX(900, 500)
    s = 85; base = 420
    for i, (H, gd, e, lab) in enumerate([(H0, GD0, E0, "受壓前"), (H1, GD1, E1, "受壓後")]):
        x = 110 + i * 330
        cv.R(x, base - H * s, 150, H * s, "#DCE3EE", C["member"], 2)
        cv.T(x + 75, base - H * s - 50, lab, 19, C["text"], weight="700")
        cv.T(x + 75, base - H * s - 20, f"e = {e:.3f}", 16, C["muted"])
        cv.T(x + 75, base - H * s / 2 - 16, f"H = {H:.3f} m", 17, C["text"])
        cv.T(x + 75, base - H * s / 2 + 14, f"γd = {gd:.2f}", 17, C["text"])
        cv.T(x + 75, base + 30, f"γd·H = {gd*H:.2f} kN/m²", 17, C["bmd"], weight="700")
    cv.L(70, base, 660, base, color=C["member"], w=2.5)
    cv.R(690, 160, 190, 150, "#EAF3F1", C["bmd"], 2, 12)
    cv.T(785, 200, "每平方公尺固體重", 17, C["bmd"], weight="700")
    cv.T(785, 235, "前後相等", 17, C["bmd"], weight="700")
    cv.T(785, 275, "→ Vs 不變的驗證", 15, C["muted"])
    cv.T(450, 485, "算完 Sc 後，用 γd·H 是否守恆來自我檢查", 16, C["muted"])
    return save(cv, 11, "check")


# ─────────── 圖 12：以 e 為樞紐的解題路線 ───────────
def fig_hub():
    cv = PX(1000, 520)
    cx, cy = 500, 260
    cv.CI(cx, cy, 78, "#FFF4E5", C["accent"], 3)
    cv.T(cx, cy - 16, "孔隙比", 20, C["accent"], weight="700"); cv.M(cx, cy + 20, "e", 32, C["accent"])
    left = [("γd、γt 與 w", 90, C["load"], "①"), ("w 與 S", 260, C["deform"], "②"), ("RC 或 Dr", 430, C["load"], "①")]
    right = [("Δe、εv", 90, C["bmd"], "③"), ("Sc（沉陷量）", 260, C["bmd"], "③"), ("ZAVC 上下限", 430, C["deform"], "②")]
    for t, y, col, n in left:
        cv.R(50, y - 38, 260, 76, "#FFFFFF", col, 2.5, 12)
        cv.T(180, y, t, 19, C["text"], weight="700")
        cv.A(312, y, cx - 80, cy + (y - cy) * 0.35, color=col, w=3, head=12)
        cv.T(360, y + (cy - y) * 0.3 - 14, n, 18, col, weight="700")
    for t, y, col, n in right:
        cv.R(690, y - 38, 260, 76, "#FFFFFF", col, 2.5, 12)
        cv.T(820, y, t, 19, C["text"], weight="700")
        cv.A(cx + 80, cy + (y - cy) * 0.35, 688, y, color=col, w=3, head=12)
        cv.T(640, y + (cy - y) * 0.3 - 14, n, 18, col, weight="700")
    cv.T(180, 30, "題目給的", 18, C["muted"], weight="700"); cv.T(820, 30, "要求的", 18, C["muted"], weight="700")
    cv.T(500, 500, "①②③ 為使用的關係式編號：先換成 e，再從 e 走出去", 16, C["muted"])
    return save(cv, 12, "hub")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for f in [fig_map, fig_phase, fig_particles, fig_columns, fig_gd_e, fig_rc_dr,
              fig_sat, fig_zav, fig_elogp, fig_error, fig_check, fig_hub]:
        print(f())
    print(f"DE={DE:.4f} E1={E1:.4f} EPS={EPS:.5f} SC={SC:.4f} SCW={SC_W:.4f} ERR={ERR:.4f} H1={H1:.4f}")
    print(f"GD0={GD0:.3f} GD1={GD1:.3f} W0={W0:.4f} W1={W1:.4f} prod={GD0*H0:.3f},{GD1*H1:.3f}")
    print(f"E_B={E_B:.3f} GD_B={GD_B:.3f} GDMAX={GDMAX:.3f} GDMIN={GDMIN:.3f} RC={RC_B:.4f} RC0={RC_0:.4f}")
    print(f"S_C={S_C:.4f} GD_C={GD_C:.3f}")
