"""SM-U3-1 拼圖四：理論邊界 — 向量圖產生器（示範牆數字全部取自 params.py）"""
import math, sys
import numpy as np
from params import *
from wedge import ka_c, kp_c, ka_rs, trial
from svglib import *

F = "figs/"
f1 = lambda v: f"{v + 1e-9:.1f}"
f2 = lambda v: f"{v:.2f}"
f3 = lambda v: f"{v:.3f}"
RK, CL, PS, OK = "#2F54C8", "#B8520E", "#C0392B", "#2E7D6B"
RES, WALLc, GREY = "#E4572E", "#34495E", "#9AA3AE"
SAND, SAND2, WEDGE = "#F1E4C9", "#E6CFA0", "#F6D2BF"
LINE = "#D5DAE1"
rad = math.radians


def hatch_ground(s, pts, step=16, up=True):
    """沿折線畫地表與斜短線"""
    s.poly(pts, INK, 2)
    for (x1, y1), (x2, y2) in zip(pts[:-1], pts[1:]):
        L = math.hypot(x2 - x1, y2 - y1); n = int(L // step)
        for i in range(n):
            t = (i + 0.3) / max(n, 1)
            x, y = x1 + t * (x2 - x1), y1 + t * (y2 - y1)
            s.line(x, y, x + 9, y - 10 if up else y + 10, INK, 1.1)


def dots(s, x0, y0, x1, y1, n=40, seed=3, inside=None, color="#C9B48A"):
    rng = np.random.default_rng(seed)
    k = 0
    while k < n:
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        if inside and not inside(x, y): continue
        s.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.8" fill="{color}"/>'); k += 1


def axes(s, x0, y0, w, h, xr, yr, xt, yt, xl="", yl="", xfmt=str, yfmt=str, grid=True):
    X = lambda v: x0 + (v - xr[0]) / (xr[1] - xr[0]) * w
    Y = lambda v: y0 + h - (v - yr[0]) / (yr[1] - yr[0]) * h
    for v in yt:
        if grid: s.line(x0, Y(v), x0 + w, Y(v), GRID, 1)
        s.text(x0 - 10, Y(v) + 5, yfmt(v), 14, MUTED, "end")
    for v in xt:
        s.line(X(v), y0 + h, X(v), y0 + h + 6, "#5B6573", 1.3)
        s.text(X(v), y0 + h + 24, xfmt(v), 14, MUTED, "middle")
    s.line(x0, y0 + h, x0 + w, y0 + h, "#5B6573", 2)
    s.line(x0, y0, x0, y0 + h, "#5B6573", 2)
    if xl: s.text(x0 + w, y0 + h + 48, xl, 15, INK, "end", "bold")
    if yl: s.text(x0, y0 - 14, yl, 15, INK, "middle", "bold")
    return X, Y


def curve(s, X, Y, xs, ys, color, sw=3, dash=None):
    s.poly([(X(a), Y(b)) for a, b in zip(xs, ys)], color, sw, dash=dash)


def card(s, x, y, w, h, fill=PANEL, stroke=LINE, sw=1.5, rx=12):
    s.rect(x, y, w, h, fill=fill, stroke=stroke, sw=sw, rx=rx)


# ───────── F1 拼圖四在全單元的位置 ─────────
def fig_map():
    s = SVG(1200, 430, ts=1.0)
    pcs = [("拼圖一", "變形", "牆怎麼動 → 選 K", "#2F54C8"),
           ("拼圖二", "土質修正", "黏土、水、超載", "#B8520E"),
           ("拼圖三", "四步 SOP", "切方塊、對牆底取矩", "#2E7D6B"),
           ("拼圖四", "理論邊界", "公式能用到哪裡", "#C0392B")]
    w, gap = 270, 23
    for i, (a, b, c, col) in enumerate(pcs):
        x = 16 + i * (w + gap); last = i == 3
        card(s, x, 14, w, 150, fill="#FFFFFF" if last else PANEL, stroke=col if last else LINE, sw=3.5 if last else 1.5)
        s.text(x + 22, 50, a, 17, col, "start", "bold")
        s.text(x + 22, 96, b, 30, INK if last else "#4B5563", "start", "bold")
        s.text(x + 22, 138, c, 16, MUTED)
        if i < 3: s.arrow(x + w + 3, 89, x + w + gap - 3, 89, GREY, 2.5, 10)
    x4 = 16 + 3 * (w + gap) + w / 2
    s.text(x4, 190, "本講", 15, PS, "middle", "bold")
    bx = [(16, "邊界一", "Rankine 還是 Coulomb？", "看題目有沒有給 δ、θ、β", RK),
          (416, "邊界二", "斜填土 β 的修正", "合力平行坡面、β 必須 < φ", CL),
          (816, "邊界三", "被動土壓的保護傘", "算得出來，不一定用得到", PS)]
    for x, a, b, c, col in bx:
        s.line(x4, 200, x4, 222, GREY, 2)
        s.poly([(x4, 222), (x + 184, 222), (x + 184, 250)], GREY, 2)
        s.arrow(x + 184, 236, x + 184, 256, GREY, 2, 9)
        card(s, x, 258, 368, 160)
        s.rect(x, 258, 8, 160, fill=col, stroke="none")
        s.text(x + 30, 294, a, 17, col, "start", "bold")
        s.text(x + 30, 340, b, 25, INK, "start", "bold")
        s.text(x + 30, 388, c, 17, MUTED)
    s.save(F + "fig01_map.svg")


# ───────── F2 Rankine vs Coulomb：牆背怎麼看 ─────────
def fig_two():
    s = SVG(1200, 540, ts=1.0)
    # 左：Rankine
    card(s, 10, 10, 580, 520)
    s.text(34, 50, "Rankine：應力法", 24, RK, "start", "bold")
    s.text(566, 50, "δ = 0、θ = 0、β = 0", 16, MUTED, "end")
    gy, by, wx = 140, 450, 170           # 地表、牆底、牆背
    Hp = by - gy
    s.rect(wx, gy, 380, Hp, fill=SAND, stroke="none")
    dots(s, wx + 8, gy + 8, wx + 372, by - 8, 55, 1)
    s.rect(wx - 34, gy - 26, 34, Hp + 26, fill=WALLc, stroke="none")
    hatch_ground(s, [(wx, gy), (wx + 380, gy)])
    s.line(40, by, 560, by, INK, 2)
    a = rad(45 + PHI / 2); L = Hp / math.tan(a)
    s.line(wx, by, wx + L, gy, RK, 2.4, "8,6")
    s.arc(wx, by, 60, 0, 45 + PHI / 2, RK, 1.8)
    s.text(wx + 66, by - 26, "45°+φ/2 = 60°", 16, RK, "start", "bold")
    # 土中應力元素
    ex, ey, e = 430, 235, 46
    s.rect(ex - e / 2, ey - e / 2, e, e, fill="#FFFFFF", stroke=INK, sw=1.6)
    s.arrow(ex, ey - e / 2 - 44, ex, ey - e / 2 - 4, INK, 2, 9)
    s.arrow(ex, ey + e / 2 + 44, ex, ey + e / 2 + 4, INK, 2, 9)
    s.arrow(ex - e / 2 - 40, ey, ex - e / 2 - 4, ey, RK, 2.4, 9)
    s.arrow(ex + e / 2 + 40, ey, ex + e / 2 + 4, ey, RK, 2.4, 9)
    s.text(ex + 10, ey - e / 2 - 30, "σ_v", 17, INK, "start", "bold")
    s.text(ex + e / 2 + 14, ey - 12, "σ_h = K_aσ_v", 16, RK, "start", "bold")
    s.text(ex, ey + e / 2 + 70, "每一點都在莫爾圓破壞", 14, MUTED, "middle")
    # 合力
    yP = by - Hp / 3
    s.arrow(wx + 120, yP, wx + 4, yP, RES, 4, 16)
    s.text(wx + 126, yP + 6, "P_a 水平", 18, RES, "start", "bold")
    s.line(wx - 60, yP, wx - 60, by, MUTED, 1.2, "3,3")
    s.text(wx - 68, (yP + by) / 2 + 6, "H/3", 16, MUTED, "end", "bold")
    s.text(34, 505, "從土體內部的應力狀態推導，不看牆背", 16, INK, "start", "bold")

    # 右：Coulomb
    ox = 610
    card(s, ox, 10, 580, 520)
    s.text(ox + 24, 50, "Coulomb：楔體力平衡", 24, CL, "start", "bold")
    s.text(ox + 556, 50, "可放入 δ、θ、β", 16, MUTED, "end")
    th, bt = rad(THETA), rad(BETA)
    Ax, Ay = ox + 215, 450; Hc = 255
    Bx, By = Ax - Hc * math.tan(th), Ay - Hc
    xe = ox + 565
    ys = lambda x: By - (x - Bx) * math.tan(bt)
    # 臨界破壞面（θ、β、δ 皆有）
    _, rho, *_ = trial(H, G, PHI, DELTA, -THETA, BETA)   # wedge.trial 的 θ 與 Das 相反
    rr = rad(rho)
    # 破壞面與地表交點
    t = (Ay - By + (Ax - Bx) * math.tan(bt)) / (math.sin(rr) - math.cos(rr) * math.tan(bt))
    Cx, Cy = Ax + t * math.cos(rr), Ay - t * math.sin(rr)
    s.poly([(Ax, Ay), (Bx, By), (xe, ys(xe)), (xe, Ay)], "none", 0, fill=SAND, closed=True)
    dots(s, Bx, ys(xe), xe, Ay, 60, 2, inside=lambda x, y: y > ys(x) + 6 and (x - Ax) * (By - Ay) - (y - Ay) * (Bx - Ax) < 0)
    s.poly([(Ax, Ay), (Bx, By), (Cx, Cy)], CL, 2.2, fill=WEDGE, closed=True, op=0.75)
    s.text((Ax + Bx + Cx) / 3 + 8, (Ay + By + Cy) / 3 + 4, "破壞楔體", 18, CL, "middle", "bold")
    s.text((Ax + Cx) / 2 + 60, (Ay + Cy) / 2 + 30, "試算破壞面", 14, CL, "start")
    # 牆（重力式）
    s.poly([(Ax, Ay), (Bx, By - 20), (Bx - 46, By - 20), (Ax - 150, Ay)], WALLc, 1, fill=WALLc, closed=True)
    hatch_ground(s, [(Bx, By), (xe, ys(xe))])
    s.line(ox + 30, Ay, xe, Ay, INK, 2)
    # θ
    s.line(Ax, Ay, Ax, By - 30, MUTED, 1.3, "5,4")
    s.arc(Ax, Ay, 150, 90, 90 + THETA, INK, 1.6)
    s.text(Ax - 10, Ay - 160, "θ", 20, INK, "end", "bold")
    # β
    s.line(Bx + 10, By, Bx + 150, By, MUTED, 1.3, "5,4")
    s.arc(Bx, By, 120, 0, BETA, INK, 1.6)
    s.text(Bx + 128, By - 10, "β", 20, INK, "start", "bold")
    # P：作用於牆背 H/3，偏離法線 δ
    hP = Hc / 3
    Px, Py = Ax - hP * math.tan(th), Ay - hP
    ang = th + rad(DELTA)                     # 合力低於水平 (δ+θ)
    Lr = 120
    sx, sy = Px + Lr * math.cos(ang), Py - Lr * math.sin(ang)
    s.line(Px, Py, Px + 105 * math.cos(th), Py - 105 * math.sin(th), MUTED, 1.4, "5,4")   # 法線
    s.arrow(sx, sy, Px + 3, Py - 1, RES, 4, 16)
    s.arc(Px, Py, 78, THETA, THETA + DELTA, RES, 1.8)
    s.text(Px + 84, Py - 24, "δ", 18, RES, "start", "bold")
    s.text(sx - 6, sy - 10, "P_a", 20, RES, "end", "bold")
    s.text(Px + 110, Py - 12, "法線", 13, MUTED, "start")
    s.text(ox + 24, 505, "把滑動土體當剛體，試算找出最大（主動）推力", 16, INK, "start", "bold")
    s.save(F + "fig02_two.svg")


# ───────── F3 Coulomb 楔體試算 ─────────
def fig_wedge():
    s = SVG(1200, 520, ts=1.0)
    card(s, 10, 10, 470, 500)
    s.text(32, 48, "單一楔體的力平衡（δ = 20°）", 20, CL, "start", "bold")
    Ax, Ay, Hp = 110, 440, 300
    rho = rad(RHO_C)
    Cx, Cy = Ax + Hp / math.tan(rho), Ay - Hp
    s.rect(Ax, Ay - Hp, 340, Hp, fill=SAND, stroke="none")
    s.poly([(Ax, Ay), (Ax, Ay - Hp), (Cx, Cy)], CL, 2, fill=WEDGE, closed=True, op=0.8)
    s.rect(Ax - 28, Ay - Hp - 20, 28, Hp + 20, fill=WALLc, stroke="none")
    hatch_ground(s, [(Ax, Ay - Hp), (Ax + 340, Ay - Hp)])
    s.line(40, Ay, 460, Ay, INK, 2)
    s.arc(Ax, Ay, 56, 0, RHO_C, CL, 1.6)
    s.text(Ax + 62, Ay - 18, f"ρ = {RHO_C:.1f}°", 15, CL, "start", "bold")
    # 三個力
    gx, gy = Ax + (Cx - Ax) / 3, Ay - 2 * Hp / 3
    s.arrow(gx, gy - 20, gx, gy + 70, INK, 3, 13)
    s.text(gx + 8, gy + 60, "W", 19, INK, "start", "bold")
    d = rad(DELTA)
    s.arrow(Ax - 90 * math.cos(d) + 0, Ay - Hp / 3 + 90 * math.sin(d), Ax - 2, Ay - Hp / 3, RES, 3, 13)
    s.text(Ax - 70, Ay - Hp / 3 + 58, "P", 19, RES, "start", "bold")
    mx, my = (Ax + Cx) / 2, (Ay + Cy) / 2
    # R 作用於楔體：與破壞面法線夾 φ，指向楔體並偏上
    ang = math.atan2(math.cos(rho), -math.sin(rho))  # 世界座標法線 n_f = (−sinρ, cosρ)
    ang_r = ang - rad(PHI)
    ex, ey = mx + 22 * math.cos(ang_r), my - 22 * math.sin(ang_r)
    s.arrow(mx - 95 * math.cos(ang_r), my + 95 * math.sin(ang_r), ex - 20 * math.cos(ang_r), ey + 20 * math.sin(ang_r), OK, 3, 13)
    s.text(mx + 44, my + 74, "R", 19, OK, "start", "bold")
    s.text(32, 478, "P 偏牆背法線 δ、R 偏破壞面法線 φ", 15, MUTED)
    s.text(32, 500, "→ 三力閉合，解出這一刀的 P", 15, INK, "start", "bold")

    # 右：P(ρ) 曲線
    card(s, 495, 10, 695, 500)
    s.text(517, 48, "換不同破壞面角 ρ 試算，取 P 最大者", 20, INK, "start", "bold")
    X, Y = axes(s, 580, 90, 570, 330, (40, 80), (60, 115), range(40, 81, 5), range(60, 116, 10),
                "破壞面角 ρ (°)", "P (kN/m)", lambda v: f"{v}°")
    for dl, col, lab in ((0, RK, "δ = 0（Rankine 條件）"), (DELTA, CL, "δ = 20°")):
        _, rh, rhos, Ps = trial(H, G, PHI, dl, 0, 0)
        xs = np.degrees(rhos); m = (xs >= 40) & (xs <= 80) & (Ps >= 60)
        curve(s, X, Y, xs[m], Ps[m], col, 3.2)
        Pm = np.nanmax(Ps)
        s.line(X(rh), Y(Pm), X(rh), Y(60), col, 1.3, "4,4")
        s.circle(X(rh), Y(Pm), 7, fill=col)
        s.text(X(rh) + 12, Y(Pm) - 12, f"{f1(Pm)} kN/m @ {rh:.1f}°", 16, col, "start", "bold")
    s.text(X(72), Y(100), "δ = 0", 16, RK, "start", "bold")
    s.text(X(72), Y(78), "δ = 20°", 16, CL, "start", "bold")
    s.text(517, 488, "δ = 0 的峰值正好在 45°+φ/2 = 60°、P = ½K_aγH² = 108 → 就是 Rankine", 15, RK, "start", "bold")
    s.save(F + "fig03_wedge.svg")


# ───────── F4 示範牆：Rankine vs Coulomb 合力 ─────────
def fig_demo():
    s = SVG(1200, 470, ts=1.0)
    for k, (title, col, P, ang, Ph, Pv) in enumerate((
            ("Rankine（δ = 0）", RK, PA_R, 0, PA_R, 0.0),
            ("Coulomb（δ = 20°）", CL, PA_C, DELTA, PA_C_H, PA_C_V))):
        ox = 10 + k * 600
        card(s, ox, 10, 580, 450)
        s.text(ox + 24, 48, title, 22, col, "start", "bold")
        s.text(ox + 556, 48, f"K_a = {f3(KA_R if k == 0 else KA_C)}", 20, INK, "end", "bold")
        gy, by, wx = 118, 410, ox + 130
        Hp = by - gy
        s.rect(wx, gy, 420, Hp, fill=SAND, stroke="none")
        dots(s, wx + 10, gy + 8, wx + 410, by - 8, 45, 5 + k)
        s.rect(wx - 30, gy - 20, 30, Hp + 20, fill=WALLc, stroke="none")
        hatch_ground(s, [(wx, gy), (wx + 420, gy)])
        s.line(ox + 30, by, ox + 560, by, INK, 2)
        # 土壓分布（示意寬度 ∝ Ka）
        Kx = (KA_R if k == 0 else KA_C) * 260
        s.poly([(wx, gy), (wx + Kx, by), (wx, by)], col, 1.5, fill=col, closed=True, op=0.12)
        s.text(wx + Kx + 8, by - 8, f"{f1((KA_R if k == 0 else KA_C) * G * H)} kPa", 14, col, "start", "bold")
        yP = by - Hp / 3
        a = rad(ang); L = 170
        sx, sy = wx + L * math.cos(a), yP - L * math.sin(a)
        s.arrow(sx, sy, wx + 3, yP, RES, 4.5, 17)
        s.text(sx + 8, sy + 2, f"P_a = {f1(P)}", 19, RES, "start", "bold")
        if k == 1:
            s.line(wx, yP, wx + 190, yP, MUTED, 1.2, "4,4")
            s.arc(wx, yP, 95, 0, DELTA, RES, 1.8)
            s.text(wx + 102, yP - 4, "δ", 17, RES, "start", "bold")
        s.line(wx - 55, yP, wx - 55, by, MUTED, 1.2, "3,3")
        s.text(wx - 62, (yP + by) / 2 + 6, "2.0 m", 15, MUTED, "end", "bold")
        s.text(ox + 24, 440, f"水平 P_h = {f1(Ph)}　垂直 P_v = {f1(Pv)}（kN/m）", 17, INK, "start", "bold")
        s.text(ox + 556, 80, f"H = {H:.0f} m、γ = {G:.0f} kN/m³、φ = {PHI:.0f}°、c = 0", 14, MUTED, "end")
    s.save(F + "fig04_demo.svg")



def diamond(s, cx, cy, w, h, lines, col):
    s.poly([(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)], col, 2.2, fill="#FFFFFF", closed=True)
    for i, l in enumerate(lines):
        s.text(cx, cy + 7 + (i - (len(lines) - 1) / 2) * 26, l, 19, INK, "middle", "bold")


def box(s, x, y, w, h, title, sub, col, fill="#FFFFFF"):
    s.rect(x, y, w, h, fill=fill, stroke=col, sw=2.4, rx=12)
    s.text(x + w / 2, y + 40, title, 21, col, "middle", "bold")
    for i, l in enumerate(sub):
        s.text(x + w / 2, y + 74 + i * 26, l, 16, INK, "middle")


# ───────── F5 考場選用流程 ─────────
def fig_flow():
    s = SVG(1200, 540, ts=1.0)
    cy = 265
    s.rect(10, cy - 50, 175, 100, fill=PANEL, stroke=LINE, sw=1.5, rx=12)
    s.text(97, cy - 8, "讀題：牆背", 19, INK, "middle", "bold")
    s.text(97, cy + 22, "與填土幾何", 19, INK, "middle", "bold")
    diamond(s, 370, cy, 250, 160, ["有給 δ 或 θ？"], CL)
    diamond(s, 700, cy, 250, 160, ["填土傾斜 β？"], CL)
    s.arrow(185, cy, 243, cy, GREY, 2.5, 12)
    s.arrow(495, cy, 573, cy, GREY, 2.5, 12)
    s.text(534, cy - 12, "否", 17, MUTED, "middle", "bold")
    s.arrow(825, cy, 883, cy, GREY, 2.5, 12)
    s.text(854, cy - 12, "否", 17, MUTED, "middle", "bold")
    box(s, 885, cy - 75, 305, 150, "Rankine 基本式", ["K_a = tan²(45° − φ/2)", "合力水平、作用於 H/3"], RK, "#EEF2FB")
    s.arrow(370, cy - 80, 370, 132, GREY, 2.5, 12)
    s.text(384, cy - 104, "是", 17, CL, "start", "bold")
    box(s, 205, 10, 330, 120, "Coulomb 公式", ["K_a = f(φ, δ, θ, β)", "合力偏牆背法線 δ"], CL, "#FBF1EA")
    s.arrow(700, cy + 80, 700, 398, GREY, 2.5, 12)
    s.text(714, cy + 110, "是（牆背仍垂直光滑）", 17, CL, "start", "bold")
    box(s, 535, 400, 330, 130, "Rankine 斜填土", ["K_a 含 cosβ 修正", "合力平行坡面（偏 β）"], RK, "#EEF2FB")
    s.rect(885, 400, 305, 130, fill="#FBECEA", stroke=PS, sw=1.8, rx=12, dash="7,5")
    s.text(1037, 438, "被動側另外把關", 19, PS, "middle", "bold")
    s.text(1037, 472, "δ 大時 Coulomb K_p 過高", 16, INK, "middle")
    s.text(1037, 500, "→ Rankine 或對數螺線", 16, INK, "middle")
    s.rect(560, 20, 630, 110, fill=PANEL, stroke=LINE, sw=1.2, rx=12)
    s.text(585, 58, "關鍵字＝切換訊號", 17, CL, "start", "bold")
    s.text(585, 92, "「牆背摩擦角」「牆背傾斜」「牆背粗糙」→ Coulomb", 16, INK)
    s.text(585, 118, "只有「地表坡角」→ Rankine 斜填土即可", 16, INK)
    s.text(20, 420, "沒說 δ", 17, MUTED, "start", "bold")
    s.text(20, 448, "＝預設光滑垂直", 17, MUTED, "start", "bold")
    s.text(20, 476, "＝ Rankine", 17, RK, "start", "bold")
    s.save(F + "fig05_flow.svg")


# ───────── F6 退化：三個參數歸零都回到 1/3 ─────────
def fig_degen():
    s = SVG(1200, 450, ts=1.0)
    specs = [("K_a 隨牆背摩擦 δ", "δ (°)", np.linspace(0, 30, 61), lambda v: ka_c(PHI, v, 0, 0), (0.25, 0.40), CL),
             ("K_a 隨牆背傾角 θ", "θ (°)", np.linspace(-15, 20, 71), lambda v: ka_c(PHI, 0, v, 0), (0.20, 0.50), CL),
             ("K_a 隨填土坡角 β", "β (°)", np.linspace(0, 25, 51), lambda v: ka_c(PHI, 0, 0, v), (0.30, 0.60), CL)]
    for i, (tt, xl, xs, fn, yr, col) in enumerate(specs):
        ox = 10 + i * 400
        card(s, ox, 10, 380, 430)
        s.text(ox + 20, 46, tt, 19, INK, "start", "bold")
        xr = (xs[0], xs[-1])
        step = 10 if i != 1 else 5
        xt = [v for v in range(int(xr[0]), int(xr[1]) + 1) if v % step == 0]
        yt = np.round(np.arange(yr[0], yr[1] + 1e-9, 0.05), 2)
        X, Y = axes(s, ox + 75, 90, 280, 260, xr, yr, xt, yt, xl, "", str, lambda v: f"{v:.2f}")
        curve(s, X, Y, xs, [fn(v) for v in xs], col, 3.2)
        if i == 2:
            ys = [ka_rs(PHI, v) for v in xs]
            curve(s, X, Y, xs, ys, RK, 3, "8,5")
            s.text(X(24), Y(ka_rs(PHI, 24)) + 30, "Rankine 斜填土", 14, RK, "end", "bold")
            s.text(X(24), Y(ka_c(PHI, 0, 0, 24)) - 12, "Coulomb δ=0", 14, CL, "end", "bold")
        s.circle(X(0), Y(1 / 3), 8, fill=RK)
        s.text(X(0) + 12, Y(1 / 3) - 12 if i != 0 else Y(1 / 3) - 12, "1/3", 16, RK, "start", "bold")
        note = ["δ ↑ → K_a ↓（摩擦分擔）", "θ > 0：土壓在牆背上 → K_a ↑", "β ↑ → K_a ↑（楔體變重）"][i]
        s.text(ox + 20, 425, note, 15, MUTED, "start", "bold")
    s.save(F + "fig06_degen.svg")


# ───────── F7 斜填土：合力平行坡面 ─────────
def fig_slope():
    s = SVG(1200, 500, ts=1.0)
    card(s, 10, 10, 640, 480)
    s.text(32, 48, f"牆背垂直光滑、填土坡角 β = {BETA:.0f}°", 20, CL, "start", "bold")
    bt = rad(BETA)
    wx, by, Hp = 200, 440, 300
    gy = by - Hp
    xe = 630
    ys = lambda x: gy - (x - wx) * math.tan(bt)
    s.poly([(wx, gy), (xe, ys(xe)), (xe, by), (wx, by)], "none", 0, fill=SAND, closed=True)
    dots(s, wx + 8, ys(xe), xe, by - 6, 50, 9, inside=lambda x, y: y > ys(x) + 6)
    s.rect(wx - 32, gy - 22, 32, Hp + 22, fill=WALLc, stroke="none")
    hatch_ground(s, [(wx, gy), (xe, ys(xe))])
    s.line(40, by, 640, by, INK, 2)
    s.line(wx, gy, wx + 170, gy, MUTED, 1.3, "5,4")
    s.arc(wx, gy, 150, 0, BETA, INK, 1.6)
    s.text(wx + 158, gy - 14, "β", 20, INK, "start", "bold")
    # 分布：每一深度的應力向量平行坡面
    Kx = 190
    for fz in (0.25, 0.5, 0.75, 1.0):
        z = fz * Hp; L = Kx * fz * KA_RS / 0.3729 * 0.9
        y0 = gy + z
        s.arrow(wx + L * math.cos(bt), y0 + L * math.sin(bt) * -1, wx + 2, y0, CL, 1.8, 9)
    yP = by - Hp / 3
    Lr = 200
    tx, ty = wx + Lr * math.cos(bt), yP - Lr * math.sin(bt)
    s.arrow(tx, ty, wx + 3, yP, RES, 5, 18)
    s.text(tx + 8, ty + 4, f"P_a = {f1(PA_RS)}", 20, RES, "start", "bold")
    s.line(wx - 60, yP, wx - 60, by, MUTED, 1.2, "3,3")
    s.text(wx - 68, (yP + by) / 2 + 6, "H/3", 16, MUTED, "end", "bold")
    s.text(32, 478, "合力方向＝平行填土面（與水平夾 β），不是水平", 16, INK, "start", "bold")
    # 右：力分解
    card(s, 670, 10, 520, 480)
    s.text(692, 48, "檢核前先拆成兩個分力", 20, INK, "start", "bold")
    ox, oy, L = 1080, 250, 380
    ex, ey = ox - L * math.cos(bt), oy + L * math.sin(bt)
    s.arrow(ox, oy, ex, ey, RES, 5, 18)
    s.arrow(ox, oy, ex, oy, RK, 3.5, 14)
    s.arrow(ex, oy, ex, ey, OK, 3.5, 14)
    s.line(ox, oy, ox - 150, oy, MUTED, 0)
    s.arc(ox, oy, 120, 180, 180 + BETA, INK, 1.6)
    s.text(ox - 136, oy + 24, "β", 18, INK, "end", "bold")
    s.text((ox + ex) / 2, oy - 18, f"P_h = P_a cosβ = {f1(PA_RS_H)}", 19, RK, "middle", "bold")
    s.text(ex - 10, (oy + ey) / 2 + 8, f"P_v = {f1(PA_RS_V)}", 19, OK, "end", "bold")
    s.text((ox + ex) / 2 + 30, (oy + ey) / 2 + 44, f"P_a = {f1(PA_RS)}", 19, RES, "middle", "bold")
    s.text(692, 400, "P_h：推牆滑動、造成傾覆", 16, RK, "start", "bold")
    s.text(692, 430, "P_v：向下壓在牆背上 → 增加抗滑、抗傾", 16, OK, "start", "bold")
    s.text(692, 462, "單位 kN/m；作用點仍在牆底上方 H/3", 14, MUTED)
    s.save(F + "fig07_slope.svg")


# ───────── F8 K_a vs β，β → φ 的邊界 ─────────
def fig_beta():
    s = SVG(1200, 460, ts=1.0)
    card(s, 10, 10, 1180, 440)
    X, Y = axes(s, 110, 70, 760, 300, (0, 35), (0.2, 1.0), range(0, 36, 5), np.round(np.arange(0.2, 1.01, 0.2), 1),
                "填土坡角 β (°)", "K_a", lambda v: f"{v}°", lambda v: f"{v:.1f}")
    s.rect(X(PHI), 70, X(35) - X(PHI), 300, fill="#FBECEA", stroke="none")
    s.line(X(PHI), 70, X(PHI), 370, PS, 2, "6,4")
    s.text(X(32.5), 118, "β ≥ φ", 18, PS, "middle", "bold")
    s.text(X(32.5), 148, "根號內 < 0", 14, PS, "middle")
    s.text(X(32.5), 172, "坡面自己", 14, PS, "middle")
    s.text(X(32.5), 194, "先滑動", 14, PS, "middle")
    bs = np.linspace(0, PHI, 301)
    curve(s, X, Y, bs, [ka_rs(PHI, b) for b in bs], RK, 3.4)
    curve(s, X, Y, bs, [ka_rs(PHI, b) * math.cos(rad(b)) for b in bs], RK, 2, "7,5")
    s.text(X(23), Y(ka_rs(PHI, 23) * math.cos(rad(23))) + 34, "虛線：水平分量 K_a cosβ", 14, RK, "start")
    for b, lab, dx in ((0, f"{f3(KA_R)}", 14), (BETA, f"{f3(KA_RS)}", 14), (PHI, f"cosφ = {f3(KA_RS_LIM)}", -14)):
        k = ka_rs(PHI, b)
        s.circle(X(b), Y(k), 8, fill=CL if b == BETA else RK)
        s.text(X(b) + dx, Y(k) - 14, lab, 17, CL if b == BETA else RK, "start" if dx > 0 else "end", "bold")
    s.text(X(BETA), Y(KA_RS) + 34, "本例 β = 15°", 15, CL, "middle", "bold")
    s.text(120, 430, f"φ = {PHI:.0f}°：β 由 0 增至 15°，K_a 只多 {((KA_RS / KA_R - 1) * 100):.0f}%；但接近 φ 時急遽上升", 16, INK, "start", "bold")
    # 右側說明
    s.text(905, 110, "為什麼 β 不能 ≥ φ？", 19, PS, "start", "bold")
    for i, l in enumerate(["無限邊坡的無凝聚力砂土，", "能站住的最大坡角就是 φ。", "β ≥ φ 時填土自己會滑，", "談不上「擋土」——", "公式的根號也跟著失效。"]):
        s.text(905, 150 + i * 30, l, 16, INK)
    s.text(905, 330, "β = φ：K_a = cosφ", 17, RK, "start", "bold")
    s.text(905, 360, f"（φ = 30° → {f3(KA_RS_LIM)}，約 2.6 倍）", 15, MUTED)
    s.save(F + "fig08_beta.svg")


def mini_wall(s, ox, oy, title, col):
    pass


# ───────── F9 被動土壓在哪裡＋要動多少 ─────────
def fig_passive():
    s = SVG(1200, 520, ts=1.0)
    card(s, 10, 10, 560, 500)
    s.text(32, 48, "被動土壓出現的兩個位置", 20, INK, "start", "bold")
    # (a) 懸臂式擋土牆牆趾
    gy_b, gy_f, by = 110, 330, 420        # 背填地表、前方地表、基礎底
    stem = 300
    s.rect(stem, gy_b, 250, by - 30 - gy_b, fill=SAND, stroke="none")
    s.rect(30, gy_f, stem - 30 + 250, by - gy_f + 30, fill=SAND2, stroke="none", op=0.6)
    s.rect(stem, gy_b, 250, by - gy_b, fill=SAND, stroke="none")
    s.rect(stem - 26, gy_b - 14, 26, by - 30 - gy_b + 14, fill=WALLc, stroke="none")
    s.rect(150, by - 30, 330, 30, fill=WALLc, stroke="none")
    hatch_ground(s, [(stem, gy_b), (550, gy_b)])
    hatch_ground(s, [(30, gy_f), (stem - 26, gy_f)])
    # 主動三角
    Hh = by - gy_b
    # 被動：牆趾前 Df
    Df = by - gy_f
    s.poly([(150, gy_f), (150, by), (150 - 95, by)], PS, 1.8, fill=PS, closed=True, op=0.18)
    s.arrow(60, by - Df / 3, 146, by - Df / 3, PS, 3.5, 13)
    s.text(40, by - Df / 3 - 14, "P_p", 19, PS, "start", "bold")
    s.line(185, gy_f, 185, by - 30, INK, 1.2)
    s.line(178, gy_f, 192, gy_f, INK, 1.2)
    s.text(193, gy_f + 36, "D_f", 17, INK, "start", "bold")
    s.arrow(stem + 150, by - Hh / 3 - 20, stem + 4, by - Hh / 3 - 20, OK, 3.5, 13)
    s.text(stem + 158, by - Hh / 3 - 14, "P_a", 19, OK, "start", "bold")
    s.text(32, 470, "① 擋土牆牆趾前方的埋置深度 D_f", 16, INK, "start", "bold")
    s.text(32, 498, "② 板樁／連續壁開挖面以下的貫入段（同一個道理）", 16, INK, "start", "bold")
    s.text(300, 90, "牆滑向左 → 牆趾推擠前方土", 14, MUTED, "start")

    # 右：位移—K 曲線
    card(s, 585, 10, 605, 500)
    s.text(607, 48, "要多少位移才發揮？（示意）", 20, INK, "start", "bold")
    X, Y = axes(s, 670, 90, 490, 300, (-0.01, 0.05), (0, 3.4), [-0.01, 0, 0.01, 0.02, 0.03, 0.04, 0.05], [0, 0.5, 1, 1.5, 2, 2.5, 3],
                "牆位移 Δ/H", "K", lambda v: f"{v:g}", lambda v: f"{v:g}")
    K0 = 1 - math.sin(rad(PHI))
    xa = np.linspace(-0.01, 0, 200)
    ya = [KA_R + (K0 - KA_R) * max(0, 1 - (abs(x) / 0.001)) ** 1.6 if abs(x) < 0.001 else KA_R for x in xa]
    xp = np.linspace(0, 0.05, 400)
    yp = [K0 + (KP_R - K0) * (1 - math.exp(-x / 0.009)) for x in xp]
    curve(s, X, Y, xa, ya, OK, 3.2)
    curve(s, X, Y, xp, yp, PS, 3.2)
    s.rect(X(0.02), 90, X(0.05) - X(0.02), 300, fill=PS, stroke="none", op=0.08)
    s.line(X(0), 90, X(0), 390, MUTED, 1.2, "4,4")
    s.line(670, Y(KP_R), 1160, Y(KP_R), PS, 1.2, "5,4")
    s.text(1160, Y(KP_R) - 8, f"K_p = {KP_R:.1f}", 15, PS, "end", "bold")
    s.text(X(0.035), Y(1.4), "0.02～0.05", 17, PS, "middle", "bold")
    s.text(X(0.035), Y(1.4) + 24, "才接近全額 K_p", 14, PS, "middle")
    s.text(X(-0.005), Y(0.33) - 14, "K_a", 16, OK, "middle", "bold")
    s.text(X(-0.005), Y(0.33) + 24, "≈ 0.001", 14, OK, "middle", "bold")
    s.text(X(0.002), Y(K0) - 10, "K_0", 15, INK, "start", "bold")
    s.text(682, 110, "← 離開土", 14, OK, "start", "bold")
    s.text(X(0) + 8, Y(3.3) + 16, "推向土 →", 14, PS, "start", "bold")
    s.text(607, 470, f"本例主動：{H:.0f} m × 0.001 = {DA_ACT:.0f} mm", 16, OK, "start", "bold")
    s.text(607, 498, f"本例被動：{DF} m × (0.02～0.05) = {DP_LO:.0f}～{DP_HI:.0f} mm", 16, PS, "start", "bold")
    s.save(F + "fig09_passive.svg")


# ───────── F10 K_p 對 φ 的敏感度 ─────────
def fig_kphi():
    s = SVG(1200, 470, ts=1.0)
    card(s, 10, 10, 1180, 450)
    X, Y = axes(s, 100, 60, 700, 320, (20, 45), (0, 6), range(20, 46, 5), range(0, 7),
                "內摩擦角 φ (°)", "K", lambda v: f"{v}°")
    ph = np.linspace(20, 45, 251)
    curve(s, X, Y, ph, [math.tan(rad(45 + p / 2)) ** 2 for p in ph], PS, 3.6)
    curve(s, X, Y, ph, [math.tan(rad(45 - p / 2)) ** 2 for p in ph], OK, 3.6)
    s.text(X(44.5), Y(5.83) + 34, "K_p", 20, PS, "end", "bold")
    s.text(X(44.5), Y(0.17) - 14, "K_a", 20, OK, "end", "bold")
    for p, kp, ka in ((30, KP_R, KA_R), (40, KP_R40, KA_R40)):
        s.line(X(p), Y(kp), X(p), Y(0), MUTED, 1.2, "4,4")
        s.circle(X(p), Y(kp), 8, fill=PS)
        s.circle(X(p), Y(ka), 7, fill=OK)
        s.text(X(p) - 12, Y(kp) - 12, f"{kp:.2f}", 18, PS, "end", "bold")
        s.text(X(p) + 10, Y(ka) - 12, f"{ka:.3f}", 15, OK, "start", "bold")
    # 標註增量
    s.line(X(42), Y(KP_R), X(42), Y(KP_R40), PS, 2)
    s.line(X(30), Y(KP_R), X(42.6), Y(KP_R), PS, 1, "3,3")
    s.line(X(40), Y(KP_R40), X(42.6), Y(KP_R40), PS, 1, "3,3")
    s.text(X(42) + 10, (Y(KP_R) + Y(KP_R40)) / 2 + 8, f"+{(KP_R40 / KP_R - 1) * 100:.0f}%", 22, PS, "start", "bold")
    # 右欄
    x0 = 840
    s.text(x0, 90, "φ 高估 10°（30° → 40°）", 19, INK, "start", "bold")
    s.text(x0, 140, f"K_p：{KP_R:.2f} → {KP_R40:.2f}", 19, PS, "start", "bold")
    s.text(x0, 172, f"增加 {(KP_R40 / KP_R - 1) * 100:.0f}%", 16, PS)
    s.text(x0, 222, f"K_a：{KA_R:.3f} → {KA_R40:.3f}", 19, OK, "start", "bold")
    s.text(x0, 254, f"只差 {KA_R - KA_R40:.2f}", 16, OK)
    s.text(x0, 310, f"本例 D_f = {DF} m 的 P_p：", 16, INK, "start", "bold")
    s.text(x0, 342, f"{f1(PP_FULL)} → {f1(PP_40)} kN/m", 19, PS, "start", "bold")
    s.text(x0, 400, "被動側：參數誤差被放大", 17, PS, "start", "bold")
    s.text(x0, 428, "→ 最不能樂觀的地方", 17, PS, "start", "bold")
    s.text(110, 440, "K_p = tan²(45° + φ/2) 的斜率遠大於 K_a，而且 φ 越大越陡", 16, MUTED)
    s.save(F + "fig10_kphi.svg")


# ───────── F11 Coulomb 平面破壞面高估 K_p ─────────
def fig_kpdelta():
    s = SVG(1200, 480, ts=1.0)
    card(s, 10, 10, 520, 460)
    s.text(32, 48, "被動破壞面：平面 vs 曲面", 20, INK, "start", "bold")
    wx, by, Hp = 460, 300, 125
    gy = by - Hp
    s.rect(30, gy, wx - 30, Hp + 90, fill=SAND, stroke="none")
    s.rect(wx, gy, 50, Hp + 90, fill=SAND, stroke="none")
    dots(s, 40, gy + 8, wx - 8, by + 80, 55, 11)
    s.rect(wx, gy - 40, 28, Hp + 40, fill=WALLc, stroke="none")
    hatch_ground(s, [(30, gy), (wx, gy)])
    s.arrow(wx + 70, gy + 40, wx + 32, gy + 40, INK, 3, 12)
    s.text(wx + 40, gy + 22, "推", 16, INK, "start", "bold")
    # 平面（Coulomb，δ=20°）
    _, rh, rhos, Ps = trial(H, G, PHI, DELTA, 0, 0, "p")
    P = np.where(Ps > 0, Ps, np.nan); i = np.nanargmin(P); rp = rhos[i]
    L = Hp / math.tan(rp)
    s.line(wx, by, wx - L, gy, CL, 2.6, "9,6")
    # 曲面（示意：對數螺線）——起點切線較陡、下凹
    P0 = (wx, by); P3 = (wx - 0.72 * L, gy)
    P1 = (wx - 0.28 * L, by + 38)
    a30 = rad(45 - PHI / 2); P2 = (P3[0] + 0.22 * L * math.cos(a30), gy + 0.22 * L * math.sin(a30))
    pts = []
    for u in np.linspace(0, 1, 80):
        b = [(1 - u) ** 3, 3 * u * (1 - u) ** 2, 3 * u * u * (1 - u), u ** 3]
        pts.append((sum(bb * p[0] for bb, p in zip(b, (P0, P1, P2, P3))), sum(bb * p[1] for bb, p in zip(b, (P0, P1, P2, P3)))))
    s.poly(pts, PS, 3)
    s.text(wx - L - 2, gy - 14, "Coulomb 平面（δ = 20°）", 15, CL, "start", "bold")
    s.text(wx - 0.45 * L, by + 70, "實際：曲面（對數螺線）", 15, PS, "middle", "bold")
    s.text(32, 420, "δ 大時，真實破壞面彎曲得更明顯；", 16, INK)
    s.text(32, 448, "硬套平面 → 抗力算太大（偏不安全）", 16, PS, "start", "bold")
    # 右：Kp vs δ
    card(s, 545, 10, 645, 460)
    s.text(567, 48, f"K_p 隨 δ 的變化（φ = {PHI:.0f}°）", 20, INK, "start", "bold")
    X, Y = axes(s, 630, 90, 510, 290, (0, 30), (0, 11), range(0, 31, 5), range(0, 12, 2),
                "牆背摩擦角 δ (°)", "K_p", lambda v: f"{v}°")
    ds = np.linspace(0, 30, 121)
    curve(s, X, Y, ds, [kp_c(PHI, d, 0, 0) for d in ds], CL, 3.4)
    curve(s, X, Y, ds, [KP_R] * len(ds), RK, 3, "8,5")
    s.text(X(30), Y(KP_R) + 26, f"Rankine {KP_R:.1f}（δ = 0）", 15, RK, "end", "bold")
    s.text(X(28), Y(kp_c(PHI, 28, 0, 0)) - 4, "Coulomb 平面解", 15, CL, "end", "bold")
    for d in (DELTA, PHI):
        k = kp_c(PHI, d, 0, 0)
        s.circle(X(d), Y(k), 8, fill=CL)
        s.text(X(d) - 12, Y(k) + 6, f"{k:.2f}", 17, CL, "end", "bold")
    s.text(X(DELTA), Y(KP_C) + 32, f"δ = 20°：{KP_C / KP_R:.1f} 倍", 15, CL, "middle", "bold")
    s.text(567, 448, "同一 φ，只因多給一個 δ，K_p 就翻倍 → 這個「多」不可靠", 15, MUTED)
    s.save(F + "fig11_kpdelta.svg")


# ───────── F12 設計打折瀑布 ─────────
def fig_cut():
    s = SVG(1200, 470, ts=1.0)
    card(s, 10, 10, 800, 450)
    s.text(32, 48, f"本例牆趾前 D_f = {DF} m 的被動抗力（kN/m）", 20, INK, "start", "bold")
    bars = [("Coulomb 平面", "δ = 20°", PP_C, CL, True),
            ("Rankine 全額", "½K_pγD_f²", PP_FULL, RK, False),
            ("忽略表層", f"頂部 {DIGNORE} m 不計", PP_IGN, PS, False),
            ("再打折", "× 1/2", PP_DES, OK, False)]
    x0, y0, hh, top = 90, 80, 300, 140
    Y = lambda v: y0 + hh - v / top * hh
    for v in (0, 20, 40, 60, 80, 100, 120, 140):
        s.line(x0, Y(v), 790, Y(v), GRID, 1)
        s.text(x0 - 10, Y(v) + 5, str(v), 14, MUTED, "end")
    s.line(x0, Y(PA_R), 790, Y(PA_R), INK, 1.6, "7,5")
    s.text(786, Y(PA_R) - 8, f"對照：主動推力 P_a = {f1(PA_R)}", 14, INK, "end", "bold")
    bw, gap = 120, 52
    for i, (a, b, v, col, bad) in enumerate(bars):
        x = x0 + 30 + i * (bw + gap)
        s.rect(x, Y(v), bw, Y(0) - Y(v), fill=col, stroke=col, sw=1.5, op=0.25 if bad else 0.85)
        if bad:
            for k in range(0, int(Y(0) - Y(v)), 14):
                s.line(x, Y(v) + k, x + min(bw, Y(0) - Y(v) - k), Y(v) + k + min(bw, Y(0) - Y(v) - k), col, 1)
        s.text(x + bw / 2, Y(v) - 10, f1(v), 19, col, "middle", "bold")
        s.text(x + bw / 2, Y(0) + 28, a, 16, INK, "middle", "bold")
        s.text(x + bw / 2, Y(0) + 52, b, 14, MUTED, "middle")
        if i >= 2:
            px = x0 + 30 + (i - 1) * (bw + gap) + bw
            s.arrow(px + 6, Y(bars[i - 1][2]) + 10, x - 6, Y(v) - 4, GREY, 2, 10)
    s.text(x0 + 30 + bw / 2, Y(PP_C) - 36, "不可採", 15, CL, "middle", "bold")
    # 右：表層忽略示意
    card(s, 825, 10, 365, 450)
    s.text(847, 48, "表層為什麼不算？", 20, INK, "start", "bold")
    gx, gy, bt = 960, 110, 400
    sc = (bt - gy) / DF
    s.rect(905, gy, 190, bt - gy, fill=SAND2, stroke="none", op=0.6)
    s.rect(905, gy, 190, DIGNORE * sc, fill="#FFFFFF", stroke=PS, sw=1.5, dash="6,4")
    s.text(1000, gy + DIGNORE * sc / 2 + 6, "可能被挖、擾動", 14, PS, "middle", "bold")
    s.rect(1095, gy - 10, 26, bt - gy + 10, fill=WALLc, stroke="none")
    yi = gy + DIGNORE * sc
    w = 150 / (KP_R * G * DF)
    s.poly([(1095, yi), (1095, bt), (1095 - KP_R * G * (DF - DIGNORE) * w, bt)], PS, 2, fill=PS, closed=True, op=0.25)
    s.text(1095 - KP_R * G * (DF - DIGNORE) * w - 6, bt - 10, f"{KP_R * G * (DF - DIGNORE):.0f} kPa", 14, PS, "end", "bold")
    s.line(890, gy, 890, yi, INK, 1.2); s.text(884, (gy + yi) / 2 + 6, f"{DIGNORE} m", 14, INK, "end", "bold")
    s.line(890, yi, 890, bt, INK, 1.2); s.text(884, (yi + bt) / 2 + 6, f"{DF - DIGNORE:.1f} m", 14, INK, "end", "bold")
    s.text(847, 430, f"½ × {KP_R:.0f} × {G:.0f} × {DF - DIGNORE:.1f}² = {f1(PP_IGN)}", 16, PS, "start", "bold")
    s.save(F + "fig12_cut.svg")


# ───────── F13 全單元貫通：四塊拼圖的執行順序 ─────────
def fig_chain():
    s = SVG(1200, 380, ts=1.0)
    cards = [("1", "拼圖一 變形", "牆動不動得了？", "K_a / K_0 / K_p", "#2F54C8"),
             ("2", "拼圖四 邊界", "牆背、填土什麼幾何？", "Rankine / Coulomb", "#C0392B"),
             ("3", "拼圖二 土質", "砂？黏土？有水？", "畫出 σ 分布圖", "#B8520E"),
             ("4", "拼圖三 SOP", "切方塊、對牆底取矩", "P 與作用點", "#2E7D6B")]
    w, gap, x = 258, 46, 14
    for i, (n, t, q, out, col) in enumerate(cards):
        card(s, x, 20, w, 340, fill="#FFFFFF" if i == 1 else PANEL, stroke=col if i == 1 else LINE, sw=3 if i == 1 else 1.5)
        s.circle(x + 40, 66, 22, fill=col, stroke="none")
        s.text(x + 40, 74, n, 22, "#FFFFFF", "middle", "bold")
        s.text(x + 74, 76, t, 23, col, "start", "bold")
        s.text(x + w / 2, 140, q, 17, MUTED, "middle")
        s.line(x + 24, 172, x + w - 24, 172, GRID, 1.5)
        s.text(x + w / 2, 225, "輸出", 15, MUTED, "middle")
        s.text(x + w / 2, 270, out, 21, INK, "middle", "bold")
        if i < 3: s.arrow(x + w + 7, 190, x + w + gap - 7, 190, GREY, 3, 14)
        x += w + gap
    s.text(14 + w + gap + w / 2, 330, "第二步就決定公式", 15, PS, "middle", "bold")
    s.save(F + "fig13_chain.svg")

if __name__ == "__main__":
    which = sys.argv[1:] or None
    for name, fn in list(globals().items()):
        if name.startswith("fig_") and (not which or name[4:] in which):
            fn()
    print("figs done")
