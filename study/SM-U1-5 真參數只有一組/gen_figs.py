"""SM-U1-5 拼圖一：真參數只有一組 — 向量圖（所有幾何由 params.py 算出）"""
import math, random
from svglib import SVG, measure, INK, MUTED, GRID, PANEL
from params import *
R_ = math.radians

EFF, TOT, UU, CDC, RED, NAVY = "#E4572E", "#2F54C8", "#8A94A3", "#2E7D6B", "#C0392B", "#1B2432"
EFFBG, TOTBG, OKBG, REDBG, GOLD, GOLDBG = "#FDEDE8", "#EEF2FB", "#E6F2EF", "#FBECEA", "#B7791F", "#FBF3E4"
WATER = "#D9ECF7"


class Ax:
    """等比例座標（Mohr 圓不可變形）；x0,y0 為原點像素位置"""
    def __init__(s, g, x0, y0, k, ky=None):
        s.g, s.x0, s.y0, s.k, s.ky = g, x0, y0, k, ky or k
    def X(s, v): return s.x0 + v*s.k
    def Y(s, v): return s.y0 - v*s.ky
    def P(s, a, b): return (s.X(a), s.Y(b))
    def axes(s, xmax, ymax, xl="σ", yl="τ", xmin=0):
        g = s.g
        g.arrow(s.X(xmin), s.y0, s.X(xmax), s.y0, INK, 2, 10)
        g.arrow(s.x0, s.y0, s.x0, s.Y(ymax), INK, 2, 10)
        g.text(s.X(xmax) + 8, s.y0 + 6, xl, 20, INK, weight="bold")
        g.text(s.x0 - 8, s.Y(ymax) - 6, yl, 20, INK, anchor="end", weight="bold")
    def line(s, a, b, c, d, **kw): s.g.line(s.X(a), s.Y(b), s.X(c), s.Y(d), **kw)
    def semi(s, C, R, color, sw=2.4, dash=None, fill=None, op=0.12):
        x1, x2, y = s.X(C - R), s.X(C + R), s.y0; rr = R*s.k
        d = f' stroke-dasharray="{dash}"' if dash else ''
        f = f'fill="{fill}" fill-opacity="{op}"' if fill else 'fill="none"'
        s.g.add(f'<path d="M{x1:.1f},{y:.1f} A{rr:.1f},{rr:.1f} 0 0 1 {x2:.1f},{y:.1f}" {f} stroke="{color}" stroke-width="{sw}"{d}/>')
    def tick(s, v, lab, color=MUTED, size=15):
        s.g.line(s.X(v), s.y0, s.X(v), s.y0 + 6, INK, 1.5)
        s.g.text(s.X(v), s.y0 + 24, lab, size, color, anchor="middle")


def card(g, x, y, w, h, fill=PANEL, stroke="#D5DAE1", rx=12, sw=1.2):
    g.rect(x, y, w, h, fill=fill, stroke=stroke, sw=sw, rx=rx)


def dot(g, x, y, c, r=7): g.circle(x, y, r, fill=c, stroke="#FFFFFF", sw=2)


# ───────── fig01 表觀角度無限多、真參數只有一組 ─────────
def fig01():
    g = SVG(1200, 470)
    tests = [("CD 排水", "u = 0（閥門開）", f"φ_d = {PHI_A:.0f}°", CDC, OKBG),
             ("CU 軸壓（AC）", f"u_f = +{UF_AC:.0f} kPa", f"φ_{{cu}} = {PHI_CU_AC:.1f}°", TOT, TOTBG),
             ("CU 側向伸張（LE）", f"u_f = −{-UF_LE:.0f} kPa", f"φ_{{cu}} = {PHI_CU_LE:.1f}°", "#6D4BC2", "#F1EDFA"),
             ("UU 不排水", "u 隨圍壓等量上升", "φ_u = 0°", UU, "#F1F3F6")]
    g.text(30, 36, "試驗條件（同一塊示範黏土 A）", 19, MUTED, weight="bold")
    for i, (a, b, c, col, bg) in enumerate(tests):
        y = 58 + i*100
        card(g, 30, y, 330, 82, bg, col, 10, 1.6)
        g.text(50, y + 32, a, 20, col, weight="bold")
        g.text(50, y + 62, b, 16, INK)
        g.text(345, y + 50, c, 22, col, anchor="end", weight="bold")
        g.arrow(362, y + 41, 560, 235, col, 2.2, 12)
    # 濾網：扣 u
    card(g, 565, 150, 160, 170, NAVY, NAVY, 14)
    g.text(645, 205, "扣掉 u", 24, "#FFFFFF", anchor="middle", weight="bold")
    g.text(645, 245, "σ' = σ − u", 22, "#F2A65A", anchor="middle", weight="bold")
    g.text(645, 285, "只看骨架", 17, "#C9D3DF", anchor="middle")
    g.arrow(727, 235, 800, 235, EFF, 4, 18)
    card(g, 805, 110, 365, 250, EFFBG, EFF, 14, 2.4)
    g.text(987, 155, "唯一的真參數", 22, EFF, anchor="middle", weight="bold")
    g.text(987, 215, f"c' = 0　φ' = {PHI_A:.0f}°", 34, INK, anchor="middle", weight="bold")
    g.text(987, 262, "τ_f = c' + σ' tan φ'", 22, INK, anchor="middle")
    g.text(987, 305, "四種試驗的有效應力莫爾圓", 16, MUTED, anchor="middle")
    g.text(987, 330, "全部切在同一條線上", 16, MUTED, anchor="middle")
    g.text(987, 420, "左邊四個角度 = 試驗的產物　右邊一組 = 土的性質", 19, INK, anchor="middle", weight="bold")
    g.save("figs/fig01_map.svg")


# ───────── fig02 微觀：水不承剪 ─────────
def fig02():
    g = SVG(1200, 500)
    # 左：顆粒骨架
    bx, by, bw, bh = 30, 30, 640, 440
    g.rect(bx, by, bw, bh, fill=WATER, stroke="#A9CBE3", sw=1.5, rx=14)
    random.seed(7); P = []
    tries = 0
    while len(P) < 17 and tries < 5000:
        tries += 1
        rr = random.uniform(40, 62)
        x = random.uniform(bx + rr + 10, bx + bw - rr - 10); y = random.uniform(by + rr + 44, by + bh - rr - 12)
        if all(math.hypot(x - a, y - b) > rr + c - 3 for a, b, c in P) and all(math.hypot(x - a, y - b) > rr + c + 2 or math.hypot(x - a, y - b) < rr + c - 3 for a, b, c in P):
            P.append((x, y, rr))
    # 接觸點：距離接近 r1+r2 的對
    for x, y, rr in P:
        g.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr:.1f}" fill="#E7ECF2" stroke="{INK}" stroke-width="2"/>')
        g.add(f'<circle cx="{x - rr*0.35:.1f}" cy="{y - rr*0.35:.1f}" r="{rr*0.14:.1f}" fill="#FFFFFF"/>')
    cnt = 0
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            (x1, y1, r1), (x2, y2, r2) = P[i], P[j]
            dd = math.hypot(x2 - x1, y2 - y1)
            if dd < r1 + r2 + 14:
                ux, uy = (x2 - x1)/dd, (y2 - y1)/dd
                cx, cy = x1 + ux*r1, y1 + uy*r1
                g.line(cx - ux*16, cy - uy*16, cx + ux*16, cy + uy*16, EFF, 6, cap="round"); cnt += 1
    g.text(bx + 18, by + 32, "骨架：接觸點正向力 N → 摩擦 T ≤ N tan φ'", 18, EFF, weight="bold", bg="#FFFFFF")
    g.text(bx + bw - 16, by + bh - 14, "孔隙水：只承壓、不承剪", 16, "#2C6E9E", anchor="end", weight="bold", bg="#FFFFFF")
    # 右：兩個小元素
    def elem(x, y, title, water):
        s = 120
        g.text(x + s/2, y - 60, title, 19, INK if not water else "#2C6E9E", anchor="middle", weight="bold")
        g.rect(x, y, s, s, fill=WATER if water else "#E7ECF2", stroke=INK, sw=2)
        L = 38
        for (x1, y1, x2, y2) in [(x + s/2, y - L - 4, x + s/2, y - 4), (x + s/2, y + s + L + 4, x + s/2, y + s + 4),
                                 (x - L - 4, y + s/2, x - 4, y + s/2), (x + s + L + 4, y + s/2, x + s + 4, y + s/2)]:
            g.arrow(x1, y1, x2, y2, "#2C6E9E" if water else INK, 2.4, 10)
        if water:
            g.text(x + s/2, y + s/2 + 8, "u", 26, "#2C6E9E", anchor="middle", weight="bold")
            g.text(x + s/2, y + s + 78, "四面等壓、τ ≡ 0", 17, "#2C6E9E", anchor="middle", weight="bold")
        else:
            for (x1, y1, x2, y2) in [(x + 10, y - 10, x + s - 10, y - 10), (x + s - 10, y + s + 10, x + 10, y + s + 10),
                                     (x + s + 10, y + s - 10, x + s + 10, y + 12), (x - 10, y + 12, x - 10, y + s - 10)]:
                g.arrow(x1, y1, x2, y2, RED, 2.6, 10)
            g.text(x + s/2, y + s/2 + 8, "σ'", 26, INK, anchor="middle", weight="bold")
            g.text(x + s/2, y + s + 78, "剪力 τ 全部由骨架扛", 17, RED, anchor="middle", weight="bold")
    elem(740, 150, "水", True)
    elem(1010, 150, "骨架", False)
    g.text(950, 470, "σ = σ' + u　→　能改變 τ_f 的只有 σ'", 20, INK, anchor="middle", weight="bold")
    g.save("figs/fig02_micro.svg")


# ───────── fig03 示範黏土 A：三條包絡線 ─────────
def fig03():
    g = SVG(1200, 520)
    ax = Ax(g, 80, 470, 2.2)
    ax.axes(460, 185, "σ, σ' (kPa)", "τ")
    # 圓
    ax.semi((S1_CD + S3)/2, DSD_CD/2, CDC, 2.4, fill=CDC, op=0.06)
    ax.semi((S1E_AC + S3E_AC)/2, DSD_AC/2, EFF, 2.6, fill=EFF, op=0.10)
    ax.semi((S1_AC + S3)/2, DSD_AC/2, TOT, 2.2, "8 6")
    ax.semi((S1_AC + S3 + 200)/2, DSD_AC/2, UU, 2.0, "8 6")
    # 線
    t = math.tan(R_(PHI_A)); ax.line(0, 0, 300, 300*t, color=EFF, sw=3.4)
    tc = math.tan(R_(PHI_CU_AC)); ax.line(0, 0, 460, 460*tc, color=TOT, sw=2.4, dash="10 7")
    ax.line(0, SU, 460, SU, color=UU, sw=2.4, dash="10 7")
    for v in [S3E_AC, S3, S1E_AC, S1_AC, S1_CD]:
        ax.tick(v, f"{v:.0f}")
    g.text(ax.X(300) + 10, ax.Y(300*t) + 8, f"有效包絡線 φ' = {PHI_A:.0f}°（真）", 19, EFF, anchor="end", weight="bold", bg="#FFFFFF")
    g.text(ax.X(460), ax.Y(460*tc) - 12, f"CU 總應力 φ_{{cu}} = {PHI_CU_AC:.1f}°", 17, TOT, anchor="end", weight="bold", bg="#FFFFFF")
    g.text(ax.X(460), ax.Y(SU) + 24, f"UU：φ_u = 0、s_u = {SU:.0f} kPa", 17, "#5B6573", anchor="end", weight="bold", bg="#FFFFFF")
    g.text(ax.X(200), ax.Y(DSD_CD/2) - 12, "CD 圓（σ'_3 = 100）", 15, CDC, anchor="middle", weight="bold", bg="#FFFFFF")
    g.text(ax.X(80), ax.Y(DSD_AC/2) - 38, "CU 有效圓", 15, EFF, anchor="middle", weight="bold", bg="#FFFFFF")
    g.text(ax.X(140) + 8, ax.Y(DSD_AC/2) - 12, "CU 總應力圓", 15, TOT, anchor="start", weight="bold", bg="#FFFFFF")
    g.text(ax.X(240), ax.Y(DSD_AC/2) + 34, "UU 換圍壓（σ_3 = 200）：圓一樣大", 15, "#5B6573", anchor="middle", bg="#FFFFFF")
    # 右側說明
    card(g, 110, 20, 290, 230, PANEL)
    g.text(130, 55, "示範黏土 A（NC）", 19, INK, weight="bold")
    for i, s in enumerate([f"p'_0 = σ_3 = {S3:.0f} kPa", f"φ' = {PHI_A:.0f}°、c' = 0", f"A_f = {AF}",
                           f"CD：Δσ_d = {DSD_CD:.0f}", f"CU：Δσ_d = {DSD_AC:.0f}、u_f = {UF_AC:.0f}", f"UU：s_u = {SU:.0f}"]):
        g.text(130, 90 + i*28, s, 17, INK)
    g.save("figs/fig03_envelopes.svg")


# ───────── fig04 同一個有效圓，u 讓總應力圓左右平移 ─────────
def fig04():
    g = SVG(1200, 500)
    ax = Ax(g, 70, 420, 4.3)
    ax.axes(215, 82, "σ, σ' (kPa)", "τ")
    Ce, R = (S1E_AC + S3E_AC)/2, DSD_AC/2
    Cac, Cle = (S1_AC + S3)/2, (S1_LE + S3_LE)/2
    ax.semi(Cle, R, "#6D4BC2", 2.2, "8 6")
    ax.semi(Cac, R, TOT, 2.2, "8 6")
    ax.semi(Ce, R, EFF, 3.0, fill=EFF, op=0.12)
    ax.line(0, 0, 150, 150*math.tan(R_(PHI_A)), color=EFF, sw=3.2)
    ax.line(0, 0, 215, 215*math.tan(R_(PHI_CU_AC)), color=TOT, sw=2.2, dash="10 7")
    ax.line(0, 0, 88, 88*math.tan(R_(PHI_CU_LE)), color="#6D4BC2", sw=2.2, dash="10 7")
    for v in [S3_LE, S3E_AC, S1_LE, S1E_AC, S1_AC]:
        ax.tick(v, f"{v:.0f}")
    ax.tick(S3, "100")
    # 平移箭頭（畫在圓頂高度）
    yT = ax.Y(R) - 16
    g.arrow(ax.X(Cac), yT, ax.X(Ce) + 6, yT, TOT, 2.6, 12)
    g.text((ax.X(Cac) + ax.X(Ce))/2, yT - 10, f"扣 u_f = +{UF_AC:.0f}", 17, TOT, anchor="middle", weight="bold", bg="#FFFFFF")
    yL = ax.Y(R) - 58
    g.arrow(ax.X(Cle), yL, ax.X(Ce) - 6, yL, "#6D4BC2", 2.6, 12)
    g.text((ax.X(Cle) + ax.X(Ce))/2 - 20, yL - 10, f"扣 u_f = −{-UF_LE:.0f}", 17, "#6D4BC2", anchor="middle", weight="bold", bg="#FFFFFF")
    g.text(ax.X(150) + 6, ax.Y(150*math.tan(R_(PHI_A))) + 4, f"φ' = {PHI_A:.0f}°", 19, EFF, weight="bold", bg="#FFFFFF")
    g.text(ax.X(215) - 4, ax.Y(215*math.tan(R_(PHI_CU_AC))) - 12, f"AC：φ_{{cu}} = {PHI_CU_AC:.1f}°", 17, TOT, anchor="end", weight="bold", bg="#FFFFFF")
    g.text(ax.X(88) + 8, ax.Y(88*math.tan(R_(PHI_CU_LE))) + 2, f"LE：φ_{{cu}} = {PHI_CU_LE:.1f}°", 17, "#6D4BC2", weight="bold", bg="#FFFFFF")
    card(g, 1000, 40, 180, 330, PANEL)
    g.text(1090, 76, "三個圓", 19, INK, anchor="middle", weight="bold")
    g.text(1090, 108, "半徑都是", 16, MUTED, anchor="middle")
    g.text(1090, 140, f"R = {R:.0f} kPa", 22, INK, anchor="middle", weight="bold")
    g.text(1090, 190, "u 只會平移", 17, INK, anchor="middle")
    g.text(1090, 216, "不會改變大小", 17, INK, anchor="middle")
    g.text(1090, 268, "水不承剪", 17, EFF, anchor="middle", weight="bold")
    g.text(1090, 294, "⇒ 半徑", 17, EFF, anchor="middle", weight="bold")
    g.text(1090, 320, "（剪應力）不變", 17, EFF, anchor="middle", weight="bold")
    g.text(ax.X(Ce), 475, f"LE、AC 兩種路徑扣掉各自的 u_f，都回到同一個有效圓（{S3E_AC:.0f}～{S1E_AC:.0f} kPa）", 18, INK, anchor="middle", weight="bold")
    g.save("figs/fig04_shift.svg")


# ───────── fig05 應力路徑 p–q ─────────
def fig05():
    g = SVG(1200, 540)
    ax = Ax(g, 80, 460, 3.6)
    ax.axes(250, 110, "p, p' (kPa)", "q")
    ta = math.sin(R_(PHI_A)); tc = math.sin(R_(PHI_CU_AC)); tl = math.sin(R_(PHI_CU_LE))
    ax.line(0, 0, 232, 232*ta, color=EFF, sw=3.4)
    ax.line(0, 0, 250, 250*tc, color=TOT, sw=2.2, dash="10 7")
    ax.line(0, 0, 80, 80*tl, color="#6D4BC2", sw=2.2, dash="10 7")
    # 路徑
    g.arrow(ax.X(P0), ax.Y(0), ax.X(P_CD), ax.Y(Q_CD), CDC, 3, 13)
    g.arrow(ax.X(P0), ax.Y(0), ax.X(P_AC), ax.Y(Q_AC), TOT, 2.6, 12, dash="7 5")
    g.arrow(ax.X(P0), ax.Y(0), ax.X(P_LE), ax.Y(Q_LE), "#6D4BC2", 2.6, 12, dash="7 5")
    # ESP（示意曲線：由 p'0 彎向同一點）
    pts = []
    for i in range(31):
        t = i/30
        p = P0 + (PE_AC - P0)*t**1.6; q = Q_AC*math.sin(t*math.pi/2)
        pts.append(ax.P(p, q))
    g.poly(pts, EFF, 3.2)
    g.line(ax.X(PE_AC), ax.Y(Q_AC), ax.X(P_AC), ax.Y(Q_AC), TOT, 2, dash="5 4")
    g.line(ax.X(P_LE), ax.Y(Q_LE), ax.X(PE_AC), ax.Y(Q_AC), "#6D4BC2", 2, dash="5 4")
    for (p, q, c) in [(P_CD, Q_CD, CDC), (P_AC, Q_AC, TOT), (P_LE, Q_LE, "#6D4BC2"), (PE_AC, Q_AC, EFF)]:
        dot(g, ax.X(p), ax.Y(q), c, 8)
    dot(g, ax.X(P0), ax.Y(0), INK, 8)
    for v in [P_LE, PE_AC, P0, P_AC, P_CD]:
        ax.tick(v, f"{v:.0f}")
    g.text(ax.X(P0), ax.y0 + 48, "p'_0", 16, INK, anchor="middle", weight="bold")
    g.text(ax.X((PE_AC + P_AC)/2), ax.Y(Q_AC) + 24, f"u_f = +{UF_AC:.0f}", 16, TOT, anchor="middle", weight="bold", bg="#FFFFFF")
    g.text(ax.X((P_LE + PE_AC)/2), ax.Y(Q_AC) - 12, f"u_f = −{-UF_LE:.0f}", 16, "#6D4BC2", anchor="middle", weight="bold", bg="#FFFFFF")
    g.text(ax.X(P_CD) + 14, ax.Y(Q_CD) + 6, f"CD 終點 ({P_CD:.0f}, {Q_CD:.0f})", 16, CDC, weight="bold", bg="#FFFFFF")
    g.line(ax.X(PE_AC) - 4, ax.Y(Q_AC) - 8, ax.X(48), ax.Y(70), EFF, 1.4)
    g.text(ax.X(22), ax.Y(72), f"CU 有效終點 ({PE_AC:.0f}, {Q_AC:.0f})", 16, EFF, weight="bold", bg="#FFFFFF")
    g.text(ax.X(232) - 60, ax.Y(232*ta) + 6, f"有效 K_f：tan α' = sin φ' = {ta:.2f}", 18, EFF, anchor="end", weight="bold", bg="#FFFFFF")
    g.text(ax.X(250), ax.Y(250*tc) + 26, f"AC 總應力 K_f：sin φ_{{cu}} = {tc:.3f}", 16, TOT, anchor="end", weight="bold", bg="#FFFFFF")
    g.arc(ax.x0, ax.y0, 110, 0, ALPHA_A, EFF, 1.8)
    g.text(ax.x0 + 118, ax.y0 - 22, "α'", 17, EFF, weight="bold")
    card(g, 1000, 40, 180, 300, PANEL)
    g.text(1090, 74, "路徑怎麼走", 18, INK, anchor="middle", weight="bold")
    for i, (a, c) in enumerate([("CD：斜率 1", CDC), ("TSP 斜 45°", TOT), ("ESP 被 u 拉彎", EFF),
                                 ("LE：TSP 往左", "#6D4BC2")]):
        g.text(1016, 116 + i*34, a, 16, c, weight="bold")
    g.text(1090, 270, "有效終點都在", 16, INK, anchor="middle")
    g.text(1090, 296, "同一條 K_f 線", 17, EFF, anchor="middle", weight="bold")
    g.text(80, 528, "p = (σ_1 + σ_3)/2，q = (σ_1 − σ_3)/2；ESP 曲線形狀為示意，終點座標為計算值", 15, MUTED)
    g.save("figs/fig05_path.svg")


# ───────── fig06 K_f 線 ↔ M–C 包絡線（示範黏土 B）─────────
def fig06():
    g = SVG(1200, 470)
    ax = Ax(g, 150, 400, 3.1)
    ax.axes(250, 105, "σ', p'", "τ, q", xmin=-40)
    tf, sf, cf = math.tan(R_(PHI_B)), math.sin(R_(PHI_B)), math.cos(R_(PHI_B))
    a = C_B*cf
    x0 = -C_B/tf
    ax.line(x0, 0, 240, C_B + 240*tf, color=EFF, sw=3)
    ax.line(x0, 0, 240, a + 240*sf, color=NAVY, sw=2.6, dash="10 7")
    ax.semi(CA, RA, EFF, 2.2, fill=EFF, op=0.08)
    # 切點、頂點
    dot(g, ax.X(SFF), ax.Y(TFF), EFF, 7)
    dot(g, ax.X(CA), ax.Y(RA), NAVY, 7)
    ax.line(CA, 0, CA, RA, color=NAVY, sw=1.4, dash="4 4")
    ax.line(CA, 0, SFF, TFF, color=EFF, sw=1.4, dash="4 4")
    dot(g, ax.X(0), ax.Y(C_B), EFF, 6); dot(g, ax.X(0), ax.Y(a), NAVY, 6)
    g.text(ax.X(0) - 10, ax.Y(C_B) - 10, f"c' = {C_B:.2f}", 16, EFF, anchor="end", weight="bold", bg="#FFFFFF")
    g.text(ax.X(0) + 14, ax.Y(a) + 26, f"a = {a:.2f}", 16, NAVY, weight="bold", bg="#FFFFFF")
    g.text(ax.X(SFF) - 12, ax.Y(TFF) - 14, "M–C 切點", 15, EFF, anchor="end", weight="bold", bg="#FFFFFF")
    g.text(ax.X(CA) + 12, ax.Y(RA) - 14, f"圓頂 (C, R) = ({CA:.0f}, {RA:.0f})", 15, NAVY, weight="bold", bg="#FFFFFF")
    g.text(ax.X(240), ax.Y(C_B + 240*tf) - 12, f"M–C 包絡線：φ' = {PHI_B:.2f}°", 17, EFF, anchor="end", weight="bold", bg="#FFFFFF")
    g.text(ax.X(240), ax.Y(a + 240*sf) + 28, f"K_f 線：α' = {math.degrees(math.atan(sf)):.2f}°", 17, NAVY, anchor="end", weight="bold", bg="#FFFFFF")
    ax.tick(CA, f"{CA:.0f}")
    card(g, 930, 40, 250, 330, PANEL)
    g.text(1055, 74, "M–C 線切圓的邊", 17, EFF, anchor="middle", weight="bold")
    g.text(1055, 102, "K_f 線過圓的頂", 17, NAVY, anchor="middle", weight="bold")
    g.text(1055, 150, "tan α' = sin φ'", 21, INK, anchor="middle", weight="bold")
    g.text(1055, 186, f"= {sf:.4f}", 18, MUTED, anchor="middle")
    g.text(1055, 236, "a = c' cos φ'", 21, INK, anchor="middle", weight="bold")
    g.text(1055, 272, f"= {C_B:.2f} × {cf:.4f}", 16, MUTED, anchor="middle")
    g.text(1055, 296, f"= {a:.2f} kPa", 16, MUTED, anchor="middle")
    g.text(1055, 345, "兩條線不是同一條", 16, RED, anchor="middle", weight="bold")
    g.save("figs/fig06_kf.svg")


# ───────── fig07 砂土：剪脹、尖峰、臨界狀態 ─────────
def fig07():
    g = SVG(1200, 470)
    # 左：應力比
    x0, y0, W, H = 90, 390, 470, 320
    g.arrow(x0, y0, x0 + W + 20, y0, INK, 2, 10); g.arrow(x0, y0, x0, y0 - H - 20, INK, 2, 10)
    g.text(x0 + W + 26, y0 + 6, "ε_a", 20, INK, weight="bold"); g.text(x0 - 8, y0 - H - 24, "tan φ_{mob}", 18, INK, weight="bold", anchor="middle")
    sy = lambda phi: y0 - math.tan(R_(phi))/math.tan(R_(45))*H
    ycv = sy(PHI_CV); yp = sy(PHI_P)
    g.line(x0, ycv, x0 + W, ycv, EFF, 2, dash="8 6")
    D, L = [], []
    for i in range(101):
        t = i/100; x = x0 + t*W
        pk = 0.22
        if t < pk: ph = PHI_P*(1 - (1 - t/pk)**2.2)
        else: ph = PHI_CV + (PHI_P - PHI_CV)*math.exp(-(t - pk)*5.5)
        D.append((x, sy(ph)))
        L.append((x, sy(PHI_CV*(1 - math.exp(-t*7)))))
    g.poly(D, NAVY, 3.2); g.poly(L, TOT, 3, dash="10 7")
    dot(g, x0 + 0.22*W, yp, RED, 8)
    g.text(x0 + 0.22*W + 14, yp - 14, f"尖峰 φ_p ≈ {PHI_P:.0f}°（密砂）", 17, RED, weight="bold", bg="#FFFFFF")
    g.text(x0 + W, ycv - 12, f"臨界狀態 φ_{{cv}} = {PHI_CV:.0f}°", 17, EFF, anchor="end", weight="bold", bg="#FFFFFF")
    g.text(x0 + 0.45*W, sy(PHI_CV*0.8) + 30, "鬆砂：一路爬升", 16, TOT, weight="bold", bg="#FFFFFF")
    g.text(x0 + W/2, 440, "① 應力—應變", 18, INK, anchor="middle", weight="bold")
    # 右：孔隙比
    x0, W = 680, 440
    g.arrow(x0, y0, x0 + W + 20, y0, INK, 2, 10); g.arrow(x0, y0, x0, y0 - H - 20, INK, 2, 10)
    g.text(x0 + W + 26, y0 + 6, "ε_a", 20, INK, weight="bold"); g.text(x0, y0 - H - 24, "e", 20, INK, weight="bold", anchor="middle")
    yc = y0 - 0.55*H
    g.line(x0, yc, x0 + W, yc, EFF, 2, dash="8 6")
    D, L = [], []
    for i in range(101):
        t = i/100; x = x0 + t*W
        ed = 0.55 - 0.30*math.exp(-4.5*t) - 3.0*t*math.exp(-14*t)
        el = 0.90 - 0.35*(1 - math.exp(-t*5))
        D.append((x, y0 - ed*H)); L.append((x, y0 - el*H))
    g.poly(D, NAVY, 3.2); g.poly(L, TOT, 3, dash="10 7")
    g.text(x0 + 16, y0 - 0.25*H + 30, "密砂：先微縮後剪脹（體積變大）", 16, NAVY, weight="bold", bg="#FFFFFF")
    g.text(x0 + 16, y0 - 0.90*H - 14, "鬆砂：一路壓縮", 16, TOT, weight="bold", bg="#FFFFFF")
    g.text(x0 + W, yc - 12, "臨界孔隙比 e_{cv}", 17, EFF, anchor="end", weight="bold", bg="#FFFFFF")
    g.text(x0 + W/2, 440, "② 孔隙比變化", 18, INK, anchor="middle", weight="bold")
    g.save("figs/fig07_sand.svg")


# ───────── fig08 直剪：盒子 + 示範砂 τ–σn ─────────
def fig08():
    g = SVG(1200, 480)
    # 盒子
    bx, by, bw, bh = 90, 150, 380, 220
    for i in range(5):
        x = bx + 30 + i*80
        g.arrow(x, 70, x, by - 34, EFF, 2.4, 10)
    g.text(bx + bw/2, 56, "N → σ_n", 20, EFF, anchor="middle", weight="bold")
    g.rect(bx - 10, by - 30, bw + 20, 26, fill="#C8D1DC", stroke=INK, sw=2)
    g.rect(bx, by, bw, bh/2, fill="#EEF1F5", stroke=INK, sw=2.4)
    g.rect(bx + 26, by + bh/2, bw, bh/2, fill="#EEF1F5", stroke=INK, sw=2.4)
    random.seed(3)
    for _ in range(70):
        x = random.uniform(bx + 12, bx + bw - 12); y = random.uniform(by + 10, by + bh - 10)
        if y > by + bh/2: x += 26
        if abs(y - (by + bh/2)) > 6: g.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.4" fill="#8A94A3"/>')
    g.line(bx - 30, by + bh/2, bx + bw + 60, by + bh/2, RED, 3.4)
    g.text(bx + bw + 60, by + bh/2 - 12, "破壞面被指定：水平", 17, RED, anchor="end", weight="bold", bg="#FFFFFF")
    g.arrow(bx + bw + 120, by + bh*0.75, bx + bw + 32, by + bh*0.75, RED, 3, 13)
    g.text(bx + bw + 76, by + bh*0.75 + 34, "T → τ", 20, RED, anchor="middle", weight="bold")
    g.line(bx - 20, by + bh + 4, bx + bw + 46, by + bh + 4, INK, 2)
    for i in range(14):
        x = bx - 16 + i*30; g.line(x, by + bh + 4, x - 12, by + bh + 18, INK, 1.4)
    g.text(bx + bw/2, 430, "上盒固定、下盒推動（或反之）", 16, MUTED, anchor="middle")
    # τ–σn
    ax = Ax(g, 700, 410, 1.95)
    ax.axes(235, 190, "σ'_n (kPa)", "τ")
    tp, tc = math.tan(R_(PHI_P)), math.tan(R_(PHI_CV))
    ax.line(0, 0, 225, 225*tp, color=NAVY, sw=2.6)
    ax.line(0, 0, 235, 235*tc, color=EFF, sw=3)
    for s, t1, t2 in zip(SN, TF, TFP):
        dot(g, ax.X(s), ax.Y(t2), NAVY, 7); dot(g, ax.X(s), ax.Y(t1), EFF, 7)
        ax.tick(s, f"{s:.0f}")
        g.text(ax.X(s) + 12, ax.Y(t1) + 20, f"{t1:.1f}", 15, EFF, weight="bold", bg="#FFFFFF")
        g.text(ax.X(s) - 12, ax.Y(t2) - 8, f"{t2:.1f}", 15, NAVY, anchor="end", weight="bold", bg="#FFFFFF")
    g.text(ax.X(225) - 6, ax.Y(225*tp) - 14, f"密砂尖峰 φ_p = {PHI_P:.0f}°", 17, NAVY, anchor="end", weight="bold", bg="#FFFFFF")
    g.text(ax.X(235), ax.Y(235*tc) + 30, f"大變形 φ_{{cv}} = {PHI_CV:.0f}°", 17, EFF, anchor="end", weight="bold", bg="#FFFFFF")
    g.text(ax.X(117), 468, "每組只得到包絡線上的一個點，沒有完整的圓", 16, MUTED, anchor="middle")
    g.save("figs/fig08_direct.svg")


# ───────── fig09 莫爾圓幾何：R = C sinφ' + c' cosφ' ─────────
def fig09():
    g = SVG(1200, 470)
    ax = Ax(g, 230, 400, 3.1)
    xm = -C_B/math.tan(R_(PHI_B))
    ax.axes(180, 105, "σ' (kPa)", "τ", xmin=xm - 12)
    sf, cf, tf = math.sin(R_(PHI_B)), math.cos(R_(PHI_B)), math.tan(R_(PHI_B))
    ax.line(xm, 0, 175, C_B + 175*tf, color=EFF, sw=3)
    ax.semi(CA, RA, NAVY, 2.6, fill=NAVY, op=0.05)
    # 直角三角形
    g.poly([ax.P(xm, 0), ax.P(CA, 0), ax.P(SFF, TFF)], INK, 1.6, fill="#F2A65A", op=0.15, closed=True)
    ax.line(CA, 0, SFF, TFF, color=RED, sw=2.6)
    # 直角記號
    ux, uy = (CA - SFF), (0 - TFF); L = math.hypot(ux, uy); ux, uy = ux/L*8, uy/L*8
    vx, vy = (xm - SFF), (0 - TFF); L = math.hypot(vx, vy); vx, vy = vx/L*8, vy/L*8
    g.poly([ax.P(SFF + ux, TFF + uy), ax.P(SFF + ux + vx, TFF + uy + vy), ax.P(SFF + vx, TFF + vy)], INK, 1.4)
    dot(g, ax.X(SFF), ax.Y(TFF), EFF, 7); dot(g, ax.X(CA), ax.Y(0), NAVY, 7); dot(g, ax.X(xm), ax.Y(0), INK, 6)
    g.arc(ax.X(xm), ax.y0, 70, 0, PHI_B, EFF, 1.8)
    g.text(ax.X(xm) + 76, ax.y0 - 10, "φ'", 18, EFF, weight="bold")
    g.text((ax.X(CA) + ax.X(SFF))/2 + 12, (ax.Y(0) + ax.Y(TFF))/2, "R", 22, RED, weight="bold")
    # 大括號標示 C + c' cotφ'
    yb = ax.y0 + 44
    g.line(ax.X(xm), yb, ax.X(0), yb, "#B7791F", 3); g.line(ax.X(0), yb, ax.X(CA), yb, NAVY, 3)
    for v in [xm, 0, CA]: g.line(ax.X(v), yb - 7, ax.X(v), yb + 7, INK, 1.6)
    g.text((ax.X(xm) + ax.X(0))/2, yb + 26, f"c' cot φ' = {C_B/tf:.1f}", 15, "#B7791F", anchor="middle", weight="bold")
    g.text((ax.X(0) + ax.X(CA))/2, yb + 26, f"C = {CA:.0f}", 16, NAVY, anchor="middle", weight="bold")
    g.text(ax.X(SFF) - 10, ax.Y(TFF) - 16, f"切點 ({SFF:.1f}, {TFF:.1f})", 15, EFF, anchor="end", weight="bold", bg="#FFFFFF")
    g.text(ax.X(175), ax.Y(C_B + 175*tf) - 12, "τ = c' + σ' tan φ'", 17, EFF, anchor="end", weight="bold", bg="#FFFFFF")
    ax.tick(S3A, f"{S3A:.0f}"); ax.tick(S1A, f"{S1A:.0f}")
    card(g, 895, 40, 290, 360, PANEL)
    g.text(1040, 76, "直角三角形一行推完", 18, INK, anchor="middle", weight="bold")
    g.text(1040, 120, "sin φ' = R / (C + c' cot φ')", 18, INK, anchor="middle")
    g.text(1040, 160, "↓ 兩邊乘開", 16, MUTED, anchor="middle")
    g.text(1040, 202, "R = C sin φ' + c' cos φ'", 21, RED, anchor="middle", weight="bold")
    g.line(912, 228, 1168, 228, GRID, 1.5)
    g.text(1040, 262, "示範黏土 B 試驗 A 驗算", 16, MUTED, anchor="middle", weight="bold")
    g.text(1040, 294, f"{CA:.0f}×{sf:.4f} + {C_B:.2f}×{cf:.4f}", 16, INK, anchor="middle")
    g.text(1040, 326, f"= {CA*sf:.2f} + {C_B*cf:.2f} = {R_CHECK:.2f}", 16, INK, anchor="middle")
    g.text(1040, 360, f"= R = {RA:.0f} ✓", 19, CDC, anchor="middle", weight="bold")
    g.save("figs/fig09_geom.svg")


# ───────── fig10 選式流程 ─────────
def fig10():
    g = SVG(1200, 500)
    def box(x, y, w, h, t1, t2=None, col=INK, bg=PANEL, sz=19):
        card(g, x, y, w, h, bg, col, 10, 2)
        if t2:
            g.text(x + w/2, y + h/2 - 6, t1, sz, col, anchor="middle", weight="bold")
            g.text(x + w/2, y + h/2 + 22, t2, 16, INK, anchor="middle")
        else:
            g.text(x + w/2, y + h/2 + 7, t1, sz, col, anchor="middle", weight="bold")
    def dia(cx, cy, w, h, t):
        g.poly([(cx, cy - h/2), (cx + w/2, cy), (cx, cy + h/2), (cx - w/2, cy)], NAVY, 2, fill="#FFFFFF", closed=True)
        g.text(cx, cy + 6, t, 17, NAVY, anchor="middle", weight="bold")
    box(30, 205, 170, 80, "先換成有效應力", "σ' = σ − u", NAVY, "#E8ECF2", 17)
    g.arrow(200, 245, 250, 245, INK, 2.2)
    dia(345, 245, 190, 110, "c' = 0（NC）？")
    g.arrow(345, 190, 345, 110, INK, 2.2); g.text(355, 158, "是", 16, CDC, weight="bold")
    box(250, 30, 300, 80, "③ sin φ' = R / C", "直角三角形，最快", EFF, EFFBG)
    g.arrow(440, 245, 520, 245, INK, 2.2); g.text(470, 234, "否", 16, RED, weight="bold")
    dia(630, 245, 220, 110, "有幾組試驗？")
    g.arrow(630, 300, 630, 370, INK, 2.2); g.text(640, 342, "兩組", 16, NAVY, weight="bold")
    box(480, 370, 300, 90, "相減法消去 c'", "K_p = Δσ'_1 / Δσ'_3", TOT, TOTBG)
    g.arrow(740, 245, 820, 245, INK, 2.2); g.text(752, 234, "一組", 15, NAVY, weight="bold")
    dia(930, 245, 200, 110, "已知 C、R？")
    g.arrow(930, 190, 930, 110, INK, 2.2); g.text(940, 158, "是", 16, CDC, weight="bold")
    box(790, 30, 300, 80, "② R = C sin φ' + c' cos φ'", None, "#6D4BC2", "#F1EDFA", 18)
    g.arrow(930, 300, 930, 370, INK, 2.2); g.text(940, 342, "給 σ'_3 求 σ'_1", 15, NAVY, weight="bold")
    box(820, 370, 360, 90, "① σ'_1 = σ'_3 K_p + 2c'√K_p", "萬能式，K_p = tan²(45° + φ'/2)", CDC, OKBG, 18)
    g.arrow(780, 415, 820, 415, INK, 2.2)
    g.text(1080, 245, "最後一律", 16, MUTED, anchor="middle")
    g.text(1080, 272, "θ = 45° + φ'/2", 19, RED, anchor="middle", weight="bold")
    g.save("figs/fig10_flow.svg")


# ───────── fig11 破壞面角度 ─────────
def fig11():
    g = SVG(1200, 470)
    ax = Ax(g, 80, 400, 3.2)
    ax.axes(140, 62, "σ' (kPa)", "τ")
    Ce, R = (S1E_AC + S3E_AC)/2, DSD_AC/2
    sf, cf = math.sin(R_(PHI_A)), math.cos(R_(PHI_A))
    ax.line(0, 0, 135, 135*math.tan(R_(PHI_A)), color=EFF, sw=3)
    ax.semi(Ce, R, NAVY, 2.6, fill=NAVY, op=0.05)
    sx, sy = Ce - R*sf, R*cf
    ax.line(Ce, 0, sx, sy, color=RED, sw=2.4)
    dot(g, ax.X(sx), ax.Y(sy), EFF, 7); dot(g, ax.X(Ce), ax.Y(0), NAVY, 6)
    g.arc(ax.X(Ce), ax.y0, 40, 0, 2*TH_A, RED, 2)
    g.text(ax.X(Ce) + 20, ax.y0 - 48, f"2θ = {2*TH_A:.0f}°", 17, RED, weight="bold", bg="#FFFFFF")
    g.text(ax.X(sx) - 10, ax.Y(sy) - 14, f"切點 ({sx:.0f}, {sy:.1f})", 15, EFF, anchor="end", weight="bold", bg="#FFFFFF")
    for v in [S3E_AC, Ce, S1E_AC]: ax.tick(v, f"{v:.0f}")
    g.text(ax.X(135), ax.Y(135*math.tan(R_(PHI_A))) - 12, f"φ' = {PHI_A:.0f}°", 17, EFF, anchor="end", weight="bold", bg="#FFFFFF")
    g.text(ax.X(Ce), 450, "示範黏土 A 的 CU 有效圓", 16, MUTED, anchor="middle")
    # 試體
    cx, cy, w, h = 760, 235, 170, 290
    g.rect(cx - w/2, cy - h/2, w, h, fill="#EEF1F5", stroke=INK, sw=2.4)
    for i in range(4):
        x = cx - 60 + i*40
        g.arrow(x, cy - h/2 - 50, x, cy - h/2 - 4, INK, 2.2, 10); g.arrow(x, cy + h/2 + 50, x, cy + h/2 + 4, INK, 2.2, 10)
    g.text(cx - 110, cy - h/2 - 26, "σ'_1", 18, INK, weight="bold")
    def plane(th, col, dash=None, sw=3):
        t = math.tan(R_(th)); dx = min(w/2, (h/2)/t) - 3
        g.line(cx - dx, cy + dx*t, cx + dx, cy - dx*t, col, sw, dash)
    plane(TH_A, RED)
    plane(TH_WRONG, TOT, "8 6", 2.4)
    g.line(cx, cy, cx + 95, cy, INK, 1.2, "4 4")
    g.arc(cx, cy, 58, 0, TH_A, RED, 2)
    g.text(cx + 52, cy - 70, f"{TH_A:.0f}°", 18, RED, weight="bold", bg="#FFFFFF")
    card(g, 960, 60, 225, 330, PANEL)
    g.text(1072, 96, "θ = 45° + φ'/2", 21, RED, anchor="middle", weight="bold")
    g.text(1072, 128, f"= 45° + {PHI_A:.0f}°/2 = {TH_A:.0f}°", 16, INK, anchor="middle")
    g.text(1072, 176, "（與 σ_1 作用面夾角）", 14, MUTED, anchor="middle")
    g.line(980, 200, 1165, 200, GRID, 1.5)
    g.text(1072, 236, "誤代 φ_{cu}", 18, TOT, anchor="middle", weight="bold")
    g.text(1072, 268, f"45° + {PHI_CU_AC:.1f}°/2", 16, INK, anchor="middle")
    g.text(1072, 296, f"= {TH_WRONG:.1f}°（錯）", 18, TOT, anchor="middle", weight="bold")
    g.text(1072, 344, "顆粒怎麼滑，", 15, MUTED, anchor="middle")
    g.text(1072, 368, "只聽有效應力的", 15, MUTED, anchor="middle")
    g.save("figs/fig11_plane.svg")


# ───────── fig12 兩組試驗相減法（示範黏土 B）─────────
def fig12():
    g = SVG(1260, 480)
    ax = Ax(g, 70, 400, 1.85)
    ax.axes(435, 170, "σ' (kPa)", "τ")
    tf = math.tan(R_(PHI_B))
    ax.semi(CA, RA, CDC, 2.6, fill=CDC, op=0.07)
    ax.semi(CB, RB, TOT, 2.6, fill=TOT, op=0.07)
    ax.line(0, C_B, 430, C_B + 430*tf, color=EFF, sw=3)
    for v in [S3A, S1A, S3B, S1B]: ax.tick(v, f"{v:.0f}")
    g.text(ax.X(CA), ax.Y(RA) - 14, "試驗 A", 16, CDC, anchor="middle", weight="bold", bg="#FFFFFF")
    g.text(ax.X(CB), ax.Y(RB) - 14, "試驗 B", 16, TOT, anchor="middle", weight="bold", bg="#FFFFFF")
    dot(g, ax.X(0), ax.Y(C_B), EFF, 6)
    g.text(ax.X(0) + 12, ax.Y(C_B) + 24, f"c' = {C_B:.2f}", 15, EFF, weight="bold", bg="#FFFFFF")
    g.text(ax.X(430) - 40, ax.Y(C_B + 430*tf) - 10, f"共同切線 φ' = {PHI_B:.2f}°", 17, EFF, anchor="end", weight="bold", bg="#FFFFFF")
    # 右側算式
    card(g, 985, 30, 262, 410, PANEL)
    x = 1085
    rows = [("A：", f"{S1A:.0f} = {S3A:.0f}K_p + 2c'√K_p", CDC), ("B：", f"{S1B:.0f} = {S3B:.0f}K_p + 2c'√K_p", TOT)]
    for i, (a, b, c) in enumerate(rows):
        g.text(1000, 70 + i*36, a + b, 17, c, weight="bold")
    g.line(1000, 116, 1232, 116, GRID, 1.5)
    g.text(1000, 150, "B − A：c' 項整個消失", 16, MUTED)
    g.text(1000, 186, f"{S1B - S1A:.0f} = {S3B - S3A:.0f} K_p", 20, INK, weight="bold")
    g.text(1000, 224, f"K_p = {KP_B:.2f}　√K_p = {SKP_B:.4f}", 18, RED, weight="bold")
    g.line(1000, 244, 1232, 244, GRID, 1.5)
    g.text(1000, 278, "回代 A：", 16, MUTED)
    g.text(1000, 310, f"2c'×{SKP_B:.4f} = {S1A:.0f} − {S3A*KP_B:.0f}", 17, INK)
    g.text(1000, 344, f"c' = {C_B:.2f} kPa", 20, EFF, weight="bold")
    g.text(1000, 382, f"sin φ' = (K_p−1)/(K_p+1) = {(KP_B-1)/(KP_B+1):.4f}", 15, INK)
    g.text(1000, 414, f"φ' = {PHI_B:.2f}°", 20, EFF, weight="bold")
    g.save("figs/fig12_subtract.svg")


# ───────── fig13 比例法只適用 NC ─────────
def fig13():
    g = SVG(1200, 460)
    def panel(ox, title, col, circles, env_c, env_phi, wrong):
        ax = Ax(g, ox, 380, 1.05)
        ax.axes(440, 185, "σ'", "τ")
        g.text(ox + 220, 40, title, 20, col, anchor="middle", weight="bold")
        t = math.tan(R_(env_phi))
        ax.line(0, env_c, 430, env_c + 430*t, color=EFF, sw=3)
        for (C, R, cc) in circles:
            ax.semi(C, R, cc, 2.4, fill=cc, op=0.06)
        for (ang, lab, cc) in wrong:
            L = 430; ax.line(0, 0, L, L*math.tan(R_(ang)), color=cc, sw=1.8, dash="7 5")
            g.text(ax.X(L) + 4, ax.Y(L*math.tan(R_(ang))) + 5, lab, 14, cc, weight="bold")
        return ax
    # NC：示範黏土 A 的 CD 圓（σ'3 = 100、200）
    c1 = ((S1_CD + S3)/2, DSD_CD/2, CDC); c2 = (2*(S1_CD + S3)/2, 2*DSD_CD/2, TOT)
    panel(60, "NC（c' = 0）：圓互為相似形", CDC, [c1, (c1[0]*0.5, c1[1]*0.5, CDC), (c2[0]*0.8, c2[1]*0.8, TOT)], 0, PHI_A, [])
    g.text(290, 432, "σ'_3 加倍 → σ'_1 也加倍，比例法 OK", 16, CDC, anchor="middle", weight="bold")
    panel(640, "OC（c' ≠ 0）：比例法失效", RED, [(CA, RA, CDC), (CB, RB, TOT)], C_B, PHI_B,
          [(PHI_WRONG_A, f"A 單算 {PHI_WRONG_A:.1f}°", CDC), (PHI_WRONG_B, f"B 單算 {PHI_WRONG_B:.1f}°", TOT)])
    g.text(870, 432, f"每組各自用 sin φ = R/C 得到不同角度；真值 φ' = {PHI_B:.2f}°", 16, RED, anchor="middle", weight="bold")
    g.save("figs/fig13_ncoc.svg")


for f in [fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13]:
    f()
print("figs done")
