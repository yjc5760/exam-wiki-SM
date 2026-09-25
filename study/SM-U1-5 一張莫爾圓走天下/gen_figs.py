"""SM-U1-5 拼圖三：一張 Mohr 圓走天下 — 向量圖（所有幾何由 params.py 算出）"""
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


def specimen(g, cx, top, w, h, theta, col=RED, wrong=None, lab=True):
    """圓柱試體側視：破壞面由水平量起 θ"""
    ry = w*0.14
    g.add(f'<rect x="{cx-w/2:.1f}" y="{top:.1f}" width="{w}" height="{h}" fill="#DCE4EE" stroke="{INK}" stroke-width="2.4"/>')
    g.add(f'<ellipse cx="{cx}" cy="{top+h:.1f}" rx="{w/2}" ry="{ry:.1f}" fill="#DCE4EE" stroke="{INK}" stroke-width="2.4"/>')
    g.add(f'<rect x="{cx-w/2+1.2:.1f}" y="{top:.1f}" width="{w-2.4}" height="{h}" fill="#DCE4EE" stroke="none"/>')
    g.line(cx - w/2, top, cx - w/2, top + h, INK, 2.4); g.line(cx + w/2, top, cx + w/2, top + h, INK, 2.4)
    g.add(f'<ellipse cx="{cx}" cy="{top:.1f}" rx="{w/2}" ry="{ry:.1f}" fill="#FFFFFF" stroke="{INK}" stroke-width="2.4"/>')
    # 破壞面：從左下起跑
    x0, y0 = cx - w/2, top + h - 20
    def plane(th, c, sw, dash=None):
        L = w/math.cos(R_(th)); x1, y1 = x0 + w, y0 - w*math.tan(R_(th))
        g.line(x0, y0, x1, y1, c, sw, dash)
        return x1, y1
    if wrong is not None: plane(wrong, TOT, 2.6, "8 5")
    plane(theta, col, 4)
    g.line(x0 - 30, y0, x0 + w + 40, y0, SLATE, 1.6, "6 5")
    if lab:
        ang(g, x0, y0, 70, 0, theta, col, "θ", 88, 20)


# ───────── fig01 一張圖三件事 ─────────
def fig01():
    g = SVG(1200, 470)
    ax = Ax(g, 70, 400, 1.55)
    ax.axes(400, 215, size=20)
    ax.env(CC, PHI, 0, 395, color=EFF, sw=3)
    ax.semi(C, R, INK, 2.8, fill=TOT, op=0.08)
    cx, cy = ax.P(C, 0); tx, ty = ax.P(SF, TF)
    g.line(cx, cy, tx, ty, SLATE, 2.4, "7 5")
    dot(g, cx, cy, NAVY, 7); dot(g, tx, ty, EFF, 9)
    g.text(cx, cy + 30, "C", 22, NAVY, anchor="middle", weight="bold")
    g.text((cx + tx)/2 + 16, (cy + ty)/2 + 4, "R", 22, SLATE, weight="bold")
    g.text(tx - 16, ty - 18, "T（切點）", 19, EFF, anchor="end", weight="bold")
    g.text(ax.X(0) - 10, ax.Y(CC) + 6, "c'", 18, EFF, anchor="end", weight="bold")
    ax.tick(S3, "σ'_3"); ax.tick(S1, "σ'_1")
    g.text(ax.X(360), ax.Y(CC + 360*math.tan(R_(PHI))) - 14, "破壞包絡線", 18, EFF, anchor="end", weight="bold")
    # 右側三把鑰匙
    X = 760
    keys = [("C", "圓心 = 平均有效應力", "(σ'_1 + σ'_3) / 2", NAVY, PANEL, "#C9D3DF"),
            ("R", "半徑 = 最大剪應力", "(σ'_1 − σ'_3) / 2 = Δσ_d / 2", SLATE, TOTBG, "#B9C6EA"),
            ("T", "切點 = 破壞面上的 (σ, τ)", "圓心角 2θ = 90° + φ'", EFF, EFFBG, "#F2B8A6")]
    for i, (k, a, b, col, bg, ln) in enumerate(keys):
        y = 30 + i*140
        card(g, X, y, 420, 120, bg, ln, 12, 1.6)
        g.circle(X + 50, y + 60, 30, fill=col, stroke=W, sw=0)
        g.text(X + 50, y + 70, k, 28, W, anchor="middle", weight="bold")
        g.text(X + 100, y + 50, a, 19, col, weight="bold")
        g.text(X + 100, y + 88, b, 19, INK)
    g.save("figs/fig01_map.svg")


# ───────── fig02 應力轉換：平面轉 θ → 圓上轉 2θ ─────────
def fig02():
    g = SVG(1200, 470)
    # 左：土壤元素
    cx, cy, a = 250, 245, 180
    card(g, 20, 20, 470, 430, PANEL)
    g.text(40, 56, "試體內一個小元素", 20, NAVY, weight="bold")
    g.rect(cx - a/2, cy - a/2, a, a, fill="#DCE4EE", stroke=INK, sw=2.4)
    for dx in (-45, 0, 45):
        g.arrow(cx + dx, cy - a/2 - 60, cx + dx, cy - a/2 - 6, RED, 2.6, 11)
        g.arrow(cx + dx, cy + a/2 + 60, cx + dx, cy + a/2 + 6, RED, 2.6, 11)
    for dy in (-45, 45):
        g.arrow(cx - a/2 - 60, cy + dy, cx - a/2 - 6, cy + dy, SLATE, 2.6, 11)
        g.arrow(cx + a/2 + 60, cy + dy, cx + a/2 + 6, cy + dy, SLATE, 2.6, 11)
    g.text(cx + 62, cy - a/2 - 38, "σ_1", 20, RED, weight="bold")
    g.text(cx + a/2 + 20, cy - 58, "σ_3", 20, SLATE, weight="bold")
    # 斜切面 θ = 30°（由水平量起）
    th = TH_EX; L = a/2/math.cos(R_(th))
    x1, y1 = cx - a/2, cy + a/2*math.tan(R_(th)); x2, y2 = cx + a/2, cy - a/2*math.tan(R_(th))
    g.line(x1, y1, x2, y2, EFF, 3.6)
    g.line(x1, y1, x1 + 120, y1, MUTED, 1.4, "5 4")
    ang(g, x1, y1, 62, 0, th, EFF, "θ", 80, 19)
    # 面上的 σ、τ
    mx, my = cx, cy; nx, ny = -math.sin(R_(th)), -math.cos(R_(th))  # 法向（向左上）
    tx_, ty_ = math.cos(R_(th)), -math.sin(R_(th))
    g.arrow(mx + 70*nx, my + 70*ny, mx + 4*nx, my + 4*ny, EFF, 3, 11)
    g.arrow(mx, my, mx + 70*tx_, my + 70*ty_, GOLD, 3, 11)
    g.text(mx + 70*nx - 8, my + 70*ny - 8, "σ_θ", 18, EFF, anchor="end", weight="bold")
    g.text(mx + 70*tx_ + 6, my + 70*ty_ + 22, "τ_θ", 18, GOLD, weight="bold")
    g.text(255, 432, f"例：θ = {TH_EX:.0f}° 的斜面", 18, INK, anchor="middle", weight="bold")
    # 右：莫爾圓
    ax = Ax(g, 560, 385, 1.6)
    ax.axes(370, 170, "σ", "τ", size=20)
    ax.semi(C, R, INK, 2.8, fill=TOT, op=0.08)
    ox, oy = ax.P(C, 0); px, py = ax.P(SX_EX, TX_EX); bx, by = ax.P(S1, 0)
    g.line(ox, oy, px, py, EFF, 2.6)
    g.line(px, py, px, oy, EFF, 1.4, "5 4"); g.line(px, py, ax.X(0), py, GOLD, 1.4, "5 4")
    ang(g, ox, oy, 52, 0, 2*TH_EX, EFF, "2θ", 74, 19)
    dot(g, ox, oy, NAVY, 6); dot(g, bx, by, RED, 7); dot(g, ax.X(S3), oy, SLATE, 7); dot(g, px, py, EFF, 9)
    g.text(px + 14, py - 12, f"({SX_EX:.0f}, {TX_EX:.1f})", 17, EFF, weight="bold")
    ax.tick(S3, "σ_3 面", SLATE, 15); ax.tick(S1, "σ_1 面", RED, 15); ax.tick(C, "C", NAVY, 16, weight="bold")
    g.text(ax.X(0) - 8, py + 6, f"{TX_EX:.1f}", 14, GOLD, anchor="end", weight="bold")
    g.text(1185, 60, "圓上每一點 = 一個方向的平面", 18, NAVY, anchor="end", weight="bold")
    g.text(1185, 90, "實體轉 θ → 圓上轉 2θ", 18, EFF, anchor="end", weight="bold")
    g.save("figs/fig02_transform.svg")


# ───────── fig03 三軸加載兩階段 ─────────
def fig03():
    g = SVG(1200, 480)
    card(g, 15, 15, 400, 450, PANEL)
    g.text(35, 50, "三軸室", 20, NAVY, weight="bold")
    cx = 215
    g.rect(75, 110, 280, 290, fill=WATER, stroke=SLATE, sw=2.4, rx=8)
    g.text(340, 136, "圍壓室水", 15, WATERD, anchor="end", weight="bold")
    g.rect(cx - 12, 60, 24, 108, fill="#C0C8D2", stroke=INK, sw=2)
    g.arrow(cx, 38, cx, 72, EFF, 3, 11)
    g.text(cx + 22, 58, "Δσ_d（軸差）", 17, EFF, weight="bold")
    g.rect(cx - 62, 168, 124, 16, fill="#C0C8D2", stroke=INK, sw=2)
    g.rect(cx - 52, 184, 104, 176, fill="#DCE4EE", stroke=INK, sw=2.2)
    g.rect(cx - 62, 360, 124, 16, fill="#C0C8D2", stroke=INK, sw=2)
    g.text(cx, 278, "試體", 19, INK, anchor="middle", weight="bold")
    for yy in (215, 272, 330):
        g.arrow(88, yy, cx - 58, yy, SLATE, 2.2, 9); g.arrow(342, yy, cx + 58, yy, SLATE, 2.2, 9)
    g.text(96, 200, "σ_3", 18, SLATE, weight="bold")
    card(g, 40, 412, 350, 44, GOLDBG, GOLD, 8, 1.6)
    g.text(215, 442, "σ_1 = σ_3 + Δσ_d", 21, GOLD, anchor="middle", weight="bold")
    # 右：Mohr
    ax = Ax(g, 480, 395, 1.62)
    ax.axes(420, 205, size=20)
    ax.env(CC, PHI, 0, 415, color=EFF, sw=3)
    for i, dsd in enumerate(STAGES[1:-1]):
        ax.semi(S3 + dsd/2, dsd/2, "#9DB0C6", 2, "7 5")
        ax.tick(S3 + dsd, f"{S3+dsd:.0f}", "#8A99AB", 14)
    ax.semi(C, R, INK, 2.8, fill=TOT, op=0.08)
    dot(g, ax.X(S3), ax.y0, SLATE, 8)
    dot(g, ax.X(SF), ax.Y(TF), EFF, 9)
    g.text(ax.X(SF) - 12, ax.Y(TF) - 14, "碰到包絡線 = 破壞", 17, EFF, anchor="end", weight="bold")
    ax.tick(S3, "σ_3 = 100", SLATE, 15, weight="bold"); ax.tick(S1, "σ_1 = 340", INK, 15, weight="bold")
    g.text(ax.X(4), ax.Y(188), "階段① 各向同性圍壓 σ_3：圓縮成一點", 17, SLATE, weight="bold")
    g.text(ax.X(4), ax.Y(166), "階段② 加 Δσ_d = 80 → 160 → 240：圓往右長大", 17, INK, weight="bold")
    g.arrow(ax.X(260), ax.Y(40), ax.X(318), ax.Y(40), NAVY, 2.4, 11)
    g.save("figs/fig03_loading.svg")


# ───────── fig04 陷阱：Δσd 不是 σ1 ─────────
def fig04():
    g = SVG(1200, 460)
    ax = Ax(g, 70, 390, 1.9)
    ax.axes(400, 175, size=20)
    ax.env(CC, PHI, 0, 395, color=EFF, sw=3)
    ax.semi(C, R, GREEN, 3, fill=GREEN, op=0.10)
    ax.semi(C_WRONG, R_WRONG, RED, 2.6, "8 5", fill=RED, op=0.08)
    ax.tick(S3, "σ_3 = 100", SLATE, 15, weight="bold")
    ax.tick(S1_WRONG, "240", RED, 15, weight="bold"); ax.tick(S1, "340", GREEN, 15, weight="bold")
    dot(g, ax.X(SF), ax.Y(TF), GREEN, 8)
    g.text(ax.X(C) + 30, ax.Y(R) - 14, "正確：σ_1 = 100 + 240 = 340 → 剛好相切", 17, GREEN, weight="bold")
    g.text(ax.X(C_WRONG), ax.Y(R_WRONG) - 12, "誤把 σ_1 = 240", 16, RED, anchor="middle", weight="bold")
    # 空隙標註
    gx = ax.X(C_WRONG) - 70*math.sin(R_(PHI))*ax.k/ax.k
    g.text(ax.X(C_WRONG), ax.Y(R_WRONG) + 60, "圓太小、碰不到包絡線", 15, RED, anchor="middle", weight="bold")
    # 右側對照卡
    X = 870
    card(g, X, 30, 315, 170, GREENBG, GREEN, 12, 1.8)
    g.text(X + 20, 66, "✓ 先加回 σ_3", 19, GREEN, weight="bold")
    g.text(X + 20, 104, f"C = {C:.0f}、R = {R:.0f}", 18, INK)
    g.text(X + 20, 140, f"反推 φ' = {PHI:.2f}°", 18, INK, weight="bold")
    card(g, X, 220, 315, 170, REDBG, RED, 12, 1.8)
    g.text(X + 20, 256, "× 直接當 σ_1", 19, RED, weight="bold")
    g.text(X + 20, 294, f"C = {C_WRONG:.0f}、R = {R_WRONG:.0f}", 18, INK)
    g.text(X + 20, 330, f"反推 φ' = {PHI_TRAP:.2f}°", 18, INK, weight="bold")
    g.text(X + 20, 364, f"少了 {PHI - PHI_TRAP:.1f}°，整題全錯", 16, RED, weight="bold")
    g.save("figs/fig04_trap.svg")


# ───────── fig05 C 與 R 的物理意義 ─────────
def fig05():
    g = SVG(1200, 450)
    ax = Ax(g, 80, 380, 2.0)
    ax.axes(390, 160, size=20)
    ax.semi(C, R, INK, 2.8, fill=TOT, op=0.08)
    cx, cy = ax.P(C, 0); topx, topy = ax.P(C, R)
    g.line(cx, cy, topx, topy, SLATE, 2.6, "7 5")
    dot(g, cx, cy, NAVY, 8); dot(g, topx, topy, GOLD, 9)
    # 直徑標
    y = ax.y0 + 52
    g.arrow(ax.X(C), y, ax.X(S3) + 2, y, SLATE, 1.8, 9); g.arrow(ax.X(C), y, ax.X(S1) - 2, y, SLATE, 1.8, 9)
    g.text(ax.X((S3 + C)/2), y - 8, "R = 120", 16, SLATE, anchor="middle", weight="bold")
    g.text(ax.X((S1 + C)/2), y - 8, "R = 120", 16, SLATE, anchor="middle", weight="bold")
    ax.tick(S3, "σ'_3 = 100", SLATE, 15, weight="bold"); ax.tick(S1, "σ'_1 = 340", INK, 15, weight="bold")
    g.text(cx, cy + 26, "C = 220", 17, NAVY, anchor="middle", weight="bold")
    g.text(topx + 14, topy - 14, "τ_{max} = R = 120（θ = 45° 的面）", 17, GOLD, weight="bold")
    g.text(cx + 12, (cy + topy)/2, "R", 22, SLATE, weight="bold")
    X = 870
    card(g, X, 40, 315, 150, PANEL, "#C9D3DF", 12, 1.6)
    g.text(X + 20, 76, "C：圓的位置", 19, NAVY, weight="bold")
    g.text(X + 20, 110, "= 平均有效應力", 17, INK)
    g.text(X + 20, 142, "u 改變 → 圓左右平移", 17, MUTED)
    g.text(X + 20, 170, "（拼圖二的 CU 平移法）", 15, MUTED)
    card(g, X, 210, 315, 150, TOTBG, "#B9C6EA", 12, 1.6)
    g.text(X + 20, 246, "R：圓的大小", 19, SLATE, weight="bold")
    g.text(X + 20, 280, "= 最大剪應力 = Δσ_d / 2", 17, INK)
    g.text(X + 20, 312, "水不承剪 → u 改變不了 R", 17, MUTED)
    g.text(X + 20, 340, "UU 的 S_u 就是這個 R", 15, MUTED)
    g.save("figs/fig05_cr.svg")


# ───────── fig06 相切 → 直角三角形（公式②） ─────────
def fig06():
    g = SVG(1200, 470)
    ax = Ax(g, 190, 395, 2.2)
    ax.axes(385, 160, xmin=-75, size=20)
    O = -A0
    ax.env(CC, PHI, O - 10, 380, color=EFF, sw=3)
    ax.semi(C, R, INK, 2.6, fill=TOT, op=0.07)
    ox, oy = ax.P(O, 0); cx, cy = ax.P(C, 0); tx, ty = ax.P(SF, TF)
    g.poly([(ox, oy), (cx, cy), (tx, ty)], GREEN, 2.2, fill=GREEN, closed=True, op=0.10)
    g.line(ox, oy, cx, cy, GREEN, 4); g.line(cx, cy, tx, ty, SLATE, 3.4)
    # 直角記號
    u = (ox - tx, oy - ty); lu = math.hypot(*u); u = (u[0]/lu*14, u[1]/lu*14)
    v = (cx - tx, cy - ty); lv = math.hypot(*v); v = (v[0]/lv*14, v[1]/lv*14)
    g.poly([(tx + u[0], ty + u[1]), (tx + u[0] + v[0], ty + u[1] + v[1]), (tx + v[0], ty + v[1])], INK, 1.6)
    ang(g, ox, oy, 70, 0, PHI, EFF, "φ'", 90, 19)
    dot(g, ox, oy, EFF, 7); dot(g, cx, cy, NAVY, 7); dot(g, tx, ty, EFF, 9)
    dot(g, ax.X(0), ax.Y(CC), EFF, 6)
    g.text(ax.X(0) - 10, ax.Y(CC) - 8, "c'", 19, EFF, anchor="end", weight="bold")
    g.text(ox, oy + 30, "−c' cot φ'", 16, EFF, anchor="middle", weight="bold")
    g.text(cx, cy + 30, "C", 19, NAVY, anchor="middle", weight="bold")
    g.text(tx - 10, ty - 16, "T", 20, EFF, anchor="end", weight="bold")
    # 標註斜邊、對邊
    y = oy + 58
    g.line(ox, y - 8, ox, y + 8, GREEN, 2); g.line(cx, y - 8, cx, y + 8, GREEN, 2)
    g.arrow((ox + cx)/2, y, ox + 2, y, GREEN, 1.8, 9); g.arrow((ox + cx)/2, y, cx - 2, y, GREEN, 1.8, 9)
    g.text((ox + cx)/2, y - 8, "斜邊 = c' cot φ' + C", 17, GREEN, anchor="middle", weight="bold")
    g.text((cx + tx)/2 + 14, (cy + ty)/2 + 10, "對邊 = R", 18, SLATE, weight="bold")
    X = 930
    card(g, X, 30, 255, 250, GREENBG, GREEN, 12, 1.8)
    g.text(X + 18, 64, "圓心到切線 ⊥", 18, GREEN, weight="bold")
    g.text(X + 18, 100, "sin φ' = 對邊 / 斜邊", 17, INK)
    g.text(X + 18, 144, "R = (C + c' cot φ') sin φ'", 16, INK, weight="bold")
    g.text(X + 18, 184, "R = C sin φ' + c' cos φ'", 17, EFF, weight="bold")
    g.text(X + 18, 222, "（cot φ' · sin φ' = cos φ'）", 14, MUTED)
    g.text(X + 18, 258, "示範題：斜邊 = 50.5 + 220", 14, MUTED)
    g.save("figs/fig06_triangle.svg")


# ───────── fig07 NC 黏土：包絡線過原點 ─────────
def fig07():
    g = SVG(1200, 450)
    ax = Ax(g, 80, 385, 2.0)
    ax.axes(360, 160, size=20)
    Cn, Rn = (NC_S1 + NC_S3)/2, (NC_S1 - NC_S3)/2
    ax.env(0, NC_PHI, 0, 350, color=EFF, sw=3)
    ax.semi(Cn, Rn, INK, 2.6, fill=TOT, op=0.07)
    sf, tf = Cn - Rn*math.sin(R_(NC_PHI)), Rn*math.cos(R_(NC_PHI))
    ox, oy = ax.P(0, 0); cx, cy = ax.P(Cn, 0); tx, ty = ax.P(sf, tf)
    g.poly([(ox, oy), (cx, cy), (tx, ty)], GREEN, 2.2, fill=GREEN, closed=True, op=0.10)
    g.line(ox, oy, cx, cy, GREEN, 4); g.line(cx, cy, tx, ty, SLATE, 3.4)
    ang(g, ox, oy, 70, 0, NC_PHI, EFF, "φ'", 90, 19)
    dot(g, cx, cy, NAVY, 7); dot(g, tx, ty, EFF, 9); dot(g, ox, oy, EFF, 7)
    g.text(ox - 8, oy + 26, "O", 18, EFF, anchor="end", weight="bold")
    g.text((ox + cx)/2, oy + 58, f"斜邊 = C = {Cn:.0f}", 17, GREEN, anchor="middle", weight="bold")
    g.text((cx + tx)/2 + 14, (cy + ty)/2 + 10, f"對邊 = R = {Rn:.0f}", 17, SLATE, weight="bold")
    ax.tick(NC_S3, "σ'_3 = 100", SLATE, 14, 26); ax.tick(NC_S1, "σ'_1 = 300", INK, 14, 26)
    g.text(ax.X(250), ax.Y(250*math.tan(R_(NC_PHI))) - 16, "c' = 0：包絡線過原點", 17, EFF, anchor="end", weight="bold")
    X = 860
    card(g, X, 40, 325, 180, GREENBG, GREEN, 12, 1.8)
    g.text(X + 18, 74, "斜邊直接就是 C", 18, GREEN, weight="bold")
    g.text(X + 18, 112, "sin φ' = R / C", 19, INK, weight="bold")
    g.text(X + 18, 150, "= (σ'_1 − σ'_3)/(σ'_1 + σ'_3)", 17, INK)
    g.text(X + 18, 190, f"例：200/400 = {NC_SIN:.2f} → φ' = {NC_PHI:.0f}°", 16, EFF, weight="bold")
    card(g, X, 240, 325, 150, REDBG, RED, 12, 1.8)
    g.text(X + 18, 274, "c' ≠ 0 時不能用", 18, RED, weight="bold")
    g.text(X + 18, 310, f"示範題硬套：R/C = 120/220", 16, INK)
    g.text(X + 18, 342, f"→ {PHI_NC_WRONG:.1f}°（真值 {PHI:.2f}°）", 16, INK, weight="bold")
    g.text(X + 18, 372, "斜邊少算了 c' cot φ'", 15, MUTED)
    g.save("figs/fig07_nc.svg")


# ───────── fig08 選式流程圖 ─────────
def fig08():
    g = SVG(1200, 470)
    def diamond(cx, cy, w, h, t, col=NAVY):
        g.poly([(cx, cy - h/2), (cx + w/2, cy), (cx, cy + h/2), (cx - w/2, cy)], col, 2.2, fill=W, closed=True)
        g.text(cx, cy + 6, t, 17, col, anchor="middle", weight="bold")
    def box(x, y, w, h, t1, t2, col, bg):
        card(g, x, y, w, h, bg, col, 10, 2)
        g.text(x + w/2, y + 32, t1, 18, col, anchor="middle", weight="bold")
        g.text(x + w/2, y + 62, t2, 16, INK, anchor="middle")
    card(g, 40, 30, 200, 56, NAVY, NAVY, 10)
    g.text(140, 65, "先算 C、R", 20, W, anchor="middle", weight="bold")
    g.arrow(240, 58, 300, 58, INK, 2.2, 10)
    ys = [58, 188, 318]
    qs = ["c' = 0？（NC、砂）", "已知 φ'，求 c'？", "已知 c'，求 φ'？"]
    outs = [("③ 正弦式", "sin φ' = R / C", GREEN, GREENBG),
            ("② 幾何式移項", "c' = (R − C sin φ') / cos φ'", SLATE, TOTBG),
            ("① 萬能式", "令 y = √K_p 解一元二次式", EFF, EFFBG)]
    for i, (q, (t1, t2, col, bg)) in enumerate(zip(qs, outs)):
        cy = ys[i]
        diamond(420, cy, 240, 92, q)
        g.arrow(540, cy, 640, cy, INK, 2.2, 10); g.text(590, cy - 10, "是", 16, GREEN, anchor="middle", weight="bold")
        box(640, cy - 42, 330, 84, t1, t2, col, bg)
        if i < 2:
            g.arrow(420, cy + 46, 420, ys[i + 1] - 46, INK, 2.2, 10)
            g.text(432, (cy + ys[i + 1])/2 + 6, "否", 16, RED, weight="bold")
    g.arrow(420, 364, 420, 400, INK, 2.2, 10)
    g.text(432, 390, "否", 16, RED, weight="bold")
    box(270, 400, 300, 62, "兩組試驗：① 相減", "", GOLD, GOLDBG)
    g.text(420, 452, "K_p = Δσ'_1 / Δσ'_3，再回代求 c'", 15, INK, anchor="middle")
    # 右側：驗算
    card(g, 1000, 60, 185, 360, NAVY, NAVY, 12)
    g.text(1092, 106, "最後一律", 18, "#F2A65A", anchor="middle", weight="bold")
    g.text(1092, 146, "用 ② 驗算", 22, W, anchor="middle", weight="bold")
    for k, t in enumerate(["C sin φ'", "+ c' cos φ'", "是否 = R？", "", "差 < 0.1 kPa", "才交卷"]):
        g.text(1092, 196 + k*34, t, 17, "#C9D3DF", anchor="middle")
    for cy in ys:
        g.arrow(972, cy, 998, cy, "#9AA3AE", 1.8, 8)
    g.save("figs/fig08_flow.svg")


# ───────── fig09 破壞面角度：實體 θ ↔ 圓上 2θ ─────────
def fig09():
    g = SVG(1200, 470)
    card(g, 15, 15, 400, 440, PANEL)
    g.text(35, 50, "試體上的破壞面", 20, NAVY, weight="bold")
    specimen(g, 215, 120, 160, 250, TH)
    g.arrow(215, 64, 215, 104, RED, 3, 11); g.text(232, 86, "σ'_1", 19, RED, weight="bold")
    g.arrow(58, 250, 128, 250, SLATE, 3, 11); g.text(50, 238, "σ'_3", 19, SLATE, weight="bold")
    g.text(215, 430, f"θ = {TH:.2f}°（由水平面量起）", 18, RED, anchor="middle", weight="bold")
    ax = Ax(g, 490, 395, 1.7)
    ax.axes(385, 170, size=20)
    ax.env(CC, PHI, 0, 380, color=EFF, sw=3)
    ax.semi(C, R, INK, 2.6, fill=TOT, op=0.07)
    cx, cy = ax.P(C, 0); tx, ty = ax.P(SF, TF)
    g.line(cx, cy, tx, ty, SLATE, 2.6, "7 5"); g.line(cx, cy, ax.X(S1), cy, SLATE, 2.6, "7 5")
    ang(g, cx, cy, 62, 0, 2*TH, RED, f"2θ = {2*TH:.2f}°", 96, 18, 2.4)
    dot(g, cx, cy, NAVY, 7); dot(g, tx, ty, EFF, 9); dot(g, ax.X(S1), cy, RED, 7)
    g.text(tx - 12, ty - 16, "T 破壞面", 18, EFF, anchor="end", weight="bold")
    ax.tick(S3, "σ'_3", SLATE, 16); ax.tick(S1, "σ'_1 面", RED, 15); ax.tick(C, "C", NAVY, 16)
    g.text(525, 40, "① 半徑 ⊥ 切線 → 2θ = 90° + φ'", 18, NAVY, weight="bold")
    g.text(525, 72, "② 圓上角 = 2 × 實體角 → θ = 45° + φ'/2", 18, RED, weight="bold")
    g.save("figs/fig09_angle.svg")


# ───────── fig10 切點座標：σff、τff ─────────
def fig10():
    g = SVG(1200, 490)
    ax = Ax(g, 80, 400, 2.2)
    ax.axes(370, 160, size=20)
    ax.env(CC, PHI, 0, 360, color=EFF, sw=3)
    ax.semi(C, R, INK, 2.6, fill=TOT, op=0.07)
    cx, cy = ax.P(C, 0); tx, ty = ax.P(SF, TF); fx = ax.X(SF)
    g.line(cx, cy, tx, ty, SLATE, 3)
    g.line(cx, cy, cx, ax.Y(R + 12), MUTED, 1.4, "5 4")
    g.line(tx, ty, fx, cy, GOLD, 3)                      # τff
    g.line(fx, cy, cx, cy, GREEN, 4)                     # R sinφ
    ang(g, cx, cy, 58, 90, 90 + PHI, EFF, "φ'", 78, 19)
    dot(g, cx, cy, NAVY, 7); dot(g, tx, ty, EFF, 9); dot(g, fx, cy, GOLD, 6)
    g.text(tx - 12, ty - 14, f"T ({SF:.2f}, {TF:.2f})", 18, EFF, anchor="end", weight="bold")
    g.text(fx - 10, (ty + cy)/2 + 10, f"τ_{{ff}} = R cos φ' = {TF:.2f}", 17, GOLD, anchor="end", weight="bold")
    g.text((fx + cx)/2, cy + 28, f"R sin φ' = {R*math.sin(R_(PHI)):.2f}", 15, GREEN, anchor="middle", weight="bold")
    g.text(fx, cy + 62, f"σ'_{{ff}} = C − R sin φ' = {SF:.2f}", 17, EFF, anchor="middle", weight="bold")
    g.line(cx, cy, cx, cy + 6, INK, 1.5); g.text(cx + 10, cy + 28, "C = 220", 15, NAVY, weight="bold")
    g.text((cx + tx)/2 + 14, (cy + ty)/2 - 4, "R = 120", 17, SLATE, weight="bold")
    X = 900
    card(g, X, 40, 285, 200, PANEL, "#C9D3DF", 12, 1.6)
    g.text(X + 18, 74, "為什麼是 sin、cos？", 18, NAVY, weight="bold")
    g.text(X + 18, 110, "半徑與鉛垂線夾角 = φ'", 16, INK)
    g.text(X + 18, 140, "（2θ − 90° = φ'）", 16, MUTED)
    g.text(X + 18, 176, "水平分量 R sin φ' 往左", 16, INK)
    g.text(X + 18, 206, "鉛垂分量 R cos φ' 往上", 16, INK)
    card(g, X, 260, 285, 130, GOLDBG, GOLD, 12, 1.6)
    g.text(X + 18, 294, "另一種寫法（同答案）", 17, GOLD, weight="bold")
    g.text(X + 18, 330, "σ = C + R cos 2θ", 17, INK)
    g.text(X + 18, 362, "τ = R sin 2θ", 17, INK)
    g.save("figs/fig10_point.svg")


# ───────── fig11 黃金鐵律：只用 φ' ─────────
def fig11():
    g = SVG(1200, 470)
    card(g, 15, 15, 360, 440, PANEL)
    g.text(35, 50, "同一個試體，只有一個破壞面", 18, NAVY, weight="bold")
    specimen(g, 195, 110, 150, 260, TH_A, wrong=TH_WRONG_A, lab=False)
    x0, y0 = 120, 110 + 260 - 20
    ang(g, x0, y0, 64, 0, TH_A, RED, "", 0)
    ang(g, x0, y0, 96, 0, TH_WRONG_A, TOT, "", 0)
    g.text(35, 420, f"✓ θ = 45° + φ'/2 = {TH_A:.0f}°", 17, RED, weight="bold")
    g.text(35, 446, f"× 用 φ_{{cu}}：{TH_WRONG_A:.1f}°（低估 {TH_A-TH_WRONG_A:.1f}°）", 17, TOT, weight="bold")
    ax = Ax(g, 440, 395, 3.2)
    ax.axes(215, 115, "σ", "τ", size=20)
    Ce, Ct, Rr = 80.0, 140.0, 40.0
    ax.env(0, PHI_A, 0, 185, color=EFF, sw=3)
    ax.env(0, PHI_CU_A, 0, 215, color=TOT, sw=2.4, dash="8 5")
    ax.semi(Ct, Rr, TOT, 2.4, "8 5")
    ax.semi(Ce, Rr, EFF, 2.8, fill=EFF, op=0.12)
    for Cc, ph, col in [(Ce, PHI_A, EFF), (Ct, PHI_CU_A, TOT)]:
        px, py = ax.P(Cc - Rr*math.sin(R_(ph)), Rr*math.cos(R_(ph))); cx, cy = ax.P(Cc, 0)
        g.line(cx, cy, px, py, col, 2, "5 4"); dot(g, px, py, col, 8)
    ax.tick(40, "40", EFF, 14); ax.tick(120, "120", EFF, 14); ax.tick(100, "100", TOT, 14, 46); ax.tick(180, "180", TOT, 14, 46)
    g.text(ax.X(125) - 12, ax.Y(125*math.tan(R_(PHI_A))), "φ' = 30°（有效）", 17, EFF, anchor="end", weight="bold")
    g.text(ax.X(212), ax.Y(212*math.tan(R_(PHI_CU_A))) - 12, f"φ_{{cu}} = {PHI_CU_A:.1f}°（總）", 17, TOT, anchor="end", weight="bold")
    g.text(1185, 40, "拼圖二 黏土 A（CU，u_f = 60）", 16, MUTED, anchor="end", weight="bold")
    g.save("figs/fig11_rule.svg")


# ───────── fig12 示範題 Step 1：建主應力與 C、R ─────────
def fig12():
    g = SVG(1200, 400)
    k = 2.5; x0 = 70; y = 190
    X = lambda v: x0 + v*k
    g.arrow(X(0), y, X(400), y, INK, 2, 10)
    g.text(X(400) + 8, y + 7, "σ'（kPa）", 18, INK, weight="bold")
    for v in range(0, 401, 50):
        g.line(X(v), y, X(v), y + 6, INK, 1.4); g.text(X(v), y + 28, f"{v}", 14, MUTED, anchor="middle")
    g.rect(X(0), y - 70, S3*k, 40, fill=SLATE, stroke="none", op=0.85)
    g.text(X(S3/2), y - 43, "σ'_3 = 100（圍壓）", 17, W, anchor="middle", weight="bold")
    g.rect(X(S3), y - 70, DSD*k, 40, fill=EFF, stroke="none", op=0.9)
    g.text(X(S3 + DSD/2), y - 43, "+ Δσ_d = 240（軸差，活塞額外推）", 17, W, anchor="middle", weight="bold")
    g.line(X(S1), y - 90, X(S1), y + 6, INK, 2.4)
    g.text(X(S1), y - 100, "σ'_1 = 340", 19, INK, anchor="middle", weight="bold")
    # C、R
    yy = y + 80
    g.line(X(S3), yy - 10, X(S3), yy + 10, SLATE, 2); g.line(X(S1), yy - 10, X(S1), yy + 10, SLATE, 2)
    g.arrow(X(C), yy, X(S3) + 2, yy, SLATE, 2, 10); g.arrow(X(C), yy, X(S1) - 2, yy, SLATE, 2, 10)
    dot(g, X(C), yy, NAVY, 8)
    g.text(X((S3 + C)/2), yy - 12, "R = 120", 17, SLATE, anchor="middle", weight="bold")
    g.text(X((S1 + C)/2), yy - 12, "R = 120", 17, SLATE, anchor="middle", weight="bold")
    g.text(X(C), yy + 34, "C = (340 + 100)/2 = 220", 18, NAVY, anchor="middle", weight="bold")
    card(g, 40, 330, 1140, 56, GOLDBG, GOLD, 10, 1.6)
    g.text(610, 366, "CD 試驗 u = 0：總應力 = 有效應力，這個圓直接就是有效應力圓", 18, GOLD, anchor="middle", weight="bold")
    g.save("figs/fig12_setup.svg")


# ───────── fig13 Step 2：保留 y = √Kp 的計算鏈 ─────────
def fig13():
    g = SVG(1200, 470)
    # 左：拋物線
    card(g, 15, 15, 380, 440, PANEL)
    g.text(35, 50, "f(y) = 10y² + 5y − 34", 18, NAVY, weight="bold")
    ox, oy, kx, ky = 205, 250, 58, 3.6
    g.arrow(35, oy, 380, oy, INK, 1.8, 9); g.arrow(ox, 420, ox, 80, INK, 1.8, 9)
    g.text(372, oy + 26, "y", 17, INK, weight="bold")
    pts = [(ox + t*kx, oy - (10*t*t + 5*t - 34)*ky) for t in [i/50 for i in range(-150, 116)]]
    pts = [p for p in pts if 80 < p[1] < 430]
    g.poly(pts, SLATE, 2.8)
    dot(g, ox + Y*kx, oy, EFF, 8); dot(g, ox + Y_NEG*kx, oy, "#9AA3AE", 7)
    g.text(ox + Y*kx + 6, oy + 30, f"{Y:.4f}", 16, EFF, weight="bold")
    g.text(ox + Y_NEG*kx - 8, oy + 24, "−2.11", 15, MUTED, anchor="end")
    g.text(35, 414, "y = (−5 + √1385)/20 = 1.6108", 16, INK, weight="bold")
    g.text(35, 442, f"另一根 {Y_NEG:.4f} < 0：√ 不可為負 → 捨", 15, MUTED)
    # 右：計算鏈
    def node(x, y, w, t1, t2, col, bg):
        card(g, x, y, w, 84, bg, col, 10, 2)
        g.text(x + w/2, y + 34, t1, 18, col, anchor="middle", weight="bold")
        g.text(x + w/2, y + 64, t2, 17, INK, anchor="middle")
    node(430, 40, 250, "y = √K_p", f"= {Y:.4f}（保留！）", EFF, EFFBG)
    node(740, 40, 440, "θ = arctan y = 45° + φ'/2", f"= {TH:.2f}°（破壞面角直接到手）", RED, REDBG)
    node(740, 160, 440, "φ' = 2θ − 90°", f"= {PHI:.2f}°", GREEN, GREENBG)
    node(430, 160, 250, "K_p = y²", f"= {KP:.4f}", SLATE, TOTBG)
    g.arrow(680, 82, 738, 82, INK, 2.4, 11); g.arrow(960, 124, 960, 158, INK, 2.4, 11)
    g.arrow(555, 124, 555, 158, INK, 2.4, 11)
    card(g, 430, 280, 750, 175, W, "#C9D3DF", 12, 1.6)
    g.text(450, 314, "對照：先把 φ' 四捨五入成 26° 再轉回 K_p", 18, MUTED, weight="bold")
    g.text(450, 350, f"K_p = tan²(58°) = {KP_RND:.4f}（真值 {KP:.4f}）", 17, INK)
    g.text(450, 384, f"回代 σ'_1 = {S1_RND:.1f} kPa（真值 {S1:.0f}，差 {S1 - S1_RND:.1f}）", 17, INK)
    g.text(450, 420, f"→ 誤差 {(S1 - S1_RND)/S1*100:.1f}%，後面每一步都繼承這個誤差", 17, RED, weight="bold")
    g.save("figs/fig13_chain.svg")


# ───────── fig14 示範題全圖（按比例） ─────────
def fig14():
    g = SVG(1200, 480)
    ax = Ax(g, 90, 410, 2.2)
    ax.axes(385, 165, size=20)
    ax.env(CC, PHI, 0, 380, color=EFF, sw=3)
    ax.semi(C, R, INK, 2.8, fill=TOT, op=0.08)
    cx, cy = ax.P(C, 0); tx, ty = ax.P(SF, TF)
    g.line(cx, cy, tx, ty, SLATE, 2.6, "7 5"); g.line(cx, cy, ax.X(S1), cy, SLATE, 1.8, "7 5")
    g.line(tx, ty, tx, cy, GOLD, 1.8, "5 4"); g.line(tx, ty, ax.X(0), ty, GOLD, 1.8, "5 4")
    ang(g, cx, cy, 56, 0, 2*TH, RED, f"2θ = {2*TH:.2f}°", 90, 17, 2.4)
    # φ' 角：畫在包絡線上的水平參考
    bx, by = ax.P(20, CC + 20*math.tan(R_(PHI)))
    g.line(ax.X(0), ax.Y(CC), ax.X(95), ax.Y(CC), EFF, 1.3, "4 4")
    ang(g, ax.X(0), ax.Y(CC), 150, 0, PHI, EFF, f"φ' = {PHI:.2f}°", 190, 16)
    dot(g, cx, cy, NAVY, 7); dot(g, tx, ty, EFF, 10); dot(g, ax.X(0), ax.Y(CC), EFF, 6)
    g.text(ax.X(0) - 10, ax.Y(CC) + 6, "c' = 25", 16, EFF, anchor="end", weight="bold")
    g.text(ax.X(0) - 10, ty + 6, f"{TF:.2f}", 15, GOLD, anchor="end", weight="bold")
    g.text(tx - 14, ty - 18, "T 破壞面", 18, EFF, anchor="end", weight="bold")
    ax.tick(S3, "100", SLATE, 15, weight="bold"); ax.tick(SF, f"{SF:.2f}", GOLD, 15, 48, "bold")
    ax.tick(C, "C = 220", NAVY, 15, weight="bold"); ax.tick(S1, "340", INK, 15, weight="bold")
    X = 975
    card(g, X, 30, 210, 260, PANEL, "#C9D3DF", 12, 1.6)
    rows = [("σ'_1", "340"), ("C", "220"), ("R", "120"), ("√K_p", f"{Y:.4f}"), ("φ'", f"{PHI:.2f}°"), ("θ", f"{TH:.2f}°")]
    for i, (a, b) in enumerate(rows):
        g.text(X + 20, 66 + i*38, a, 17, MUTED, weight="bold"); g.text(X + 190, 66 + i*38, b, 17, INK, anchor="end", weight="bold")
    card(g, X, 305, 210, 110, EFFBG, "#F2B8A6", 12, 1.6)
    g.text(X + 20, 340, "σ'_{ff}", 17, EFF, weight="bold"); g.text(X + 190, 340, f"{SF:.2f}", 17, INK, anchor="end", weight="bold")
    g.text(X + 20, 382, "τ_{ff}", 17, EFF, weight="bold"); g.text(X + 190, 382, f"{TF:.2f}", 17, INK, anchor="end", weight="bold")
    g.save("figs/fig14_full.svg")


if __name__ == "__main__":
    for f in [fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13, fig14]:
        f()
    print("figs ok")
