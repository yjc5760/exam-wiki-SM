"""SM-U1-5 拼圖二：兩個閥門定生死 — 向量圖（所有幾何由 params.py 算出）"""
import math
from svglib import SVG, measure, INK, MUTED, GRID, PANEL
from params import *
R_ = math.radians

EFF, TOT, RED, NAVY = "#E4572E", "#2F54C8", "#C0392B", "#1B2432"
UUC, CUC, CDC = "#C0392B", "#E07B39", "#2E7D6B"
UUBG, CUBG, CDBG = "#FBECEA", "#FDF1E7", "#E6F2EF"
EFFBG, TOTBG, GOLD, GOLDBG, PUR, PURBG = "#FDEDE8", "#EEF2FB", "#B7791F", "#FBF3E4", "#6D4BC2", "#F1EDFA"
WATER, WATERD = "#D9ECF7", "#2C6E9E"
W = "#FFFFFF"


class Ax:
    def __init__(s, g, x0, y0, k, ky=None):
        s.g, s.x0, s.y0, s.k, s.ky = g, x0, y0, k, ky or k
    def X(s, v): return s.x0 + v*s.k
    def Y(s, v): return s.y0 - v*s.ky
    def axes(s, xmax, ymax, xl="σ", yl="τ", xmin=0, size=20):
        g = s.g
        g.arrow(s.X(xmin), s.y0, s.X(xmax), s.y0, INK, 2, 10)
        g.arrow(s.x0, s.y0, s.x0, s.Y(ymax), INK, 2, 10)
        g.text(s.X(xmax) + 8, s.y0 + 6, xl, size, INK, weight="bold")
        g.text(s.x0 - 8, s.Y(ymax) - 6, yl, size, INK, anchor="end", weight="bold")
    def line(s, a, b, c, dd, **kw): s.g.line(s.X(a), s.Y(b), s.X(c), s.Y(dd), **kw)
    def semi(s, C, Rr, color, sw=2.4, dash=None, fill=None, op=0.12):
        x1, x2, y = s.X(C - Rr), s.X(C + Rr), s.y0; rr = Rr*s.k
        dsh = f' stroke-dasharray="{dash}"' if dash else ''
        f = f'fill="{fill}" fill-opacity="{op}"' if fill else 'fill="none"'
        s.g.add(f'<path d="M{x1:.1f},{y:.1f} A{rr:.1f},{rr:.1f} 0 0 1 {x2:.1f},{y:.1f}" {f} stroke="{color}" stroke-width="{sw}"{dsh}/>')
    def tick(s, v, lab, color=MUTED, size=15, dy=24):
        s.g.line(s.X(v), s.y0, s.X(v), s.y0 + 6, INK, 1.5)
        s.g.text(s.X(v), s.y0 + dy, lab, size, color, anchor="middle")
    def ray(s, phi, xend, **kw):
        s.line(0, 0, xend, xend*math.tan(R_(phi)), **kw)


def card(g, x, y, w, h, fill=PANEL, stroke="#D5DAE1", rx=12, sw=1.2):
    g.rect(x, y, w, h, fill=fill, stroke=stroke, sw=sw, rx=rx)


def dot(g, x, y, c, r=7): g.circle(x, y, r, fill=c, stroke=W, sw=2)


def valve(g, cx, cy, is_open, r=30):
    """閥門圖示：開 = 綠底橫向流動箭頭；關 = 紅底叉叉"""
    if is_open:
        g.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{CDBG}" stroke="{CDC}" stroke-width="3"/>')
        g.arrow(cx - r*0.62, cy, cx + r*0.66, cy, CDC, 4, 12)
    else:
        g.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{UUBG}" stroke="{UUC}" stroke-width="3"/>')
        k = r*0.45
        g.line(cx - k, cy - k, cx + k, cy + k, UUC, 4.5, cap="round")
        g.line(cx - k, cy + k, cx + k, cy - k, UUC, 4.5, cap="round")


def particles(g, pts, rr, fill="#E7ECF2"):
    for x, y in pts:
        g.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr}" fill="{fill}" stroke="{INK}" stroke-width="2"/>')


# ───────── fig01 兩個閥門 2×2 矩陣 ─────────
def fig01():
    g = SVG(1200, 480)
    x0, y0, cw, ch = 300, 95, 420, 175
    g.text(x0 + cw, 36, "閥門②：剪切階段排不排水？", 21, NAVY, anchor="middle", weight="bold")
    for j, (lab, op) in enumerate([("開（慢慢剪，水隨時排走）", True), ("關（快速剪，水困在裡面）", False)]):
        cx = x0 + cw*j + cw/2
        valve(g, cx - measure(lab, 17, True)/2 - 30, 70, op, 16)
        g.text(cx + 8, 76, lab, 17, CDC if op else UUC, anchor="middle", weight="bold")
    g.text(150, y0 + ch + 8, "閥門①", 21, NAVY, anchor="middle", weight="bold")
    g.text(150, y0 + ch + 36, "壓密階段", 18, NAVY, anchor="middle", weight="bold")
    for i, (lab, op) in enumerate([("開：先壓密", True), ("關：不壓密", False)]):
        cy = y0 + ch*i + ch/2
        valve(g, 230, cy - 16, op, 18)
        g.text(230, cy + 30, lab, 16, CDC if op else UUC, anchor="middle", weight="bold")
    cells = [[("CD", "壓密排水", "u 全程 = 0", "直接量到 c'、φ'", CDC, CDBG),
              ("CU", "壓密不排水", "剪切時累積 u_f", "φ_{cu}（總）＋ φ'（有效）", CUC, CUBG)],
             [("UD", "不壓密排水", "現場沒有這種情境", "不做這個試驗", "#9AA3AE", "#F4F5F7"),
              ("UU", "不壓密不排水", "Δu = Δσ_3，σ' 鎖死", "φ_u = 0、S_u = R", UUC, UUBG)]]
    for i in range(2):
        for j in range(2):
            name, zh, l1, l2, col, bg = cells[i][j]
            x, y = x0 + cw*j + 8, y0 + ch*i + 8
            card(g, x, y, cw - 16, ch - 16, bg, col, 12, 2.4)
            g.text(x + 28, y + 70, name, 50, col, weight="bold")
            g.text(x + 30, y + 110, zh, 18, col, weight="bold")
            g.text(x + 175, y + 62, l1, 18, INK)
            g.text(x + 175, y + 100, l2, 18, col if name != "UD" else MUTED, weight="bold")
            if name == "UD":
                g.line(x + 18, y + 80, x + 140, y + 36, "#9AA3AE", 4)
    g.text(x0 + cw, 468, "閥門的開關組合 → 決定孔隙水壓 u 怎麼變 → 決定你量到的是哪一組參數", 19, INK, anchor="middle", weight="bold")
    g.save("figs/fig01_valves.svg")


# ───────── fig02 三軸儀構造 ─────────
def fig02():
    g = SVG(1200, 500)
    # 壓力室
    cx, top, bot = 330, 70, 440
    g.rect(cx - 190, top, 380, bot - top, fill="#F3F8FC", stroke=INK, sw=3, rx=10)
    g.text(cx - 175, top + 30, "壓力室（充水）", 17, WATERD, weight="bold")
    # 活塞
    g.rect(cx - 12, 20, 24, 118, fill="#C9D3DF", stroke=INK, sw=2)
    g.arrow(cx, 0, cx, 30, RED, 3, 12)
    g.text(cx + 24, 30, "軸向加載 Δσ_d（剪切）", 17, RED, weight="bold")
    # 試體
    sx, sy, sw_, sh = cx - 70, 150, 140, 230
    g.rect(sx - 6, sy - 22, sw_ + 12, 22, fill="#B0BAC6", stroke=INK, sw=2)          # 頂帽
    g.rect(sx - 6, sy + sh, sw_ + 12, 18, fill="#CDB892", stroke=INK, sw=2)           # 透水石
    g.rect(sx - 20, sy + sh + 18, sw_ + 40, 22, fill="#B0BAC6", stroke=INK, sw=2)     # 底座
    g.rect(sx, sy, sw_, sh, fill="#D8CFC0", stroke=INK, sw=2)
    g.rect(sx - 4, sy - 4, sw_ + 8, sh + 8, fill="none", stroke=PUR, sw=2, dash="6 4")
    g.text(cx, sy + sh/2 - 6, "土壤", 20, INK, anchor="middle", weight="bold")
    g.text(cx, sy + sh/2 + 22, "試體", 20, INK, anchor="middle", weight="bold")
    g.text(sx - 30, sy + 40, "橡皮膜", 15, PUR, anchor="end", weight="bold")
    for yy in [sy + 80, sy + 160]:
        g.arrow(cx - 180, yy, sx - 10, yy, WATERD, 2.4, 10); g.arrow(cx + 180, yy, sx + sw_ + 10, yy, WATERD, 2.4, 10)
    g.text(cx + 180, sy + 110, "圍壓 σ_3", 17, WATERD, anchor="end", weight="bold")
    # 排水管線
    py = sy + sh + 29
    g.line(sx + sw_ + 20, py, 640, py, INK, 5)
    g.line(640, py, 640, 160, INK, 5)
    valve(g, 640, 280, True, 30)
    g.text(684, 272, "排水閥", 19, NAVY, weight="bold")
    g.text(684, 298, "（同一顆閥門）", 15, MUTED)
    # 量管
    g.rect(620, 60, 40, 100, fill=WATER, stroke=INK, sw=2, rx=4)
    g.text(640, 46, "量管（量 ΔV）", 16, WATERD, anchor="middle", weight="bold")
    # 孔壓計
    g.line(sx + sw_ + 60, py, sx + sw_ + 60, py + 34, INK, 3)
    g.circle(sx + sw_ + 60, py + 44, 13, fill="#FFFFFF", stroke=INK, sw=2.4)
    g.text(sx + sw_ + 82, py + 50, "孔壓計：量 u", 16, INK, weight="bold")
    # 右：兩階段時間軸
    X = 820
    card(g, X, 40, 360, 200, CDBG, CDC, 12, 2)
    g.text(X + 20, 76, "階段① 壓密：加圍壓 σ_3", 19, CDC, weight="bold")
    g.text(X + 20, 112, "閥開 → 水排出、u 消散", 17, INK)
    g.text(X + 20, 142, "σ' 上升到 σ_3（C）", 17, INK)
    g.text(X + 20, 176, "閥關 → u = Δσ_3、σ' 不變（U）", 17, INK)
    g.text(X + 20, 214, "決定：試體剪切前有多緊", 16, MUTED)
    card(g, X, 260, 360, 200, CUBG, CUC, 12, 2)
    g.text(X + 20, 296, "階段② 剪切：加 Δσ_d", 19, CUC, weight="bold")
    g.text(X + 20, 332, "閥開 → 慢剪、u ≈ 0、量 ΔV（D）", 17, INK)
    g.text(X + 20, 362, "閥關 → 快剪、ΔV = 0", 17, INK)
    g.text(X + 20, 392, "　　　 量孔壓 u_f（U）", 17, INK)
    g.text(X + 20, 434, "決定：破壞時骨架被推多少", 16, MUTED)
    g.save("figs/fig02_apparatus.svg")


# ───────── fig03 閥門①：壓密階段 u–t ─────────
def fig03():
    g = SVG(1200, 470)
    for i, (op, title, col) in enumerate([(True, "閥門① 開（C）", CDC), (False, "閥門① 關（U）", UUC)]):
        ox = 90 + i*600; oy = 380; w, h = 460, 250
        valve(g, ox + 10, 50, op, 20)
        g.text(ox + 42, 58, title, 22, col, weight="bold")
        g.arrow(ox, oy, ox + w, oy, INK, 2, 10); g.arrow(ox, oy, ox, oy - h - 20, INK, 2, 10)
        g.text(ox + w + 6, oy + 6, "t", 20, INK, weight="bold")
        g.text(ox - 10, oy - h - 22, "kPa", 16, INK, anchor="end", weight="bold")
        yT = oy - 200
        g.line(ox - 6, yT, ox, yT, INK, 1.5); g.text(ox - 10, yT + 6, "σ_3", 16, MUTED, anchor="end")
        g.line(ox, yT, ox + w - 20, yT, "#9AA3AE", 1.5, "4 4")
        if op:
            pu = [(ox + t, oy - 200*math.exp(-t/80)) for t in range(0, w - 19, 6)]
            ps = [(ox + t, oy - 200*(1 - math.exp(-t/80))) for t in range(0, w - 19, 6)]
            g.poly(pu, WATERD, 3.2); g.poly(ps, EFF, 3.2)
            g.text(ox + 190, oy - 50, "u 消散 → 0", 18, WATERD, weight="bold")
            g.text(ox + 230, yT - 14, "σ' → σ_3（骨架變緊）", 18, EFF, weight="bold")
            g.text(ox + w/2, oy + 44, "剪切前：σ'_3 = σ_3，u_0 = 0", 18, INK, anchor="middle", weight="bold")
        else:
            g.line(ox, yT, ox + w - 20, yT, WATERD, 3.2)
            g.line(ox, oy - 3, ox + w - 20, oy - 3, EFF, 3.2)
            g.text(ox + 120, yT - 14, "u = Δσ_3（水全扛，B = 1）", 18, WATERD, weight="bold")
            g.text(ox + 120, oy - 16, "Δσ' = 0：骨架沒被加壓", 18, EFF, weight="bold")
            g.text(ox + w/2, oy + 44, "剪切前：σ' 仍是取樣時的 σ'_0", 18, INK, anchor="middle", weight="bold")
    g.text(600, 460, "壓密閥決定「起跑點」：剪切開始前，骨架承受多少有效應力", 18, NAVY, anchor="middle", weight="bold")
    g.save("figs/fig03_consol.svg")


# ───────── fig04 閥門②：剪切階段 ΔV vs u ─────────
def fig04():
    g = SVG(1200, 470)
    def curve(ox, oy, amp, shape):
        pts = []
        for i in range(0, 101):
            e = i/100
            if shape == "nc": v = amp*(1 - math.exp(-e*5))
            else: v = amp*(0.35*math.sin(math.pi*min(e, 0.25)/0.25*0.5)*(1 if e < 0.2 else 1) - 1.25*max(0, e - 0.12)**0.8)
            pts.append((ox + e*420, oy - v))
        return pts
    for i, (op, title, col, yl, sub) in enumerate([
            (True, "閥門② 開（D）：水排得掉", CDC, "體積應變 ε_v（+ 壓縮）", "體積想變 → 真的變了，u ≈ 0"),
            (False, "閥門② 關（U）：水排不掉", UUC, "超額孔壓 Δu", "體積不能變 → 傾向轉成 u")]):
        ox, oy = 110 + i*600, 250
        valve(g, ox - 30, 48, op, 20)
        g.text(ox + 2, 56, title, 21, col, weight="bold")
        g.arrow(ox, oy, ox + 450, oy, INK, 2, 10); g.arrow(ox, oy + 150, ox, 90, INK, 2, 10)
        g.text(ox + 456, oy + 6, "ε_a", 18, INK, weight="bold")
        g.text(ox + 8, 104, yl, 16, INK, weight="bold")
        g.poly(curve(ox, oy, 110, "nc"), TOT, 3.2)
        g.poly(curve(ox, oy, 110, "oc"), PUR, 3.2)
        g.text(ox + 425, oy - 116, "NC（鬆）", 17, TOT, anchor="end", weight="bold")
        g.text(ox + 425, oy + 120, "OC（密）", 17, PUR, anchor="end", weight="bold")
        g.text(ox + 225, oy + 186, sub, 18, INK, anchor="middle", weight="bold")
    g.text(115 + 600 - 10, 180, "+u（剪縮）", 16, TOT, anchor="end", weight="bold")
    g.text(115 + 600 - 10, 330, "−u（剪脹）", 16, PUR, anchor="end", weight="bold")
    g.arrow(570, 118, 640, 118, NAVY, 3.5, 14)
    g.text(605, 104, "閥一關", 15, NAVY, anchor="middle", weight="bold")
    g.save("figs/fig04_shear.svg")


# ───────── fig05 為什麼沒有 UD ─────────
def fig05():
    g = SVG(1200, 400)
    steps = [("① 不壓密", "閥①關：加完圍壓", "u = Δσ_3 困在裡面", UUC, UUBG),
             ("② 剪切時開閥", "水開始往外排", "u 一邊消散", CDC, CDBG),
             ("③ 其實在壓密", "σ' 一邊上升", "起跑點一直在變", GOLD, GOLDBG)]
    for i, (a, b, c, col, bg) in enumerate(steps):
        x = 30 + i*272
        card(g, x, 60, 235, 170, bg, col, 12, 2.2)
        g.text(x + 117, 104, a, 22, col, anchor="middle", weight="bold")
        g.text(x + 117, 150, b, 18, INK, anchor="middle")
        g.text(x + 117, 188, c, 18, INK, anchor="middle", weight="bold")
        if i < 2: g.arrow(x + 238, 145, x + 268, 145, INK, 2.6, 12)
    g.arrow(785, 145, 845, 145, INK, 2.6, 12)
    card(g, 850, 40, 320, 210, NAVY, NAVY, 14)
    g.text(1010, 96, "結論", 20, "#F2A65A", anchor="middle", weight="bold")
    g.text(1010, 142, "等於「邊壓密邊剪」", 22, W, anchor="middle", weight="bold")
    g.text(1010, 182, "既不是 C 也不是 U", 18, "#C9D3DF", anchor="middle")
    g.text(1010, 218, "→ 結果無法解讀", 18, "#C9D3DF", anchor="middle")
    card(g, 40, 280, 1130, 90, PANEL)
    g.text(70, 318, "現場角度：", 19, NAVY, weight="bold")
    g.text(170, 318, "土體若排得了水，在它的覆土／圍壓下早就壓密完成了——", 19, INK)
    g.text(170, 352, "不存在「能排水、卻還沒壓密」的現場狀態，所以 UD 沒有工程意義。", 19, INK, weight="bold")
    g.save("figs/fig05_noud.svg")


# ───────── fig06 同一塊土、同一個 σ3：三個試驗並排 ─────────
def fig06():
    g = SVG(1200, 470)
    k = 0.98
    panels = [("CD", CDC, CDBG), ("CU", CUC, CUBG), ("UU", UUC, UUBG)]
    for i, (name, col, bg) in enumerate(panels):
        ox = 15 + i*392
        card(g, ox, 20, 378, 430, bg, col, 12, 2)
        g.text(ox + 20, 56, name, 30, col, weight="bold")
        ax = Ax(g, ox + 30, 360, k)
        ax.axes(320, 160, "σ", "τ", size=16)
        ax.ray(PHI, 310, color=EFF, sw=2.4)
        if name == "CD":
            ax.semi(C_CD, R_CD, CDC, 2.8, fill=CDC, op=0.12)
            for v in [S3, S1_CD]: ax.tick(v, f"{v:.0f}")
            g.text(ox + 110, 56, f"Δσ_d = {DSD_CD:.0f}", 19, INK, weight="bold")
            lines = ["u = 0：總 = 有效，一個圓", f"σ'_1 = 3 × {S3:.0f} = {S1_CD:.0f}"]
        elif name == "CU":
            ax.semi(C_T, R, TOT, 2.4, "7 5")
            ax.semi(C_E, R, EFF, 2.8, fill=EFF, op=0.14)
            g.arrow(ax.X(C_T), ax.Y(R) - 12, ax.X(C_E) + 4, ax.Y(R) - 12, TOT, 2.4, 10)
            g.text((ax.X(C_T) + ax.X(C_E))/2, ax.Y(R) - 22, f"u_f = {UF:.0f}", 15, TOT, anchor="middle", weight="bold", bg=bg)
            for v in [S3E, S1E]: ax.tick(v, f"{v:.0f}", EFF)
            for v in [S3, S1]: ax.tick(v, f"{v:.0f}", TOT, dy=44)
            g.text(ox + 110, 56, f"Δσ_d = {DSD:.0f}", 19, INK, weight="bold")
            lines = ["有效圓 = 總應力圓左移 u_f", f"有效 {S3E:.0f}～{S1E:.0f}、總 {S3:.0f}～{S1:.0f}"]
        else:
            ax.semi(C_T, R, TOT, 2.4, "7 5")
            ax.semi(C_E, R, EFF, 2.8, fill=EFF, op=0.14)
            ax.line(0, SU, 320, SU, color=UUC, sw=2.4)
            g.text(ax.X(320), ax.Y(SU) - 8, f"S_u = {SU:.0f}", 15, UUC, anchor="end", weight="bold", bg=bg)
            for v in [S3E, S1E]: ax.tick(v, f"{v:.0f}", EFF)
            for v in [S3, S1]: ax.tick(v, f"{v:.0f}", TOT, dy=44)
            g.text(ox + 110, 56, f"S_u = Δσ_d/2 = {SU:.0f}", 19, INK, weight="bold")
            lines = ["σ' 鎖在取樣前的 100", "破壞圓與 CU 相同，但只報 S_u"]
        g.text(ox + 187, 425, lines[0], 16, INK, anchor="middle", weight="bold")
        g.text(ox + 187, 90, lines[1], 15, MUTED, anchor="middle")
    g.save("figs/fig06_three.svg")


# ───────── fig07 CD：兩個圓、同一條線 ─────────
def fig07():
    g = SVG(1200, 470)
    ax = Ax(g, 70, 410, 1.28)
    ax.axes(600, 290, "σ", "τ")
    S3b = 200.0; S1b = KP*S3b
    ax.semi(C_CD, R_CD, CDC, 2.8, fill=CDC, op=0.10)
    ax.semi((S1b + S3b)/2, (S1b - S3b)/2, CDC, 2.8, fill=CDC, op=0.06)
    ax.ray(PHI, 500, color=EFF, sw=3.2)
    for C_, R0 in [(C_CD, R_CD), ((S1b + S3b)/2, (S1b - S3b)/2)]:
        tx, ty = C_ - R0*math.sin(R_(PHI)), R0*math.cos(R_(PHI)); dot(g, ax.X(tx), ax.Y(ty), EFF, 6)
    for v in [S3, S3b, S1_CD, S1b]: ax.tick(v, f"{v:.0f}")
    g.text(ax.X(500) + 10, ax.Y(500*math.tan(R_(PHI))) + 34, f"φ' = {PHI:.0f}°（直接量到）", 19, EFF, anchor="end", weight="bold", bg=W)
    card(g, 870, 40, 310, 390, PANEL)
    g.text(890, 80, "CD 的特權", 22, CDC, weight="bold")
    for i, s in enumerate(["兩閥門都開，剪得夠慢", "u ≡ 0 → σ = σ'", "畫出來就是有效應力圓",
                           "", f"σ_3 = {S3:.0f} → σ_1 = {S1_CD:.0f}", f"σ_3 = {S3b:.0f} → σ_1 = {S1b:.0f}",
                           f"K_p = σ_1/σ_3 = {KP:.0f}", "", "代價：黏土一組要做好幾天"]):
        g.text(890, 122 + i*34, s, 17, INK if i < 8 else MUTED, weight="bold" if i in (1, 6) else "normal")
    g.save("figs/fig07_cd.svg")


# ───────── fig08 CU：平移 u_f ─────────
def fig08():
    g = SVG(1200, 520)
    ax = Ax(g, 70, 395, 3.95)
    ax.axes(210, 86, "σ", "τ")
    ax.semi(C_T, R, TOT, 2.4, "8 6", fill=TOT, op=0.05)
    ax.semi(C_E, R, EFF, 3.0, fill=EFF, op=0.12)
    ax.ray(PHI, 150, color=EFF, sw=3.2)
    ax.ray(PHI_CU, 205, color=TOT, sw=2.4, dash="10 7")
    ax.tick(S3E, f"σ'_3 = {S3E:.0f}", EFF); ax.tick(S1E, f"σ'_1 = {S1E:.0f}", EFF)
    ax.tick(S3, f"σ_3 = {S3:.0f}", TOT, dy=46); ax.tick(S1, f"σ_1 = {S1:.0f}", TOT, dy=46)
    dot(g, ax.X(C_E), ax.y0, EFF, 6); dot(g, ax.X(C_T), ax.y0, TOT, 6)
    yA = ax.y0 + 76
    g.line(ax.X(C_E), ax.y0 + 8, ax.X(C_E), yA + 6, RED, 1.4, "4 3"); g.line(ax.X(C_T), ax.y0 + 8, ax.X(C_T), yA + 6, RED, 1.4, "4 3")
    g.arrow(ax.X(C_T), yA, ax.X(C_E), yA, RED, 2.8, 12)
    g.text((ax.X(C_T) + ax.X(C_E))/2, yA + 26, f"整個圓左移 u_f = {UF:.0f}（圓心 {C_T:.0f} → {C_E:.0f}）", 17, RED, anchor="middle", weight="bold")
    yD = ax.Y(R) - 30
    g.line(ax.X(S3E), yD, ax.X(S1E), yD, INK, 1.5); g.line(ax.X(S3E), yD - 7, ax.X(S3E), yD + 7, INK, 1.5); g.line(ax.X(S1E), yD - 7, ax.X(S1E), yD + 7, INK, 1.5)
    g.text(ax.X(C_E), yD - 10, f"2R = {DSD:.0f}（不變）", 16, INK, anchor="middle", weight="bold", bg=W)
    g.text(ax.X(150), ax.Y(150*math.tan(R_(PHI))) - 10, f"φ' = {PHI:.0f}°（有效）", 18, EFF, anchor="end", weight="bold", bg=W)
    g.text(ax.X(205), ax.Y(205*math.tan(R_(PHI_CU))) - 12, f"φ_{{cu}} = {PHI_CU:.1f}°（總）", 18, TOT, anchor="end", weight="bold", bg=W)
    card(g, 1000, 40, 185, 360, PANEL)
    g.text(1092, 80, "對帳", 21, NAVY, anchor="middle", weight="bold")
    for i, (s, c) in enumerate([(f"R = {R:.0f}", INK), ("兩圓相同", MUTED), (f"C = {C_T:.0f} → {C_E:.0f}", INK), ("只差 u_f", MUTED),
                                (f"sin φ' = {R:.0f}/{C_E:.0f}", EFF), (f"= {SIN_E:.1f} → {PHI:.0f}°", EFF),
                                (f"sin φ_{{cu}} = {R:.0f}/{C_T:.0f}", TOT), (f"→ {PHI_CU:.1f}°", TOT)]):
        g.text(1092, 118 + i*36, s, 17, c, anchor="middle", weight="bold")
    g.save("figs/fig08_cu.svg")


# ───────── fig09 u_f 的正負決定往哪移 ─────────
def fig09():
    g = SVG(1200, 470)
    Ct, Ce, Ro = S3 + DSD_OC/2, (S3E_OC + S1E_OC)/2, DSD_OC/2
    for i, (lab, col, ct, ce, rr, u, phc, k, xm) in enumerate([
            ("NC 黏土：+u_f → 圓往左", TOT, C_T, C_E, R, UF, PHI_CU, 2.0, 200),
            ("重 OC 黏土：−u_f → 圓往右", PUR, Ct, Ce, Ro, UF_OC, PHI_CU_OC, 0.72, 560)]):
        ox = 50 + i*430
        g.text(ox, 40, lab, 20, col, weight="bold")
        ax = Ax(g, ox, 380, k)
        g.arrow(ox, 380, ox + 390, 380, INK, 2, 10); g.arrow(ox, 380, ox, 70, INK, 2, 10)
        g.text(ox + 392, 386, "σ", 18, INK, weight="bold"); g.text(ox - 6, 76, "τ", 18, INK, anchor="end", weight="bold")
        xe = min(xm, 290/k/math.tan(R_(PHI)))
        ax.ray(PHI, xe, color=EFF, sw=3)
        xc = min(xm, 290/k/math.tan(R_(phc)))
        ax.ray(phc, xc, color=col, sw=2.2, dash="9 6")
        ax.semi(ct, rr, col, 2.2, "7 5")
        ax.semi(ce, rr, col, 2.8, fill=col, op=0.12)
        yA = ax.Y(rr) - 14
        g.arrow(ax.X(ct), yA, ax.X(ce) + (3 if u > 0 else -3), yA, col, 2.6, 11)
        g.text((ax.X(ct) + ax.X(ce))/2, yA - 10, f"u_f = {u:+.0f}" if u > 0 else f"u_f = {u:.1f}", 16, col, anchor="middle", weight="bold", bg=W)
        ax.tick(S3, f"{S3:.0f}", col)
        if u > 0: ax.tick(S3E, f"{S3E:.0f}", EFF); ax.tick(S1, f"{S1:.0f}", col)
        else: ax.tick(S1E_OC, f"{S1E_OC:.0f}", EFF); ax.tick(S3 + DSD_OC, f"{S3 + DSD_OC:.0f}", col)
        g.text(ox + 200, 440, f"φ_{{cu}} = {phc:.1f}° " + ("<" if u > 0 else ">") + f" φ' = {PHI:.0f}°", 19, col, anchor="middle", weight="bold")
    card(g, 900, 30, 285, 410, PANEL)
    g.text(920, 70, "為什麼？", 20, NAVY, weight="bold")
    for i, (t, c, bb) in enumerate([("兩個圓一樣大", INK, True), ("切線都從原點出發", INK, False), ("", INK, False),
                                    ("圓離原點近 → 切線較陡", INK, False), ("圓離原點遠 → 切線較平", INK, False), ("", INK, False),
                                    ("有效圓固定切在 φ'", EFF, True), ("總應力圓在右 → φ_{cu} 小", TOT, True), ("總應力圓在左 → φ_{cu} 大", PUR, True)]):
        g.text(920, 110 + i*34, t, 17, c, weight="bold" if bb else "normal")
    g.text(1042, 426, "兩圖比例尺不同；OC 例取 c' = 0、A_f = −0.2 示意", 12, MUTED, anchor="middle")
    g.save("figs/fig09_sign.svg")


# ───────── fig10 UU：圓一樣大 ─────────
def fig10():
    g = SVG(1200, 470)
    ax = Ax(g, 70, 360, 2.2)
    ax.axes(420, 110, "σ, σ' (kPa)", "τ")
    ax.semi(C_E, R, EFF, 3.0, fill=EFF, op=0.16)
    for i, s3 in enumerate(UU_S3):
        ax.semi(s3 + R, R, UUC, 2.2, "8 6", fill=UUC, op=0.03)
        ax.tick(s3, f"{s3:.0f}", UUC)
        g.text(ax.X(s3 + R), ax.Y(R) - 12, f"u = {UU_U[i]:.0f}", 15, UUC, anchor="middle", weight="bold", bg=W)
    ax.tick(S3E, f"{S3E:.0f}", EFF); ax.tick(S1E, f"{S1E:.0f}", EFF)
    ax.line(0, SU, 420, SU, color=UUC, sw=3)
    ax.ray(PHI, 150, color=EFF, sw=2.4, dash="8 5")
    g.text(ax.x0 - 10, ax.Y(SU) + 6, "S_u", 18, UUC, anchor="end", weight="bold")
    g.text(ax.X(420), ax.Y(SU) - 62, f"φ_u = 0（總應力包絡線水平）S_u = {SU:.0f}", 17, UUC, anchor="end", weight="bold", bg=W)
    g.text(ax.X(C_E), ax.y0 + 52, "唯一的有效圓", 16, EFF, anchor="middle", weight="bold")
    g.text(ax.X(300), ax.y0 + 52, "三個總應力圓：位置不同，大小相同", 16, UUC, anchor="middle", weight="bold")
    card(g, 1000, 30, 185, 400, PANEL)
    g.text(1092, 68, "室壓每加 100", 18, NAVY, anchor="middle", weight="bold")
    for i, (s, c) in enumerate([("Δu = +100", WATERD), ("Δσ' = 0", EFF), ("", INK), ("破壞時 σ'_3", INK), (f"永遠 = {S3E:.0f}", EFF),
                                ("", INK), ("所以 Δσ_d", INK), (f"永遠 = {DSD:.0f}", UUC), ("R = S_u", UUC)]):
        g.text(1092, 108 + i*34, s, 17, c, anchor="middle", weight="bold")
    g.save("figs/fig10_uu.svg")


# ───────── fig11 UC：σ3 = 0 的 UU ─────────
def fig11():
    g = SVG(1200, 440)
    ax = Ax(g, 80, 360, 4.6)
    ax.axes(140, 60, "σ (kPa)", "τ")
    ax.semi(SU, SU, UUC, 3, fill=UUC, op=0.12)
    ax.line(0, SU, 130, SU, color=UUC, sw=2.4, dash="9 6")
    ax.line(SU, 0, SU, SU, color=INK, sw=1.6, dash="4 4")
    ax.tick(0, "0"); ax.tick(QU, f"q_u = {QU:.0f}", UUC, 16)
    g.text(ax.X(SU) + 8, ax.Y(SU/2), f"R = S_u = {SU:.0f}", 17, INK, weight="bold")
    g.text(ax.X(130), ax.Y(SU) - 10, "φ_u = 0", 17, UUC, anchor="end", weight="bold")
    g.text(ax.X(0) + 8, ax.y0 + 50, "圓的左端就在原點（σ_3 = 0）", 16, MUTED)
    # 試體
    cx, cy = 900, 200
    g.rect(cx - 55, cy - 110, 110, 220, fill="#D8CFC0", stroke=INK, sw=2.4)
    for x in [cx - 30, cx, cx + 30]:
        g.arrow(x, cy - 170, x, cy - 114, RED, 2.6, 11); g.arrow(x, cy + 170, x, cy + 114, RED, 2.6, 11)
    g.text(cx + 70, cy - 140, "q_u（軸壓）", 18, RED, weight="bold")
    g.text(cx - 75, cy, "σ_3 = 0", 18, WATERD, anchor="end", weight="bold")
    g.text(cx - 75, cy + 28, "（沒有壓力室）", 15, MUTED, anchor="end")
    g.text(cx + 75, cy + 10, "S_u = q_u / 2", 22, UUC, weight="bold")
    g.save("figs/fig11_uc.svg")


# ───────── fig12 Skempton 兩段拆解 + B ─────────
def fig12():
    g = SVG(1200, 470)
    card(g, 20, 20, 560, 430, PANEL)
    g.text(40, 58, "把一次加載拆成兩段", 21, NAVY, weight="bold")
    def elem(x, y, lab, iso):
        g.rect(x, y, 80, 80, fill="#D8CFC0", stroke=INK, sw=2)
        for (a, b, c, dd) in [(x + 40, y - 40, x + 40, y - 4), (x + 40, y + 120, x + 40, y + 84)]:
            g.arrow(a, b, c, dd, RED, 2.6, 10)
        if iso:
            for (a, b, c, dd) in [(x - 40, y + 40, x - 4, y + 40), (x + 120, y + 40, x + 84, y + 40)]:
                g.arrow(a, b, c, dd, RED, 2.6, 10)
        g.text(x + 40, y + 160, lab, 17, INK, anchor="middle", weight="bold")
    elem(80, 140, "等向 Δσ_3", True)
    g.text(215, 190, "+", 34, INK, anchor="middle", weight="bold")
    elem(280, 140, "軸差 (Δσ_1 − Δσ_3)", False)
    g.text(80 + 40, 360, "Δu_a = B·Δσ_3", 18, WATERD, anchor="middle", weight="bold")
    g.text(320, 360, "Δu_d = A·B·(Δσ_1 − Δσ_3)", 18, PUR, anchor="middle", weight="bold")
    g.text(300, 410, "B 管「飽不飽和」，A 管「剪縮還剪脹」", 18, INK, anchor="middle", weight="bold")
    # B vs S
    ax = Ax(g, 700, 380, 1, 1)
    g.arrow(700, 380, 1150, 380, INK, 2, 10); g.arrow(700, 380, 700, 60, INK, 2, 10)
    g.text(1150, 432, "飽和度 S", 17, INK, anchor="end", weight="bold"); g.text(690, 70, "B", 20, INK, anchor="end", weight="bold")
    X = lambda s: 700 + (s - 70)/30*420; Y = lambda b: 380 - b*280
    pts = [(X(s), Y(min(1, 0.02 + 0.98*((s - 70)/30)**6))) for s in [70 + i*0.3 for i in range(101)]]
    g.poly(pts, WATERD, 3.2)
    for s in [70, 80, 90, 100]:
        g.line(X(s), 380, X(s), 386, INK, 1.5); g.text(X(s), 404, f"{s}%", 14, MUTED, anchor="middle")
    for b in [0.5, 1.0]:
        g.line(694, Y(b), 700, Y(b), INK, 1.5); g.text(690, Y(b) + 5, f"{b}", 14, MUTED, anchor="end")
    g.line(700, Y(1), 1130, Y(1), "#9AA3AE", 1.2, "4 4")
    g.text(X(99.3), Y(1) - 14, "完全飽和 B = 1", 16, WATERD, anchor="end", weight="bold")
    g.text(X(80), Y(0.5), "少一點氣泡，", 16, INK)
    g.text(X(80), Y(0.5) + 26, "B 就大幅下降", 16, INK)
    g.text(760, 432, "（曲線形狀為示意）", 13, MUTED, anchor="middle")
    g.save("figs/fig12_skempton.svg")


# ───────── fig13 微觀：剪縮 vs 剪脹 ─────────
def fig13():
    g = SVG(1200, 460)
    for i, (title, col, dense) in enumerate([("NC 黏土（鬆）：顆粒想掉進孔隙", TOT, False), ("重 OC 黏土（密）：顆粒要爬過彼此", PUR, True)]):
        ox = 40 + i*590
        card(g, ox, 20, 550, 420, WATER if True else PANEL, "#A9CBE3", 12, 1.5)
        g.text(ox + 20, 56, title, 20, col, weight="bold")
        rr = 30
        if not dense:
            pts = [(ox + 120, 200), (ox + 200, 170), (ox + 280, 205), (ox + 165, 270), (ox + 250, 285), (ox + 330, 260)]
            particles(g, pts, rr)
            g.arrow(ox + 200, 170 - rr - 5, ox + 210, 225, col, 3, 12)
            g.text(ox + 380, 170, "往下擠", 18, col, weight="bold")
            g.text(ox + 380, 200, "體積想縮", 18, col, weight="bold")
            res = [("閥關 → 水被擠壓", "+u（正孔壓）", "A_f > 0")]
        else:
            pts = [(ox + 90 + 60*j, 280) for j in range(6)] + [(ox + 120 + 60*j, 228) for j in range(5)]
            particles(g, pts, rr)
            g.arrow(ox + 150, 228 - rr - 10, ox + 330, 170, col, 3, 12)
            g.text(ox + 350, 150, "往上爬", 18, col, weight="bold")
            g.text(ox + 350, 180, "體積想脹", 18, col, weight="bold")
            res = [("閥關 → 水被吸住", "−u（負孔壓）", "A_f < 0")]
        a, b, c = res[0]
        g.arrow(ox + 60, 318, ox + 480, 318, INK, 2.4, 12) if False else None
        g.text(ox + 275, 360, a, 19, INK, anchor="middle", weight="bold")
        g.text(ox + 275, 400, f"{b}　→　{c}", 21, col, anchor="middle", weight="bold")
    g.save("figs/fig13_dilat.svg")


# ───────── fig14 A_f 典型範圍 ─────────
def fig14():
    g = SVG(1200, 430)
    X = lambda a: 400 + (a + 0.6)/2.2*740
    rows = [("高靈敏黏土", 0.75, 1.5, RED), ("正常壓密（NC）黏土", 0.5, 1.0, TOT),
            ("輕度過壓密黏土", 0.0, 0.5, GOLD), ("重度過壓密黏土", -0.5, 0.0, PUR)]
    g.line(X(0), 40, X(0), 330, INK, 2)
    for a in [-0.5, 0, 0.5, 1.0, 1.5]:
        g.line(X(a), 330, X(a), 338, INK, 1.5); g.text(X(a), 360, f"{a:g}", 16, MUTED, anchor="middle")
        g.line(X(a), 40, X(a), 330, GRID, 1)
    for i, (lab, lo, hi, col) in enumerate(rows):
        y = 60 + i*68
        g.text(380, y + 30, lab, 19, INK, anchor="end", weight="bold")
        g.rect(X(lo), y + 6, X(hi) - X(lo), 36, fill=col, stroke=col, sw=1, rx=6, op=0.85)
        g.text((X(lo) + X(hi))/2, y + 31, f"{lo:g} ～ {hi:g}", 16, W, anchor="middle", weight="bold")
    for a, lab, col in [(AF, f"示範黏土 A：{AF}", TOT), (AF_OC, f"OC 示意：{AF_OC}", PUR)]:
        g.poly([(X(a), 32), (X(a) - 8, 18), (X(a) + 8, 18)], col, 1, fill=col, closed=True)
        g.text(X(a), 12, lab, 15, col, anchor="middle", weight="bold")
    g.text(X(0) + 8, 395, "A_f = u_f / Δσ_d（飽和、σ_3 固定的軸壓）", 18, INK, anchor="middle", weight="bold")
    g.text(X(-0.5), 420, "← 負孔壓（剪脹）", 15, PUR, anchor="middle", weight="bold")
    g.text(X(1.2), 420, "正孔壓（剪縮）→", 15, TOT, anchor="middle", weight="bold")
    g.save("figs/fig14_arange.svg")


# ───────── fig15 S_u / σ'v0 幾何 ─────────
def fig15():
    g = SVG(1200, 480)
    ax = Ax(g, 70, 400, 3.9)
    ax.axes(215, 86, "σ", "τ")
    ax.ray(PHI, 150, color=EFF, sw=3.2)
    D1 = 2*SU_A1
    ax.semi(S3 + SU_A1, SU_A1, TOT, 2.2, "8 6")
    ax.semi(S3E_A1 + SU_A1, SU_A1, EFF, 3, fill=EFF, op=0.14)
    ax.semi(C_E, R, "#9AA3AE", 1.8, "5 5")
    ax.tick(S3E_A1, f"{S3E_A1:.1f}", EFF); ax.tick(S3, f"{S3:.0f}", INK); ax.tick(S3 + D1, f"{S3 + D1:.1f}", TOT)
    g.text(ax.X(S3), ax.y0 + 48, "σ'_{1f} = σ'_{v0}", 16, RED, anchor="middle", weight="bold")
    g.line(ax.X(S3), ax.y0, ax.X(S3), ax.Y(0) - 0, RED, 1)
    dot(g, ax.X(S3), ax.y0, RED, 7)
    xc = S3E_A1 + SU_A1
    ax.line(xc, 0, xc, SU_A1, color=INK, sw=1.6, dash="4 4")
    g.text(ax.X(xc) + 6, ax.Y(SU_A1/2), f"S_u = {SU_A1:.1f}", 16, INK, weight="bold", bg=W)
    g.text(ax.X(128), ax.y0 + 48, f"灰虛線：A_f = {AF} 的破壞圓（S_u = {SU:.0f}）", 14, MUTED, weight="bold")
    g.text(ax.X(150), ax.Y(150*math.tan(R_(PHI))) - 10, f"φ' = {PHI:.0f}°", 18, EFF, anchor="end", weight="bold", bg=W)
    g.arrow(ax.X(S3 + SU_A1), ax.Y(SU_A1) - 14, ax.X(xc) + 4, ax.Y(SU_A1) - 14, TOT, 2.4, 10)
    g.text(ax.X(150), ax.Y(SU_A1) - 24, "A_f = 1：u_f = Δσ_d", 15, TOT, weight="bold", bg=W)
    card(g, 960, 30, 225, 410, PANEL)
    g.text(1072, 66, "推導三行", 20, NAVY, anchor="middle", weight="bold")
    for i, (s, c) in enumerate([("A_f = 1 ⇒ u_f = Δσ_d", INK), ("σ'_1 = σ_3 + Δσ_d − u_f", INK), ("　　= σ_3 = σ'_{v0}", RED), ("", INK),
                                ("右端點固定，圓往左長", INK), ("直到切到 φ'：", INK), ("R = (σ'_{v0} − R) sin φ'", EFF), ("", INK),
                                (f"S_u/σ'_{{v0}} = {SUR_A1:.3f}", NAVY)]):
        g.text(980, 104 + i*36, s, 16, c, weight="bold")
    g.save("figs/fig15_surat.svg")


# ───────── fig16 深度剖面 ─────────
def fig16():
    g = SVG(1200, 470)
    ox, oy, kx, kz = 170, 60, 2.6, 18
    g.arrow(ox, oy, ox + 440, oy, INK, 2, 10); g.arrow(ox, oy, ox, oy + 380, INK, 2, 10)
    g.text(ox + 444, oy + 6, "kPa", 16, INK, weight="bold"); g.text(ox - 10, oy + 384, "z (m)", 16, INK, anchor="end", weight="bold")
    for z in ZS:
        g.line(ox - 6, oy + z*kz, ox, oy + z*kz, INK, 1.5); g.text(ox - 10, oy + z*kz + 5, f"{z}", 14, MUTED, anchor="end")
    for v in [0, 40, 80, 120, 160]:
        g.line(ox + v*kx, oy - 6, ox + v*kx, oy, INK, 1.5); g.text(ox + v*kx, oy - 12, f"{v}", 14, MUTED, anchor="middle")
    g.poly([(ox + s*kx, oy + z*kz) for s, z in zip(SV, ZS)], WATERD, 3.2)
    g.poly([(ox + s*kx, oy + z*kz) for s, z in zip(SU_Z, ZS)], UUC, 3.4)
    g.text(ox + SV[-1]*kx - 8, oy + ZS[-1]*kz + 26, "σ'_{v0} = γ'z", 17, WATERD, anchor="end", weight="bold")
    g.text(ox + SU_Z[-1]*kx + 10, oy + ZS[-1]*kz - 4, "S_u = 0.333 σ'_{v0}", 17, UUC, weight="bold")
    zz = 10
    g.line(ox, oy + zz*kz, ox + SV10*kx, oy + zz*kz, "#9AA3AE", 1.2, "4 4")
    dot(g, ox + SU10*kx, oy + zz*kz, UUC, 6); dot(g, ox + SV10*kx, oy + zz*kz, WATERD, 6)
    g.text(ox + SV10*kx + 10, oy + zz*kz - 8, f"z = 10 m：σ'_{{v0}} = {SV10:.0f}、S_u = {SU10:.1f}", 15, INK, weight="bold", bg=W)
    card(g, 700, 50, 480, 380, PANEL)
    g.text(720, 88, "這條直線告訴你什麼", 20, NAVY, weight="bold")
    for i, s in enumerate([f"• 假設 γ' = {GAM:.0f} kN/m³、水位在地表", "• NC 黏土 S_u 從地表 0 開始線性增加",
                           "• 斜率只由 φ'（與 A_f）決定", "", "考場用途：", "• 給 φ'，直接估某深度 S_u",
                           "• 給 S_u 剖面，反推是否 NC", "• 算出比值 > 0.5 → 一定代錯"]):
        g.text(720, 128 + i*36, s, 17, INK if s != "考場用途：" else EFF, weight="bold" if s in ("考場用途：",) else "normal")
    g.save("figs/fig16_depth.svg")


# ───────── fig17 CU 四步速算 ─────────
def fig17():
    g = SVG(1200, 400)
    steps = [("1", "組總應力", "σ_1 = σ_3 + Δσ_d", f"= {S3:.0f} + {DSD:.0f} = {S1:.0f}", TOT, TOTBG),
             ("2", "兩邊同扣 u_f", "σ'_3 = σ_3 − u_f", f"= {S3E:.0f}；σ'_1 = {S1E:.0f}", EFF, EFFBG),
             ("3", "正弦捷徑", "sin φ' = (σ'_1−σ'_3)/(σ'_1+σ'_3)", f"= {S1E - S3E:.0f}/{S1E + S3E:.0f} → {PHI:.0f}°", CDC, CDBG),
             ("4", "回頭檢查", "A_f = u_f / Δσ_d", f"= {UF:.0f}/{DSD:.0f} = {AF_BACK:.2f} ✓", GOLD, GOLDBG)]
    for i, (n, a, b, c, col, bg) in enumerate(steps):
        x = 20 + i*295
        card(g, x, 40, 270, 250, bg, col, 12, 2.2)
        g.circle(x + 40, 84, 22, fill=col, stroke=W, sw=2); g.text(x + 40, 92, n, 22, W, anchor="middle", weight="bold")
        g.text(x + 74, 92, a, 21, col, weight="bold")
        g.text(x + 135, 170, b, 15 if i == 2 else 18, INK, anchor="middle", weight="bold")
        g.text(x + 135, 220, c, 18, col, anchor="middle", weight="bold")
        if i < 3: g.arrow(x + 272, 165, x + 293, 165, INK, 2.4, 9)
    g.text(600, 345, f"示範黏土 A：σ_3 = {S3:.0f}、Δσ_d = {DSD:.0f}、u_f = {UF:.0f}（kPa）", 19, INK, anchor="middle", weight="bold")
    g.text(600, 380, "c' ≠ 0 時第 3 步改用 σ'_1 = σ'_3 K_p + 2c'√K_p（兩組試驗相減消去 c'）", 16, MUTED, anchor="middle")
    g.save("figs/fig17_cuflow.svg")


# ───────── fig18 NC 比例法：相似圓 ─────────
def fig18():
    g = SVG(1200, 480)
    ax = Ax(g, 70, 410, 2.05)
    ax.axes(420, 175, "σ", "τ")
    ax.ray(PHI, 290, color=EFF, sw=3)
    ax.ray(PHI_CU, 420, color=TOT, sw=2.2, dash="9 6")
    for s3, D, u, op in [(S3, DSD, UF, 0.14), (S3_2, DSD_2, UF_2, 0.08)]:
        ax.semi(s3 + D/2, D/2, TOT, 2.2, "7 5")
        ax.semi(s3 - u + D/2, D/2, EFF, 2.8, fill=EFF, op=op)
    for v in [S3E, S1E, 2*S3E, 2*S1E]: ax.tick(v, f"{v:.0f}", EFF)
    for v in [S3, S1, S3_2, S3_2 + DSD_2]: ax.tick(v, f"{v:.0f}", TOT, dy=44)
    g.text(ax.X(290), ax.Y(290*math.tan(R_(PHI))) - 10, f"φ' = {PHI:.0f}°", 18, EFF, anchor="end", weight="bold", bg=W)
    g.text(ax.X(420), ax.Y(420*math.tan(R_(PHI_CU))) - 10, f"φ_{{cu}} = {PHI_CU:.1f}°", 18, TOT, anchor="end", weight="bold", bg=W)
    g.text(ax.X(15), 40, "σ_3 加倍 → 整張圖從原點放大 2 倍", 17, NAVY, anchor="start", weight="bold", bg=W)
    card(g, 960, 30, 225, 420, PANEL)
    g.text(1072, 68, "比例法", 21, NAVY, anchor="middle", weight="bold")
    rows = [("σ_3", f"{S3:.0f} → {S3_2:.0f}"), ("Δσ_d", f"{DSD:.0f} → {DSD_2:.0f}"), ("u_f", f"{UF:.0f} → {UF_2:.0f}"),
            ("Δσ_d/σ_3", f"{DSD/S3:.1f}（不變）"), ("u_f/σ_3", f"{UF/S3:.1f}（不變）")]
    for i, (a, b) in enumerate(rows):
        g.text(980, 112 + i*52, a, 17, MUTED, weight="bold"); g.text(980, 136 + i*52, b, 18, INK, weight="bold")
    g.text(1072, 400, "前提：同一 NC 土、c' = 0", 14, RED, anchor="middle", weight="bold")
    g.text(1072, 424, "包絡線過原點", 14, RED, anchor="middle", weight="bold")
    g.save("figs/fig18_ratio.svg")


# ───────── fig19 破壞面角度陷阱 ─────────
def fig19():
    g = SVG(1200, 470)
    cx, cy, w, h = 330, 235, 200, 320
    g.rect(cx - w/2, cy - h/2, w, h, fill="#EEF1F5", stroke=INK, sw=2.4)
    for i in range(4):
        x = cx - 70 + i*47
        g.arrow(x, cy - h/2 - 44, x, cy - h/2 - 4, INK, 2.2, 10); g.arrow(x, cy + h/2 + 44, x, cy + h/2 + 4, INK, 2.2, 10)
    g.text(cx + w/2 + 12, cy - h/2 - 16, "σ'_1", 18, INK, weight="bold")
    def plane(th, col, dash=None, sw=3.4):
        t = math.tan(R_(th)); dx = min(w/2, (h/2)/t) - 3
        g.line(cx - dx, cy + dx*t, cx + dx, cy - dx*t, col, sw, dash)
        return dx, t
    dx, t = plane(TH, CDC)
    plane(TH_WRONG, RED, "9 6", 2.6)
    g.line(cx, cy, cx + 90, cy, INK, 1.2, "4 4")
    g.arc(cx, cy, 58, 0, TH, CDC, 2.2); g.arc(cx, cy, 82, 0, TH_WRONG, RED, 2)
    g.text(cx + 66, cy - 40, f"{TH:.0f}°", 17, CDC, weight="bold", bg="#EEF1F5")
    g.text(cx + 92, cy - 6, f"{TH_WRONG:.1f}°", 16, RED, weight="bold", bg="#EEF1F5")
    g.text(cx, 462, "與大主應力面（水平面）的夾角", 15, MUTED, anchor="middle")
    card(g, 620, 40, 560, 170, CDBG, CDC, 12, 2.2)
    g.text(640, 80, "✓ 用 φ'（顆粒真的沿這個面滑）", 20, CDC, weight="bold")
    g.text(640, 126, f"θ = 45° + φ'/2 = 45° + {PHI:.0f}°/2 = {TH:.0f}°", 20, INK, weight="bold")
    g.text(640, 170, "只有一個答案：由骨架摩擦決定", 17, MUTED)
    card(g, 620, 230, 560, 200, UUBG, UUC, 12, 2.2)
    g.text(640, 270, "× 用 φ_{cu}（試驗路徑的產物）", 20, UUC, weight="bold")
    g.text(640, 316, f"45° + {PHI_CU:.1f}°/2 = {TH_WRONG:.1f}°　錯", 20, INK, weight="bold")
    g.text(640, 358, f"同一土換路徑 φ_{{cu}} 就跳：AC {PHI_CU_AC13}°、LE {PHI_CU_LE13}°", 16, INK)
    g.text(640, 390, "（SM-2013-3）→ 破壞面不可能跟著跳", 16, MUTED)
    g.text(640, 418, "φ_u = 0 也一樣：45° 不是真的破壞面", 16, UUC, weight="bold")
    g.save("figs/fig19_plane.svg")


# ───────── fig20 現場情境選試驗 ─────────
def fig20():
    g = SVG(1200, 460)
    def box(x, y, w, h, t1, t2, col, bg, s1=19):
        card(g, x, y, w, h, bg, col, 10, 2.2)
        g.text(x + w/2, y + h/2 - 6, t1, s1, col, anchor="middle", weight="bold")
        g.text(x + w/2, y + h/2 + 22, t2, 15, INK, anchor="middle")
    def dia(cx, cy, w, h, t):
        g.poly([(cx, cy - h/2), (cx + w/2, cy), (cx, cy + h/2), (cx - w/2, cy)], NAVY, 2.2, fill=W, closed=True)
        g.text(cx, cy + 6, t, 17, NAVY, anchor="middle", weight="bold")
    box(20, 190, 180, 80, "分析哪個時點？", "問：水來得及排嗎", NAVY, "#E8ECF2", 18)
    g.arrow(200, 230, 250, 230, INK, 2.2)
    dia(360, 230, 220, 120, "載重施加速度 ≫ 排水？")
    g.line(360, 170, 360, 110, INK, 2.2); g.text(370, 146, "是（黏土、快）", 15, UUC, weight="bold")
    g.arrow(470, 230, 560, 230, INK, 2.2); g.text(480, 220, "否（砂、慢、長期）", 15, CDC, weight="bold")
    dia(640, 70, 240, 100, "先在前期載重下壓密？")
    g.line(360, 110, 360, 70, INK, 2.2); g.arrow(360, 70, 518, 70, INK, 2.2)
    g.arrow(760, 70, 820, 70, INK, 2.2); g.text(752, 58, "否", 16, UUC, weight="bold")
    box(825, 25, 350, 95, "UU → S_u（φ_u = 0）", "施工期／開挖後立即／快速填土", UUC, UUBG)
    g.arrow(640, 120, 640, 175, INK, 2.2); g.text(650, 155, "是", 16, CUC, weight="bold")
    box(825, 150, 350, 95, "CU → φ_{cu} ＋ c'、φ'", "既有堤上再加高／水位驟降", CUC, CUBG)
    g.line(640, 175, 640, 197, INK, 2.2); g.arrow(640, 197, 820, 197, INK, 2.2)
    box(565, 300, 610, 95, "CD（或 CU 量 u）→ c'、φ'", "長期穩定／砂土／緩慢加載：一律有效應力分析", CDC, CDBG)
    g.line(560, 230, 560, 347, INK, 2.2); g.arrow(560, 347, 565, 347, INK, 2.2)
    g.text(600, 440, "黏土短期多半最危險（UU），長期（CD）再檢核；一個工程常同時需要兩組參數", 18, INK, anchor="middle", weight="bold")
    g.save("figs/fig20_field.svg")


if __name__ == "__main__":
    import sys
    names = sys.argv[1:] or [f"fig{i:02d}" for i in range(1, 21)]
    for n in names: globals()[n]()
    print("ok", len(names))
