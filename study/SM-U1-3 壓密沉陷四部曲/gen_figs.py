"""SM-U1-3 壓密沉陷四部曲 — 向量圖產生器（數字全部取自 params.py）"""
from math import log10
from params import *
from svglib import *
import params as P

F = "figs/"
f1 = lambda v: f"{v:.1f}"

# ───────── F1 四部曲總覽 ─────────
def fig_overview():
    s = SVG(1200, 330, ts=1.1)
    cards = [
        ("1", "算現況", "黏土層中點 z = 8 m", f"p_0' = {f1(P0)}", "kPa", "水位下用浮單位重累加", P0c),
        ("2", "算增量", "載重型式決定擴散與否", f"Δσ = {DS_AREA:.0f}", "kPa", f"基腳 2:1 法僅 {f1(DS_FOOT)} kPa", CCc),
        ("3", "看歷史", "土壤記得被壓過多重", f"p_c' = {PC:.0f}", "kPa", f"OCR = {OCR:.2f} → 過壓密", PCc),
        ("4", "選公式", "三點排上對數軸", f"S_c = {f1(S_C)}", "mm", f"p_f' = {f1(PF)} > p_c' → Case C", CRc),
    ]
    w, gap, x = 252, 51, 16
    for i, (n, t, q, big, unit, sub, col) in enumerate(cards):
        s.rect(x, 20, w, 290, fill=PANEL, stroke="#D5DAE1", sw=1.5, rx=14)
        s.circle(x+40, 66, 22, fill=col, stroke="none")
        s.text(x+40, 74, n, 22, "#FFFFFF", "middle", "bold")
        s.text(x+74, 75, t, 26, col, "start", "bold")
        s.text(x+w/2, 128, q, 17, MUTED, "middle")
        s.line(x+24, 150, x+w-24, 150, GRID, 1.5)
        s.text(x+w/2, 208, big, 34, INK, "middle", "bold")
        s.text(x+w/2, 240, unit, 17, MUTED, "middle")
        s.text(x+w/2, 285, sub, 16, col, "middle", "bold")
        if i < 3:
            s.arrow(x+w+8, 165, x+w+gap-8, 165, "#9AA3AE", 3, 14)
        x += w + gap
    s.save(F+"fig01_overview.svg")

# ───────── F2 地層 + σ/u/σ′ ─────────
def fig_profile():
    s = SVG(1200, 640, ts=1.35)
    top, sc = 70, 50                        # 50 px / m
    Y = lambda z: top + z*sc
    x0, x1 = 120, 470
    fills = [SAND1, SAND2, CLAY]
    for (t, b, g, name), fc in zip(LAYERS, fills):
        s.rect(x0, Y(t), x1-x0, Y(b)-Y(t), fill=fc, stroke=INK, sw=1.5)
        ym = (Y(t)+Y(b))/2
        gl = "γ" if t < Z_WT else "γ_{sat}"
        dy = -62 if name == "黏土" else -8
        s.text((x0+x1)/2, ym+dy, name, 20, INK, "middle", "bold")
        s.text((x0+x1)/2, ym+dy+30, f"{gl} = {g} kN/m³", 17, MUTED, "middle")
    s.rect(x0, Y(10), x1-x0, 30, fill=ROCK, stroke=INK, sw=1.5)
    s.text((x0+x1)/2, Y(10)+21, "不透水岩盤", 16, "#FFFFFF", "middle", "bold")
    for z in (0, 2, 6, 10):
        s.text(x0-12, Y(z)+6, f"{z} m", 16, MUTED, "end")
    s.line(x0, Y(Z_WT), x1+30, Y(Z_WT), WATER, 2.5)
    s.poly([(x1+14, Y(2)-14), (x1+30, Y(2)-14), (x1+22, Y(2)-2)], WATER, 1, WATER, closed=True)
    s.text(x1+40, Y(2)+6, "地下水位", 17, WATER, "start", "bold")
    s.line(x0, Y(Z_MID), x1, Y(Z_MID), CCc, 2.5, "10,7")
    s.circle((x0+x1)/2, Y(Z_MID), 9, fill=CCc)
    s.text(x1+40, Y(Z_MID)+6, "中點 z = 8 m", 18, CCc, "start", "bold")
    # 黏土厚度標註
    s.dim(x1+22, Y(6), x1+22, Y(10), "", MUTED)
    s.text(x1+32, Y(9.2)+6, "H = 4 m", 16, MUTED, "start", "bold")
    # ── 右：應力圖 ──
    ox, px = 700, 2.3
    X = lambda p: ox + p*px
    for p in (0, 50, 100, 150, 200):
        s.line(X(p), Y(0), X(p), Y(10), GRID, 1)
        s.text(X(p), Y(0)-10, str(p), 15, MUTED, "middle")
    for z in (0, 2, 4, 6, 8, 10):
        s.line(ox, Y(z), X(200), Y(z), GRID, 1)
        s.text(ox-12, Y(z)+5, str(z), 15, MUTED, "end")
    s.line(ox, Y(0), ox, Y(10)+8, INK, 1.8); s.line(ox, Y(0), X(205), Y(0), INK, 1.8)
    s.text(X(200)+10, Y(0)-32, "應力 (kPa)", 16, MUTED, "end")
    s.text(ox-12, Y(0)-32, "z (m)", 16, MUTED, "end")
    zs = [0, 2, 6, 10]
    s.poly([(X(sigma(z)), Y(z)) for z in zs], "#3B4656", 3)
    s.poly([(X(u(z)), Y(z)) for z in zs], WATER, 3, dash="9,6")
    s.poly([(X(sig_eff(z)), Y(z)) for z in zs], CCc, 3.5)
    s.text(X(sigma(10))-6, Y(9.6), "σ", 22, "#3B4656", "end", "bold")
    s.text(X(u(9.3))-14, Y(9.3), "u", 22, WATER, "end", "bold")
    s.text(X(sig_eff(10))+12, Y(9.4), "σ'", 22, CCc, "start", "bold")
    s.line(ox, Y(8), X(sigma(8)), Y(8), PCc, 2, "7,5")
    s.circle(X(P0), Y(8), 9, fill=CCc)
    s.line(X(P0)+8, Y(8)-8, 1080, Y(6.9)+10, CCc, 1.5)
    lab = f"p_0' = {f1(P0)} kPa"; bw_ = measure(lab, 19*s.ts, True) + 24
    s.rect(1195-bw_, Y(6.9)-22, bw_, 40, fill="#FFFFFF", stroke=CCc, sw=1.5, rx=8)
    s.text(1195-bw_/2, Y(6.9)+7, lab, 19, CCc, "middle", "bold")
    s.text(X(sigma(8))+20, Y(8)+22, f"σ = {f1(sigma(8))}", 15, "#3B4656")
    s.text(X(u(8))-10, Y(8)+22, f"u = {f1(u(8))}", 15, WATER, "end")
    s.save(F+"fig02_profile.svg")

# ───────── F3 為什麼取中點：分層驗證 ─────────
def fig_midpoint():
    s = SVG(900, 470, ts=1.3)
    # 左：黏土條分 4 層
    top, sc = 60, 90
    Y = lambda z: top + (z-CLAY_TOP)*sc
    x0, x1 = 60, 230
    s.text((x0+x1)/2, 36, "黏土分 4 薄層", 18, INK, "middle", "bold")
    for i in range(4):
        z0 = CLAY_TOP + i; zm = z0 + 0.5
        s.rect(x0, Y(z0), x1-x0, sc, fill=CLAY, stroke=INK, sw=1.2)
        s.circle((x0+x1)/2, Y(zm), 6, fill=P0c, stroke="none")
        s.text(x1+12, Y(zm)+6, f"p_0' = {f1(sig_eff(zm))}", 16, P0c)
    s.line(x0-10, Y(8), x1+150, Y(8), CCc, 2, "8,6")
    s.text(x0-14, Y(8)+6, "8 m", 15, CCc, "end", "bold")
    s.text(x0-14, Y(6)+6, "6 m", 15, MUTED, "end"); s.text(x0-14, Y(10)+6, "10 m", 15, MUTED, "end")
    s.text((x0+x1)/2+40, Y(10)+42, "σ' 沿深度線性：74.8 → 105.5", 15, MUTED, "middle")
    # 右：分層數 vs 沉陷
    bx, bw = 520, 330
    s.text(bx+bw/2-40, 36, "Case C 沉陷量 S_c (mm)", 18, INK, "middle", "bold")
    rows = [(1, "中點一次算"), (2, "分 2 層"), (4, "分 4 層"), (8, "分 8 層")]
    vmax = 100
    for k, (n, lab) in enumerate(rows):
        y = 80 + k*78
        v = sublayer(n)
        col = CCc if n == 1 else "#8E9AAB"
        s.text(bx-14, y+30, lab, 17, INK, "end", "bold" if n == 1 else "normal")
        s.rect(bx, y+8, bw*v/vmax, 34, fill=col, stroke="none", rx=4)
        s.text(bx+bw*v/vmax+10, y+32, f"{v:.2f}", 18, col, "start", "bold")
    err = (sublayer(1)-sublayer(8))/sublayer(8)*100
    s.rect(bx-150, 400, 490, 50, fill="#E6F2EF", stroke=OK, sw=1.5, rx=10)
    s.text(bx+95, 432, f"中點一次算 vs 分 8 層：差 {err:.1f}%", 19, OK, "middle", "bold")
    s.save(F+"fig03_midpoint.svg")

# ───────── F4 2:1 應力傳佈幾何 ─────────
def fig_21():
    s = SVG(720, 490, ts=1.3)
    gy, sc, cx = 90, 38, 350
    Y = lambda z: gy + z*sc            # z 從地表起算
    X = lambda m: cx + m*sc
    s.rect(20, Y(6), 680, Y(10)-Y(6), fill=CLAY, stroke="none")
    s.text(34, Y(6)+26, "黏土", 17, P0c, "start", "bold")
    s.line(20, gy, 700, gy, INK, 2.5)
    s.text(34, gy-10, "地表", 15, MUTED)
    # 柱 + 基腳
    s.rect(X(-0.3), gy-30, 0.6*sc, Y(DF)-gy-14+30, fill="#B8BEC7", stroke=INK, sw=1.5)
    s.rect(X(-B/2), Y(DF)-14, B*sc, 14, fill="#8C95A1", stroke=INK, sw=1.5)
    s.arrow(cx, gy-64, cx, gy-32, CCc, 3, 13)
    s.text(cx+14, gy-44, f"Q = {Q:.0f} kN", 18, CCc, "start", "bold")
    # 2:1 擴散
    zb = CLAY_BOT - DF
    s.poly([(X(-B/2), Y(DF)), (X(-(B+zb)/2), Y(CLAY_BOT)), (X((B+zb)/2), Y(CLAY_BOT)), (X(B/2), Y(DF))],
           PCc, 2.2, fill=PCc, dash="8,6", closed=True, op=0.10)
    # 中點寬度
    wm = B + Z_FROM_BASE
    s.line(20, Y(Z_MID), 700, Y(Z_MID), WATER, 2, "9,6")
    s.circle(cx, Y(Z_MID), 8, fill=CCc)
    s.dim(X(-wm/2), Y(Z_MID)+26, X(wm/2), Y(Z_MID)+26, f"B + z = {B+Z_FROM_BASE:.1f} m", INK, 16, (0, 22))
    s.text(cx, Y(DF)+26, "B = 2 m", 15, INK, "middle", "bold")
    # z 從基礎底面
    xr = X(3.9)
    s.line(X(B/2)+4, Y(DF), xr+12, Y(DF), "#9AA3AE", 1, "3,3")
    s.dim(xr, Y(DF), xr, Y(Z_MID), "", OK)
    s.text(xr+10, (Y(DF)+Y(Z_MID))/2+6, f"z = {Z_FROM_BASE} m（對）", 17, OK, "start", "bold")
    s.text(xr+10, (Y(DF)+Y(Z_MID))/2+30, "從基礎底面起算", 14, OK)
    # 錯誤：地表起算
    xl = X(-4.2)
    s.dim(xl, gy, xl, Y(Z_MID), "", CCc)
    s.text(xl-10, Y(4.2), "z = 8 m（錯）", 17, CCc, "end", "bold")
    s.text(xl-10, Y(4.2)+24, "地表起算", 14, CCc, "end")
    s.dim(X(1.9), gy, X(1.9), Y(DF), "", MUTED)
    s.text(X(1.9)+8, Y(0.75)+6, f"D_f = {DF} m", 14, MUTED)
    s.text(cx, Y(3.4), "2 垂直 : 1 水平擴散", 16, PCc, "middle", "bold")
    s.save(F+"fig04_21geom.svg")

# ───────── F5 Δσ 隨深度 ─────────
def fig_depth():
    s = SVG(560, 570, ts=1.45)
    ox, oy, W, Hh = 120, 80, 400, 420
    X = lambda p: ox + p/200*W
    Y = lambda z: oy + z/10*Hh
    for p in (0, 50, 100, 150, 200):
        s.line(X(p), oy, X(p), Y(10), GRID, 1); s.text(X(p), oy-12, str(p), 15, MUTED, "middle")
    for z in (0, 2, 4, 6, 8, 10):
        s.line(ox, Y(z), X(200), Y(z), GRID, 1); s.text(ox-12, Y(z)+5, str(z), 15, MUTED, "end")
    s.line(ox, oy, ox, Y(10)+6, INK, 1.8); s.line(ox, oy, X(205), oy, INK, 1.8)
    s.text(X(200), oy-40, "Δσ (kPa)", 16, MUTED, "end")
    s.text(ox-12, oy-40, "z (m)", 15, MUTED, "end")
    s.text(ox, Y(10)+42, "z 從基礎底面起算", 14, MUTED, "start")
    pts = [(X(ds21(z/20)), Y(z/20)) for z in range(0, 201)]
    s.poly(pts, PCc, 3.5)
    s.line(X(DS_AREA), oy, X(DS_AREA), Y(10), CCc, 3.5)
    s.text(X(DS_AREA)+10, Y(9.3), "大面積：垂直線 80", 16, CCc, "start", "bold")
    s.text(X(100), Y(1.9), "2:1 法：急速衰減", 16, PCc, "start", "bold")
    s.circle(X(DS_FOOT), Y(Z_FROM_BASE), 8, fill=OK)
    s.text(X(DS_FOOT)+14, Y(Z_FROM_BASE)+6, f"z=6.5 → {f1(DS_FOOT)}（對）", 15, OK, "start", "bold", bg="#FFFFFF")
    s.add(f'<circle cx="{X(DS_FOOT_WRONG):.1f}" cy="{Y(Z_MID):.1f}" r="8" fill="#FFFFFF" stroke="{CCc}" stroke-width="3"/>')
    s.text(X(DS_FOOT_WRONG)+14, Y(Z_MID)+6, f"z=8 → {f1(DS_FOOT_WRONG)}（錯）", 15, CCc, "start", "bold", bg="#FFFFFF")
    s.save(F+"fig05_depth.svg")

# ───────── F6 e-log p′ ─────────
def e_of(p):
    return E0 - CR*log10(p/P0) if p <= PC else E0 - CR*log10(PC/P0) - CC*log10(p/PC)
def fig_elogp():
    s = SVG(900, 540, ts=1.25)
    ox, oy, W, Hh = 90, 40, 760, 420
    pmin, pmax, emin, emax = 20, 500, 0.84, 1.10
    X = lambda p: ox + (log10(p)-log10(pmin))/(log10(pmax)-log10(pmin))*W
    Y = lambda e: oy + (emax-e)/(emax-emin)*Hh
    for p in (20, 50, 100, 200, 500):
        s.line(X(p), oy, X(p), oy+Hh, GRID, 1); s.text(X(p), oy+Hh+26, str(p), 15, MUTED, "middle")
    for e in (0.85, 0.90, 0.95, 1.00, 1.05, 1.10):
        s.line(ox, Y(e), ox+W, Y(e), GRID, 1); s.text(ox-12, Y(e)+5, f"{e:.2f}", 15, MUTED, "end")
    s.line(ox, oy, ox, oy+Hh, INK, 1.8); s.line(ox, oy+Hh, ox+W, oy+Hh, INK, 1.8)
    s.text(ox+W, oy+Hh+52, "log p' (kPa)", 16, MUTED, "end")
    s.text(ox-12, oy-14, "e", 18, MUTED, "end", "bold")
    s.line(X(pmin), Y(e_of(pmin)), X(PC), Y(e_of(PC)), CRc, 4, cap="round")
    s.line(X(PC), Y(e_of(PC)), X(pmax), Y(e_of(pmax)), CCc, 4, cap="round")
    s.text(X(28), Y(e_of(28))-16, f"再壓縮線 C_r = {CR}", 18, CRc, "start", "bold")
    s.text(X(240), Y(0.975), f"處女壓縮線 C_c = {CC}", 18, CCc, "start", "bold")
    for p, col, lab, dy in ((P0, P0c, f"p_0' = {f1(P0)}", 0), (PC, PCc, f"p_c' = {PC:.0f}", 0), (PF, CCc, f"p_f' = {f1(PF)}", 0)):
        s.line(X(p), Y(e_of(p)), X(p), oy+Hh, col, 1.8, "6,5")
        s.circle(X(p), Y(e_of(p)), 8, fill=col)
    s.text(X(P0)-10, Y(E0)-16, f"p_0' = {f1(P0)}", 16, P0c, "end", "bold")
    s.text(X(PC)+2, Y(e_of(PC))-18, f"p_c' = {PC:.0f}", 16, PCc, "start", "bold")
    s.text(X(PF)+16, Y(e_of(PF))-12, f"p_f' = {f1(PF)}", 16, CCc, "start", "bold")
    # Δe 標註（左側 y 軸旁）
    xa = ox + 26
    for ea, eb, col, lab in ((E0, e_of(PC), CRc, f"Δe_r = {DE_R:.4f}"), (e_of(PC), e_of(PF), CCc, f"Δe_c = {DE_C:.4f}")):
        s.line(xa-8, Y(ea), X(P0), Y(ea), "#B7BEC8", 1, "3,3")
        s.line(xa, Y(ea), xa, Y(eb), col, 5)
    s.line(xa-8, Y(e_of(PF)), X(PF), Y(e_of(PF)), "#B7BEC8", 1, "3,3")
    s.text(xa+12, Y(E0)-6, f"Δe_r = {DE_R:.4f}", 15, CRc, "start", "bold")
    s.text(xa+12, (Y(e_of(PC))+Y(e_of(PF)))/2+10, f"Δe_c = {DE_C:.4f}", 15, CCc, "start", "bold")
    s.save(F+"fig06_elogp.svg")

# ───────── F7 三相圖：S = Δe/(1+e0)·H ─────────
def fig_phase():
    s = SVG(680, 500, ts=1.15)
    k = 190; base = 440; w = 150
    def col(x, e, title, colr):
        s.rect(x, base-k, w, k, fill="#C9B8A6", stroke=INK, sw=1.8)
        s.text(x+w/2, base-k/2+7, "土粒 1", 19, INK, "middle", "bold")
        s.rect(x, base-k-e*k, w, e*k, fill="#DCEBF5", stroke=INK, sw=1.8)
        s.text(x+w/2, 28, title, 18, colr, "middle", "bold")
    col(150, E0, "加載前", INK)
    s.text(225, base-k-E0*k/2+7, "孔隙 e_0", 19, WATER, "middle", "bold")
    show = 0.40
    col(430, E0-show, "加載後", CCc)
    s.text(505, base-k-(E0-show)*k/2+7, "e_0 − Δe", 19, WATER, "middle", "bold")
    top0, top1 = base-k-E0*k, base-k-(E0-show)*k
    s.rect(430, top0, w, top1-top0, fill="none", stroke=CCc, sw=2, dash="7,5")
    s.text(505, (top0+top1)/2+7, "Δe", 20, CCc, "middle", "bold")
    s.line(300, top0, 430, top0, "#9AA3AE", 1.2, "4,4")
    s.dim(110, top0, 110, base, "", INK)
    s.text(100, (top0+base)/2-4, "1 + e_0", 17, INK, "end", "bold")
    s.text(100, (top0+base)/2+20, "↔ H", 17, INK, "end", "bold")
    s.dim(610, top0, 610, top1, "", CCc)
    s.text(622, (top0+top1)/2-2, "Δe", 17, CCc, "start", "bold")
    s.text(622, (top0+top1)/2+22, "↔ S", 17, CCc, "start", "bold")
    s.text(340, 488, "（Δe 放大示意；本例實際 Δe = 0.045）", 14, MUTED, "middle")
    s.save(F+"fig07_phase.svg")

# ───────── F8 Case A / B / C 對數軸 ─────────
def fig_cases():
    s = SVG(1200, 780, ts=1.35)
    lo, hi, xa, xb = 60, 260, 60, 810
    X = lambda p: xa + (log10(p)-log10(lo))/(log10(hi)-log10(lo))*(xb-xa)
    A = sum(settle(P0, PF, pc=P0))
    rows = [
        ("Case A　正常壓密 NC", "p_0' = p_c'，全程走 C_c", CCc, P0, PF, P0, [(P0, PF, CCc, "C_c")], A, "全程 C_c"),
        ("Case B　過壓密、未跨越", "p_f' ≤ p_c'，全程走 C_r（基腳 2:1）", CRc, P0, PF_FOOT, PC, [(P0, PF_FOOT, CRc, "C_r")], S_B, "全程 C_r"),
        ("Case C　過壓密且跨越", "p_0' < p_c' < p_f'，兩段相加（大面積）", PCc, P0, PF, PC,
         [(P0, PC, CRc, "C_r"), (PC, PF, CCc, "C_c")], S_C, f"{f1(S_C_r)} + {f1(S_C_c)}"),
    ]
    for i, (t, sub, col, p0, pf, pc, segs, S, how) in enumerate(rows):
        y0 = 8 + i*256
        fill = "#FBF1EA" if i == 2 else PANEL
        s.rect(10, y0, 1180, 240, fill=fill, stroke=col if i == 2 else "#D5DAE1", sw=2.5 if i == 2 else 1.5, rx=14)
        s.text(34, y0+40, t, 23, col, "start", "bold")
        s.text(34, y0+76, sub, 16, MUTED)
        ay = y0 + 150
        s.line(xa, ay, xb, ay, "#5B6573", 2.2)
        for p in (60, 80, 100, 130, 170, 220, 260):
            s.line(X(p), ay-7, X(p), ay+7, "#5B6573", 1.6)
            s.text(X(p), ay+30, str(p), 13, "#9AA3AE", "middle")
        for a, b, c, lab in segs:
            s.rect(X(a), ay-30, X(b)-X(a), 20, fill=c, stroke="none", rx=5, op=0.75)
            s.text((X(a)+X(b))/2, ay-40, lab, 18, c, "middle", "bold")
        pts = [(p0, P0c), (pc, PCc), (pf, CCc)]
        for p, c in pts: s.circle(X(p), ay, 8, fill=c)
        ly = ay + 64
        if abs(p0-pc) < 1:
            s.text(X(p0), ly, f"p_0' = p_c' = {f1(p0)}", 16, P0c, "middle", "bold")
            s.text(X(pf), ly, f"p_f' = {f1(pf)}", 16, CCc, "middle", "bold")
        else:
            near = X(pf)-X(p0) < 130
            s.text(X(p0)+(6 if near else 0), ly, f"p_0' = {f1(p0)}", 16, P0c, "end" if near else "middle", "bold")
            s.text(X(pc), ay-22 if near else ly, f"p_c' = {pc:.0f}", 16, PCc, "middle", "bold")
            s.text(X(pf)-(6 if near else 0), ly, f"p_f' = {f1(pf)}", 16, CCc, "start" if near else "middle", "bold")
        s.text(xb+14, ay+6, "log p'", 14, MUTED, "start")
        # 結果框
        s.rect(930, y0+40, 236, 160, fill="#FFFFFF", stroke=col, sw=2, rx=12)
        s.text(1048, y0+80, "S_c", 20, MUTED, "middle", "bold")
        s.text(1048, y0+134, f"{f1(S)} mm", 30, col, "middle", "bold")
        s.text(1048, y0+176, how, 15, MUTED, "middle")
    s.save(F+"fig08_cases.svg")

# ───────── F9 判斷流程 ─────────
def fig_flow():
    s = SVG(1000, 640, ts=1.2)
    cx = 300
    def box(x, y, w, h, t1, t2=None, fill=PANEL, stroke="#8E9AAB", col=INK):
        s.rect(x-w/2, y-h/2, w, h, fill=fill, stroke=stroke, sw=2, rx=10)
        if t2:
            s.text(x, y-5, t1, 19, col, "middle", "bold"); s.text(x, y+22, t2, 15, MUTED, "middle")
        else:
            s.text(x, y+7, t1, 19, col, "middle", "bold")
    def diamond(x, y, w, h, t1, t2):
        s.poly([(x, y-h/2), (x+w/2, y), (x, y+h/2), (x-w/2, y)], PCc, 2.2, "#FDF0E6", closed=True)
        s.text(x, y-2, t1, 18, PCc, "middle", "bold"); s.text(x, y+22, t2, 14, MUTED, "middle")
    box(cx, 50, 340, 64, "已知 p_0'、Δσ、p_c'", "步驟 1~3 的產出")
    s.arrow(cx, 82, cx, 116, "#8E9AAB")
    box(cx, 146, 340, 56, "p_f' = p_0' + Δσ")
    s.arrow(cx, 174, cx, 210, "#8E9AAB")
    diamond(cx, 275, 300, 124, "p_c' = p_0' ?", "（OCR = 1）")
    s.arrow(cx+150, 275, 640, 275, CCc); s.text(560, 262, "是", 17, CCc, "middle", "bold")
    box(790, 275, 300, 92, "Case A　全程 C_c", "S ∝ C_c · log(p_f'/p_0')", "#FBECEA", CCc, CCc)
    s.arrow(cx, 337, cx, 378, "#8E9AAB"); s.text(cx+14, 364, "否（OC）", 16, MUTED, "start", "bold")
    diamond(cx, 440, 300, 124, "p_f' ≤ p_c' ?", "（有沒有衝破記憶）")
    s.arrow(cx+150, 440, 640, 440, CRc); s.text(560, 427, "是", 17, CRc, "middle", "bold")
    box(790, 440, 300, 92, "Case B　全程 C_r", "S ∝ C_r · log(p_f'/p_0')", "#EAF0FB", CRc, CRc)
    s.arrow(cx, 502, cx, 546, "#8E9AAB"); s.text(cx+14, 530, "否", 16, MUTED, "start", "bold")
    box(cx, 590, 440, 92, "Case C　C_r 段 + C_c 段", "p_0'→p_c' 走 C_r；p_c'→p_f' 走 C_c", "#FBF1EA", PCc, PCc)
    s.rect(625, 548, 350, 84, fill="#E6F2EF", stroke=OK, sw=1.5, rx=10)
    s.text(790, 582, "驗算：C_r全套 < S_C < C_c全套", 16, OK, "middle", "bold")
    s.text(790, 610, f"{f1(S_ALL_CR)} < {f1(S_C)} < {f1(S_ALL_CC)} mm", 16, OK, "middle")
    s.save(F+"fig09_flow.svg")

# ───────── F10 Case C 兩段拆解 ─────────
def fig_split():
    s = SVG(860, 430, ts=1.1)
    bx, W = 200, 600
    lr, lc = log10(PC/P0), log10(PF/PC)
    s.text(bx-16, 92, "對數軸長度", 18, INK, "end", "bold")
    s.text(bx-16, 116, "log(比值)", 14, MUTED, "end")
    tot = lr + lc
    s.rect(bx, 70, W*lr/tot, 50, fill=CRc, stroke="#FFFFFF", sw=2, rx=4, op=0.85)
    s.rect(bx+W*lr/tot, 70, W*lc/tot, 50, fill=CCc, stroke="#FFFFFF", sw=2, rx=4, op=0.85)
    s.text(bx+W*lr/tot/2, 102, f"{lr:.3f}", 19, "#FFFFFF", "middle", "bold")
    s.text(bx+W*lr/tot+W*lc/tot/2, 102, f"{lc:.3f}", 19, "#FFFFFF", "middle", "bold")
    s.text(bx+W*lr/tot/2, 56, "p_0' → p_c'（C_r 段）", 15, CRc, "middle", "bold")
    s.text(bx+W*lr/tot+W*lc/tot/2, 56, "p_c' → p_f'（C_c 段）", 15, CCc, "middle", "bold")
    s.text(bx+W/2, 170, f"× 斜率（C_c / C_r = {CC/CR:.1f} 倍）", 18, PCc, "middle", "bold")
    s.arrow(bx+W/2, 184, bx+W/2, 214, PCc)
    s.text(bx-16, 262, "沉陷貢獻", 18, INK, "end", "bold")
    s.text(bx-16, 286, "mm", 14, MUTED, "end")
    s.rect(bx, 240, W*S_C_r/S_C, 50, fill=CRc, stroke="#FFFFFF", sw=2, rx=4, op=0.85)
    s.rect(bx+W*S_C_r/S_C, 240, W*S_C_c/S_C, 50, fill=CCc, stroke="#FFFFFF", sw=2, rx=4, op=0.85)
    s.text(bx+W*S_C_r/S_C/2, 272, f"{f1(S_C_r)}", 18, "#FFFFFF", "middle", "bold")
    s.text(bx+W*S_C_r/S_C+W*S_C_c/S_C/2, 272, f"{f1(S_C_c)} mm（{S_C_c/S_C*100:.0f}%）", 19, "#FFFFFF", "middle", "bold")
    s.line(bx, 314, bx+W, 314, INK, 1.5)
    s.line(bx, 306, bx, 322, INK, 1.5); s.line(bx+W, 306, bx+W, 322, INK, 1.5)
    s.text(bx+W/2, 350, f"S_c = {f1(S_C_r)} + {f1(S_C_c)} = {f1(S_C)} mm", 24, PCc, "middle", "bold")
    s.text(bx+W/2, 395, "C_r 段在對數軸上較長，卻只貢獻 16%——沉陷量幾乎全由跨過 p_c' 之後決定", 15, MUTED, "middle")
    s.save(F+"fig10_split.svg")

# ───────── F11 一秒驗算：量級數線 ─────────
def fig_check():
    s = SVG(1100, 330)
    x0, x1, vmax, ay = 60, 1040, 180, 170
    X = lambda v: x0 + v/vmax*(x1-x0)
    s.rect(X(S_ALL_CR), ay-12, X(S_ALL_CC)-X(S_ALL_CR), 24, fill=OK, stroke="none", rx=6, op=0.18)
    s.line(x0, ay, x1, ay, "#5B6573", 2.5)
    for v in range(0, 181, 20):
        s.line(X(v), ay-6, X(v), ay+6, "#5B6573", 1.5); s.text(X(v), ay+28, str(v), 13, "#9AA3AE", "middle")
    s.text(x1, ay+52, "S (mm)", 14, MUTED, "end")
    pts = [(S_B, "#6B7280", "基腳 Case B", "down"), (S_ALL_CR, CRc, "全套 C_r", "up"),
           (S_C, PCc, "本例 Case C", "up"), (S_ALL_CC, CCc, "全套 C_c", "up")]
    for v, c, lab, d in pts:
        s.circle(X(v), ay, 10, fill=c)
        if d == "up":
            s.line(X(v), ay-14, X(v), ay-50, c, 1.5)
            s.text(X(v), ay-86, lab, 17, c, "middle", "bold")
            s.text(X(v), ay-60, f"{f1(v)} mm", 19, c, "middle", "bold")
        else:
            s.line(X(v), ay+14, X(v), ay+60, c, 1.5, "4,3")
            s.text(X(v)+8, ay+84, f"{lab}　{f1(v)} mm（p_f' 未達 p_c'）", 16, c, "start", "bold")
    s.text((X(S_ALL_CR)+X(S_ALL_CC))/2, 36, "Case C 必落在綠色區間內；落在外面 → 回頭檢查", 18, OK, "middle", "bold")
    s.save(F+"fig11_check.svg")

for fn in (fig_overview, fig_profile, fig_midpoint, fig_21, fig_depth, fig_elogp, fig_phase, fig_cases, fig_flow, fig_split, fig_check):
    fn()
print("done")
