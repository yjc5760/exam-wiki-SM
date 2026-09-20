"""
gen_figs.py — SM-U1-3 夯實曲線與夯實能量：SVG 向量圖解
所有幾何由 demo.py 的數值決定；改 demo.py 重跑即可。
輸出：figs/*.svg ＋ figs/*.png (2x) ＋ diagram_manifest.json
"""
import sys, json, math, random
sys.path.insert(0, "/mnt/skills/user/struct-diagram/scripts")
from structdraw import Canvas, C, esc
import numpy as np
import demo as D

OUT = "figs"
PFX = "SM-U1-3c"
DRY = "#B45309"      # 乾側（與 C['accent'] 同色系）
WET = "#1D4ED8"      # 濕側（C['deform']）
MOD = "#C0392B"      # 修正 Proctor
OK = "#2E7D6F"       # 最佳（C['bmd']）
T = C["text"]; M = C["muted"]


class Plot:
    """資料座標 → 畫布像素（Canvas 以 sx=1 使用，模型座標＝像素，y 向上）"""
    def __init__(self, cv, x0, y0, w, h, xr, yr):
        self.cv, self.x0, self.y0, self.w, self.h, self.xr, self.yr = cv, x0, y0, w, h, xr, yr

    def P(self, x, y):
        return (self.x0 + (x - self.xr[0]) / (self.xr[1] - self.xr[0]) * self.w,
                self.y0 + (y - self.yr[0]) / (self.yr[1] - self.yr[0]) * self.h)

    def frame(self, xt, yt, xlab="w (%)", ylab="γ_{d} (kN/m^{3})", fs=21):
        cv = self.cv
        for y in yt:
            cv.line(self.P(self.xr[0], y), self.P(self.xr[1], y), C["border"], 1.3)
            cv.text(self.P(self.xr[0], y), f"{y:g}", fs, M, "end", dx=-12)
        for x in xt:
            cv.text(self.P(x, self.yr[0]), f"{x:g}", fs, M, dy=24)
        cv.arrow(self.P(self.xr[0], self.yr[0]), (self.x0 + self.w + 18, self.y0), M, 2, 11)
        cv.arrow(self.P(self.xr[0], self.yr[0]), (self.x0, self.y0 + self.h + 18), M, 2, 11)
        cv.text((self.x0 + self.w, self.y0), xlab, fs, M, "end", dy=58)
        cv.text((self.x0 - 10, self.y0 + self.h + 42), ylab, fs, M, "start")

    def curve(self, f, a, b, color, w=5, dash=None, n=200):
        ws = np.linspace(a, b, n)
        self.cv.poly([self.P(x, float(f(x))) for x in ws], color, w, dash)

    def clip_curve(self, f, a, b, color, w, dash=None):
        """只畫落在 y 範圍內的部分"""
        ws = np.linspace(a, b, 300)
        pts = [self.P(x, float(f(x))) for x in ws if self.yr[0] <= f(x) <= self.yr[1]]
        self.cv.poly(pts, color, w, dash)


def save(cv, name, man, ar_note=""):
    path = f"{OUT}/{PFX}-{name}.svg"
    cv.save(path)
    man[name] = {"svg": path, "png": path.replace(".svg", ".png"), "ar": cv.w / cv.h}
    return path


def bg(cv):
    cv.rect_px(0, 0, cv.w, cv.h, "#FFFFFF", 0)


# ════════════════════════════════════════════════════════════
# fig-1 鐘形曲線：乾側／濕側兩機制交會
# ════════════════════════════════════════════════════════════
def fig_bell(man):
    cv = Canvas(1000, 700); bg(cv)
    pl = Plot(cv, 110, 110, 820, 520, (8, 24), (15, 20))
    f = D.curve(D.STD); wo, gm = D.W_OPT_S, D.GD_MAX_S
    a, _ = pl.P(D.STD[0]["w"], 15); b, _ = pl.P(wo, 15); c, _ = pl.P(D.STD[-1]["w"], 15)
    top = 110 + 520
    cv.parts.append(f'<rect x="{a:.1f}" y="{700-top:.1f}" width="{b-a:.1f}" height="520" fill="{DRY}" opacity="0.08"/>')
    cv.parts.append(f'<rect x="{b:.1f}" y="{700-top:.1f}" width="{c-b:.1f}" height="520" fill="{WET}" opacity="0.08"/>')
    pl.frame([8, 12, 16, 20, 24], [15, 16, 17, 18, 19, 20])
    pl.clip_curve(D.zav_gd, 8, 24, M, 3, "10 8")
    zx, zy = pl.P(21.2, D.zav_gd(21.2))
    cv.text_px(zx + 18, 700 - zy - 20, "ZAVC（S = 100%）", 21, M, "start", "700")
    pl.curve(f, D.STD[0]["w"], D.STD[-1]["w"], WET, 6)
    for r in D.STD:
        cv.dot(pl.P(r["w"], r["gd"]), 7, "#FFFFFF", WET, 3)
    p = pl.P(wo, gm)
    cv.line(pl.P(8, gm), p, WET, 2.2, "8 6"); cv.line(pl.P(wo, 15), p, WET, 2.2, "8 6")
    cv.dot(p, 10, WET, "#FFFFFF", 2.5)
    cv.text(pl.P(8.2, gm), f"γ_{{d,max}} = {gm:.2f}", 22, WET, "start", "700", dy=-22)
    cv.text(pl.P(wo, 15), f"w_{{opt}} = {wo:.1f}%", 22, WET, "start", "700", dx=12, dy=-24)
    cv.text(pl.P(12, 19.6), "乾側：水是潤滑劑", 24, DRY, weight="700")
    cv.text(pl.P(12, 19.2), "加水 → γ_{d} 上升", 20, DRY)
    cv.text(pl.P(19.3, 19.6), "濕側：水是阻擋物", 24, WET, weight="700")
    cv.text(pl.P(19.3, 19.2), "加水 → γ_{d} 下降", 20, WET)
    cv.text_px(500, 38, f"示範案例：標準 Proctor，G_{{s}} = {D.GS}，五點試驗", 22, T, weight="700")
    return save(cv, "fig-1-bell", man)


# ════════════════════════════════════════════════════════════
# fig-2 顆粒尺度三狀態 ＋ 每單位體積三相比例（由示範數據算出）
# ════════════════════════════════════════════════════════════
def phases(row):
    Vs = row["gd"] / (D.GS * D.GW); Vw = (row["w"] / 100) * row["gd"] / D.GW
    return Vs, Vw, 1 - Vs - Vw


def fig_particles(man):
    rows = [D.STD[0], D.STD[2], D.STD[4]]
    titles = [("乾側：摩擦鎖死", DRY, "水膜太薄，顆粒卡住無法重排"),
              ("最佳含水量：排列最密", OK, "水膜剛好潤滑，滑到最緊密位置"),
              ("濕側：水墊效應", WET, "水不可壓縮又排不掉，把顆粒撐開")]
    W, Hr = 1000, 250
    cv = Canvas(W, Hr * 3 + 70); bg(cv)
    cv.text_px(W / 2, 34, "每單位總體積的三相比例（由示範數據算出）", 22, T, weight="700")
    rnd = random.Random(7)
    for k, (row, (tt, col, sub)) in enumerate(zip(rows, titles)):
        y0 = 70 + k * Hr            # 像素（由上）
        cv.rect_px(14, y0 + 8, W - 28, Hr - 16, C["panel"], 14, C["border"], 1.2)
        Vs, Vw, Va = phases(row)
        # 顆粒示意：間距由 Vs 決定（越密越擠）
        bx, by, bw, bh = 40, y0 + 30, 400, Hr - 60
        if k == 2:
            cv.rect_px(bx - 6, by - 6, bw + 12, bh + 12, "#C7D5F5", 10, WET, 2)
        r = 26
        pitch = (66, 57, 74)[k]; jit = (9, 2, 3)[k]
        n = int((bw - 2 * r) // pitch) + 1
        vp = pitch * 0.87
        nrow = int((bh - 2 * r) // vp) + 1
        for row_i in range(nrow):
            for i in range(n):
                cx = bx + r + i * pitch + (pitch / 2 if row_i % 2 else 0) + rnd.uniform(-jit, jit)
                if cx > bx + bw - r: continue
                cy = by + r + row_i * vp + rnd.uniform(-jit, jit)
                if k == 1:
                    cv.parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r+4}" fill="#BFD0F2"/>')
                cv.parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="#7A8699" stroke="#3F4A5A" stroke-width="2.4"/>')
        # 標題
        cv.text_px(470, y0 + 50, tt, 25, col, "start", "700")
        cv.text_px(470, y0 + 86, sub, 19, M, "start")
        cv.text_px(470, y0 + 122, f"w = {row['w']:.0f}%，γ_{{d}} = {row['gd']:.2f}，S = {row['S']*100:.0f}%", 19, T, "start")
        # 三相長條
        x0, yb, Lb, hb = 470, y0 + 158, 500, 44
        segs = [(Vs, "#7A8699", "固"), (Vw, "#4F7BE0", "水"), (Va, "#E8EDF4", "氣")]
        xx = x0
        for v, fc, lab in segs:
            wpx = v * Lb
            cv.parts.append(f'<rect x="{xx:.1f}" y="{yb}" width="{wpx:.1f}" height="{hb}" fill="{fc}" stroke="#3F4A5A" stroke-width="1.2"/>')
            txt = f"{lab} {v:.2f}"
            if wpx > 75:
                cv.text_px(xx + wpx / 2, yb + hb / 2, txt, 18, "#FFFFFF" if lab != "氣" else T, weight="700")
            else:
                cv.text_px(x0 + Lb, yb + hb + 18, txt, 16, T, "end")
            xx += wpx
    return save(cv, "fig-2-particles", man)


# ════════════════════════════════════════════════════════════
# fig-3 三相圖（Vs = 1）：夯實只排氣、不排水 → 推出 ZAVC
# ════════════════════════════════════════════════════════════
def fig_phase(man):
    cv = Canvas(1000, 700); bg(cv)
    wG = D.E_ZAV
    cases = [("夯實前（鬆散）", D.E_LOOSE, D.GD_LOOSE),
             ("夯實後（最佳點）", D.E_COMP, D.GD_MAX_S),
             ("理論極限 Va = 0", D.E_ZAV, D.zav_gd(D.W_PHASE))]
    base, scale, bw = 150, 220, 170      # 像素（y 向上）；1.0 體積 = 250 px
    cv.text_px(500, 38, f"同一含水量 w = {D.W_PHASE:.0f}%，以 V_{{s}} = 1 為基準", 22, T, weight="700")
    for i, (lab, e, gd) in enumerate(cases):
        x = 110 + i * 300
        hs, hw, ha = 1 * scale, wG * scale, (e - wG) * scale
        cv.polygon([(x, base), (x + bw, base), (x + bw, base + hs), (x, base + hs)], "#7A8699", "#3F4A5A", 2)
        cv.polygon([(x, base + hs), (x + bw, base + hs), (x + bw, base + hs + hw), (x, base + hs + hw)], "#4F7BE0", "#3F4A5A", 2)
        if ha > 0.5:
            cv.polygon([(x, base + hs + hw), (x + bw, base + hs + hw), (x + bw, base + hs + hw + ha), (x, base + hs + hw + ha)], "#E8EDF4", "#3F4A5A", 2)
            if ha > 40:
                cv.text((x + bw / 2, base + hs + hw + ha / 2), f"氣 {e - wG:.3f}", 19, T, weight="700")
            else:
                cv.text((x + bw, base + hs + hw + ha / 2), f"← 氣 {e - wG:.3f}", 18, DRY, "start", "700", dx=8)
        cv.text((x + bw / 2, base + hs / 2), "固 1.000", 19, "#FFFFFF", weight="700")
        cv.text((x + bw / 2, base + hs + hw / 2), f"水 wG_{{s}} = {wG:.3f}", 18, "#FFFFFF", weight="700")
        cv.text((x + bw / 2, base - 34), f"e = {e:.3f}", 21, T, weight="700")
        cv.text((x + bw / 2, base - 66), f"γ_{{d}} = {gd:.2f}", 21, WET if i == 2 else T, weight="700")
        cv.text((x + bw / 2, base + hs + hw + max(ha, 0) + (30 if ha > 40 else 36)), lab, 21, DRY if i == 2 else T, weight="700")
        if i < 2:
            cv.arrow((x + bw + 30, base + 200), (x + 270, base + 200), M, 3, 14)
    cv.text_px(500, 668, "水的體積 wG_{s} 三格一樣高：夯實能壓掉的只有空氣", 20, M)
    return save(cv, "fig-3-phase", man)


# ════════════════════════════════════════════════════════════
# fig-4 飽和度等值線族：夯實曲線與 S = 60/80/100%
# ════════════════════════════════════════════════════════════
def fig_slines(man):
    cv = Canvas(1000, 700); bg(cv)
    pl = Plot(cv, 110, 110, 820, 520, (8, 24), (15, 20))
    pl.frame([8, 12, 16, 20, 24], [15, 16, 17, 18, 19, 20])
    for S, lab_w in ((0.6, 9.3), (0.8, 10.2), (1.0, 20.5)):
        fS = lambda w, S=S: D.s_line(w, S)
        pl.clip_curve(fS, 8, 24, M if S == 1 else C["member2"], 3 if S == 1 else 2.2, "10 8" if S == 1 else "4 6")
        x, y = pl.P(lab_w, fS(lab_w))
        cv.text_px(x + 10, 700 - y - 16, f"S = {S*100:.0f}%", 20, M if S == 1 else C["member2"], "start", "700")
    f = D.curve(D.STD)
    pl.curve(f, D.STD[0]["w"], D.STD[-1]["w"], WET, 6)
    for r in D.STD:
        q = pl.P(r["w"], r["gd"]); cv.dot(q, 7, "#FFFFFF", WET, 3)
        cv.text(q, f"{r['S']*100:.0f}%", 19, WET, dy=36, weight="700")
    p = pl.P(D.W_OPT_S, D.GD_MAX_S); cv.dot(p, 10, WET, "#FFFFFF", 2.5)
    cv.text(p, f"峰值 S ≈ {D.S_OPT_S*100:.0f}%", 21, WET, "start", "700", dx=14, dy=-30)
    cv.text_px(500, 38, "夯實曲線一路穿過 S 等值線，但永遠停在 S = 100% 左下方", 22, T, weight="700")
    return save(cv, "fig-4-slines", man)


# ════════════════════════════════════════════════════════════
# fig-5 ZAVC 合理性檢核：忘了除 (1+w) 的點
# ════════════════════════════════════════════════════════════
def fig_check(man):
    cv = Canvas(1000, 700); bg(cv)
    pl = Plot(cv, 110, 110, 820, 520, (8, 24), (15, 21))
    bad_region = [pl.P(x, D.zav_gd(x)) for x in np.linspace(8.9, 24, 60)] + [pl.P(24, 21), pl.P(8.9, 21)]
    cv.polygon(bad_region, MOD, op=0.08)
    pl.frame([8, 12, 16, 20, 24], [15, 16, 17, 18, 19, 20, 21])
    pl.clip_curve(D.zav_gd, 8, 24, M, 3, "10 8")
    pl.curve(D.curve(D.STD), D.STD[0]["w"], D.STD[-1]["w"], WET, 5)
    r = D.BAD_ROW; w = r["w"]
    pb, pg, pz = pl.P(w, D.BAD_GD), pl.P(w, r["gd"]), pl.P(w, D.zav_gd(w))
    cv.line(pl.P(w, 15), pb, M, 1.5, "3 5")
    cv.dot(pb, 11, MOD, "#FFFFFF", 2.5)
    cv.text(pb, f"算得 {D.BAD_GD:.2f}（誤把 γ 當 γ_{{d}}）", 21, MOD, "end", "700", dx=-18)
    cv.dot(pz, 8, "#FFFFFF", M, 3)
    cv.text(pz, f"ZAVC 上限 {D.zav_gd(w):.2f}", 20, M, "start", "700", dx=16, dy=-4)
    cv.arrow((pb[0], pb[1] - 16), (pg[0], pg[1] + 14), OK, 3.4, 15)
    cv.dot(pg, 10, OK, "#FFFFFF", 2.5)
    cv.text(pg, f"÷(1 + w) 後 {r['gd']:.2f} ✓", 21, OK, "end", "700", dx=-18)
    cv.text(pl.P(19.8, 19.5), "不可能區", 26, MOD, "start", "700")
    cv.text(pl.P(19.8, 19.1), "（S > 100%）", 21, MOD, "start", "700")
    cv.text_px(500, 38, f"檢核：同一 w = {w:.0f}% 下，γ_{{d}} 不得超過 ZAVC", 22, T, weight="700")
    return save(cv, "fig-5-check", man)


# ════════════════════════════════════════════════════════════
# fig-6 能量連乘：標準 → 修正，每個因子各放大多少
# ════════════════════════════════════════════════════════════
def fig_energy(man):
    cv = Canvas(1000, 700); bg(cv)
    steps = [("標準 Proctor", 1.0, None),
             ("W：24.5 → 44.5 N", 44.5 / 24.5, "W"),
             ("h：305 → 457 mm", 0.457 / 0.305, "h"),
             ("L：3 → 5 層", 5 / 3, "L")]
    vals, v = [], D.E_STD
    for lab, k, _ in steps:
        v = v * k if _ else v
        vals.append(v)
    assert abs(vals[-1] - D.E_MOD) < 0.5
    x0, xmax, Lb = 330, 3000, 470
    cv.text_px(500, 40, f"E_{{mod}} / E_{{std}} = {D.E_MOD/D.E_STD:.2f}：三個因子連乘", 23, T, weight="700")
    prev = 0
    for i, ((lab, k, sym), val) in enumerate(zip(steps, vals)):
        y = 100 + i * 130                     # 像素由上
        cv.text_px(x0 - 20, y + 30, lab, 21, T, "end", "700")
        if i:
            cv.text_px(x0 - 20, y + 60, f"× {k:.3f}", 20, DRY, "end", "700")
        wprev = prev / xmax * Lb; wv = val / xmax * Lb
        col = WET if i == 0 else (MOD if i == 3 else "#8A94A6")
        cv.parts.append(f'<rect x="{x0}" y="{y}" width="{wv:.1f}" height="64" rx="6" fill="{col}" opacity="{1 if i in (0,3) else 0.55}"/>')
        if i:
            cv.parts.append(f'<rect x="{x0}" y="{y}" width="{wprev:.1f}" height="64" rx="6" fill="none" stroke="#3F4A5A" stroke-width="1.6" stroke-dasharray="6 5"/>')
        cv.text_px(x0 + wv + 14, y + 32, f"{val:.0f} kJ/m^{{3}}", 22, col if i in (0, 3) else T, "start", "700")
        prev = val
    cv.text_px(500, 648, "N = 25 下／層、V = 944 cm^{3} 兩者相同，不影響倍數", 20, M)
    return save(cv, "fig-6-energy", man)


# ════════════════════════════════════════════════════════════
# fig-7 能量增加 → 曲線往左上移（正確版）
# ════════════════════════════════════════════════════════════
def fig_shift(man, name="fig-7-shift", wrong=False, W=1000, H=700):
    cv = Canvas(W, H); bg(cv)
    pl = Plot(cv, 110, 110, W - 180, H - 180, (6, 24), (15, 21))
    pl.frame([8, 12, 16, 20, 24], [15, 16, 17, 18, 19, 20, 21])
    pl.clip_curve(D.zav_gd, 6, 24, M, 3, "10 8")
    fs, fm = D.curve(D.STD), D.curve(D.MOD)
    pl.curve(fs, D.STD[0]["w"], D.STD[-1]["w"], WET, 5)
    if wrong:
        # 原圖的錯誤畫法：修正曲線濕側越過 ZAVC
        wr = lambda w: float(fm(min(w, D.MOD[-1]["w"]))) if w <= 13 else D.GD_MAX_M - 0.03 * (w - 12.5) ** 2
        ws = np.linspace(D.MOD[0]["w"], 20.0, 200)
        pts = [pl.P(x, wr(x)) for x in ws]
        above = [pl.P(x, wr(x)) for x in ws if wr(x) > D.zav_gd(x)]
        cv.poly(pts, MOD, 5)
        if above:
            xs = [x for x in ws if wr(x) > D.zav_gd(x)]
            reg = [pl.P(x, wr(x)) for x in xs] + [pl.P(x, D.zav_gd(x)) for x in xs[::-1]]
            cv.polygon(reg, MOD, op=0.35)
            q = pl.P(xs[len(xs) // 2], wr(xs[len(xs) // 2]))
            cv.text_px(q[0] + 30, H - q[1] - 44, "穿越 ZAVC", 22, MOD, "start", "700")
            cv.text_px(q[0] + 30, H - q[1] - 16, "S > 100%，不可能", 19, MOD, "start")
        cv.dot(pl.P(D.W_OPT_M, D.GD_MAX_M), 9, MOD, "#FFFFFF", 2.5)
    else:
        pl.curve(fm, D.MOD[0]["w"], D.MOD[-1]["w"], MOD, 5)
        for rows, col in ((D.STD, WET), (D.MOD, MOD)):
            for r in rows:
                cv.dot(pl.P(r["w"], r["gd"]), 6, "#FFFFFF", col, 2.6)
        # 最佳點連線：約沿 S ≈ 85% 等值線
        Sbar = (D.S_OPT_S + D.S_OPT_M) / 2
        pl.clip_curve(lambda w: D.s_line(w, Sbar), 9.5, 18.5, OK, 2.4, "3 6")
        lw = 18.3; lp = pl.P(lw, D.s_line(lw, Sbar))
        cv.text_px(lp[0] + 8, H - lp[1] + 24, f"最佳點連線 ≈ S {Sbar*100:.0f}%", 19, OK, "start", "700")
        ps, pm = pl.P(D.W_OPT_S, D.GD_MAX_S), pl.P(D.W_OPT_M, D.GD_MAX_M)
        cv.arrow((ps[0] - 6, ps[1] + 10), (pm[0] + 8, pm[1] - 14), DRY, 3.6, 16)
        cv.dot(ps, 10, WET, "#FFFFFF", 2.5); cv.dot(pm, 10, MOD, "#FFFFFF", 2.5)
        for k, (lab, col, wo, gm) in enumerate((("修正", MOD, D.W_OPT_M, D.GD_MAX_M), ("標準", WET, D.W_OPT_S, D.GD_MAX_S))):
            lx, ly = pl.P(16.2, 15.95 - 0.42 * k)
            cv.dot((lx, ly), 8, col, "#FFFFFF", 2)
            cv.text((lx, ly), f"{lab}：w_{{opt}} = {wo:.1f}%，γ_{{d,max}} = {gm:.2f}", 19, col, "start", "700", dx=16)
        cv.text(pl.P(6.3, 16.5), f"E ↑ {D.E_MOD/D.E_STD:.1f} 倍", 22, DRY, "start", "700")
        cv.text(pl.P(6.3, 16.05), "γ_{d,max} ↑、w_{opt} ↓", 20, DRY, "start", "700")
        zx = pl.P(21.8, D.zav_gd(21.8))
        cv.text_px(zx[0] + 8, H - zx[1] - 22, "ZAVC", 20, M, "start", "700")
    return cv


def fig7(man):
    cv = fig_shift(man)
    cv.text_px(500, 38, "標準 vs 修正 Proctor：兩條曲線都停在 ZAVC 左下方", 22, T, weight="700")
    return save(cv, "fig-7-shift", man)


def fig8(man):
    """錯誤示範 vs 修正：把原圖的錯畫出來，旁邊放正確版"""
    L = fig_shift(man, wrong=True, W=820, H=640)
    R = fig_shift(man, wrong=False, W=820, H=640)
    L.text_px(410, 36, "錯誤：原圖的修正曲線濕側穿越 ZAVC", 23, MOD, weight="700")
    R.text_px(410, 36, "正確：濕側沿 S ≈ 92% 平行下降", 23, OK, weight="700")
    W, H = 1640, 640
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
           '<defs><clipPath id="cL"><rect width="820" height="640"/></clipPath><clipPath id="cR"><rect width="820" height="640"/></clipPath></defs>',
           f'<g clip-path="url(#cL)">{"".join(L.parts)}</g>',
           f'<g transform="translate(820,0)" clip-path="url(#cR)">{"".join(R.parts)}</g>',
           f'<line x1="820" y1="20" x2="820" y2="620" stroke="{C["border"]}" stroke-width="2"/>', '</svg>']
    path = f"{OUT}/{PFX}-fig-8-wrong-vs-right.svg"
    open(path, "w", encoding="utf-8").write("".join(svg))
    man["fig-8-wrong-vs-right"] = {"svg": path, "png": path.replace(".svg", ".png"), "ar": W / H}


# ════════════════════════════════════════════════════════════
# fig-9 乾側 vs 濕側夯實的黏土組構（凝聚 vs 分散）
# ════════════════════════════════════════════════════════════
def fig_fabric(man):
    cv = Canvas(1000, 620); bg(cv)
    rnd = random.Random(3)
    for k, (tt, col, sub) in enumerate([("乾側夯實：凝聚（絮狀）結構", DRY, "板片隨機邊對面接觸"),
                                        ("濕側夯實：分散（平行）結構", WET, "板片被剪動排成平行")]):
        x0 = 30 + k * 490
        cv.rect_px(x0, 70, 450, 520, C["panel"], 14, C["border"], 1.2)
        cv.text_px(x0 + 225, 105, tt, 23, col, weight="700")
        cv.text_px(x0 + 225, 138, sub, 19, M)
        for i in range(5):
            for j in range(4):
                cx, cy = x0 + 70 + i * 78, 190 + j * 95
                ang = rnd.uniform(0, 180) if k == 0 else rnd.uniform(-8, 8)
                L = 62
                dx, dy = L / 2 * math.cos(math.radians(ang)), L / 2 * math.sin(math.radians(ang))
                cv.parts.append(f'<line x1="{cx-dx:.1f}" y1="{cy-dy:.1f}" x2="{cx+dx:.1f}" y2="{cy+dy:.1f}" stroke="#3F4A5A" stroke-width="7" stroke-linecap="round"/>')
    cv.text_px(500, 36, "同一 γ_{d}，夯實含水量不同，土的組構與工程性質不同", 22, T, weight="700")
    return save(cv, "fig-9-fabric", man)


if __name__ == "__main__":
    import os
    os.makedirs(OUT, exist_ok=True)
    for rows in (D.STD, D.MOD):
        D.check_below_zav(rows)
    man = {}
    for fn in (fig_bell, fig_particles, fig_phase, fig_slines, fig_check, fig_energy, fig7, fig8, fig_fabric):
        fn(man)
    json.dump(man, open("figs_manifest_raw.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("OK", len(man))
