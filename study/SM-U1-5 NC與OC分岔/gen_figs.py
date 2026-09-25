"""SM-U1-5 拼圖四：NC / OC 分岔 — 向量圖（所有幾何由 params.py 算出）"""
import math
from svglib import SVG, measure, INK, MUTED, GRID, PANEL
from params import *
R_ = math.radians

EFF, TOT, RED, NAVY = "#E4572E", "#2F54C8", "#C0392B", "#1B2432"
GREEN, GREENBG = "#2E7D6B", "#E6F2EF"
EFFBG, TOTBG, GOLD, GOLDBG, PUR, PURBG = "#FDEDE8", "#EEF2FB", "#B7791F", "#FBF3E4", "#6D4BC2", "#F1EDFA"
REDBG = "#FBECEA"
WATER, WATERD = "#D9ECF7", "#2C6E9E"
SLATE = "#4A6380"
W = "#FFFFFF"


class Ax:
    def __init__(s, g, x0, y0, k):
        s.g, s.x0, s.y0, s.k = g, x0, y0, k
    def X(s, v): return s.x0 + v*s.k
    def Y(s, v): return s.y0 - v*s.k
    def P(s, a, b): return (s.X(a), s.Y(b))
    def axes(s, xmax, ymax, xl="σ'", yl="τ", xmin=0, size=20):
        g = s.g
        g.arrow(s.X(xmin), s.y0, s.X(xmax), s.y0, INK, 2, 10)
        g.arrow(s.x0, s.y0 + 4, s.x0, s.Y(ymax), INK, 2, 10)
        g.text(s.X(xmax) + 8, s.y0 + 7, xl, size, INK, weight="bold")
        g.text(s.x0 - 10, s.Y(ymax) + 4, yl, size, INK, anchor="end", weight="bold")
    def line(s, a, b, c, dd, **kw): s.g.line(s.X(a), s.Y(b), s.X(c), s.Y(dd), **kw)
    def semi(s, Cc, Rr, color, sw=2.6, dash=None, fill=None, op=0.12):
        x1, x2, y = s.X(Cc - Rr), s.X(Cc + Rr), s.y0; rr = Rr*s.k
        dsh = f' stroke-dasharray="{dash}"' if dash else ''
        f = f'fill="{fill}" fill-opacity="{op}"' if fill else 'fill="none"'
        s.g.add(f'<path d="M{x1:.1f},{y:.1f} A{rr:.1f},{rr:.1f} 0 0 1 {x2:.1f},{y:.1f}" {f} stroke="{color}" stroke-width="{sw}"{dsh}/>')
    def tick(s, v, lab, color=MUTED, size=15, dy=26, weight="normal"):
        s.g.line(s.X(v), s.y0, s.X(v), s.y0 + 6, INK, 1.5)
        s.g.text(s.X(v), s.y0 + dy, lab, size, color, anchor="middle", weight=weight)
    def env(s, c, phi, a, b, **kw):
        t = math.tan(R_(phi)); s.line(a, c + a*t, b, c + b*t, **kw)


def card(g, x, y, w, h, fill=PANEL, stroke="#D5DAE1", rx=12, sw=1.2):
    g.rect(x, y, w, h, fill=fill, stroke=stroke, sw=sw, rx=rx)


def dot(g, x, y, c, r=7): g.circle(x, y, r, fill=c, stroke=W, sw=2)


def ang(g, cx, cy, rad, a1, a2, color, lab=None, lr=None, size=17, sw=2):
    g.arc(cx, cy, rad, a1, a2, color, sw)
    if lab:
        m = R_((a1 + a2)/2); lr = lr or rad + 16
        g.text(cx + lr*math.cos(m), cy - lr*math.sin(m) + 6, lab, size, color, anchor="middle", weight="bold")




class XY:
    """獨立 x、y 比例尺的座標系（σ'1–σ'3 平面、K_p–φ' 曲線用）"""
    def __init__(s, g, x0, y0, kx, ky, xmin=0, ymin=0):
        s.g, s.x0, s.y0, s.kx, s.ky, s.xmin, s.ymin = g, x0, y0, kx, ky, xmin, ymin
    def X(s, v): return s.x0 + (v - s.xmin)*s.kx
    def Y(s, v): return s.y0 - (v - s.ymin)*s.ky
    def P(s, a, b): return (s.X(a), s.Y(b))
    def axes(s, xmax, ymax, xl, yl, size=19):
        g = s.g
        g.arrow(s.x0, s.y0, s.X(xmax), s.y0, INK, 2, 10)
        g.arrow(s.x0, s.y0 + 4, s.x0, s.Y(ymax), INK, 2, 10)
        g.text(s.X(xmax) + 8, s.y0 + 7, xl, size, INK, weight="bold")
        g.text(s.x0 + 10, s.Y(ymax) + 4, yl, size, INK, weight="bold")
    def xt(s, v, lab, color=MUTED, size=14, dy=24, weight="normal"):
        s.g.line(s.X(v), s.y0, s.X(v), s.y0 + 6, INK, 1.4)
        s.g.text(s.X(v), s.y0 + dy, lab, size, color, anchor="middle", weight=weight)
    def yt(s, v, lab, color=MUTED, size=14, weight="normal"):
        s.g.line(s.x0 - 6, s.Y(v), s.x0, s.Y(v), INK, 1.4)
        s.g.text(s.x0 - 10, s.Y(v) + 5, lab, size, color, anchor="end", weight=weight)
    def seg(s, a, b, c, dd, **kw): s.g.line(s.X(a), s.Y(b), s.X(c), s.Y(dd), **kw)
    def curve(s, pts, **kw): s.g.poly([s.P(a, b) for a, b in pts], **kw)


def mini_mohr(g, x0, y0, k, c, phi, circles, col, xmax, ymax):
    ax = Ax(g, x0, y0, k)
    g.arrow(x0, y0, x0 + xmax*k, y0, INK, 1.6, 8); g.arrow(x0, y0 + 3, x0, y0 - ymax*k, INK, 1.6, 8)
    g.text(x0 + xmax*k + 4, y0 + 5, "σ'", 14, INK, weight="bold"); g.text(x0 - 6, y0 - ymax*k + 4, "τ", 14, INK, anchor="end", weight="bold")
    for (cc, rr) in circles: ax.semi(cc, rr, INK, 1.8, fill=TOT, op=0.07)
    ax.env(c, phi, 0, xmax*0.95, color=col, sw=2.6)
    return ax


# ───────── fig01 總覽：一個問題分兩條路 ─────────
def fig01():
    g = SVG(1200, 460)
    card(g, 330, 12, 540, 58, NAVY, NAVY, 10)
    g.text(600, 49, "讀題：正常壓密？OCR = 1？首次加載？", 20, W, anchor="middle", weight="bold")
    g.arrow(600, 70, 600, 92, INK, 2.2, 10)
    g.poly([(600, 92), (760, 140), (600, 188), (440, 140)], NAVY, 2.4, fill=W, closed=True)
    g.text(600, 147, "包絡線過原點？（c' = 0？）", 18, NAVY, anchor="middle", weight="bold")
    g.poly([(440, 140), (275, 140)], INK, 2.2); g.arrow(275, 140, 275, 202, INK, 2.2, 10)
    g.poly([(760, 140), (925, 140)], INK, 2.2); g.arrow(925, 140, 925, 202, INK, 2.2, 10)
    g.text(360, 130, "是 → NC", 17, GREEN, anchor="middle", weight="bold")
    g.text(840, 130, "否 → OC", 17, RED, anchor="middle", weight="bold")
    for X, col, bg, ttl, lines, c, cir in [
        (30, GREEN, GREENBG, "NC：c' = 0，包絡線過原點",
         ["捷徑 1　正弦式 sin φ' = R / C", "捷徑 2　比例法 Δσ_d ∝ σ_3", "捷徑 3　S_u / σ'_{v0} 比值式"], 0.0,
         [(55, 25), (138, 62)]),
        (680, RED, REDBG, "OC：c' ≠ 0，包絡線有截距",
         ["回到萬能式 σ'_1 = σ'_3 K_p + 2c'√K_p", "兩組數據 → 相減法", "單組數據 → 令 y = √K_p 解二次式"], 18.0,
         [(70, 45), (160, 80)])]:
        card(g, X, 202, 490, 170, bg, col, 12, 2)
        g.text(X + 20, 236, ttl, 19, col, weight="bold")
        phi = 30 if c == 0 else 24
        if c == 0:
            cir = [(C0, C0*math.sin(R_(phi))) for C0 in (50, 125)]
        else:
            cir = [(C0, C0*math.sin(R_(phi)) + c*math.cos(R_(phi))) for C0 in (60, 140)]
        mini_mohr(g, X + 24, 356, 0.62, c, phi, cir, col, 215, 150)
        for i, t in enumerate(lines):
            g.text(X + 190, 280 + i*32, t, 16, INK, weight="bold" if i == 0 else "normal")
    card(g, 30, 388, 1140, 60, NAVY, NAVY, 12)
    g.text(600, 426, "兩邊共用 捷徑 4：K_p ↔ φ' 互推、兩組試驗相減法（相減法正是為 c' ≠ 0 而生）", 19, "#F2A65A", anchor="middle", weight="bold")
    g.save("figs/fig01_fork.svg")


# ───────── fig02 應力歷史：e–log σ' ─────────
def fig02():
    g = SVG(1200, 460)
    card(g, 15, 15, 740, 430, PANEL)
    g.text(35, 50, "同一種黏土、同樣的 σ'_0 = 50 kPa，歷史不同 → 狀態不同（示意）", 18, NAVY, weight="bold")
    x0, y0, kd = 110, 395, 250          # 每 decade 250 px，σ' 從 10 起
    ke = 700                            # e 每 1.0 = 700 px
    X = lambda s: x0 + (math.log10(s) - 1)*kd
    Y = lambda e: y0 - (e - 0.72)*ke
    g.arrow(x0, y0, x0 + 2.35*kd, y0, INK, 2, 10); g.arrow(x0, y0 + 4, x0, Y(1.14), INK, 2, 10)
    g.text(x0 + 2.35*kd + 6, y0 + 7, "log σ'", 18, INK, weight="bold"); g.text(x0 - 12, Y(1.14) + 6, "e", 20, INK, anchor="end", weight="bold")
    for s in (10, 100):
        g.line(X(s), y0, X(s), y0 + 6, INK, 1.4); g.text(X(s), y0 + 24, f"{s}", 14, MUTED, anchor="middle")
    Cc, Cs, eref, sref = 0.30, 0.06, 1.12, 20
    ncl = lambda s: eref - Cc*math.log10(s/sref)
    g.poly([(X(s), Y(ncl(s))) for s in (20, 400)], NAVY, 3.2)
    g.text(X(330), Y(ncl(330)) - 14, "原始壓縮線 NCL", 16, NAVY, weight="bold")
    eP = ncl(H_SP); eO = eP + Cs*math.log10(H_SP/H_S0); eN = ncl(H_S0)
    # 卸載
    g.arrow(X(H_SP), Y(eP), X(H_S0) + 8, Y(eO) + 1, RED, 2.8, 11)
    g.line(X(H_S0), y0, X(H_S0), Y(eN), MUTED, 1.4, "5 4"); g.line(X(H_SP), y0, X(H_SP), Y(eP), MUTED, 1.4, "5 4")
    g.text(X(H_S0), y0 + 24, "σ'_0 = 50", 15, INK, anchor="middle", weight="bold")
    g.text(X(H_SP), y0 + 24, "σ'_p = 200", 15, RED, anchor="middle", weight="bold")
    dot(g, X(H_S0), Y(eN), GREEN, 9); dot(g, X(H_S0), Y(eO), RED, 9); dot(g, X(H_SP), Y(eP), GOLD, 8)
    g.text(X(H_S0) + 14, Y(eN) - 12, "NC 土：現在就站在 NCL 上", 16, GREEN, weight="bold")
    g.text(X(H_S0) - 14, Y(eO) + 24, "OC 土：從 σ'_p 卸載回來", 16, RED, anchor="end", weight="bold")
    g.text(X(H_SP) + 12, Y(eP) - 12, "歷史最大 σ'_p", 15, GOLD, weight="bold")
    g.arrow(X(H_S0) - 22, Y(eN) + 6, X(H_S0) - 22, Y(eO) - 10, SLATE, 1.8, 8)
    g.text(X(H_S0) - 32, (Y(eN) + Y(eO))/2 + 5, "e 較小 = 較密", 15, SLATE, anchor="end", weight="bold")
    # 右側
    Xr = 780
    card(g, Xr, 15, 405, 128, GOLDBG, GOLD, 12, 1.6)
    g.text(Xr + 20, 52, "過壓密比", 19, GOLD, weight="bold")
    g.text(Xr + 20, 90, "OCR = σ'_p / σ'_0", 22, INK, weight="bold")
    g.text(Xr + 20, 124, f"本圖 OC 土：200 / 50 = {H_OCR:.0f}", 16, MUTED)
    card(g, Xr, 158, 405, 130, GREENBG, GREEN, 12, 1.6)
    g.text(Xr + 20, 194, "NC（OCR = 1）", 19, GREEN, weight="bold")
    g.text(Xr + 20, 228, "現在的 σ'_0 就是歷史最大", 16, INK)
    g.text(Xr + 20, 260, "沒有「更大應力」的擠壓記憶 → c' = 0", 16, INK, weight="bold")
    card(g, Xr, 303, 405, 142, REDBG, RED, 12, 1.6)
    g.text(Xr + 20, 339, "OC（OCR > 1）", 19, RED, weight="bold")
    g.text(Xr + 20, 373, "成因：地層侵蝕、冰河退去、開挖解壓", 16, INK)
    g.text(Xr + 20, 405, "顆粒保持較緊密排列 → 重新剪切時", 16, INK)
    g.text(Xr + 20, 433, "多出一段截距 c' ≠ 0", 16, INK, weight="bold")
    g.save("figs/fig02_history.svg")


def particles(g, x, y, w, h, sp, rr, seed, col):
    import random
    rnd = random.Random(seed); n = 0
    row = 0; yy = y + rr + 4
    while yy < y + h - rr - 2:
        xx = x + rr + 4 + (sp/2 if row % 2 else 0)
        while xx < x + w - rr - 2:
            jx, jy = rnd.uniform(-sp*0.12, sp*0.12), rnd.uniform(-sp*0.12, sp*0.12)
            r0 = rr*rnd.uniform(0.9, 1.05)
            cx, cy = min(max(xx + jx, x + r0 + 2), x + w - r0 - 2), min(max(yy + jy, y + r0 + 2), y + h - r0 - 2)
            g.circle(cx, cy, round(r0, 1), fill=col, stroke=INK, sw=1.4); n += 1
            xx += sp
        yy += sp*0.87; row += 1
    return n


# ───────── fig03 微觀：壓密記憶 = 截距 ─────────
def fig03():
    g = SVG(1200, 460)
    for X, ttl, col, bg, sp, note in [(20, "NC：鬆散排列", GREEN, GREENBG, 44, "顆粒間接觸少、無額外咬合"),
                                      (300, "OC：曾被 σ'_p 擠密", RED, REDBG, 33, "接觸點多、互相嵌鎖")]:
        card(g, X, 15, 265, 430, bg, col, 12, 1.8)
        g.text(X + 132, 50, ttl, 19, col, anchor="middle", weight="bold")
        g.rect(X + 22, 70, 221, 290, fill=W, stroke=SLATE, sw=1.6, rx=6)
        particles(g, X + 24, 72, 217, 286, sp, 14, 7 if sp > 40 else 11, "#E7D9BF")
        g.text(X + 132, 392, note, 16, INK, anchor="middle", weight="bold")
        if sp < 40:
            for xx in (X + 80, X + 132, X + 184):
                g.arrow(xx, 64, xx, 76, RED, 2, 8)
            g.text(X + 132, 424, "卸載後「記得」大應力", 15, RED, anchor="middle")
        else:
            g.text(X + 132, 424, "σ'_0 就是歷史最大", 15, GREEN, anchor="middle")
    # 右：包絡線
    card(g, 580, 15, 605, 430, PANEL)
    g.text(600, 50, "反映到莫爾–庫倫包絡線上", 19, NAVY, weight="bold")
    ax = Ax(g, 640, 395, 1.9)
    ax.axes(270, 160, size=19)
    ax.env(0, 26, 0, 262, color=GREEN, sw=3, dash="9 5")
    ax.env(22, 22, 0, 262, color=RED, sw=3)
    g.text(ax.X(215), ax.Y(215*math.tan(R_(26))) + 34, "NC：過原點", 16, GREEN, anchor="middle", weight="bold")
    g.text(ax.X(150), ax.Y(22 + 150*math.tan(R_(22))) - 16, "OC：多一段截距", 16, RED, anchor="end", weight="bold")
    g.text(ax.X(0) - 10, ax.Y(22) + 6, "c'", 18, RED, anchor="end", weight="bold")
    g.arrow(ax.X(8), ax.Y(0) - 2, ax.X(8), ax.Y(22) + 4, RED, 2, 8)
    card(g, 670, 72, 290, 128, W, "#D5DAE1", 10, 1.2)
    g.text(685, 102, "c' 是「壓密記憶」", 17, RED, weight="bold")
    g.text(685, 132, "不是膠結的真凝聚力", 16, INK)
    g.text(685, 162, "σ' 超過 σ'_p 後，記憶被抹平", 15, MUTED)
    g.text(685, 188, "→ 回到 NC 線（見陷阱 2）", 15, MUTED)
    g.save("figs/fig03_micro.svg")


# ───────── fig04 NC 位似：兩圓相似形（SM-2018-2 有效圓） ─────────
def fig04():
    g = SVG(1200, 460)
    ax = Ax(g, 70, 400, 1.95)
    ax.axes(330, 175, size=20)
    ax.env(0, N_PHI, 0, 245, color=GREEN, sw=3)
    c1, r1 = (N_S1E + N_S3E)/2, (N_S1E - N_S3E)/2
    c2, r2 = (N_S1BE + N_S3BE)/2, (N_S1BE - N_S3BE)/2
    ax.semi(c1, r1, INK, 2.4, fill=TOT, op=0.10)
    ax.semi(c2, r2, INK, 2.8, fill=TOT, op=0.08)
    # 位似射線：原點 → 圓頂
    ax.line(0, 0, c2*1.06, r2*1.06, color=GOLD, sw=2, dash="7 5")
    for (cc, rr) in [(c1, r1), (c2, r2)]:
        dot(g, ax.X(cc), ax.Y(rr), GOLD, 7)
        t = math.sin(R_(N_PHI)); tx, ty = cc - rr*t, rr*math.cos(R_(N_PHI))
        dot(g, ax.X(tx), ax.Y(ty), GREEN, 7)
    g.circle(ax.X(0), ax.Y(0), 10, fill="none", stroke=GOLD, sw=3)
    g.text(ax.X(4), ax.Y(0) + 46, "位似中心 = 原點", 16, GOLD, weight="bold")
    g.text(ax.X(c2*1.06) + 10, ax.Y(r2*1.06) + 26, "圓頂連線也過原點", 16, GOLD, weight="bold")
    ang(g, ax.X(0), ax.Y(0), 90, 0, N_PHI, GREEN, "φ'", 108, 17)
    ax.tick(N_S3E, "33", SLATE, 14, weight="bold"); ax.tick(N_S1E, "118", SLATE, 14, weight="bold")
    ax.tick(N_S3BE, "82.5", INK, 14, weight="bold"); ax.tick(N_S1BE, "295", INK, 14, weight="bold")
    g.text(ax.X(c1), ax.Y(r1) - 14, "試體 1", 15, SLATE, anchor="middle", weight="bold")
    g.text(ax.X(c2 + r2*0.8) + 8, ax.Y(r2*0.6) - 6, "試體 2", 15, INK, weight="bold")
    X = 770
    card(g, X, 20, 415, 330, PANEL, "#C9D3DF", 12, 1.6)
    g.text(X + 20, 56, "[SM-2018-2] 有效應力圓（kPa）", 17, NAVY, weight="bold")
    rows = [("", "試體 1", "試體 2", "比值"), ("σ'_3", "33", "82.5", "2.5"), ("σ'_1", "118", "295", "2.5"),
            ("C", f"{c1:.1f}", f"{c2:.2f}", "2.5"), ("R", f"{r1:.1f}", f"{r2:.2f}", "2.5"), ("sin φ'", f"{N_SIN_E:.4f}", f"{N_SIN_E:.4f}", "同")]
    for i, row in enumerate(rows):
        y = 96 + i*42
        if i: g.line(X + 16, y - 28, X + 399, y - 28, GRID, 1)
        for j, t in enumerate(row):
            xx = [X + 22, X + 170, X + 280, X + 395][j]
            g.text(xx, y, t, 16, (MUTED if i == 0 else (GOLD if j == 3 else INK)), anchor="start" if j == 0 else ("end" if j == 3 else "middle"), weight="bold")
    card(g, X, 365, 415, 80, GREENBG, GREEN, 12, 1.6)
    g.text(X + 20, 398, "包絡線過原點 → 所有破壞圓互為相似形", 16, GREEN, weight="bold")
    g.text(X + 20, 428, "圍壓 × 2.5 → 整張圖放大 2.5 倍", 16, INK)
    g.save("figs/fig04_homo.svg")


# ───────── fig05 OC 不相似（SM-2024-1） ─────────
def fig05():
    g = SVG(1200, 460)
    ax = Ax(g, 70, 410, 0.68)
    ax.axes(740, 360, size=20)
    ax.env(O_C, O_PHI, 0, 715, color=RED, sw=3)
    ax.semi((O_S1 + O_S3)/2, O_DSD/2, INK, 2.4, fill=TOT, op=0.10)
    ax.semi((O_S1B + O_S3B)/2, O_DSDB/2, INK, 2.8, fill=TOT, op=0.08)
    s1w = O_S3B + O_DSD_PROP
    ax.semi((s1w + O_S3B)/2, O_DSD_PROP/2, RED, 2.2, "8 5")
    ax.tick(O_S3, "100", SLATE, 14, weight="bold"); ax.tick(O_S1, "340", SLATE, 14, weight="bold")
    ax.tick(O_S3B, "200", INK, 14, weight="bold"); ax.tick(O_S1B, f"{O_S1B:.2f}", INK, 14, 42, "bold")
    ax.tick(s1w, f"{s1w:.0f}", RED, 14, weight="bold")
    g.text(ax.X(0) - 8, ax.Y(O_C) + 6, "c' = 25", 15, RED, anchor="end", weight="bold")
    g.text(ax.X(610), ax.Y(200), "比例法的圓：", 15, RED, weight="bold")
    g.text(ax.X(610), ax.Y(200) + 22, "衝出包絡線 = 不可能", 15, RED, weight="bold")
    X = 800
    card(g, X, 20, 385, 250, PANEL, "#C9D3DF", 12, 1.6)
    g.text(X + 20, 54, "圍壓 100 → 200（× 2）", 18, NAVY, weight="bold")
    kb = 0.62
    for i, (lab, v, col) in enumerate([("σ'_3 = 100", O_DSD, SLATE), ("σ'_3 = 200 真值", O_DSDB, GREEN), ("× 2 比例法", O_DSD_PROP, RED)]):
        y = 82 + i*60
        g.text(X + 20, y + 4, lab, 15, col, weight="bold")
        g.rect(X + 20, y + 14, v*kb, 20, fill=col, stroke="none", rx=3, op=0.85)
        g.text(X + 26 + v*kb, y + 30, f"{v:.2f}".rstrip("0").rstrip("."), 15, col, weight="bold")
    g.text(X + 20, 262, f"比例法高估 {O_OVER:.1f}%", 17, RED, weight="bold")
    card(g, X, 285, 385, 160, REDBG, RED, 12, 1.6)
    g.text(X + 20, 320, "為什麼不能等比放大？", 17, RED, weight="bold")
    g.text(X + 20, 352, f"σ'_1 = σ'_3 K_p + 2c'√K_p", 17, INK, weight="bold")
    g.text(X + 20, 384, f"第一項隨圍壓放大（× {O_KP:.4f}）", 15, INK)
    g.text(X + 20, 412, f"第二項 2c'√K_p = {O_ICPT:.2f} 固定不動", 15, INK, weight="bold")
    g.text(X + 20, 436, "→ 兩圓不相似，比例法失效", 15, RED, weight="bold")
    g.save("figs/fig05_oc.svg")


# ───────── fig06 σ'1–σ'3 平面：比例法 = 過原點的直線 ─────────
def fig06():
    g = SVG(1200, 460)
    p = XY(g, 130, 410, 2.5, 0.52)
    p.axes(235, 720, "σ'_3", "σ'_1")
    for v in (100, 200): p.xt(v, f"{v}")
    for v in (200, 400, 600): p.yt(v, f"{v}")
    p.seg(0, O_ICPT, 225, O_ICPT + 225*O_KP, color=RED, sw=3.2)
    p.seg(0, 0, 225, 225*O_S1/O_S3, color=GREEN, sw=2.4, dash="8 5")
    for s3, s1 in [(O_S3, O_S1), (O_S3B, O_S1B)]: dot(g, *p.P(s3, s1), RED, 8)
    g.circle(*p.P(O_S3B, 2*O_S1), 7, fill=W, stroke=GREEN, sw=2.6)
    g.text(p.X(O_S3B) + 14, p.Y(O_S1B) + 24, f"真值 {O_S1B:.2f}", 15, RED, weight="bold")
    g.text(p.X(O_S3B) + 14, p.Y(2*O_S1) + 5, f"比例法 {2*O_S1:.0f}", 15, GREEN, weight="bold")
    g.arrow(p.X(O_S3B) - 12, p.Y(2*O_S1) + 8, p.X(O_S3B) - 12, p.Y(O_S1B) - 8, GOLD, 2.2, 9)
    g.arrow(p.X(O_S3B) - 12, p.Y(O_S1B) - 8, p.X(O_S3B) - 12, p.Y(2*O_S1) + 8, GOLD, 2.2, 9)
    g.text(p.X(O_S3B) - 20, p.Y((O_S1B + 2*O_S1)/2) + 6, f"差 {2*O_S1 - O_S1B:.2f}", 15, GOLD, anchor="end", weight="bold")
    p.yt(O_ICPT, f"{O_ICPT:.2f}", RED, 14, "bold")
    g.text(p.x0 - 10, p.Y(O_ICPT) - 22, "截距 2c'√K_p", 14, RED, anchor="end", weight="bold")
    g.text(p.X(O_S3) - 8, p.Y(O_S1) - 14, "(100, 340)", 14, RED, anchor="end", weight="bold")
    g.text(p.X(125), p.Y(125*O_KP + O_ICPT) + 40, f"[SM-2024-1] 真破壞線：斜率 {O_KP:.4f}、截距 {O_ICPT:.2f}", 15, RED, weight="bold")
    g.text(p.X(160) - 12, p.Y(160*O_S1/O_S3) - 10, "過原點的線（比例法的假設）", 15, GREEN, anchor="end", weight="bold")
    X = 770
    card(g, X, 20, 415, 200, GOLDBG, GOLD, 12, 1.6)
    g.text(X + 20, 56, "換個座標，一眼看穿", 18, GOLD, weight="bold")
    g.text(X + 20, 92, "破壞條件在 σ'_1–σ'_3 平面是一條直線：", 15, INK)
    g.text(X + 20, 124, "斜率 = K_p、截距 = 2c'√K_p", 17, INK, weight="bold")
    g.text(X + 20, 160, "NC：截距 = 0 → 直線過原點 → 比例法成立", 15, GREEN, weight="bold")
    g.text(X + 20, 192, "OC：截距 ≠ 0 → 比例法就是畫錯線", 15, RED, weight="bold")
    card(g, X, 235, 415, 210, REDBG, RED, 12, 1.6)
    g.text(X + 20, 270, "誤差剛好等於一個截距", 18, RED, weight="bold")
    g.text(X + 20, 306, "比例法：2 × 340 = 680", 16, INK)
    g.text(X + 20, 336, f"真值：200 × {O_KP:.4f} + {O_ICPT:.2f} = {O_S1B:.2f}", 16, INK)
    g.text(X + 20, 366, f"差 = {2*O_S1 - O_S1B:.2f} = 2c'√K_p", 16, RED, weight="bold")
    g.text(X + 20, 400, "圍壓加倍時，截距被「多算了一次」", 15, MUTED)
    g.text(X + 20, 428, f"Δσ_d：480 vs {O_DSDB:.2f}（高估 {O_OVER:.1f}%）", 15, MUTED)
    g.save("figs/fig06_lines.svg")


# ───────── fig07 捷徑適用範圍矩陣 ─────────
def fig07():
    g = SVG(1200, 460)
    cols = [30, 330, 700, 945]; wid = [300, 370, 245, 245]
    heads = ["捷徑", "公式", "NC（c' = 0）", "OC（c' ≠ 0）"]
    card(g, 30, 12, 1140, 48, NAVY, NAVY, 10)
    for x, w, h in zip(cols, wid, heads):
        g.text(x + w/2, 44, h, 18, W, anchor="middle", weight="bold")
    rows = [("1  正弦式", "sin φ' = R / C", True, False, "高估 φ'"),
            ("2  相似形比例法", "Δσ_d ∝ σ_3", True, False, "高估 Δσ_d"),
            ("3  S_u / σ'_{v0} 比值", "sin φ' / (1 + sin φ')", True, False, "不成立"),
            ("4a  K_p ↔ φ' 互推", "K_p = (1 + sin φ') / (1 − sin φ')", True, True, ""),
            ("4b  兩組試驗相減", "K_p = Δσ'_1 / Δσ'_3", True, True, "")]
    for i, (a, b, nc, oc, why) in enumerate(rows):
        y = 70 + i*72
        bg = PANEL if i < 3 else GOLDBG
        card(g, 30, y, 1140, 62, bg, "#D5DAE1" if i < 3 else "#E6CFA0", 10, 1.2)
        g.text(50, y + 39, a, 18, INK, weight="bold")
        g.text(cols[1] + 15, y + 39, b, 17, INK)
        notes = [("可用" if i != 2 else "可用（A_f = 1 課本式）"), ("可用（OC 的主力）" if i == 4 else "可用" if oc else why)]
        for x, ok, note in [(cols[2], nc, notes[0]), (cols[3], oc, notes[1])]:
            col = GREEN if ok else RED; cx, cy = x + 36, y + 31
            g.circle(cx, cy, 16, fill=col, stroke=W, sw=0)
            if ok: g.poly([(cx - 8, cy + 1), (cx - 2, cy + 7), (cx + 8, cy - 6)], W, 3.2)
            else:
                g.line(cx - 6, cy - 6, cx + 6, cy + 6, W, 3.2, cap="round"); g.line(cx - 6, cy + 6, cx + 6, cy - 6, W, 3.2, cap="round")
            g.text(x + 62, y + 38, note, 15, col, weight="bold")
    g.text(600, 448, "原講義標題寫「四大捷徑 OC 一律不能用」；更精確地說：捷徑 1～3 是 NC 專用，捷徑 4 兩邊通用", 15, MUTED, anchor="middle", weight="bold")
    g.save("figs/fig07_matrix.svg")


# ───────── fig08 捷徑 1 正弦式（SM-2018-2 總應力圓＋有效圓） ─────────
def fig08():
    g = SVG(1200, 460)
    ax = Ax(g, 70, 405, 2.75)
    ax.axes(225, 118, size=20)
    ax.env(0, N_PHICU, 0, 222, color=TOT, sw=2.8)
    ax.env(0, N_PHI, 0, 158, color=EFF, sw=3)
    ax.semi((N_S1 + N_S3)/2, N_SU, TOT, 2.6, fill=TOT, op=0.08)
    ax.semi((N_S1E + N_S3E)/2, N_SU, EFF, 2.8, fill=EFF, op=0.10)
    yA = ax.Y(N_SU) - 4
    g.arrow(ax.X((N_S1 + N_S3)/2), yA - 12, ax.X((N_S1E + N_S3E)/2) + 4, yA - 12, GOLD, 2.4, 10)
    g.text(ax.X(((N_S1 + N_S3)/2 + (N_S1E + N_S3E)/2)/2), yA - 22, "u_f = 67 左移", 16, GOLD, anchor="middle", weight="bold")
    ax.tick(N_S3E, "33", EFF, 14, weight="bold"); ax.tick(N_S1E, "118", EFF, 14, weight="bold")
    ax.tick(N_S3, "100", TOT, 14, 44, "bold"); ax.tick(N_S1, "185", TOT, 14, weight="bold")
    g.arc(ax.X(0), ax.Y(0), 55, 0, N_PHICU, TOT, 2); g.arc(ax.X(0), ax.Y(0), 75, 0, N_PHI, EFF, 2)
    g.text(ax.X(158) + 8, ax.Y(158*math.tan(R_(N_PHI))) + 4, f"有效 φ' = {N_PHI:.2f}°", 16, EFF, weight="bold")
    g.text(ax.X(222) - 4, ax.Y(222*math.tan(R_(N_PHICU))) - 14, f"總應力 φ_{{cu}} = {N_PHICU:.2f}°", 16, TOT, anchor="end", weight="bold")
    X = 740
    card(g, X, 20, 445, 150, TOTBG, "#B9C6EA", 12, 1.6)
    g.text(X + 20, 56, "總應力圓：100 ～ 185", 18, TOT, weight="bold")
    g.text(X + 20, 96, f"sin φ_{{cu}} = 85 / 285 = {N_SIN_CU:.4f}", 17, INK)
    g.text(X + 20, 134, f"φ_{{cu}} = {N_PHICU:.2f}°", 20, TOT, weight="bold")
    card(g, X, 185, 445, 150, EFFBG, "#F2B8A6", 12, 1.6)
    g.text(X + 20, 221, "有效圓：33 ～ 118", 18, EFF, weight="bold")
    g.text(X + 20, 261, f"sin φ' = 85 / 151 = {N_SIN_E:.4f}", 17, INK)
    g.text(X + 20, 299, f"φ' = {N_PHI:.2f}°", 20, EFF, weight="bold")
    card(g, X, 350, 445, 95, PANEL, "#D5DAE1", 12, 1.2)
    g.text(X + 20, 384, "分子都是 Δσ_d = 85（半徑不變）", 16, INK, weight="bold")
    g.text(X + 20, 416, "分母差 2u_f：有效圓離原點近 → 角度大", 15, MUTED)
    g.save("figs/fig08_sine.svg")


# ───────── fig09 捷徑 2 比例法：整組應力 × 2.5 ─────────
def fig09():
    g = SVG(1200, 460)
    card(g, 15, 15, 790, 430, PANEL)
    g.text(35, 50, "[SM-2018-2] 第二試體：圍壓 100 → 250，所有量 × 2.5", 18, NAVY, weight="bold")
    items = [("σ_3", N_S3, N_S3B, TOT), ("Δσ_d", N_DSD, N_DSDB, INK), ("u_f", N_UF, N_UFB, GOLD),
             ("σ'_3", N_S3E, N_S3BE, EFF), ("σ'_1", N_S1E, N_S1BE, EFF)]
    k = 0.66
    g.text(130, 88, "試體 1（σ_3 = 100）", 15, MUTED, weight="bold"); g.text(330, 88, "試體 2（σ_3 = 250）", 15, MUTED, weight="bold")
    for i, (lab, a, b, col) in enumerate(items):
        y = 108 + i*64
        g.text(40, y + 22, lab, 19, col, weight="bold")
        g.rect(130, y + 6, a*k, 22, fill=col, stroke="none", rx=3, op=0.45)
        g.text(138 + a*k, y + 23, f"{a:g}", 15, INK, weight="bold")
        g.text(292, y + 23, "×2.5", 14, GOLD, anchor="middle", weight="bold")
        g.rect(330, y + 6, b*k, 22, fill=col, stroke="none", rx=3, op=0.85)
        g.text(338 + b*k, y + 23, f"{b:g}", 16, col, weight="bold")
    g.text(35, 432, "u_f 也跟著放大：A_f 相同 → u_{f2} = 0.788 × 212.5 = 167.5", 15, MUTED, weight="bold")
    X = 825
    card(g, X, 15, 360, 140, GREENBG, GREEN, 12, 1.6)
    g.text(X + 20, 50, "(一) 3 秒答案", 18, GREEN, weight="bold")
    g.text(X + 20, 90, "Δσ_{d2} = 85 × 250/100", 18, INK)
    g.text(X + 20, 128, f"= {N_DSDB:g} kPa", 22, GREEN, weight="bold")
    card(g, X, 170, 360, 130, TOTBG, "#B9C6EA", 12, 1.6)
    g.text(X + 20, 204, "驗算 ①：總應力法", 17, TOT, weight="bold")
    g.text(X + 20, 238, "250 × tan²(45° + φ_{cu}/2)", 16, INK)
    g.text(X + 20, 270, f"= 250 × {N_KP_CU:.3f} = {N_S3B*N_KP_CU:.1f} ✓", 16, INK, weight="bold")
    card(g, X, 315, 360, 130, EFFBG, "#F2B8A6", 12, 1.6)
    g.text(X + 20, 349, "驗算 ②：有效圓角度不變", 17, EFF, weight="bold")
    g.text(X + 20, 383, "sin φ' = 212.5 / 377.5", 16, INK)
    g.text(X + 20, 415, f"= {N_SIN_E:.4f}（與試體 1 相同）✓", 16, INK, weight="bold")
    g.save("figs/fig09_ratio.svg")


# ───────── fig10 捷徑 3：S_u / σ'_v0 ─────────
def fig10():
    g = SVG(1200, 460)
    card(g, 15, 15, 580, 430, GREENBG, GREEN, 12, 1.6)
    g.text(35, 50, "課本式：A_f = 1 → 有效圓右緣 = σ'_{v0}", 18, GREEN, weight="bold")
    phi = 30.0; sv = 100.0; su = sv*math.sin(R_(phi))/(1 + math.sin(R_(phi)))
    ax = Ax(g, 60, 345, 3.9)
    ax.axes(128, 64, size=18)
    ax.env(0, phi, 0, 118, color=GREEN, sw=2.8)
    ax.semi(sv - su, su, INK, 2.6, fill=TOT, op=0.1)
    cx = ax.X(sv - su)
    g.line(cx, ax.y0, cx, ax.Y(su), SLATE, 1.8, "6 4")
    g.text(cx + 8, ax.Y(su/2), "R = S_u", 16, SLATE, weight="bold")
    dot(g, ax.X(sv), ax.y0, RED, 8)
    ax.tick(sv, "σ'_{1f} = σ'_{v0}", RED, 15, weight="bold")
    ax.tick(sv - su, "C = σ'_{v0} − S_u", NAVY, 14, 26, "bold")
    g.arc(ax.X(0), ax.Y(0), 60, 0, phi, GREEN, 2)
    g.text(ax.X(0) + 70, ax.Y(0) - 12, "φ'", 16, GREEN, weight="bold")
    g.text(35, 402, "sin φ' = R/C = S_u/(σ'_{v0} − S_u)", 16, INK, weight="bold")
    g.text(35, 432, f"→ S_u/σ'_{{v0}} = sin φ'/(1 + sin φ')；φ' = 30° → {su/sv:.3f}", 16, GREEN, weight="bold")
    card(g, 610, 15, 575, 430, PANEL, "#C9D3DF", 12, 1.6)
    g.text(630, 50, f"[SM-2018-2]：A_f = {N_AF:.3f}，右緣 118 ≠ 100", 18, NAVY, weight="bold")
    ax2 = Ax(g, 650, 345, 3.4)
    ax2.axes(150, 70, size=18)
    ax2.env(0, N_PHI, 0, 95, color=EFF, sw=2.8)
    ax2.semi((N_S1E + N_S3E)/2, N_SU, EFF, 2.6, fill=EFF, op=0.1)
    g.line(ax2.X(N_S3), ax2.y0 + 4, ax2.X(N_S3), ax2.Y(60), MUTED, 1.6, "6 4")
    ax2.tick(N_S3, "100", MUTED, 14, 26, "bold"); g.text(ax2.X(N_S3), ax2.Y(60) - 8, "σ'_c", 14, MUTED, anchor="middle", weight="bold"); ax2.tick(N_S1E, "118", EFF, 14, weight="bold")
    ax2.tick(N_S3E, "33", EFF, 14, weight="bold")
    card(g, 985, 70, 185, 110, W, "#D5DAE1", 10, 1.2)
    g.text(1000, 98, "實測", 15, MUTED, weight="bold")
    g.text(1000, 128, "S_u/σ'_c = 42.5/100", 15, INK)
    g.text(1000, 162, f"= {N_SU_RATIO:.3f}", 18, EFF, weight="bold")
    g.text(630, 410, f"課本式會算成 {N_SU_AF1:.3f}；一般式 sin φ'/[1 + (2A_f − 1) sin φ']", 15, INK, weight="bold")
    g.text(630, 434, f"= {N_SU_GEN:.3f} ✓（A_f = 1 時退化為課本式）", 15, INK, weight="bold")
    g.save("figs/fig10_su.svg")


# ───────── fig11 捷徑 4a：K_p ↔ φ' ─────────
def fig11():
    g = SVG(1200, 460)
    p = XY(g, 90, 405, 17.0, 95.0, xmin=10, ymin=1.0)
    p.axes(42, 4.6, "φ'（度）", "K_p")
    for v in (10, 20, 30, 40): p.xt(v, f"{v}°")
    for v in (1, 2, 3, 4): p.yt(v, f"{v}")
    p.curve([(a/2, kp_of(a/2)) for a in range(20, 81)], color=NAVY, sw=3)
    pts = [(Q_PHI, Q_KP, "[SM-2025-2]", GOLD), (O_PHI, O_KP, "[SM-2024-1]", RED), (30.0, 3.0, "黏土 A", GREEN), (N_PHI, N_KP_E, "[SM-2018-2]", EFF)]
    for i, (ph, kp, lab, col) in enumerate(pts):
        x, y = p.P(ph, kp)
        g.line(x, y, x, p.y0, col, 1.3, "4 4"); g.line(x, y, p.x0, y, col, 1.3, "4 4")
        dot(g, x, y, col, 7)
        if i == 0: g.text(x + 12, y + 26, f"{lab}  φ' = {ph:.2f}° ↔ K_p = {kp:.4g}", 14, col, weight="bold")
        else: g.text(x - 12, y - 12 - (8 if i == 2 else 0), f"{lab}  φ' = {ph:.2f}° ↔ K_p = {kp:.4g}", 14, col, anchor="end", weight="bold")
    X = 770
    card(g, X, 20, 415, 200, PANEL, "#C9D3DF", 12, 1.6)
    g.text(X + 20, 56, "同一個量的三種寫法", 18, NAVY, weight="bold")
    g.text(X + 20, 94, "K_p = tan²(45° + φ'/2)", 17, INK, weight="bold")
    g.text(X + 20, 128, "    = (1 + sin φ') / (1 − sin φ')", 17, INK, weight="bold")
    g.text(X + 20, 164, "√K_p = tan θ（θ = 破壞面角）", 16, INK)
    g.text(X + 20, 198, "sin φ' = (K_p − 1) / (K_p + 1)", 17, EFF, weight="bold")
    card(g, X, 235, 415, 210, GOLDBG, GOLD, 12, 1.6)
    g.text(X + 20, 270, "考場用法", 18, GOLD, weight="bold")
    g.text(X + 20, 306, "有 K_p 就有 φ'，兩者互推免查表", 16, INK)
    g.text(X + 20, 340, "NC、OC 都成立（只是三角恆等式）", 16, INK, weight="bold")
    g.text(X + 20, 374, "中間計算一律保留 K_p、√K_p", 16, INK)
    g.text(X + 20, 408, "最後要報告時才換成角度", 16, INK)
    g.text(X + 20, 434, "（拼圖三技巧：避開進位誤差）", 14, MUTED)
    g.save("figs/fig11_kp.svg")


# ───────── fig12 捷徑 4b：相減法（SM-2025-2，σ'1–σ'3 平面） ─────────
def fig12():
    g = SVG(1200, 460)
    p = XY(g, 90, 410, 2.55, 0.86)
    p.axes(235, 430, "σ'_3", "σ'_1")
    for v in (40, 80, 200): p.xt(v, f"{v:g}")
    for v in (80, 150, 360): p.yt(v, f"{v:g}")
    p.seg(0, Q_ICPT, 225, Q_ICPT + 225*Q_KP, color=GOLD, sw=3.2)
    p.seg(0, 0, 212, 212*Q_S1AE/Q_S3AE, color=RED, sw=2, dash="8 5")
    A, B, Cc = p.P(Q_S3AE, Q_S1AE), p.P(Q_S3BE, Q_S1BE), p.P(Q_S3C, Q_S1C)
    # 斜率三角形
    g.line(A[0], A[1], B[0], A[1], SLATE, 2, "5 4"); g.line(B[0], A[1], B[0], B[1], SLATE, 2, "5 4")
    g.text((A[0] + B[0])/2, A[1] + 22, "Δσ'_3 = 40", 15, SLATE, anchor="middle", weight="bold")
    g.text(B[0] + 10, (A[1] + B[1])/2 + 5, "Δσ'_1 = 70", 15, SLATE, weight="bold")
    dot(g, *A, GOLD, 8); dot(g, *B, GOLD, 8); dot(g, *Cc, GREEN, 9)
    g.text(A[0] - 12, A[1] - 12, "試體一 (40, 80)", 15, GOLD, anchor="end", weight="bold")
    g.text(B[0] - 12, B[1] - 12, "試體二 (80, 150)", 15, GOLD, anchor="end", weight="bold")
    g.text(Cc[0] + 14, Cc[1] + 24, "試體三 CD (200, 360)", 15, GREEN, weight="bold")
    wx, wy = p.P(Q_S3C, Q_S3C*2)
    g.circle(wx, wy, 7, fill=W, stroke=RED, sw=2.4)
    g.text(wx - 14, wy - 8, "過原點外推 400（錯）", 15, RED, anchor="end", weight="bold")
    p.yt(Q_ICPT, "10", GOLD, 14, "bold")
    g.text(p.X(95), p.Y(0) - 26, "截距 2c'√K_p = 10", 15, GOLD, weight="bold")
    g.arrow(p.X(92), p.Y(0) - 32, p.X(3), p.Y(Q_ICPT) + 2, GOLD, 1.6, 8)
    X = 770
    card(g, X, 20, 415, 215, GOLDBG, GOLD, 12, 1.6)
    g.text(X + 20, 56, "相減 = 算直線斜率", 18, GOLD, weight="bold")
    g.text(X + 20, 92, "兩點代入同一條直線，相減後截距消失", 15, INK)
    g.text(X + 20, 128, "K_p = 70 / 40 = 1.75", 19, INK, weight="bold")
    g.text(X + 20, 164, "回代：2c'√K_p = 80 − 40 × 1.75 = 10", 16, INK)
    g.text(X + 20, 200, "兩項都保留，不必先解 c'、φ'", 15, MUTED)
    card(g, X, 250, 415, 195, GREENBG, GREEN, 12, 1.6)
    g.text(X + 20, 286, "CD 試體三（σ'_3 = 200）", 18, GREEN, weight="bold")
    g.text(X + 20, 322, "σ'_1 = 200 × 1.75 + 10 = 360", 17, INK, weight="bold")
    g.text(X + 20, 358, "Δσ = 360 − 200 = 160 kN/m²", 19, GREEN, weight="bold")
    g.text(X + 20, 394, "若把試體一「過原點」外推：", 15, MUTED)
    g.text(X + 20, 424, "σ'_1 = 400 → Δσ = 200（高估 25%）", 15, RED, weight="bold")
    g.save("figs/fig12_subtract.svg")


# ───────── fig13 SM-2025-2 莫爾圓全圖 ─────────
def fig13():
    g = SVG(1200, 460)
    ax = Ax(g, 70, 405, 1.85)
    ax.axes(372, 150, size=20)
    ax.env(Q_C, Q_PHI, 0, 362, color=GOLD, sw=3)
    for s3, s1, col, dash in [(Q_S3A, Q_S3A + Q_DA, TOT, "7 5"), (Q_S3B, Q_S3B + Q_DB, TOT, "7 5")]:
        ax.semi((s1 + s3)/2, (s1 - s3)/2, col, 1.8, dash)
    for s3, s1, col in [(Q_S3AE, Q_S1AE, EFF), (Q_S3BE, Q_S1BE, EFF), (Q_S3C, Q_S1C, GREEN)]:
        cc, rr = (s1 + s3)/2, (s1 - s3)/2
        ax.semi(cc, rr, col, 2.8, fill=col, op=0.10)
        t = math.sin(R_(Q_PHI)); dot(g, ax.X(cc - rr*t), ax.Y(rr*math.cos(R_(Q_PHI))), col, 6)
    for v, lab, col, dy in [(Q_S3AE, "40", EFF, 24), (Q_S1AE, "80", EFF, 24), (Q_S1BE, "150", EFF, 24),
                            (Q_S3C, "200", GREEN, 24), (Q_S1C, "360", GREEN, 24), (Q_S3A, "75", TOT, 46), (Q_S3B + Q_DB, "220", TOT, 46)]:
        ax.tick(v, lab, col, 14, dy, "bold")
    g.text(ax.X(0) - 8, ax.Y(Q_C) + 6, f"c' = {Q_C:.2f}", 14, GOLD, anchor="end", weight="bold")
    g.text(ax.X(362), ax.Y(Q_C + 362*math.tan(R_(Q_PHI))) - 12, f"φ' = {Q_PHI:.2f}°", 16, GOLD, anchor="end", weight="bold")
    g.text(ax.X(Q_S3B + Q_DB/2), ax.Y(Q_DB/2) - 30, "總應力圓（虛線）", 14, TOT, anchor="middle", weight="bold")
    g.text(ax.X((Q_S3C + Q_S1C)/2), ax.Y(34), "CD 試體三：Δσ = 160", 16, GREEN, anchor="middle", weight="bold")
    X = 800
    card(g, X, 20, 385, 425, PANEL, "#C9D3DF", 12, 1.6)
    g.text(X + 20, 56, "[SM-2025-2] 數據（kN/m²）", 17, NAVY, weight="bold")
    rows = [("", "σ_3", "Δσ", "u", "σ'_3", "σ'_1"), ("試體一", "75", "40", "35", "40", "80"),
            ("試體二", "150", "70", "70", "80", "150"), ("試體三 CD", "200", "?", "0", "200", "?")]
    xs = [X + 20, X + 150, X + 200, X + 245, X + 295, X + 350]
    for i, row in enumerate(rows):
        y = 94 + i*36
        for j, t in enumerate(row):
            g.text(xs[j], y, t, 14 if j == 0 else 15, MUTED if i == 0 else INK, anchor="start" if j == 0 else "middle", weight="bold")
    g.line(X + 16, 104, X + 370, 104, GRID, 1.2)
    card(g, X + 15, 240, 355, 190, REDBG, RED, 10, 1.4)
    g.text(X + 30, 272, "OC 的證據：不成比例", 16, RED, weight="bold")
    g.text(X + 30, 304, "圍壓 75 → 150（× 2）", 15, INK)
    g.text(X + 30, 334, "比例法預測 Δσ = 80", 15, INK)
    g.text(X + 30, 364, "實測只有 70", 15, INK, weight="bold")
    g.text(X + 30, 396, "→ c' ≠ 0，改走相減法", 15, RED, weight="bold")
    g.text(X + 30, 422, f"（c' = {Q_C:.2f}、φ' = {Q_PHI:.2f}°，僅供報告）", 13, MUTED)
    g.save("figs/fig13_2025.svg")


def flowbox(g, x, y, w, h, t1, t2, col, bg, t3=None):
    card(g, x, y, w, h, bg, col, 10, 2)
    g.text(x + w/2, y + 30, t1, 17, col, anchor="middle", weight="bold")
    if t2: g.text(x + w/2, y + 58, t2, 15, INK, anchor="middle")
    if t3: g.text(x + w/2, y + 82, t3, 14, MUTED, anchor="middle")


# ───────── fig14 OC 解題 SOP 流程圖 ─────────
def fig14():
    g = SVG(1200, 460)
    flowbox(g, 20, 20, 300, 92, "Step 1　列萬能式", "σ'_1 = σ'_3 K_p + 2c'√K_p", NAVY, PANEL, "（CU 先扣 u_f 變有效應力）")
    g.arrow(320, 66, 370, 66, INK, 2.2, 10)
    g.poly([(485, 16), (600, 66), (485, 116), (370, 66)], NAVY, 2.2, fill=W, closed=True)
    g.text(485, 72, "幾組破壞數據？", 16, NAVY, anchor="middle", weight="bold")
    # 兩組
    g.poly([(600, 66), (640, 66)], INK, 2.2); g.arrow(640, 66, 660, 66, INK, 2.2, 10)
    g.text(628, 54, "兩組", 14, GOLD, anchor="middle", weight="bold")
    flowbox(g, 660, 20, 520, 100, "Step 2A　相減法消去截距", "K_p = (σ'_{1a} − σ'_{1b}) / (σ'_{3a} − σ'_{3b})，回代得 2c'√K_p", GOLD, GOLDBG,
            "[SM-2025-2]：K_p = 70/40 = 1.75、2c'√K_p = 10")
    # 單組
    g.arrow(485, 116, 485, 160, INK, 2.2, 10)
    g.text(497, 144, "單組（已知 c'）", 14, RED, weight="bold")
    flowbox(g, 250, 160, 470, 100, "Step 2B　令 y = √K_p 解二次式", "σ'_3 y² + 2c' y − σ'_1 = 0，取正根", RED, REDBG,
            f"[SM-2024-1]：10y² + 5y − 34 = 0 → y = {O_Y:.4f}")
    g.poly([(920, 120), (920, 300)], INK, 2.2); g.poly([(485, 260), (485, 300)], INK, 2.2)
    g.poly([(485, 300), (920, 300)], INK, 2.2); g.arrow(700, 300, 700, 322, INK, 2.2, 10)
    flowbox(g, 330, 322, 740, 60, "Step 3　保留 K_p、√K_p 直接代下一步（新圍壓的 σ'_1、c'）", "", GREEN, GREENBG)
    g.arrow(700, 382, 700, 398, INK, 2.2, 10)
    flowbox(g, 330, 398, 740, 56, "Step 4　要報告時才換角度：φ' = arcsin[(K_p − 1)/(K_p + 1)]", "", TOT, TOTBG)
    card(g, 20, 160, 210, 294, NAVY, NAVY, 12)
    g.text(125, 196, "為什麼", 17, "#F2A65A", anchor="middle", weight="bold")
    g.text(125, 226, "不先轉 φ'？", 17, W, anchor="middle", weight="bold")
    for k, t in enumerate(["K_p → φ' → K_p", "每轉一次", "就多一次進位", "", "[SM-2024-1]", "φ' 取 26° 回代", "σ'_1 少 3.9 kPa"]):
        g.text(125, 270 + k*26, t, 15, "#C9D3DF", anchor="middle")
    g.save("figs/fig14_ocsop.svg")


# ───────── fig15 NC 解題 SOP（SM-2018-2 四小題） ─────────
def fig15():
    g = SVG(1200, 460)
    steps = [("Step 1", "宣告 NC", ["c' = 0", "c_{cu} = 0", "兩條包絡線過原點"], GREEN, GREENBG),
             ("Step 2", "正弦式求角度", [f"φ_{{cu}} = {N_PHICU:.2f}°", f"φ' = {N_PHI:.2f}°", "（第二小題）"], EFF, EFFBG),
             ("Step 3", "比例法換圍壓", ["85 × 250/100", f"= {N_DSDB:g} kPa", "（第一小題）"], GOLD, GOLDBG),
             ("Step 4", "破壞面與 A_f", [f"θ = 45° + φ'/2 = {N_TH:.2f}°", f"A_f = 67/85 = {N_AF:.3f}", "（第三、四小題）"], TOT, TOTBG)]
    w = 270
    for i, (a, b, lines, col, bg) in enumerate(steps):
        x = 20 + i*(w + 23)
        card(g, x, 20, w, 290, bg, col, 12, 2)
        g.circle(x + 40, 62, 24, fill=col, stroke=W, sw=0)
        g.text(x + 40, 69, f"{i+1}", 20, W, anchor="middle", weight="bold")
        g.text(x + 74, 56, a, 14, col, weight="bold"); g.text(x + 74, 80, b, 18, INK, weight="bold")
        for k, t in enumerate(lines):
            g.text(x + w/2, 150 + k*44, t, 18 if k < 2 else 15, INK if k < 2 else MUTED, anchor="middle", weight="bold" if k < 2 else "normal")
        if i < 3: g.arrow(x + w + 2, 165, x + w + 21, 165, INK, 2.2, 9)
    card(g, 20, 330, 560, 115, REDBG, RED, 12, 1.6)
    g.text(40, 364, "Step 4 的陷阱：破壞面只認 φ'", 17, RED, weight="bold")
    g.text(40, 398, f"誤用 φ_{{cu}}：θ = {N_TH_WRONG:.2f}°（低估 {N_TH - N_TH_WRONG:.2f}°）", 16, INK)
    g.text(40, 428, "實體破壞面由顆粒摩擦（有效應力）決定", 15, MUTED)
    card(g, 600, 330, 580, 115, PANEL, "#C9D3DF", 12, 1.6)
    g.text(620, 364, "免費閉合檢核（φ' 與 A_f 互相綁住）", 17, NAVY, weight="bold")
    g.text(620, 398, f"Δσ_d = σ_3 (K_p − 1) / (1 − A_f + A_f K_p)", 16, INK, weight="bold")
    g.text(620, 428, f"= 100 × {N_KP_E - 1:.4f} / {1 - N_AF + N_AF*N_KP_E:.3f} = {N_DSD_CHK:.1f} ✓", 16, GREEN, weight="bold")
    g.save("figs/fig15_ncsop.svg")


# ───────── fig16 陷阱 1：OC 硬套比例法 ─────────
def fig16():
    g = SVG(1200, 460)
    groups = [("[SM-2024-1] CD：圍壓 100 → 200", [("正解（萬能式）", O_DSDB, GREEN), ("比例法 240 × 2", O_DSD_PROP, RED)], O_OVER),
              ("[SM-2025-2] CU：圍壓 75 → 150", [("實測", Q_DB, GREEN), ("比例法 40 × 2", Q_DB_PROP, RED)], (Q_DB_PROP - Q_DB)/Q_DB*100),
              ("[SM-2025-2] CD 外推：σ'_3 = 200", [("正解（相減法）", Q_DC, GREEN), ("試體一過原點外推", Q_DC_PROP_E, RED)], (Q_DC_PROP_E - Q_DC)/Q_DC*100)]
    y = 20
    for ttl, bars, over in groups:
        card(g, 20, y, 1160, 134, PANEL, "#D5DAE1", 12, 1.2)
        g.text(40, y + 34, ttl, 18, NAVY, weight="bold")
        vmax = max(b[1] for b in bars); k = 560/vmax
        for i, (lab, v, col) in enumerate(bars):
            yy = y + 54 + i*36
            g.text(40, yy + 20, lab, 15, col, weight="bold")
            g.rect(250, yy + 4, v*k, 24, fill=col, stroke="none", rx=4, op=0.85)
            g.text(258 + v*k, yy + 22, f"{v:.2f}".rstrip("0").rstrip("."), 16, col, weight="bold")
        g.text(1160, y + 90, f"高估 {over:.1f}%", 24, RED, anchor="end", weight="bold")
        y += 146
    g.save("figs/fig16_trap1.svg")


# ───────── fig17 陷阱 2：虛擬凝聚力 ─────────
def fig17():
    g = SVG(1200, 460)
    p = XY(g, 90, 410, 2.3, 0.62)
    p.axes(250, 590, "σ'_3", "σ'_1")
    g.rect(p.X(0), p.Y(580), F_SP*p.kx, 580*p.ky, fill=RED, stroke="none", op=0.06)
    g.line(p.X(F_SP), p.y0, p.X(F_SP), p.Y(580), RED, 1.6, "6 4")
    g.text(p.X(F_SP/2), p.Y(560), "σ'_c < σ'_{v0}：試體被「人造過壓密」", 15, RED, anchor="middle", weight="bold")
    p.xt(F_T1, "50"); p.xt(F_T2, "100"); p.xt(F_SP, "σ'_{v0} = 150", RED, 14, 24, "bold")
    p.yt(F_ICPT, "75", RED, 14, "bold"); p.yt(F_S1P, "450", MUTED, 14)
    p.seg(0, 0, 190, 190*F_KP, color=GREEN, sw=3.2)
    p.seg(0, F_ICPT, F_SP, F_S1P, color=RED, sw=3)
    p.seg(F_SP, F_S1P, 192, 192*F_KP, color=GREEN, sw=3.2)
    for s3, s1 in [(F_T1, F_S1T1), (F_T2, F_S1T2)]: dot(g, *p.P(s3, s1), RED, 8)
    dot(g, *p.P(F_SP, F_S1P), GOLD, 8)
    dot(g, *p.P(F_T1, F_NC_T1), GREEN, 7)
    g.arrow(p.X(F_T1) - 12, p.Y(F_NC_T1) - 6, p.X(F_T1) - 12, p.Y(F_S1T1) + 8, RED, 2, 9)
    g.text(p.X(F_T1) - 22, p.Y((F_S1T1 + F_NC_T1)/2) + 14, f"高估 {F_OVER:.0f}%", 14, RED, anchor="end", weight="bold")
    g.text(p.X(F_T2) + 12, p.Y(F_S1T2) + 26, "實驗室兩點（在 OC 段）", 14, RED, weight="bold")
    g.text(p.X(172), p.Y(172*F_KP) + 40, f"現地真 NC：c' = 0、φ' = {F_PHI:.0f}°", 15, GREEN, weight="bold")
    g.text(p.X(60), p.Y(40), f"外推截距 75 → 假 c' = {F_C:.1f}", 14, RED, weight="bold")
    g.arrow(p.X(58), p.Y(46), p.X(3), p.Y(F_ICPT) - 2, RED, 1.6, 8)
    X = 770
    card(g, X, 20, 415, 160, GOLDBG, GOLD, 12, 1.6)
    g.text(X + 20, 56, "考題訊號：同時給兩個數字", 17, GOLD, weight="bold")
    g.text(X + 20, 92, "取樣深度 z → 先算 σ'_{v0} = Σγ'h", 16, INK)
    g.text(X + 20, 126, "實驗室壓密壓力 σ'_c", 16, INK)
    g.text(X + 20, 160, "比較兩者：σ'_c < σ'_{v0} 就要警覺", 16, INK, weight="bold")
    card(g, X, 195, 415, 250, REDBG, RED, 12, 1.6)
    g.text(X + 20, 231, "為什麼偏於不安全", 17, RED, weight="bold")
    g.text(X + 20, 267, "試體「記得」現地 σ'_{v0}，壓密壓力不夠大", 15, INK)
    g.text(X + 20, 297, "→ 量到的是 OC 段：c' > 0、φ' 偏小", 15, INK)
    g.text(X + 20, 331, f"本例：K_p = {F_KPO} 與截距 75 → c' = {F_C:.1f}", 15, INK, weight="bold")
    g.text(X + 20, 365, "但現地土其實是 NC，c' = 0", 15, INK)
    g.text(X + 20, 399, f"σ'_3 = 50 時：σ'_1 = {F_S1T1:.0f} vs 真值 {F_NC_T1:.0f}", 15, RED, weight="bold")
    g.text(X + 20, 429, "（圖中數值為示意）", 14, MUTED)
    g.save("figs/fig17_fake.svg")


# ───────── fig18 陷阱 3＋雙重驗算 ─────────
def fig18():
    g = SVG(1200, 460)
    card(g, 15, 15, 620, 430, PANEL)
    g.text(35, 50, "課本式 S_u/σ'_{v0} = sin φ'/(1 + sin φ') 的天花板", 17, NAVY, weight="bold")
    p = XY(g, 85, 395, 5.3, 500.0)
    p.axes(95, 0.6, "φ'", "S_u/σ'_{v0}")
    for v in (0, 30, 60, 90): p.xt(v, f"{v}°")
    for v in (0.2, 0.35, 0.5): p.yt(v, f"{v}")
    g.rect(p.X(0), p.Y(0.35), 90*p.kx, 0.15*p.ky, fill=GREEN, stroke="none", op=0.12)
    g.text(p.X(88), p.Y(0.35) + 20, "一般 NC 黏土 0.2～0.35", 14, GREEN, anchor="end", weight="bold")
    p.seg(0, 0.5, 92, 0.5, color=RED, sw=2, dash="8 5")
    g.text(p.X(3), p.Y(0.5) - 10, "上限 0.5（φ' → 90°）", 14, RED, weight="bold")
    p.curve([(a, math.sin(R_(a))/(1 + math.sin(R_(a)))) for a in range(0, 91, 2)], color=NAVY, sw=3)
    for ph in (20, 30):
        v = math.sin(R_(ph))/(1 + math.sin(R_(ph)))
        dot(g, *p.P(ph, v), NAVY, 6); g.text(p.X(ph) + 10, p.Y(v) + 22, f"{ph}° → {v:.3f}", 14, NAVY, weight="bold")
    g.text(35, 434, "算出 > 0.5 → 必定代錯（課本式數學上到不了 0.5）", 15, RED, weight="bold")
    X = 655
    card(g, X, 15, 530, 200, GREENBG, GREEN, 12, 1.6)
    g.text(X + 20, 50, "驗算 ①：切點落在包絡線上", 17, GREEN, weight="bold")
    g.text(X + 20, 84, "R = C sin φ' + c' cos φ'（拼圖三 ② 式）", 15, INK)
    cA, rA = (Q_S1BE + Q_S3BE)/2, (Q_S1BE - Q_S3BE)/2
    g.text(X + 20, 118, f"[SM-2025-2] 試體二：C = {cA:.0f}、R = {rA:.0f}", 15, INK)
    g.text(X + 20, 152, f"{cA:.0f} × {math.sin(R_(Q_PHI)):.4f} + {Q_C:.3f} × {math.cos(R_(Q_PHI)):.4f}", 15, INK)
    g.text(X + 20, 186, f"= {cA*math.sin(R_(Q_PHI)) + Q_C*math.cos(R_(Q_PHI)):.2f} = R ✓", 17, GREEN, weight="bold")
    card(g, X, 230, 530, 215, TOTBG, "#B9C6EA", 12, 1.6)
    g.text(X + 20, 265, "驗算 ②：Skempton A_f 合不合理", 17, TOT, weight="bold")
    q = XY(g, X + 45, 365, 250.0, 1, xmin=-0.5)
    g.line(q.X(-0.5), 365, q.X(1.25), 365, INK, 2)
    g.rect(q.X(0.5), 353, 0.5*q.kx, 24, fill=GREEN, stroke="none", op=0.25)
    for v in (-0.5, 0, 0.5, 1.0):
        g.line(q.X(v), 359, q.X(v), 371, INK, 1.4); g.text(q.X(v), 393, f"{v:g}", 14, MUTED, anchor="middle")
    g.text(q.X(0.75), 343, "NC：0.5～1.0", 14, GREEN, anchor="middle", weight="bold")
    g.text(q.X(-0.25), 343, "重 OC：負值", 14, RED, anchor="middle", weight="bold")
    x = q.X(N_AF); g.poly([(x, 379), (x - 8, 395), (x + 8, 395)], EFF, 1, fill=EFF, closed=True)
    g.text(x, 414, f"{N_AF:.3f}", 14, EFF, anchor="middle", weight="bold")
    g.text(X + 20, 300, f"[SM-2018-2]：A_f = u_f / Δσ_d = 67/85 = {N_AF:.3f} ✓", 15, INK, weight="bold")
    g.text(X + 20, 436, "落在區間外 → 回頭檢查 u_f 正負號或 Δσ_d", 14, MUTED)
    g.save("figs/fig18_checks.svg")


if __name__ == "__main__":
    for f in [fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13, fig14, fig15, fig16, fig17, fig18]:
        f()
    print("figs ok")
