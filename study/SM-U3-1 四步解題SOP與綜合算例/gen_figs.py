"""SM-U3-1 側向土壓力 四步解題 SOP — 向量圖產生器（示範題數字全部取自 params.py）"""
import math, json
from params import *
from svglib import *

F = "figs/"
f1 = lambda v: f"{v:.1f}"
f2 = lambda v: f"{v:.2f}"
KAc, K0c, KPc = "#2F54C8", "#2E7D6B", "#C0392B"     # 主動・靜止・被動
REC, TRI, RES = "#3B6FD4", "#2E9C7A", "#E4572E"      # 矩形塊・三角塊・合力
WALLc = "#34495E"
S1c, S2c = "#F1E4C9", "#E6CFA0"
WATc = "#0891B2"                      # 上層、下層土色
STEPc = ["#2F54C8", "#B8520E", "#2E7D6B", "#C0392B"]

def hatch_ground(s, x1, x2, y, step=16):
    s.line(x1, y, x2, y, INK, 2)
    x = x1
    while x < x2 - 4:
        s.line(x + 4, y, x + 14, y - 10, INK, 1.2); x += step

def wall(s, x, y1, y2, w=14):
    s.rect(x - w, y1, w, y2 - y1, fill=WALLc, stroke="none")

# ───────── F1 四步 SOP 總覽 ─────────
def fig_sop():
    s = SVG(1200, 340, ts=1.1)
    cards = [
        ("1", "確定 K", "牆能不能動？往哪動？", "K_a", "牆頂可外傾 → 主動"),
        ("2", "列轉折點", "σ_a 只在這些深度轉彎", "4 個深度", "0 / 3上 / 3下 / 7 m"),
        ("3", "逐點算 σ_a", "有效 × K，水壓另加", f"{f1(SA0)} → {f1(SA7)}", "kPa（3 m 處跳一次）"),
        ("4", "切方塊取矩", "對牆底，一個基準到底", f"ȳ = {f2(YBAR)} m", f"P = {f1(P)} kN/m"),
    ]
    w, gap, x = 252, 51, 16
    for i, (n, t, q, big, sub) in enumerate(cards):
        col = STEPc[i]
        s.rect(x, 20, w, 300, fill=PANEL, stroke="#D5DAE1", sw=1.5, rx=14)
        s.circle(x + 40, 66, 22, fill=col, stroke="none")
        s.text(x + 40, 74, n, 22, "#FFFFFF", "middle", "bold")
        s.text(x + 74, 75, t, 25, col, "start", "bold")
        s.text(x + w / 2, 128, q, 16, MUTED, "middle")
        s.line(x + 24, 150, x + w - 24, 150, GRID, 1.5)
        s.text(x + w / 2, 212, big, 30, INK, "middle", "bold")
        s.text(x + w / 2, 280, sub, 15, col, "middle", "bold")
        if i < 3:
            s.arrow(x + w + 8, 170, x + w + gap - 8, 170, "#9AA3AE", 3, 14)
        x += w + gap
    s.save(F + "fig01_sop.svg")

# ───────── F2 確定 K：三種牆況 ─────────
def fig_k():
    s = SVG(1200, 480, ts=1.15)
    phi = 30
    Ka = math.tan(math.radians(45 - phi / 2)) ** 2
    K0 = 1 - math.sin(math.radians(phi))
    Kp = math.tan(math.radians(45 + phi / 2)) ** 2
    panels = [
        ("主動 K_a", "牆離開土（外傾）", "一般擋土牆・懸臂板樁", KAc, "act"),
        ("靜止 K_0", "牆完全不能動", "地下室外牆・箱涵", K0c, "rest"),
        ("被動 K_p", "牆被推向土", "錨碇前方・牆趾前土", KPc, "pas"),
    ]
    pw = 380
    for i, (t, d, ex, col, mode) in enumerate(panels):
        x0 = 15 + i * (pw + 10)
        s.rect(x0, 10, pw, 330, fill=PANEL, stroke="#D5DAE1", sw=1.2, rx=12)
        gy, by = 90, 290          # 地表、牆底
        wx = x0 + 120             # 牆背
        s.rect(wx, gy, x0 + pw - 20 - wx, by - gy, fill=S1c, stroke="none")
        hatch_ground(s, wx, x0 + pw - 20, gy)
        if mode == "act":
            tilt = 16
            s.poly([(wx - 14 - tilt, gy - 20), (wx - tilt, gy - 20), (wx, by), (wx - 14, by)], color=WALLc, fill=WALLc, closed=True, sw=1)
            s.rect(wx - 14, gy - 20, 14, by - gy + 20, stroke=WALLc, sw=1.2, dash="4,3")
            s.arrow(wx - 30, gy + 10, wx - 72, gy + 10, col, 3, 13)
            # 破壞楔 45+φ/2 = 60°
            a = math.radians(45 + phi / 2); L = (by - gy) / math.tan(a)
            s.line(wx, by, wx + L, gy, col, 2, "7,5")
            s.text(wx + L + 6, gy + 28, "45°+φ/2", 14, col, "start", "bold")
        elif mode == "rest":
            wall(s, wx, gy - 20, by)
            for yy in (gy + 50, gy + 140):
                s.rect(wx - 95, yy, 81, 10, fill="#9AA3AE", stroke="none")
            s.text(wx - 55, gy + 44, "樓板", 13, MUTED, "middle")
            s.text(wx - 55, gy + 134, "樓板", 13, MUTED, "middle")
            s.text(wx - 55, by - 20, "位移 ≈ 0", 14, col, "middle", "bold")
        else:
            tilt = 16
            s.poly([(wx - 14 + tilt, gy - 20), (wx + tilt, gy - 20), (wx, by), (wx - 14, by)], color=WALLc, fill=WALLc, closed=True, sw=1)
            s.rect(wx - 14, gy - 20, 14, by - gy + 20, stroke=WALLc, sw=1.2, dash="4,3")
            s.arrow(wx - 80, gy + 10, wx - 30, gy + 10, col, 3, 13)
            a = math.radians(45 - phi / 2); L = (by - gy) / math.tan(a)
            Lc = min(L, x0 + pw - 30 - wx)
            s.line(wx, by, wx + Lc, by - Lc * math.tan(a), col, 2, "7,5")
            s.text(wx + Lc - 4, by - Lc * math.tan(a) - 10, "45°−φ/2", 14, col, "end", "bold")
        s.line(x0 + 20, by, x0 + pw - 20, by, INK, 2)
        s.text(x0 + 20, 48, t, 24, col, "start", "bold")
        s.text(x0 + pw - 20, 48, d, 15, MUTED, "end")
        s.text(x0 + pw / 2, 322, ex, 16, INK, "middle", "bold")
    # K 數線（φ = 30°）
    y = 410; xa, xb = 90, 1110
    X = lambda k: xa + (k / 3.2) * (xb - xa)
    s.line(xa, y, xb, y, "#5B6573", 2.5)
    for k in (0, 1, 2, 3):
        s.line(X(k), y - 6, X(k), y + 6, "#5B6573", 1.5); s.text(X(k), y + 28, str(k), 14, "#9AA3AE", "middle")
    s.text(xa - 16, y + 6, "K", 18, INK, "end", "bold")
    for k, lab, col, dy in ((Ka, f"K_a = {Ka:.2f}", KAc, -18), (K0, f"K_0 = {K0:.2f}", K0c, -44), (Kp, f"K_p = {Kp:.2f}", KPc, -18)):
        s.circle(X(k), y, 9, fill=col)
        s.text(X(k), y + dy, lab, 16, col, "middle", "bold")
    s.text(xb, y + 58, "以 φ = 30° 為例：K_p 是 K_a 的 9 倍", 15, MUTED, "end")
    s.save(F + "fig02_k.svg")

# ───────── F3 轉折點清單（一般剖面，形狀由實際函數算出）─────────
def fig_breaks():
    s = SVG(1030, 560, ts=1.15)
    # 一般剖面：黏土 0–4 m（c=12, φ=20°, γ=18）；砂 4–8 m（φ=30°, γsat=20）；q=10；水位 3 m
    q, c1, g1, gs1, g2 = 10.0, 12.0, 18.0, 19.0, 20.0
    K1 = math.tan(math.radians(35)) ** 2; K2 = 1 / 3; zw, zi, Hh = 3.0, 4.0, 8.0; gw = 9.81
    def sv_eff(z):
        if z <= zw: return q + g1 * z
        if z <= zi: return q + g1 * zw + (gs1 - gw) * (z - zw)
        return q + g1 * zw + (gs1 - gw) * (zi - zw) + (g2 - gw) * (z - zi)
    def eff(z, below=False):
        if z < zi or (z == zi and not below):
            return max(0.0, K1 * sv_eff(z) - 2 * c1 * math.sqrt(K1))
        return K2 * sv_eff(z)
    u = lambda z: max(0.0, z - zw) * gw
    zc = (2 * c1 * math.sqrt(K1) / K1 - q) / g1
    y0, ky = 70, 56; Y = lambda z: y0 + z * ky
    # 左：剖面
    lx, rx = 50, 260
    s.rect(lx, Y(0), rx - lx, Y(zi) - Y(0), fill="#D9C7B0", stroke="none")
    s.rect(lx, Y(zi), rx - lx, Y(Hh) - Y(zi), fill=S1c, stroke="none")
    wall(s, lx, Y(0) - 20, Y(Hh))
    for xx in range(lx + 10, rx, 26):
        s.arrow(xx, Y(0) - 44, xx, Y(0) - 4, "#B8520E", 1.6, 8)
    s.text(rx, Y(0) - 50, "超載 q", 15, "#B8520E", "end", "bold")
    hatch_ground(s, lx, rx, Y(0))
    s.text((lx + rx) / 2, Y(2.2), "黏土（c, φ）", 16, INK, "middle", "bold")
    s.text((lx + rx) / 2, Y(6.2), "砂（φ）", 16, INK, "middle", "bold")
    # 張力裂縫示意
    for xx in (lx + 45, lx + 110, lx + 175):
        s.poly([(xx, Y(0)), (xx + 5, Y(zc * 0.5)), (xx - 2, Y(zc * 0.8)), (xx + 2, Y(zc))], color="#7A5C3A", sw=1.6)
    s.line(lx, Y(zw), rx, Y(zw), WATER, 2, "8,5")
    s.poly([(rx - 30, Y(zw) - 12), (rx - 18, Y(zw) - 12), (rx - 24, Y(zw) - 2)], color=WATER, fill=WATER, closed=True, sw=1)
    s.line(lx, Y(Hh), rx, Y(Hh), INK, 2)
    # 中：σa 分布（有效＋水壓）
    px0, kx = 320, 2.8
    pts_e = []
    zs = [i / 100 for i in range(0, int(zi * 100) + 1)]
    for z in zs: pts_e.append((px0 + kx * eff(z), Y(z)))
    zs2 = [zi + i / 100 for i in range(0, int((Hh - zi) * 100) + 1)]
    pts_e2 = [(px0 + kx * eff(z, below=True), Y(z)) for z in zs2]
    # 有效土壓面
    s.poly([(px0, Y(0))] + pts_e + [(px0, Y(zi))], color="none", fill=KAc, closed=True, op=0.22, sw=0)
    s.poly([(px0, Y(zi))] + pts_e2 + [(px0, Y(Hh))], color="none", fill=KAc, closed=True, op=0.22, sw=0)
    # 水壓疊加在外側
    tot1 = [(px0 + kx * (eff(z) + u(z)), Y(z)) for z in zs if z >= zw]
    tot2 = [(px0 + kx * (eff(z, True) + u(z)), Y(z)) for z in zs2]
    s.poly(pts_e[int(zw * 100):] + list(reversed(tot1)), color="none", fill=WATc, closed=True, op=0.3, sw=0)
    s.poly(pts_e2 + list(reversed(tot2)), color="none", fill=WATc, closed=True, op=0.3, sw=0)
    s.poly(pts_e[:int(zw * 100) + 1] + tot1, color=INK, sw=2.5)
    s.poly(tot2, color=INK, sw=2.5)
    s.line(pts_e[-1][0] + kx * u(zi), Y(zi), tot2[0][0], Y(zi), INK, 2.5)
    s.line(px0, Y(0) - 10, px0, Y(Hh) + 4, INK, 2)
    s.line(px0, Y(Hh), tot2[-1][0], Y(Hh), INK, 2)
    s.text(px0 + 12, Y(7.4), "有效 × K", 14, KAc, "start", "bold")
    s.text(px0 + kx * (eff(6.8, True) + u(6.8) / 2), Y(6.8), "u 另加", 14, WATc, "middle", "bold")
    # 右：轉折點清單
    marks = [
        (0, "①", "地表 / 超載面", "K·q − 2c√K 為負 → 有裂縫", "#B8520E"),
        (zc, "②", "張力裂縫 z_c", f"σ_a = 0 的深度（本例 ≈ {zc:.2f} m）", "#7A5C3A"),
        (zw, "③", "地下水位面", "以下改用 γ′，並開始加 u", WATER),
        (zi, "④", "土層交界面", "上下各算一次（K、c 換了）", "#C0392B"),
        (Hh, "⑤", "牆底", "取矩的基準點", INK),
    ]
    tx = 600
    for z, n, t, d, col in marks:
        s.line(lx - 14, Y(z), tx - 16, Y(z), col, 1.2, "3,4")
        s.circle(tx + 8, Y(z), 15, fill=col, stroke="none")
        s.text(tx + 8, Y(z) + 6, n, 16, "#FFFFFF", "middle", "bold")
        s.text(tx + 34, Y(z) - 2, t, 19, col, "start", "bold")
        s.text(tx + 34, Y(z) + 22, d, 14, MUTED, "start")
    s.text(px0 + 100, Y(0) - 30, "σ_a（示意）", 15, MUTED, "middle", "bold")
    s.save(F + "fig03_breaks.svg")
    return zc

# ───────── F4 有效 × K，水壓另加（小例：砂 H=6 m、水位 2 m）─────────
def fig_water():
    s = SVG(1200, 470)
    g, gs, gw, K, Hh, zw = 18.0, 20.0, 9.81, 1 / 3, 6.0, 2.0
    se2 = K * g * zw
    sv6 = g * zw + (gs - gw) * (Hh - zw)
    se6 = K * sv6; u6 = gw * (Hh - zw)
    y0, ky, kx = 60, 55, 4.2
    Y = lambda z: y0 + z * ky
    def axes(x0, xmax_val, title, col):
        s.line(x0, Y(0) - 6, x0, Y(Hh), INK, 2)
        s.line(x0, Y(Hh), x0 + kx * xmax_val + 10, Y(Hh), INK, 1.5)
        s.text(x0 + 60, Y(0) - 22, title, 17, col, "middle", "bold")
        s.line(x0 - 8, Y(zw), x0 + kx * xmax_val + 14, Y(zw), WATER, 1.3, "6,4")
    # 有效
    x1 = 70
    axes(x1, se6, "有效土壓 K·σ_v′", KAc)
    s.poly([(x1, Y(0)), (x1 + kx * se2, Y(zw)), (x1 + kx * se6, Y(Hh)), (x1, Y(Hh))], color=KAc, fill=KAc, closed=True, op=0.25)
    s.text(x1 + kx * se2 + 10, Y(zw) + 5, f"{f1(se2)}", 15, KAc, "start", "bold", bg="#FFFFFF")
    s.text(x1 + kx * se6 + 8, Y(Hh) - 4, f"{f1(se6)}", 15, KAc, "start", "bold")
    s.text(310, Y(3.5), "＋", 40, INK, "middle", "bold")
    # 水壓
    x2 = 370
    axes(x2, u6, "孔隙水壓 u（×1）", WATc)
    s.poly([(x2, Y(zw)), (x2 + kx * u6, Y(Hh)), (x2, Y(Hh))], color=WATc, fill=WATc, closed=True, op=0.3)
    s.text(x2 + kx * u6 + 8, Y(Hh) - 4, f"{f1(u6)}", 15, WATc, "start", "bold")
    s.text(620, Y(3.5), "＝", 40, INK, "middle", "bold")
    # 總和
    x3 = 680
    tot = se6 + u6
    axes(x3, tot, "側向總壓 σ_a", INK)
    s.poly([(x3, Y(0)), (x3 + kx * se2, Y(zw)), (x3 + kx * se6, Y(Hh)), (x3, Y(Hh))], color="none", fill=KAc, closed=True, op=0.25, sw=0)
    s.poly([(x3 + kx * se2, Y(zw)), (x3 + kx * tot, Y(Hh)), (x3 + kx * se6, Y(Hh))], color="none", fill=WATc, closed=True, op=0.3, sw=0)
    s.poly([(x3, Y(0)), (x3 + kx * se2, Y(zw)), (x3 + kx * tot, Y(Hh))], color=INK, sw=2.5)
    s.text(x3 + kx * tot + 8, Y(Hh) - 4, f"{f1(tot)} kPa", 16, INK, "start", "bold")
    # 錯誤對照
    wrong = K * (g * zw + gs * (Hh - zw))
    bx = 960
    s.rect(bx, 90, 225, 300, fill="#FBECEA", stroke="#E6B0AA", sw=1.2, rx=10)
    s.text(bx + 112, 122, "常見錯誤", 18, "#C0392B", "middle", "bold")
    s.text(bx + 16, 160, "用 γ_{sat} 算 σ_v 再乘 K，", 14, INK)
    s.text(bx + 16, 182, "等於水壓也被 K 打了折：", 14, INK)
    s.text(bx + 112, 225, f"K·(18×2 + 20×4)", 15, MUTED, "middle")
    s.text(bx + 112, 252, f"= {f1(wrong)} kPa", 20, "#C0392B", "middle", "bold")
    s.text(bx + 112, 292, f"正確 {f1(tot)} kPa", 16, INK, "middle", "bold")
    s.text(bx + 112, 322, f"少算 {f1(tot - wrong)} kPa（{(tot - wrong) / tot * 100:.0f}%）", 16, "#C0392B", "middle", "bold")
    s.text(bx + 112, 362, "水沒有剪力強度 → 各向等壓", 13, MUTED, "middle")
    s.text(60, 440, f"小例：砂 γ = 18、γ_{{sat}} = 20 kN/m³，K_a = 1/3，水位在地表下 2 m，牆高 6 m（γ_w = 9.81）", 15, MUTED)
    s.save(F + "fig04_water.svg")
    return dict(se2=se2, se6=se6, u6=u6, tot=tot, wrong=wrong)

# ───────── F5 切方塊原理：梯形 = 矩形 + 三角形 ─────────
def fig_rule():
    s = SVG(1200, 440)
    a, b, h = 80, 200, 260       # 像素：上邊、下邊、高
    y0 = 80; yb = y0 + h
    # 梯形
    x0 = 70
    s.poly([(x0, y0), (x0 + a, y0), (x0 + b, yb), (x0, yb)], color=INK, fill="#E7ECF3", closed=True, sw=2)
    s.text(x0 + a / 2, y0 - 12, "a", 20, INK, "middle", "bold")
    s.text(x0 + b / 2, yb + 30, "b", 20, INK, "middle", "bold")
    s.dim(x0 - 22, y0, x0 - 22, yb, "", INK, 16)
    s.text(x0 - 34, (y0 + yb) / 2 + 6, "h", 20, INK, "end", "bold")
    s.text(305, (y0 + yb) / 2 + 12, "＝", 40, INK, "middle", "bold")
    # 矩形
    x1 = 340
    s.rect(x1, y0, a, h, fill=REC, stroke=REC, sw=2, op=0.3)
    cy = y0 + h / 2
    s.circle(x1 + a / 2, cy, 7, fill=REC)
    s.dim(x1 + a + 26, yb, x1 + a + 26, cy, "", REC)
    s.text(x1 + a + 36, (yb + cy) / 2 + 6, "h/2", 18, REC, "start", "bold")
    s.text(x1 + a / 2, yb + 30, "a·h", 18, REC, "middle", "bold")
    s.text(x1 + 200, (y0 + yb) / 2 + 12, "＋", 40, INK, "middle", "bold")
    # 三角形
    x2 = 600
    s.poly([(x2, y0), (x2 + b - a, yb), (x2, yb)], color=TRI, fill=TRI, closed=True, op=0.3, sw=2)
    ty = yb - h / 3
    s.circle(x2 + (b - a) / 3, ty, 7, fill=TRI)
    s.dim(x2 + b - a + 26, yb, x2 + b - a + 26, ty, "", TRI)
    s.text(x2 + b - a + 36, (yb + ty) / 2 + 6, "h/3", 18, TRI, "start", "bold")
    s.text(x2 + (b - a) / 2, yb + 30, "½(b−a)·h", 18, TRI, "middle", "bold")
    # 右側要點
    bx = 900
    s.rect(bx, 60, 285, 320, fill=PANEL, stroke="#D5DAE1", sw=1.2, rx=12)
    s.text(bx + 20, 98, "兩個只需要記的形心", 18, INK, "start", "bold")
    s.text(bx + 20, 140, "矩形：高度一半", 16, REC, "start", "bold")
    s.text(bx + 20, 178, "三角形：距「寬邊」h/3", 16, TRI, "start", "bold")
    s.text(bx + 20, 204, "（寬邊在下 → 距底 h/3；", 14, MUTED)
    s.text(bx + 20, 226, "　寬邊在上 → 距底 2h/3）", 14, MUTED)
    s.line(bx + 20, 252, bx + 265, 252, GRID, 1.5)
    s.text(bx + 20, 288, "所有 y_i 都從「牆底」量", 16, RES, "start", "bold")
    s.text(bx + 20, 314, "上層方塊要加下層厚度，", 14, MUTED)
    s.text(bx + 20, 336, "例如 y_A = 4 + 3/2", 14, MUTED)
    s.save(F + "fig05_rule.svg")

# ───────── 示範題共用 ─────────
Y0, KY = 90, 62
def Yd(z): return Y0 + z * KY

# ───────── F6 示範題剖面 ─────────
def fig_problem():
    s = SVG(980, 580, ts=1.25)
    wx, rx = 170, 560
    s.rect(wx, Yd(0), rx - wx, H1 * KY, fill=S1c, stroke="none")
    s.rect(wx, Yd(H1), rx - wx, H2 * KY, fill=S2c, stroke="none")
    wall(s, wx, Yd(0) - 24, Yd(H) + 2, 18)
    s.rect(wx - 70, Yd(H), 130, 22, fill="#9AA3AE", stroke="none")
    for xx in range(wx + 20, rx, 34):
        s.arrow(xx, Yd(0) - 52, xx, Yd(0) - 4, "#B8520E", 1.8, 9)
    s.text((wx + rx) / 2, Yd(0) - 62, f"q = {Q:.0f} kPa", 18, "#B8520E", "middle", "bold")
    hatch_ground(s, wx, rx, Yd(0))
    s.line(wx, Yd(H1), rx, Yd(H1), INK, 1.5, "8,5")
    s.text((wx + rx) / 2, Yd(1.3), "土層 1", 20, INK, "middle", "bold")
    s.text((wx + rx) / 2, Yd(2.0), "γ_1 = 17 kN/m³　K_{a1} = 1/3", 17, INK, "middle")
    s.text((wx + rx) / 2, Yd(4.9), "土層 2", 20, INK, "middle", "bold")
    s.text((wx + rx) / 2, Yd(5.6), "γ_2 = 19 kN/m³　K_{a2} = 0.26", 17, INK, "middle")
    s.dim(rx + 30, Yd(0), rx + 30, Yd(H1), "", INK)
    s.text(rx + 42, Yd(1.5) + 6, "3 m", 17, INK, "start", "bold")
    s.dim(rx + 30, Yd(H1), rx + 30, Yd(H), "", INK)
    s.text(rx + 42, Yd(5) + 6, "4 m", 17, INK, "start", "bold")
    s.dim(wx - 140, Yd(0), wx - 140, Yd(H), "", INK)
    s.text(wx - 130, Yd(3.5) + 6, "H = 7 m", 17, INK, "start", "bold")
    s.arrow(wx - 40, Yd(0) + 20, wx - 90, Yd(0) + 20, KAc, 3, 12)
    s.text(wx - 40, Yd(0) + 50, "可外傾", 14, KAc, "end", "bold")
    marks = [(0, "①", "z = 0", "地表（超載面）"), (H1, "②③", "z = 3 m 上／下", "層界：上下各算一次"), (H, "④", "z = 7", "牆底（取矩基準）")]
    for z, n, t, d in marks:
        s.line(rx + 60, Yd(z), rx + 100, Yd(z), "#C0392B", 1.5, "3,3")
        s.text(rx + 108, Yd(z) - 2, f"{n}　{t}", 18, "#C0392B", "start", "bold")
        s.text(rx + 108, Yd(z) + 21, d, 14, MUTED)
    s.save(F + "fig06_problem.svg")

# ───────── F7 σv 與 σa 並排 ─────────
def fig_points():
    s = SVG(1200, 560, ts=1.25)
    # 左：σv
    x0, kx = 120, 2.3
    s.rect(x0, Yd(0), 380, H1 * KY, fill=S1c, stroke="none", op=0.55)
    s.rect(x0, Yd(H1), 380, H2 * KY, fill=S2c, stroke="none", op=0.55)
    s.line(x0, Yd(0) - 10, x0, Yd(H), INK, 2); s.line(x0, Yd(H), x0 + 380, Yd(H), INK, 1.5)
    pv = [(x0 + kx * SV0, Yd(0)), (x0 + kx * SV3, Yd(H1)), (x0 + kx * SV7, Yd(H))]
    s.poly([(x0, Yd(0))] + pv + [(x0, Yd(H))], color="#6B7280", fill="#6B7280", closed=True, op=0.15, sw=0)
    s.poly(pv, color=INK, sw=3)
    for (px, py), v in zip(pv, (SV0, SV3, SV7)):
        s.circle(px, py, 6, fill=INK)
        s.text(px + 12, py + (6 if v < 100 else -10), f"{v:.0f}", 17, INK, "start", "bold")
    s.text(x0 + 190, 52, "垂直應力 σ_v（kPa）", 18, INK, "middle", "bold")
    s.text(x0 + 150, Yd(1.6), "+17 × 3", 15, MUTED, "start")
    s.text(x0 + 290, Yd(5.6), "+19 × 4", 15, MUTED, "start")
    for z, lab in ((0, "0"), (H1, "3"), (H, "7")):
        s.text(x0 - 12, Yd(z) + 6, lab, 15, MUTED, "end")
    s.text(x0 - 40, Yd(3.5), "z (m)", 14, MUTED, "end")
    # 中間箭頭
    s.arrow(530, Yd(1.5), 610, Yd(1.5), KAc, 3, 13)
    s.text(570, Yd(1.5) - 14, "× 1/3", 17, KAc, "middle", "bold")
    s.arrow(530, Yd(5), 610, Yd(5), "#B8520E", 3, 13)
    s.text(570, Yd(5) - 14, "× 0.26", 17, "#B8520E", "middle", "bold")
    # 右：σa
    x1, kx2 = 660, 11.0
    s.rect(x1, Yd(0), 500, H1 * KY, fill=S1c, stroke="none", op=0.55)
    s.rect(x1, Yd(H1), 500, H2 * KY, fill=S2c, stroke="none", op=0.55)
    s.line(x1, Yd(0) - 10, x1, Yd(H), INK, 2); s.line(x1, Yd(H), x1 + 500, Yd(H), INK, 1.5)
    pa = [(x1 + kx2 * SA0, Yd(0)), (x1 + kx2 * SA3m, Yd(H1)), (x1 + kx2 * SA3p, Yd(H1)), (x1 + kx2 * SA7, Yd(H))]
    s.poly([(x1, Yd(0))] + pa + [(x1, Yd(H))], color="none", fill=KAc, closed=True, op=0.18, sw=0)
    s.poly(pa, color=INK, sw=3)
    labs = [("①", SA0, "start", 12, 6), ("②", SA3m, "start", 12, -6), ("③", SA3p, "end", -14, 24), ("④", SA7, "start", 12, -10)]
    for (px, py), (n, v, an, dx, dy) in zip(pa, labs):
        s.circle(px, py, 6, fill="#C0392B")
        s.text(px + dx, py + dy, f"{n} {f2(v)}", 17, "#C0392B", an, "bold")
    s.text(x1 + 250, 52, "側向主動土壓 σ_a（kPa）", 18, INK, "middle", "bold")
    s.text(x1 + kx2 * SA3m + 14, Yd(H1) + 34, f"跳 −{f2(SA3m - SA3p)}", 15, "#C0392B", "start", "bold")
    s.save(F + "fig07_points.svg")

# ───────── F8 界面跳動：同一個 σv、兩個 σh ─────────
def fig_jump():
    s = SVG(1150, 470)
    iy = 235; cx = 300; e = 120; k = 1.55
    s.rect(60, 40, 480, iy - 40, fill=S1c, stroke="none")
    s.rect(60, iy, 480, 430 - iy, fill=S2c, stroke="none")
    s.line(60, iy, 540, iy, INK, 2, "8,5")
    s.text(70, 66, "土層 1　K_{a1} = 1/3", 16, INK, "start", "bold")
    s.text(70, 420, "土層 2　K_{a2} = 0.26", 16, INK, "start", "bold")
    for (ty, sh, col, tag) in ((iy - 12 - e, SA3m, KAc, "3 上"), (iy + 12, SA3p, "#B8520E", "3 下")):
        ex = cx - e / 2
        s.rect(ex, ty, e, e, fill="#FFFFFF", stroke=INK, sw=2)
        s.text(cx, ty + e / 2 + 7, f"z = {tag}", 18, INK, "middle", "bold")
        L = k * SV3 * 0.5
        s.arrow(cx + 26, ty - L + 4 if False else ty - 2, cx + 26, ty - 2, INK, 2.2, 10) if False else None
        # 水平應力（兩側）
        Lh = k * sh * 2
        s.arrow(ex - Lh - 6, ty + e / 2, ex - 4, ty + e / 2, col, 4, 13)
        s.arrow(ex + e + Lh + 6, ty + e / 2, ex + e + 4, ty + e / 2, col, 4, 13)
        s.text(ex + e + Lh + 14, ty + e / 2 + 7, f"σ_h = {f2(sh)}", 18, col, "start", "bold")
    # σv 標示（貫穿界面）
    s.text(cx - 130, iy + 6, f"σ_v = {SV3:.0f}（上下相同）", 16, INK, "end", "bold") if False else None
    s.rect(560, 40, 560, 390, fill=PANEL, stroke="#D5DAE1", sw=1.2, rx=12)
    s.text(585, 82, f"垂直：σ_v = 20 + 17×3 = {SV3:.0f} kPa", 19, INK, "start", "bold")
    s.text(585, 110, "界面上下同一個值 —— 上方土重沒有變", 15, MUTED)
    s.text(585, 160, "水平：σ_h = K × σ_v", 19, INK, "start", "bold")
    s.text(585, 188, f"3 m 上側用 K_{{a1}}：{SV3:.0f} × 1/3 = {f2(SA3m)}", 16, KAc, "start", "bold")
    s.text(585, 214, f"3 m 下側用 K_{{a2}}：{SV3:.0f} × 0.26 = {f2(SA3p)}", 16, "#B8520E", "start", "bold")
    s.text(585, 240, "K 是「土的性質」，換土就換 K → σ_h 必跳", 15, MUTED)
    s.line(585, 262, 1095, 262, GRID, 1.5)
    wrongC = SA3m * H2 + 0.5 * (KA2 * G2 * H2) * H2
    s.text(585, 298, "若界面只算一次（23.67 直接往下接）：", 16, "#C0392B", "start", "bold")
    s.text(585, 326, f"下層矩形 23.67 × 4 = {f1(SA3m * H2)}（正確 {f1(SA3p * H2)}）", 15, INK)
    Pw = BLOCKS[0][2] + BLOCKS[1][2] + SA3m * H2 + BLOCKS[3][2]
    s.text(585, 354, f"P 變成 {f1(Pw)} kN/m，多算 {(Pw - P) / P * 100:.0f}%", 15, INK)
    s.text(585, 400, "分層 = 兩條 σ_a 線，各用各的 K", 18, "#2E7D6B", "start", "bold")
    s.save(F + "fig08_jump.svg")

# ───────── F9 切方塊（示範題）─────────
def fig_blocks():
    s = SVG(1080, 620, ts=1.2)
    x0, kx = 190, 11.0
    Yb = Yd(H)
    X = lambda v: x0 + kx * v
    wall(s, x0, Yd(0) - 20, Yb + 2, 18)
    s.line(x0 - 60, Yb, x0 + 880, Yb, INK, 2)
    s.text(x0 + 880, Yb + 28, "牆底（取矩基準 y = 0）", 15, INK, "end", "bold")
    polys = {
        "A": [(x0, Yd(0)), (X(SA0), Yd(0)), (X(SA0), Yd(H1)), (x0, Yd(H1))],
        "B": [(X(SA0), Yd(0)), (X(SA3m), Yd(H1)), (X(SA0), Yd(H1))],
        "C": [(x0, Yd(H1)), (X(SA3p), Yd(H1)), (X(SA3p), Yb), (x0, Yb)],
        "D": [(X(SA3p), Yd(H1)), (X(SA7), Yb), (X(SA3p), Yb)],
    }
    cen = {
        "A": (x0 + kx * SA0 / 2, Yd(H1 / 2)),
        "B": (X(SA0) + kx * (SA3m - SA0) / 3, Yd(H1 * 2 / 3)),
        "C": (x0 + kx * SA3p / 2, Yd(H1 + H2 / 2)),
        "D": (X(SA3p) + kx * (SA7 - SA3p) / 3, Yd(H1 + H2 * 2 / 3)),
    }
    for (key, name, Pi, yi, shp) in BLOCKS:
        col = REC if shp == "rect" else TRI
        s.poly(polys[key], color=col, fill=col, closed=True, op=0.28, sw=2)
    for (key, name, Pi, yi, shp) in BLOCKS:
        col = REC if shp == "rect" else TRI
        cx, cy = cen[key]
        s.circle(cx, cy, 16, fill=col, stroke="#FFFFFF", sw=2.5)
        s.text(cx, cy + 6, key, 16, "#FFFFFF", "middle", "bold")
    # 壓力值
    s.text(X(SA0) + 6, Yd(0) - 8, f"{f2(SA0)}", 16, INK, "start", "bold")
    s.text(X(SA3m) + 8, Yd(H1) - 6, f"{f2(SA3m)}", 16, INK, "start", "bold")
    s.text(X(SA3p) - 8, Yd(H1) + 24, f"{f2(SA3p)}", 16, INK, "end", "bold", bg="#FFFFFF")
    s.text(X(SA7) + 8, Yb - 8, f"{f2(SA7)} kPa", 16, INK, "start", "bold")
    # y_i 尺寸線：由低到高排列，避免引線交叉
    order = sorted(BLOCKS, key=lambda b: b[3])
    cxs = [720, 790, 860, 930]
    for (key, name, Pi, yi, shp), cxl in zip(order, cxs):
        col = REC if shp == "rect" else TRI
        ty = Yb - yi * KY
        s.line(cen[key][0] + 18, ty, cxl, ty, col, 1.2, "3,4")
        s.dim(cxl, Yb, cxl, ty, "", col)
        s.text(cxl + 8, ty + 22, f"y_{key}", 16, col, "start", "bold")
        s.text(cxl + 8, ty + 48, f"{f2(yi)}", 16, col, "start", "bold")
    # 合力
    yr = Yb - YBAR * KY
    s.arrow(x0 + 520, yr, x0 + 4, yr, RES, 5, 20)
    s.text(x0 + 300, yr - 16, f"P = {f1(P)} kN/m", 20, RES, "start", "bold", bg="#FFFFFF")
    s.dim(x0 - 45, Yb, x0 - 45, yr, "", RES)
    s.text(x0 - 55, (Yb + yr) / 2 + 6, f"ȳ = {f2(YBAR)} m", 18, RES, "end", "bold")
    s.text(x0 - 55, Yd(1.5) + 6, "上層 3 m", 15, MUTED, "end")
    s.text(x0 - 55, Yd(3.4) + 6, "下層 4 m", 15, MUTED, "end")
    s.line(x0 - 90, Yd(H1), x0, Yd(H1), MUTED, 1, "3,3")
    s.save(F + "fig09_blocks.svg")

# ───────── F10 H/3 對照 ─────────
def fig_h3():
    s = SVG(1150, 440, ts=1.2)
    x0, yb, ky = 150, 390, 48
    wall(s, x0, yb - H * ky - 10, yb + 2, 18)
    s.line(x0 - 60, yb, x0 + 340, yb, INK, 2)
    yc, yw = yb - YBAR * ky, yb - Y_H3 * ky
    s.arrow(x0 + 300, yc, x0 + 4, yc, RES, 5, 18)
    s.text(x0 + 305, yc + 6, f"正確 ȳ = {f2(YBAR)} m", 17, RES, "start", "bold")
    s.arrow(x0 + 300, yw, x0 + 4, yw, "#9AA3AE", 4, 16, dash="8,5")
    s.text(x0 + 305, yw + 16, f"反射寫 H/3 = {f2(Y_H3)} m", 17, "#6B7280", "start", "bold")
    s.dim(x0 - 40, yb, x0 - 40, yc, "", RES)
    s.text(x0 - 50, (yb + yc) / 2 + 6, f"{f2(YBAR)}", 16, RES, "end", "bold")
    s.text(x0 - 50, yb - H * ky + 16, "H = 7 m", 15, MUTED, "end")
    s.text(x0 + 305, yw + 50, f"作用點低估 {f2(YBAR - Y_H3)} m", 16, INK, "start", "bold")
    # 右：傾覆力矩長條
    bx, bw, by = 700, 380, 120
    mx = M * 1.05
    s.text(bx, 70, "對牆底傾覆力矩（kN·m/m）", 18, INK, "start", "bold")
    for i, (lab, v, col) in enumerate((("切方塊", M, RES), ("H/3", M_H3, "#9AA3AE"))):
        yy = by + i * 90
        s.text(bx, yy - 8, lab, 15, col, "start", "bold")
        s.rect(bx, yy, bw * v / mx, 44, fill=col, stroke="none", rx=4)
        s.text(bx + bw * v / mx - 10, yy + 29, f"{f1(v)}", 18, "#FFFFFF", "end", "bold")
    s.text(bx, by + 200, f"少算 {f1(M - M_H3)} kN·m/m ＝ {UNDER * 100:.1f}%", 20, "#C0392B", "start", "bold")
    s.text(bx, by + 232, "傾覆安全係數被高估，偏不安全", 15, MUTED)
    s.save(F + "fig10_h3.svg")

# ───────── F11 何時可以直接寫 H/3、H/2 ─────────
def fig_when():
    s = SVG(1200, 430, ts=1.2)
    pw, ph, top = 275, 250, 20
    cases = [
        ("純三角形", "單層・無超載・乾", "tri", "ȳ = H/3"),
        ("純矩形", "只看超載部分", "rect", "ȳ = H/2"),
        ("梯形", "單層＋超載", "trap", "ȳ = H(2a+b) / 3(a+b)"),
        ("折線・跳動", "分層・水位・裂縫", "jump", "只能切方塊"),
    ]
    for i, (t, d, kind, res) in enumerate(cases):
        x = 15 + i * (pw + 18)
        danger = kind == "jump"
        s.rect(x, top, pw, ph + 70, fill="#FBECEA" if danger else PANEL, stroke="#E6B0AA" if danger else "#D5DAE1", sw=1.2, rx=12)
        s.text(x + 18, top + 34, t, 20, "#C0392B" if danger else INK, "start", "bold")
        s.text(x + 18, top + 60, d, 13, MUTED, "start")
        gx, gy0, gh = x + 50, top + 85, 150
        s.line(gx, gy0, gx, gy0 + gh, INK, 2)
        s.line(gx - 20, gy0 + gh, gx + 180, gy0 + gh, INK, 1.5)
        if kind == "tri":   pts = [(gx, gy0), (gx + 150, gy0 + gh)]; yb_ = 1 / 3
        elif kind == "rect": pts = [(gx + 90, gy0), (gx + 90, gy0 + gh)]; yb_ = 0.5
        elif kind == "trap":
            pts = [(gx + 40, gy0), (gx + 150, gy0 + gh)]; a, b = 40, 150; yb_ = (2 * a + b) / (3 * (a + b))
            s.text(gx + 50, gy0 + 16, "a", 16, INK, "start", "bold"); s.text(gx + 75, gy0 + gh + 24, "b", 16, INK, "middle", "bold")
        else:
            k = 150 / SA7
            pts = [(gx + k * SA0, gy0), (gx + k * SA3m, gy0 + gh * H1 / H), (gx + k * SA3p, gy0 + gh * H1 / H), (gx + k * SA7, gy0 + gh)]
            yb_ = YBAR / H
        col = "#C0392B" if danger else KAc
        s.poly([(gx, gy0)] + pts + [(gx, gy0 + gh)], color=col, fill=col, closed=True, op=0.2, sw=2)
        yr = gy0 + gh * (1 - yb_)
        s.arrow(gx + 175, yr, gx + 4, yr, RES, 3, 12)
        s.text(x + pw / 2, top + ph + 50, res, 17, "#C0392B" if danger else INK, "middle", "bold")
    # 一秒驗算數線
    y = 395; xa, xb = 250, 950
    Xh = lambda v: xa + (v - 2.0) / 1.8 * (xb - xa)
    s.rect(Xh(Y_H3), y - 10, Xh(H / 2) - Xh(Y_H3), 20, fill="#2E7D6B", stroke="none", rx=5, op=0.2)
    s.line(xa, y, xb, y, "#5B6573", 2)
    s.text(xa - 12, y + 6, "一秒驗算", 16, "#2E7D6B", "end", "bold")
    for v, lab in ((Y_H3, "H/3 = 2.33"), (H / 2, "H/2 = 3.50")):
        s.line(Xh(v), y - 12, Xh(v), y + 12, "#5B6573", 2); s.text(Xh(v), y + 32, lab, 14, MUTED, "middle")
    s.circle(Xh(YBAR), y, 9, fill=RES)
    s.text(Xh(YBAR), y - 18, f"本例 {f2(YBAR)} ✓", 15, RES, "middle", "bold")
    s.text(xb + 20, y + 6, "例外：張力裂縫會使 ȳ < H/3", 14, MUTED)
    s.save(F + "fig11_when.svg")

if __name__ == "__main__":
    import os; os.makedirs("figs", exist_ok=True)
    fig_sop(); fig_k(); zc = fig_breaks(); W = fig_water(); fig_rule()
    fig_problem(); fig_points(); fig_jump(); fig_blocks(); fig_h3(); fig_when()
    json.dump({"zc": zc, **W}, open("figs/extra.json", "w"), indent=1)
    print("done", zc, W)
