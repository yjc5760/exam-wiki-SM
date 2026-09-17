#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SM-U1-3「土壤夯實與壓密」觀念講義 — SVG 向量圖解產生器

鐵則：圖上每個數字都由本檔頂端的常數與算式推出，不得憑印象填。
改一個輸入（Gs、e0、Cc、Cr、cv、Hdr…），圖形自動跟著變。

繪圖鐵則（沿用 SS-U2-3 踩過的坑）：
  * math_px/math 走襯線數學字型，**沒有 CJK 字面** → 含中文的字串一律用 text_px。
  * polygon/line/poly/circle 吃「模型座標」；像素版畫布請用 PX() 轉換 y。
  * 數學襯線字型缺 Unicode 上下標與根號排版 → 用 ^{} / _{} 語法，根號寫成數值。
  * compose() 的 title/sub/note 走 esc()，不解析 _{}，一律純文字；'<' 用全形＜。
"""
import sys, os, math, glob
SD = glob.glob("/root/.claude/skills/synced/*/struct-diagram")[0]
sys.path.insert(0, os.path.join(SD, "scripts"))
from structdraw import Canvas, C, compose

OUT = "figs"
os.makedirs(OUT, exist_ok=True)
LOG = math.log10

# ═══════════════════════════════════════════════════════════════
# 輸入常數（所有圖上的數字皆由此推算）
# ═══════════════════════════════════════════════════════════════
GS   = 2.70            # 土粒比重
GW   = 9.81            # kN/m3 水單位重

# --- 夯實試驗（標準 vs 修正 Proctor）---
MOLD_V = 944e-6        # m3  標準夯模體積
PROCTOR = {
    "std": dict(name="標準 Proctor", W=2.5*9.81, h=0.305, N=25, L=3,
                gdmax=17.50, wopt=0.160, col=C["compr"]),
    "mod": dict(name="修正 Proctor", W=4.54*9.81, h=0.457, N=25, L=5,
                gdmax=19.00, wopt=0.125, col=C["load"]),
}
def energy(p):                       # kJ/m3
    return p["W"]*p["h"]*p["N"]*p["L"]/MOLD_V/1000.0
for p in PROCTOR.values():
    p["E"] = energy(p)
E_RATIO = PROCTOR["mod"]["E"]/PROCTOR["std"]["E"]

def gzav(w):                         # 零空氣孔隙線 kN/m3
    return GS*GW/(1.0 + w*GS)

def gd_of_e(e):                      # 乾單位重 ← 孔隙比
    return GS*GW/(1.0 + e)

def e_of_gd(gd):
    return GS*GW/gd - 1.0

# --- 夯實品管示範（砂）---
E_MAX, E_MIN = 0.85, 0.42
GD_FIELD_SAND = 16.40
E_FIELD  = e_of_gd(GD_FIELD_SAND)
DR_FIELD = (E_MAX - E_FIELD)/(E_MAX - E_MIN)
GD_SAND_MAX = gd_of_e(E_MIN)                 # Dr = 100% 對應
GD_SAND_MIN = gd_of_e(E_MAX)                 # Dr = 0   對應
RC_FIELD  = GD_FIELD_SAND/GD_SAND_MAX
RC_AT_DR0 = GD_SAND_MIN/GD_SAND_MAX          # RC 刻度的「零點」

# --- 土方平衡示範 ---
V_FILL   = 10000.0                           # m3 完成填方體積
GD_FILL  = 0.95*PROCTOR["std"]["gdmax"]      # RC = 95%
W_TARGET = 0.160
E_BORROW = 0.78
GD_BORROW = gd_of_e(E_BORROW)
W_BORROW = 0.090
WS_TOTAL = GD_FILL*V_FILL                    # kN 乾土重（唯一守恆量）
V_BORROW = WS_TOTAL/GD_BORROW
SHRINK   = V_BORROW/V_FILL
W_ADD_KN = WS_TOTAL*(W_TARGET - W_BORROW)
W_ADD_M3 = W_ADD_KN/GW

# --- 壓密示範剖面 ---
#   GL 0~2 m 砂(濕) / 2~6 m 砂(飽和) / 6~10 m 黏土 / 10 m 以下 岩盤(不透水)
GWT = 2.0
LAYERS = [(0.0, 2.0, 18.00, "砂（地下水位以上）"),
          (2.0, 6.0, 19.50, "砂（飽和，透水）"),
          (6.0, 10.0, 17.50, "正常/過壓密黏土")]
CLAY_TOP, CLAY_BOT = 6.0, 10.0
H_CLAY = CLAY_BOT - CLAY_TOP
Z_MID  = (CLAY_TOP + CLAY_BOT)/2.0

def sigma_total(z):
    s = 0.0
    for z0, z1, g, _ in LAYERS:
        if z <= z0: break
        s += g*(min(z, z1) - z0)
    return s
def u_w(z):       return max(0.0, (z - GWT))*GW
def sigma_eff(z): return sigma_total(z) - u_w(z)

P0 = sigma_eff(Z_MID)
PC = 130.0
OCR = PC/P0
E0, CC, CR = 1.05, 0.320, 0.045
CC_OVER_CR = CC/CR
DSIG = 80.0                                  # 大面積填土 kPa
PF = P0 + DSIG

def sc_case_c(p0, pc, pf, H=H_CLAY, e0=E0, Cc=CC, Cr=CR):
    return (Cr*H/(1+e0))*LOG(pc/p0) + (Cc*H/(1+e0))*LOG(pf/pc)
def sc_all(coef, p0, pf, H=H_CLAY, e0=E0):
    return (coef*H/(1+e0))*LOG(pf/p0)

SC   = sc_case_c(P0, PC, PF)*1000.0          # mm
SC_CC = sc_all(CC, P0, PF)*1000.0
SC_CR = sc_all(CR, P0, PF)*1000.0

# --- 2:1 應力傳佈示範 ---
Q_FTG, B_FTG, L_FTG, DF = 1200.0, 2.0, 3.0, 1.5
def d_sigma_21(z):  return Q_FTG/((B_FTG + z)*(L_FTG + z))
Z_BELOW = Z_MID - DF
DSIG_21 = d_sigma_21(Z_BELOW)

# --- 壓密速率 ---
CV = 3.154                                   # m2/yr （= 1.0e-7 m2/s）
def Tv_of_U(U):
    return math.pi/4.0*U**2 if U < 0.60 else 1.781 - 0.933*LOG(100.0*(1.0-U))
def t_of_U(U, Hdr):  return Tv_of_U(U)*Hdr**2/CV
HDR_DOUBLE = H_CLAY/2.0
HDR_SINGLE = H_CLAY
T90_DOUBLE = t_of_U(0.90, HDR_DOUBLE)
T90_SINGLE = t_of_U(0.90, HDR_SINGLE)
T_RATIO = T90_SINGLE/T90_DOUBLE
TV60_A, TV60_B = math.pi/4.0*0.36, 1.781 - 0.933*LOG(40.0)

# --- 超載預壓 ---
DSIG_PRE = 125.0
SCF = sc_case_c(P0, PC, P0 + DSIG_PRE)*1000.0
U_REQ = SC/SCF
T_PRE = t_of_U(U_REQ, HDR_SINGLE)
T_SAVE = 1.0 - T_PRE/T90_SINGLE


# ═══════════════════════════════════════════════════════════════
# 版面工具
# ═══════════════════════════════════════════════════════════════
def pcv(w, h, xr, yr, pad):
    L, R, T, B = pad
    sx = min((w-L-R)/(xr[1]-xr[0]), (h-T-B)/(yr[1]-yr[0]))
    ox = L + (w-L-R-(xr[1]-xr[0])*sx)/2 - xr[0]*sx
    oy = B + (h-T-B-(yr[1]-yr[0])*sx)/2 - yr[0]*sx
    return Canvas(w, h, sx=sx, ox=ox, oy=oy)

def pxcv(w, h):
    return Canvas(w, h, sx=1, ox=0, oy=0)

def PX(cv, x, y):
    return (x, cv.h - y)

def plotbox(w, h, xr, yr, box):
    cv = Canvas(w, h, sx=1, ox=0, oy=0)
    x0, x1, y0, y1 = box
    fx = lambda v: x0 + (v-xr[0])/(xr[1]-xr[0])*(x1-x0)
    fy = lambda v: y0 + (v-yr[0])/(yr[1]-yr[0])*(y1-y0)
    return cv, fx, fy, (lambda a, b: (fx(a), fy(b)))

def axis_frame(cv, x0, x1, y0, y1, xlab, ylab, xlab_dy=4, ylab_dy=-30):
    cv.arrow((x0, y0), (x1+16, y0), C["muted"], 1.8, 9)
    cv.arrow((x0, y0), (x0, y1+16), C["muted"], 1.8, 9)
    cv.text_px(x1+24, cv.h-y0+xlab_dy, xlab, 13, C["muted"], "start")
    cv.text_px(x0, cv.h-y1+ylab_dy, ylab, 13, C["muted"])

def vdown(cv, x, y0, y1, col, w=2.4):
    cv.parts.append(f'<line x1="{x:.1f}" y1="{y0:.1f}" x2="{x:.1f}" y2="{y1-9:.1f}" '
                    f'stroke="{col}" stroke-width="{w}"/>')
    cv.parts.append(f'<polygon points="{x:.1f},{y1:.1f} {x-5.2:.1f},{y1-10:.1f} '
                    f'{x+5.2:.1f},{y1-10:.1f}" fill="{col}"/>')

def vup(cv, x, y0, y1, col, w=2.4):
    cv.parts.append(f'<line x1="{x:.1f}" y1="{y0:.1f}" x2="{x:.1f}" y2="{y1+9:.1f}" '
                    f'stroke="{col}" stroke-width="{w}"/>')
    cv.parts.append(f'<polygon points="{x:.1f},{y1:.1f} {x-5.2:.1f},{y1+10:.1f} '
                    f'{x+5.2:.1f},{y1+10:.1f}" fill="{col}"/>')

def harrow(cv, x0, x1, y, col, w=2.4):
    d = 1 if x1 > x0 else -1
    cv.parts.append(f'<line x1="{x0:.1f}" y1="{y:.1f}" x2="{x1-9*d:.1f}" y2="{y:.1f}" '
                    f'stroke="{col}" stroke-width="{w}"/>')
    cv.parts.append(f'<polygon points="{x1:.1f},{y:.1f} {x1-10*d:.1f},{y-5.2:.1f} '
                    f'{x1-10*d:.1f},{y+5.2:.1f}" fill="{col}"/>')

def bullet(cv, x, y, s, col, size=13.5, gap=20):
    cv.rect_px(x, y-10, 9, 20, col, 3)
    cv.text_px(x+gap, y, s, size, C["text"], "start")

def hline_px(cv, x0, x1, y, col, w=1.8, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    cv.parts.append(f'<line x1="{x0:.1f}" y1="{y:.1f}" x2="{x1:.1f}" y2="{y:.1f}" '
                    f'stroke="{col}" stroke-width="{w}"{d}/>')

def vline_px(cv, x, y0, y1, col, w=1.8, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    cv.parts.append(f'<line x1="{x:.1f}" y1="{y0:.1f}" x2="{x:.1f}" y2="{y1:.1f}" '
                    f'stroke="{col}" stroke-width="{w}"{d}/>')

def phase_bar(cv, x, ytop, wbar, h_air, h_wat, h_sol, lab=True, size=11.5):
    """三相體積柱：由上而下 空氣／水／固體。回傳各段像素高度起點。"""
    y = ytop
    segs = [(h_air, "rgba(138,148,166,0.28)", C["muted"], "空氣 V_{a}"),
            (h_wat, "rgba(29,78,216,0.22)",  C["compr"], "水 V_{w}"),
            (h_sol, "rgba(63,74,90,0.42)",   C["member"], "固體 V_{s}")]
    for hh, fill, col, name in segs:
        if hh <= 0.5:
            continue
        cv.rect_px(x, y, wbar, hh, fill, 0, col, 1.5)
        if lab and hh >= 22:
            cv.text_px(x + wbar/2, y + hh/2, name, size, col, weight="700")
        y += hh
    return ytop


PW, PH = 520, 600            # 兩聯圖每格
W3, H3 = 347, 476            # 三聯圖每格


# ═══════════════════════════════════════════════════════════════
# 圖 1　總開關：夯實趕空氣 ←→ 壓密擠水
# ═══════════════════════════════════════════════════════════════
def fig1():
    a = pxcv(W3, H3)
    a.panel("夯實 Compaction", "非飽和土：把「空氣」趕出去")
    # 夯錘
    a.rect_px(W3/2-30, 78, 60, 26, "rgba(192,57,43,0.25)", 4, C["load"], 2.0)
    a.text_px(W3/2, 91, "夯錘 W", 11.5, C["load"], weight="700")
    vdown(a, W3/2, 108, 140, C["load"], 3.0)
    a.text_px(W3/2+16, 124, "落距 h", 11, C["load"], "start")
    # 夯實前後三相柱
    phase_bar(a, 46, 150, 84, 40, 28, 78)
    phase_bar(a, W3-130, 174, 84, 16, 28, 78)
    a.text_px(46+42, 308, "夯實前", 12.5, C["muted"], weight="700")
    a.text_px(W3-130+42, 308, "夯實後", 12.5, C["text"], weight="700")
    harrow(a, 46+84+10, W3-130-10, 214, C["load"], 2.6)
    a.text_px(W3/2, 198, "空氣被擠出", 12, C["load"], weight="700")
    # 逸出的空氣泡
    for k, (dx, dy, r) in enumerate([(-8, -22, 4.5), (6, -34, 3.4), (16, -18, 2.8)]):
        a.parts.append(f'<circle cx="{W3/2+dx}" cy="{168+dy}" r="{r}" fill="none" '
                       f'stroke="{C["muted"]}" stroke-width="1.6"/>')
    for i, s in enumerate(["瞬間完成（幾秒～數分鐘）", "本質是「能量」問題",
                           "出力就有：E 越大 γ_{d} 越高", "含水量 w 不變（只趕空氣）"]):
        bullet(a, 30, 334 + i*28, s, C["load"], 12.5)
    a.text_px(W3/2, H3-26, "變數：w、E ⇒ 求 γ_{d}", 13.5, C["load"], weight="700")

    b = pxcv(W3, H3)
    b.panel("壓密 Consolidation", "飽和土：把「水」擠出去")
    # Terzaghi 彈簧—活塞模型
    cyl_x, cyl_y, cyl_w, cyl_h = 92, 132, 164, 150
    b.rect_px(cyl_x, cyl_y, cyl_w, cyl_h, "rgba(29,78,216,0.16)", 4, C["member"], 2.0)
    vdown(b, W3/2, 82, 118, C["load"], 3.0)
    b.text_px(W3/2, 72, "載重 Δσ", 12, C["load"], weight="700")
    b.rect_px(cyl_x, cyl_y-10, cyl_w, 14, "rgba(63,74,90,0.42)", 2, C["member"], 1.8)
    # 排水孔
    for dx in (-34, 0, 34):
        vup(b, W3/2+dx, cyl_y-14, cyl_y-40, C["compr"], 2.2)
    b.text_px(W3/2+62, cyl_y-34, "水緩慢滲出", 11.5, C["compr"], "start", weight="700")
    # 彈簧（土骨架）
    n, x0, x1 = 9, cyl_x+22, cyl_x+cyl_w-22
    pts = []
    for i in range(n*2+1):
        xx = x0 + (x1-x0)*i/(n*2)
        yy = cyl_y+38 + (0 if i % 2 == 0 else 46)
        pts.append(PX(b, xx, yy))
    b.poly(pts, C["member"], 2.6)
    b.text_px(W3/2, cyl_y+104, "彈簧 = 土骨架（有效應力）", 11.5, C["member"], weight="700")
    b.text_px(W3/2, cyl_y+126, "缸內水 = 孔隙水壓 u", 11.5, C["compr"], weight="700")
    for i, s in enumerate(["需數月至數十年（等不起）", "本質是「滲流」問題",
                           "出力沒用：只能等 u 消散", "孔隙比 e 下降 ⇒ 沉陷"]):
        bullet(b, 30, 334 + i*28, s, C["compr"], 12.5)
    b.text_px(W3/2, H3-26, "變數：Δσ、c_{v}、H_{dr} ⇒ 求 S 與 t", 13.5, C["compr"], weight="700")

    c = pxcv(W3, H3)
    c.panel("兩者的唯一分界", "考卷第一眼就要分邊")
    rows = [("排掉的是什麼", "空氣", "水"),
            ("土的飽和度", "非飽和 S＜100%", "飽和 S = 100%"),
            ("完成時間", "幾秒鐘", "數月～數十年"),
            ("物理本質", "能量問題", "滲流問題"),
            ("控制變數", "w 與夯實能量 E", "c_{v} 與排水路徑 H_{dr}"),
            ("典型土層", "填方、路基", "軟弱黏土層")]
    c.rect_px(24, 88, (W3-48)*0.47, 34, C["fill_t"], 7, C["load"], 1.6)
    c.text_px(24+(W3-48)*0.235, 105, "夯實", 13.5, C["load"], weight="700")
    c.rect_px(24+(W3-48)*0.53, 88, (W3-48)*0.47, 34, C["fill_c"], 7, C["compr"], 1.6)
    c.text_px(24+(W3-48)*0.765, 105, "壓密", 13.5, C["compr"], weight="700")
    for i, (k, v1, v2) in enumerate(rows):
        y = 138 + i*50
        c.text_px(W3/2, y, k, 11.5, C["muted"])
        c.rect_px(24, y+10, (W3-48)*0.47, 28, C["fill_t"], 5, C["load"], 1.2)
        c.text_px(24+(W3-48)*0.235, y+24, v1, 12, C["text"], weight="700")
        c.rect_px(24+(W3-48)*0.53, y+10, (W3-48)*0.47, 28, C["fill_c"], 5, C["compr"], 1.2)
        c.text_px(24+(W3-48)*0.765, y+24, v2, 12, C["text"], weight="700")
    c.text_px(W3/2, H3-22, "分錯邊 ⇒ 整題公式全錯", 13.5, C["accent"], weight="700")

    compose([a, b, c],
            title="本單元的總開關：夯實趕「空氣」，壓密擠「水」",
            sub="一個是能量問題（出力就有），一個是滲流問題（只能等）",
            note="看到「填方、路基、夯實度、含水量」走夯實；看到「黏土層、沉陷量、多久沉完、"
                 "預壓」走壓密。這一刀切錯，後面所有公式都不會對。",
            path=f"{OUT}/sm13-fig-1-master-switch.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 2　萬用鑰匙：Vs 永遠不變 ⇒ ΔH/H0 = Δe/(1+e0)
# ═══════════════════════════════════════════════════════════════
def fig2():
    a = pxcv(PW, PH)
    a.panel("所有沉陷公式的起點", "固體顆粒體積 V_{s} 永遠不變")
    SC_ = 118.0                      # 每 1 單位孔隙比 = 幾像素
    e_a, e_b = 1.05, 0.72
    ytop, x0, x1, wbar = 120, 96, PW-180, 120
    h_s = SC_*1.0
    hA, hB = SC_*e_a, SC_*e_b
    # 左：初始
    a.rect_px(x0, ytop, wbar, hA, "rgba(29,78,216,0.22)", 0, C["compr"], 1.8)
    a.rect_px(x0, ytop+hA, wbar, h_s, "rgba(63,74,90,0.42)", 0, C["member"], 1.8)
    a.text_px(x0+wbar/2, ytop+hA/2, "V_{v} = e_{0}", 13.5, C["compr"], weight="700")
    a.text_px(x0+wbar/2, ytop+hA+h_s/2, "V_{s} = 1", 13.5, "#FFFFFF", weight="700")
    a.text_px(x0+wbar/2, ytop-18, "初始 H_{0}", 13, C["muted"], weight="700")
    # 右：受壓後（底部對齊）
    ytop_b = ytop + (hA - hB)
    a.rect_px(x1, ytop_b, wbar, hB, "rgba(29,78,216,0.22)", 0, C["compr"], 1.8)
    a.rect_px(x1, ytop_b+hB, wbar, h_s, "rgba(63,74,90,0.42)", 0, C["member"], 1.8)
    a.text_px(x1+wbar/2, ytop_b+hB/2, "V_{v} = e", 13.5, C["compr"], weight="700")
    a.text_px(x1+wbar/2, ytop_b+hB+h_s/2, "V_{s} = 1", 13.5, "#FFFFFF", weight="700")
    a.text_px(x1+wbar/2, ytop-18, "受壓後 H", 13, C["text"], weight="700")
    # ΔH 標示
    hline_px(a, x0, x1+wbar+28, ytop, C["dim"], 1.3, "5 4")
    hline_px(a, x1, x1+wbar+28, ytop_b, C["dim"], 1.3, "5 4")
    vline_px(a, x1+wbar+16, ytop, ytop_b, C["load"], 2.4)
    for yy in (ytop, ytop_b):
        hline_px(a, x1+wbar+8, x1+wbar+24, yy, C["load"], 2.0)
    a.text_px(x1+wbar+16, ytop-18, "ΔH = Δe", 12.5, C["load"], weight="700")
    # 固體層等高強調
    hline_px(a, x0-26, x1+wbar+12, ytop+hA, C["member"], 1.3, "4 4")
    a.text_px(x0-30, ytop+hA+h_s/2, "V_{s} 不變", 12, C["member"], "end", weight="700")
    ybase = ytop + hA + h_s
    hline_px(a, x0-26, x1+wbar+12, ybase, C["member"], 1.6)
    # 推導鏈
    yy = ybase + 44
    a.rect_px(52, yy, PW-104, 132, C["fill_m"], 10, C["bmd"], 1.8)
    a.text_px(PW/2, yy+26, "體積變化 100% 來自孔隙變化", 13.5, C["bmd"], weight="700")
    a.math_px(PW/2, yy+62, "ΔV = ΔV_{v}  ,  V_{0} = V_{s} + V_{v0} = 1 + e_{0}", 15.5, C["text"], weight="700")
    a.math_px(PW/2, yy+102, "ε_{v} = ΔH / H_{0} = Δe / (1 + e_{0})", 19, C["bmd"], weight="700")
    a.text_px(PW/2, PH-30, "分母永遠是「初始狀態」的 1 + e_{0}", 13.5, C["accent"], weight="700")

    b = pxcv(PW, PH)
    b.panel("由這把鑰匙長出來的三個關係式", "夯實與壓密共用同一套三相關係")
    items = [
        ("孔隙比 ⇄ 乾單位重", "γ_{d} = G_{s}γ_{w} / (1 + e)",
         "RC 與 D_{r} 的唯一橋樑；百分比不可直接對接", C["load"]),
        ("含水量 ⇄ 飽和度", "S e = w G_{s}",
         "S = 1 代入即得零空氣孔隙線 ZAVC", C["compr"]),
        ("孔隙比 ⇄ 沉陷量", "S_{c} = H · Δe / (1 + e_{0})",
         "把 e-log p' 曲線讀到的 Δe 換成厚度", C["bmd"]),
    ]
    for i, (t1, m, t2, col) in enumerate(items):
        y = 108 + i*118
        b.rect_px(40, y, PW-80, 100, C["panel"], 10, C["border"], 1.4)
        b.rect_px(40, y, 8, 100, col, 3)
        b.text_px(66, y+22, t1, 13, col, "start", weight="700")
        b.math_px(PW/2+14, y+54, m, 17.5, C["text"], weight="700")
        b.text_px(66, y+82, t2, 11.5, C["muted"], "start")
    y = 108 + 3*118 + 10
    b.rect_px(40, y, PW-80, 86, C["fill_t"], 10, C["load"], 1.8)
    b.text_px(PW/2, y+26, "考場最常見的自殺式錯誤", 13, C["load"], weight="700")
    b.text_px(PW/2, y+52, "分母寫成 1 + e（受壓後）而不是 1 + e_{0}", 13, C["text"], weight="700")
    b.text_px(PW/2, y+74, "應變的定義是「相對於初始體積」，分母只能是初始值", 11.5, C["muted"])
    b.text_px(PW/2, PH-30, "三式互推，題目給哪個就從哪個切入", 13, C["muted"], weight="700")

    compose([a, b],
            title="萬用鑰匙：固體顆粒體積永遠不變",
            sub="所有厚度與體積的變化，100% 來自孔隙的變化",
            note="把土切成「固體 1 份 ＋ 孔隙 e 份」之後，夯實與壓密就共用同一組關係式。"
                 "沉陷公式的分母一律是 1 + e0，因為分子是相對於初始體積的變化量。",
            path=f"{OUT}/sm13-fig-2-master-key.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 3　夯實曲線與零空氣孔隙線
# ═══════════════════════════════════════════════════════════════
def _comp_curve(p, w):
    """以峰值為頂的拋物線型夯實曲線（乾側較緩、濕側較陡）。"""
    k = 200.0 if w < p["wopt"] else 330.0
    return p["gdmax"] - k*(w - p["wopt"])**2

def fig3():
    xr, yr = (0.06, 0.26), (14.6, 20.4)
    a, fx, fy, P = plotbox(PW, PH, xr, yr, (96, PW-56, 150, 500))
    a.panel("夯實曲線：為什麼是一個「鐘形」", "同一夯實能量下，w 與 γ_{d} 的關係")
    axis_frame(a, fx(xr[0]), fx(xr[1]), fy(yr[0]), fy(yr[1]),
               "", "γ_{d}  (kN/m^{3})", ylab_dy=-26)
    a.text_px(fx(xr[1]), PH-fy(yr[0])+38, "w (%)", 12.5, C["muted"], "end")
    for wv in (8, 12, 16, 20, 24):
        a.text_px(fx(wv/100.0), PH-fy(yr[0])+18, f"{wv}", 12, C["muted"])
    for gv in (15, 16, 17, 18, 19, 20):
        a.text_px(fx(xr[0])-10, PH-fy(gv), f"{gv}", 12, C["muted"], "end")
        hline_px(a, fx(xr[0]), fx(xr[1]), PH-fy(gv), C["border"], 1.0)
    # ZAVC
    zs = [(w/1000.0, gzav(w/1000.0)) for w in range(60, 261, 4)]
    a.poly([P(w, g) for w, g in zs if yr[0] <= g <= yr[1]], C["muted"], 2.4, dash="8 5")
    a.text_px(fx(0.212), PH-fy(gzav(0.212))-14, "零空氣孔隙線 ZAVC",
              12.5, C["muted"], "start", weight="700")
    a.text_px(fx(0.212), PH-fy(gzav(0.212))+6, "（S = 100%）", 11.5, C["muted"], "start")
    # 標準 Proctor 曲線
    p = PROCTOR["std"]
    ws = [i/1000.0 for i in range(85, 236)]
    a.poly([P(w, _comp_curve(p, w)) for w in ws], p["col"], 3.8)
    a.dot(P(p["wopt"], p["gdmax"]), 6.4, fill=p["col"], stroke="#FFFFFF", w=2.2)
    vline_px(a, fx(p["wopt"]), PH-fy(p["gdmax"]), PH-fy(yr[0]), p["col"], 1.8, "6 5")
    hline_px(a, fx(xr[0]), fx(p["wopt"]), PH-fy(p["gdmax"]), p["col"], 1.8, "6 5")
    a.text_px(fx(p["wopt"])+8, PH-fy(yr[0])-16,
              f"w_{{opt}} = {p['wopt']*100:.1f}%", 12.5, p["col"], "start", weight="700")
    a.text_px(fx(xr[0])+8, PH-fy(p["gdmax"])-16,
              f"γ_{{d,max}} = {p['gdmax']:.1f}", 12.5, p["col"], "start", weight="700")
    # 乾側／濕側著色
    a.rect_px(fx(0.085), PH-fy(yr[1])+2, fx(p["wopt"])-fx(0.085),
              fy(yr[1])-fy(yr[0])-4, "rgba(180,83,9,0.07)", 0)
    a.rect_px(fx(p["wopt"]), PH-fy(yr[1])+2, fx(0.235)-fx(p["wopt"]),
              fy(yr[1])-fy(yr[0])-4, "rgba(29,78,216,0.07)", 0)
    a.text_px((fx(0.085)+fx(p["wopt"]))/2, PH-fy(yr[1])+24, "乾側（水太少）",
              13, C["accent"], weight="700")
    a.text_px((fx(0.235)+fx(p["wopt"]))/2, PH-fy(yr[1])+24, "濕側（水太多）",
              13, C["compr"], weight="700")
    a.text_px((fx(0.085)+fx(p["wopt"]))/2, PH-fy(yr[1])+44, "水是潤滑劑 → γ_{d} 上升",
              11.5, C["muted"])
    a.text_px((fx(0.235)+fx(p["wopt"]))/2, PH-fy(yr[1])+44, "水是阻擋物 → γ_{d} 下降",
              11.5, C["muted"])
    a.text_px(PW/2, PH-58, "ZAVC 是純幾何上限，夯實曲線永遠碰不到", 13, C["muted"], weight="700")
    a.text_px(PW/2, PH-32, "算出來的點若落在 ZAVC 右上方 ⇒ 一定算錯", 13.5, C["load"], weight="700")

    b = pxcv(PW, PH)
    b.panel("顆粒尺度發生什麼事", "同樣加水，兩側的角色完全相反")
    def grains(y0, kind, col, cap1, cap2):
        b.rect_px(46, y0, PW-92, 112, C["panel"], 9, C["border"], 1.4)
        r = 14
        if kind == "dry":
            pos = [(96+i*46, y0+40+(6 if i % 2 else -6)) for i in range(8)]
        elif kind == "opt":
            pos = [(92+i*36, y0+40) for i in range(10)]
        else:
            pos = [(98+i*52, y0+40+(4 if i % 2 else -4)) for i in range(7)]
            b.rect_px(72, y0+16, PW-144, 48, "rgba(29,78,216,0.22)", 6, C["compr"], 1.4)
        for (x, y) in pos:
            if kind == "opt":
                b.parts.append(f'<circle cx="{x}" cy="{y}" r="{r+3}" fill="rgba(29,78,216,0.20)"/>')
            elif kind == "dry":
                b.parts.append(f'<circle cx="{x}" cy="{y}" r="{r+1.5}" fill="rgba(29,78,216,0.12)"/>')
            b.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="rgba(63,74,90,0.55)" '
                           f'stroke="{C["member"]}" stroke-width="1.4"/>')
        b.text_px(70, y0+78, cap1, 13, col, "start", weight="700")
        b.text_px(70, y0+98, cap2, 11.5, C["muted"], "start")
    grains(108, "dry", C["accent"], "乾側：摩擦鎖死", "水膜太薄，顆粒卡住無法重新排列")
    grains(236, "opt", C["bmd"], "最佳含水量：排列最密", "水膜剛好潤滑，顆粒滑到最緊密的位置")
    grains(364, "wet", C["compr"], "濕側：水墊效應", "水不可壓縮又來不及排掉，把顆粒撐開")
    b.rect_px(46, 492, PW-92, 80, C["fill_t"], 10, C["load"], 1.8)
    b.text_px(PW/2, 516, "夯實只排得掉空氣，排不掉水", 13.5, C["load"], weight="700")
    b.text_px(PW/2, 542, "濕側加水一定讓 γ_{d} 掉 —— 夯擊是幾秒鐘的衝擊載重，", 11.5, C["muted"])
    b.text_px(PW/2, 560, "水根本沒有時間滲流出去（那是壓密的事）", 11.5, C["muted"])

    compose([a, b],
            title="夯實曲線：水在乾側是潤滑劑，在濕側是阻擋物",
            sub="鐘形不是經驗規律，而是兩個相反機制交會的結果",
            note="ZAVC 由 S = 100% 推得，是純幾何上限。考場拿它做合理性檢核：任何算出來的 "
                 "乾密度若超過同含水量下的 ZAVC 值，代表計算或單位出錯。",
            path=f"{OUT}/sm13-fig-3-compaction-curve.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 4　夯實能量：曲線往左上移
# ═══════════════════════════════════════════════════════════════
def fig4():
    xr, yr = (0.06, 0.26), (14.6, 20.8)
    a, fx, fy, P = plotbox(PW, PH, xr, yr, (96, PW-56, 150, 500))
    a.panel("能量增加 ⇒ 曲線往「左上」移", "標準 Proctor 與修正 Proctor")
    axis_frame(a, fx(xr[0]), fx(xr[1]), fy(yr[0]), fy(yr[1]),
               "", "γ_{d}  (kN/m^{3})", ylab_dy=-26)
    a.text_px(fx(xr[1]), PH-fy(yr[0])+38, "w (%)", 12.5, C["muted"], "end")
    for wv in (8, 12, 16, 20, 24):
        a.text_px(fx(wv/100.0), PH-fy(yr[0])+18, f"{wv}", 12, C["muted"])
    for gv in (15, 16, 17, 18, 19, 20):
        a.text_px(fx(xr[0])-10, PH-fy(gv), f"{gv}", 12, C["muted"], "end")
        hline_px(a, fx(xr[0]), fx(xr[1]), PH-fy(gv), C["border"], 1.0)
    zs = [(w/1000.0, gzav(w/1000.0)) for w in range(60, 261, 4)]
    a.poly([P(w, g) for w, g in zs if yr[0] <= g <= yr[1]], C["muted"], 2.2, dash="8 5")
    a.text_px(fx(0.118), PH-fy(gzav(0.118))+16, "ZAVC", 12.5, C["muted"], "start", weight="700")
    peaks = []
    for key, rng in (("mod", (70, 200)), ("std", (85, 236))):
        p = PROCTOR[key]
        ws = [i/1000.0 for i in range(*rng)]
        a.poly([P(w, _comp_curve(p, w)) for w in ws], p["col"], 3.8)
        a.dot(P(p["wopt"], p["gdmax"]), 6.4, fill=p["col"], stroke="#FFFFFF", w=2.2)
        peaks.append((p["wopt"], p["gdmax"], p))
    # 峰值連線（夯實線 line of optimums）
    a.line(P(peaks[1][0], peaks[1][1]), P(peaks[0][0], peaks[0][1]),
           C["accent"], 2.4, dash="7 5")
    a.arrow(P(peaks[1][0]-0.004, peaks[1][1]+0.15), P(peaks[0][0]+0.004, peaks[0][1]-0.15),
            C["accent"], 2.6, 10)
    a.text_px(fx(0.072), PH-fy(19.75), "能量 ↑", 13.5, C["accent"], "start", weight="700")
    a.text_px(fx(0.072), PH-fy(19.75)+20, "γ_{d,max} ↑ 且 w_{opt} ↓", 12, C["accent"], "start")
    # 圖例（放在曲線下方的空白區，避免壓線）
    lx0, ly0 = fx(0.075), 356
    a.rect_px(lx0, ly0, fx(0.205)-lx0, 84, "#FFFFFF", 8, C["border"], 1.3)
    for j, key in enumerate(("std", "mod")):
        p = PROCTOR[key]
        yy = ly0 + 20 + j*40
        a.rect_px(lx0+14, yy-6, 22, 5, p["col"], 2)
        a.text_px(lx0+46, yy, f"{p['name']}　E = {p['E']:.0f} kJ/m^{{3}}",
                  11.5, p["col"], "start", weight="700")
        a.text_px(lx0+46, yy+19,
                  f"γ_{{d,max}} = {p['gdmax']:.1f}　w_{{opt}} = {p['wopt']*100:.1f}%",
                  10.5, C["muted"], "start")
    a.text_px(PW/2, PH-58, "峰值連線大致平行於 ZAVC 且落在其左側", 12.5, C["muted"])
    a.text_px(PW/2, PH-32,
              f"修正 Proctor 的能量是標準的 {E_RATIO:.1f} 倍", 13.5, C["accent"], weight="700")

    b = pxcv(PW, PH)
    b.panel("夯實能量怎麼算", "E = W · h · N · L / V，四個輸入各自代表什麼")
    b.math_px(PW/2, 104, "E = W h N L / V", 24, C["accent"], weight="700")
    heads = ["", "W 夯錘重", "h 落距", "N 夯擊數/層", "L 層數", "E (kJ/m^{3})"]
    colx = [40, 124, 200, 272, 352, 404]
    colw = [84, 76, 72, 80, 52, PW-40-404]
    b.rect_px(40, 136, PW-80, 34, C["fill_m"], 6, C["bmd"], 1.4)
    for x, w_, s in zip(colx, colw, heads):
        if s:
            b.text_px(x+w_/2, 153, s, 11.5, C["bmd"], weight="700")
    for i, key in enumerate(("std", "mod")):
        p = PROCTOR[key]
        y = 178 + i*46
        b.rect_px(40, y, PW-80, 40, C["panel"] if i == 0 else "rgba(192,57,43,0.08)",
                  6, C["border"], 1.2)
        vals = [p["name"], f"{p['W']:.1f} N", f"{p['h']*1000:.0f} mm",
                f"{p['N']:.0f}", f"{p['L']:.0f}", f"{p['E']:.0f}"]
        for x, w_, s in zip(colx, colw, vals):
            b.text_px(x+w_/2, y+20, s, 12, p["col"] if x == 40 else C["text"],
                      weight="700" if x in (40, 404) else "400")
    b.text_px(PW/2, 278, f"夯模體積 V = {MOLD_V*1e6:.0f} cm^{{3}}（兩者相同）", 11.5, C["muted"])
    # 三個實務啟示
    notes = [("現地夯實機具的「能量」是什麼", "滾壓機重量、振動頻率、輾壓遍數、鋪築層厚", C["bmd"]),
             ("為什麼工地要指定「層厚」", "層厚 = 公式裡的 L 與有效傳遞深度，鋪太厚底部夯不到", C["accent"]),
             ("能量不是越大越好", "超過最佳點會過度夯實、破壞顆粒，濕側還可能產生彈簧土", C["load"])]
    for i, (t1, t2, col) in enumerate(notes):
        y = 312 + i*84
        b.rect_px(40, y, PW-80, 70, C["panel"], 9, C["border"], 1.4)
        b.rect_px(40, y, 8, 70, col, 3)
        b.text_px(66, y+22, t1, 12.5, col, "start", weight="700")
        b.text_px(66, y+48, t2, 11.5, C["text"], "start")
    b.text_px(PW/2, PH-30, "題目給 W、h、N、L、V 就是要你算 E 或比較兩種夯實法",
              12.5, C["muted"], weight="700")

    compose([a, b],
            title="夯實能量：曲線往左上移的物理理由",
            sub="能量大 ⇒ 顆粒被推得更密，且更早就被水墊擋住",
            note="能量增加時，乾側的摩擦鎖死被更大的衝擊克服，故 γd,max 上升；"
                 "但更密的骨架代表孔隙更少，水墊效應提早發生，故 wopt 下降。兩個效應是同一件事的兩面。",
            path=f"{OUT}/sm13-fig-4-compaction-energy.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 5　品管兩把尺：RC 與 Dr
# ═══════════════════════════════════════════════════════════════
def fig5():
    a = pxcv(PW, PH)
    a.panel("兩把尺量的是同一根土柱", "但刻度的「零點」完全不同")
    x0, x1 = 74, PW-58
    YD, YR = 152, 268
    def scale(y, lo, hi, col, ticks, lab, sub):
        a.text_px((x0+x1)/2, y-40, sub, 11.5, C["muted"])
        a.rect_px(x0, y, x1-x0, 30, C["panel"], 5, C["border"], 1.3)
        a.text_px(x0-8, y+15, lab, 13, col, "end", weight="700")
        for v in ticks:
            xx = x0 + (v-lo)/(hi-lo)*(x1-x0)
            vline_px(a, xx, y, y+30, C["border"], 1.1)
            a.text_px(xx, y+44, f"{v:.0f}", 11, C["muted"])
        return lambda v: x0 + (v-lo)/(hi-lo)*(x1-x0)
    fD = scale(YD, 0, 100, C["bmd"], [0, 20, 40, 60, 80, 100],
               "D_{r} (%)", "相對密度：最鬆 → 最緊 的百分位")
    fR = scale(YR, 70, 102, C["load"], [70, 80, 90, 100],
               "RC (%)", "相對夯實度：現地 γ_{d} ÷ 實驗室 γ_{d,max}")
    a.rect_px(fD(0), YD, fD(100)-fD(0), 30, "rgba(46,125,111,0.14)", 5)
    a.rect_px(fR(RC_AT_DR0*100), YR, fR(100)-fR(RC_AT_DR0*100), 30,
              "rgba(192,57,43,0.14)", 5)
    for v, col in ((0.0, C["muted"]), (DR_FIELD*100, C["accent"]), (100.0, C["muted"])):
        rc = (gd_of_e(E_MAX - v/100.0*(E_MAX-E_MIN))/GD_SAND_MAX)*100.0
        a.parts.append(f'<line x1="{fD(v):.1f}" y1="{YD+36:.1f}" x2="{fR(rc):.1f}" '
                       f'y2="{YR-8:.1f}" stroke="{col}" stroke-width="1.8" stroke-dasharray="5 4"/>')
        a.dot(PX(a, fD(v), YD+30), 5.0, fill=col, stroke="#FFFFFF", w=1.8)
        a.dot(PX(a, fR(rc), YR), 5.0, fill=col, stroke="#FFFFFF", w=1.8)
    a.text_px(fD(DR_FIELD*100), YD-18,
              f"現地 D_{{r}} = {DR_FIELD*100:.0f}%", 12.5, C["accent"], weight="700")
    a.text_px(fR(RC_FIELD*100), YR+62,
              f"同一根土 RC = {RC_FIELD*100:.0f}%", 12.5, C["accent"], weight="700")
    a.rect_px(56, 342, PW-112, 62, C["fill_t"], 9, C["load"], 1.8)
    a.text_px(PW/2, 364, f"D_{{r}} = 0（最鬆狀態）時，RC 已經是 {RC_AT_DR0*100:.0f}%",
              13, C["load"], weight="700")
    a.text_px(PW/2, 388, "所以 RC 95% 與 D_{r} 95% 是完全不同的要求", 12, C["text"], weight="700")
    rows = [("e_{max}", f"{E_MAX:.2f}"), ("e_{min}", f"{E_MIN:.2f}"),
            ("現地 γ_{d}", f"{GD_FIELD_SAND:.2f} kN/m^{{3}}"),
            ("現地 e", f"{E_FIELD:.3f}")]
    a.text_px(PW/2, 424, f"示範砂（G_{{s}} = {GS:.2f}）", 12.5, C["muted"], weight="700")
    for i, (k, v) in enumerate(rows):
        y = 444 + i*32
        a.rect_px(96, y, PW-192, 26, C["panel"], 5, C["border"], 1.2)
        a.text_px(120, y+13, k, 12, C["muted"], "start")
        a.text_px(PW-120, y+13, v, 12.5, C["text"], "end", weight="700")
    a.text_px(PW/2, PH-18, "細粒土看 RC、粗粒土（砂）看 D_{r}", 13.5, C["bmd"], weight="700")

    b = pxcv(PW, PH)
    b.panel("兩者的唯一橋樑", "百分比不可以直接對接，必須繞回 γ_{d}")
    b.rect_px(46, 104, PW-92, 46, C["fill_m"], 8, C["bmd"], 1.8)
    b.math_px(PW/2, 127, "γ_{d} = G_{s} γ_{w} / (1 + e)", 19, C["bmd"], weight="700")
    chain = [("D_{r} (%)", "e_{max}, e_{min} 已知", C["bmd"]),
             ("孔隙比 e", "e = e_{max} - D_{r}(e_{max} - e_{min})", C["accent"]),
             ("乾單位重 γ_{d}", "γ_{d} = G_{s}γ_{w}/(1+e)", C["member"]),
             ("RC (%)", "RC = γ_{d} ÷ γ_{d,max}", C["load"])]
    for i, (t1, t2, col) in enumerate(chain):
        y = 178 + i*78
        b.rect_px(78, y, PW-156, 54, C["panel"], 9, C["border"], 1.4)
        b.rect_px(78, y, 8, 54, col, 3)
        b.text_px(104, y+18, t1, 13, col, "start", weight="700")
        b.text_px(104, y+38, t2, 11.5, C["muted"], "start")
        if i < 3:
            vdown(b, PW/2, y+54, y+72, C["muted"], 2.2)
    b.rect_px(46, 496, PW-92, 74, C["fill_t"], 10, C["load"], 1.8)
    b.text_px(PW/2, 520, "最常見的錯誤", 13, C["load"], weight="700")
    b.text_px(PW/2, 544, "把 D_{r} = 70% 直接當成 RC = 70%", 13, C["text"], weight="700")
    b.text_px(PW/2, 562, "兩把尺的零點與滿刻度都不同，必須經 γ_{d} 換算", 11.5, C["muted"])

    compose([a, b],
            title="夯實品管的兩把尺：RC 與 Dr 不是同一件事",
            sub="細粒土用相對夯實度，粗粒土（砂）用相對密度",
            note="Dr 的零點是「最鬆狀態」，RC 的零點是 0；同一根土在 Dr = 0 時 RC 已經約 "
                 "77~80%。兩者要互換，只能透過 γd = Gs·γw/(1+e) 這條橋，不能直接對接百分比。",
            path=f"{OUT}/sm13-fig-5-rc-vs-dr.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 6　土方平衡：唯一守恆量是乾土重 Ws
# ═══════════════════════════════════════════════════════════════
def fig6():
    W, H = 1200, 520
    cv = pxcv(W, H)
    cv.rect_px(0, 0, W, H, "#FFFFFF", 0)
    states = [
        ("① 借土區（原地）", f"e = {E_BORROW:.2f}　w = {W_BORROW*100:.0f}%",
         GD_BORROW, V_BORROW, W_BORROW, C["muted"]),
        ("② 運送中（鬆方）", "體積變大，含水量不變", GD_BORROW*0.82,
         WS_TOTAL/(GD_BORROW*0.82), W_BORROW, C["accent"]),
        ("③ 完成填方（夯實後）", f"RC = 95%　w = {W_TARGET*100:.0f}%",
         GD_FILL, V_FILL, W_TARGET, C["load"]),
    ]
    CW_, GAP = 320, 60
    xs = [56, 56+CW_+GAP, 56+2*(CW_+GAP)]
    vmax = max(s[3] for s in states)
    HBAR = 150
    ytop = 96
    for (head, sub, gd, vol, wc, col), x in zip(states, xs):
        cv.text_px(x+CW_/2, ytop-34, head, 15.5, col, weight="700")
        cv.text_px(x+CW_/2, ytop-14, sub, 12, C["muted"])
        hbar = HBAR*vol/vmax
        # 體積柱（固體＋水＋空氣的示意分割）
        e_here = e_of_gd(gd)
        f_sol = 1.0/(1.0+e_here)
        f_wat = wc*GS/(1.0+e_here)
        f_air = max(0.0, 1.0 - f_sol - f_wat)
        y = ytop + (HBAR - hbar)
        for frac, fill, stroke in ((f_air, "rgba(138,148,166,0.28)", C["muted"]),
                                   (f_wat, "rgba(29,78,216,0.24)", C["compr"]),
                                   (f_sol, "rgba(63,74,90,0.45)", C["member"])):
            hh = hbar*frac
            if hh > 0.4:
                cv.rect_px(x, y, CW_, hh, fill, 0, stroke, 1.4)
            y += hh
        cv.text_px(x+CW_/2, ytop+HBAR+22, f"V = {vol:,.0f} m^{{3}}", 14, col, weight="700")
        cv.text_px(x+CW_/2, ytop+HBAR+44, f"γ_{{d}} = {gd:.2f} kN/m^{{3}}", 12.5, C["muted"])
    # 固體體積三格等高 —— 這就是 Ws 守恆的幾何意義
    ysol = ytop + HBAR
    h_sol_px = HBAR*(V_FILL/vmax)*(1.0/(1.0+e_of_gd(GD_FILL)))
    hline_px(cv, xs[0]-24, xs[2]+CW_+24, ysol, C["bmd"], 1.6, "6 5")
    hline_px(cv, xs[0]-24, xs[2]+CW_+24, ysol-h_sol_px, C["bmd"], 1.6, "6 5")
    cv.text_px(xs[1]+CW_/2, ysol-h_sol_px/2, "固體體積 V_{s} 三格等高", 14, "#FFFFFF", weight="700")
    y_ws = 336
    cv.rect_px(xs[0], y_ws, xs[2]+CW_-xs[0], 52, C["fill_m"], 10, C["bmd"], 2.2)
    cv.text_px(W/2, y_ws+18, f"三個狀態唯一守恆的量：乾土重 W_{{s}} = {WS_TOTAL:,.0f} kN",
               15.5, C["bmd"], weight="700")
    cv.text_px(W/2, y_ws+40, "體積會變、含水量會變、單位重會變 —— 只有固體顆粒的重量不變",
               12.5, C["muted"])
    for x in xs:
        vdown(cv, x+CW_/2, ysol+56, y_ws, C["bmd"], 2.0)
    # 解題三步
    steps = [("Step 1　由完成填方算總乾土重",
              f"W_{{s}} = γ_{{d,填}} · V_{{填}} = {GD_FILL:.2f} × {V_FILL:,.0f} = {WS_TOTAL:,.0f} kN", C["load"]),
             ("Step 2　用 W_{s} 回推開挖體積",
              f"V_{{借}} = W_{{s}} ÷ γ_{{d,借}} = {WS_TOTAL:,.0f} ÷ {GD_BORROW:.2f} = {V_BORROW:,.0f} m^{{3}}", C["muted"]),
             ("Step 3　加水量也由 W_{s} 算",
              f"W_{{w}} = W_{{s}}(w_{{目標}} - w_{{原}}) = {W_ADD_KN:,.0f} kN ≈ {W_ADD_M3:,.0f} m^{{3}}", C["compr"])]
    for i, (t1, t2, col) in enumerate(steps):
        y = 410 + i*36
        cv.rect_px(56, y, W-112, 30, C["panel"], 6, C["border"], 1.2)
        cv.rect_px(56, y, 7, 30, col, 3)
        cv.text_px(80, y+15, t1, 12.5, col, "start", weight="700")
        cv.text_px(400, y+15, t2, 12.5, C["text"], "start")

    compose([cv],
            title="土方平衡：借土 → 運送 → 夯實，只有乾土重守恆",
            sub=f"本例脹縮比 V借 / V填 = {SHRINK:.3f}，代表要挖出比填方多 {(SHRINK-1)*100:.1f}% 的體積",
            note="千萬不要用「體積守恆」或「總重守恆」列式 —— 運送與夯實都會改變體積與含水量。"
                 "先由完成填方算 Ws，再用 Ws 反推借土體積與加水量，三步都不會錯。",
            path=f"{OUT}/sm13-fig-6-earthwork-balance.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 7　有效應力剖面 p0'
# ═══════════════════════════════════════════════════════════════
def fig7():
    a = pxcv(PW, PH)
    a.panel("先定「黏土層中點」", "壓密沉陷一律取中點深度代表全層")
    top, bot = 116, 500
    def zy(z): return top + (bot-top)*z/CLAY_BOT
    fills = ["rgba(180,83,9,0.16)", "rgba(180,83,9,0.10)", "rgba(46,125,111,0.16)"]
    x0, x1 = 78, PW-104
    for (z0, z1, g, name), fill in zip(LAYERS, fills):
        a.rect_px(x0, zy(z0), x1-x0, zy(z1)-zy(z0), fill, 0, C["member"], 1.6)
        a.text_px((x0+x1)/2, (zy(z0)+zy(z1))/2 - 10, name, 12.5, C["text"], weight="700")
        a.text_px((x0+x1)/2, (zy(z0)+zy(z1))/2 + 12,
                  f"γ = {g:.1f} kN/m^{{3}}", 11.5, C["muted"])
        a.text_px(x0-8, zy(z0), f"{z0:.0f} m", 11.5, C["muted"], "end")
    a.text_px(x0-8, zy(CLAY_BOT), f"{CLAY_BOT:.0f} m", 11.5, C["muted"], "end")
    # 岩盤
    a.rect_px(x0, zy(CLAY_BOT), x1-x0, 26, "rgba(63,74,90,0.45)", 0, C["member"], 1.6)
    a.text_px((x0+x1)/2, zy(CLAY_BOT)+13, "不透水岩盤", 12, "#FFFFFF", weight="700")
    # 地下水位
    hline_px(a, x0-16, x1+16, zy(GWT), C["compr"], 2.2)
    for k in range(3):
        hline_px(a, x0-10+k*6, x0+2+k*6, zy(GWT)+6+k*4, C["compr"], 1.6)
    a.text_px(x1+22, zy(GWT), "地下水位", 12, C["compr"], "start", weight="700")
    # 中點
    hline_px(a, x0, x1, zy(Z_MID), C["load"], 2.2, "7 5")
    a.dot(PX(a, (x0+x1)/2, zy(Z_MID)), 6.4, fill=C["load"], stroke="#FFFFFF", w=2.2)
    a.text_px(x1+22, zy(Z_MID), f"中點 z = {Z_MID:.0f} m", 12.5, C["load"], "start", weight="700")
    a.text_px(PW/2, PH-58, "取中點是因為 e-log p' 是曲線，", 12, C["muted"])
    a.text_px(PW/2, PH-34, "中點應力代表全層的平均壓縮行為", 13, C["text"], weight="700")

    # 右：三線圖（深度向下，應力向右）
    smax = sigma_total(CLAY_BOT)*1.10
    b, fx, fy, P = plotbox(PW, PH, (0, smax), (0, CLAY_BOT), (112, PW-88, 108, 452))
    b.panel("σ、u、σ' 三條線", "有效應力是「總應力扣孔隙水壓」")
    def dy(z): return 112 + (452-112)*z/CLAY_BOT
    def dpx(sv): return fx(sv)
    b.parts.append(f'<line x1="{fx(0):.1f}" y1="{dy(0):.1f}" x2="{fx(smax):.1f}" '
                   f'y2="{dy(0):.1f}" stroke="{C["muted"]}" stroke-width="1.8"/>')
    b.parts.append(f'<line x1="{fx(0):.1f}" y1="{dy(0):.1f}" x2="{fx(0):.1f}" '
                   f'y2="{dy(CLAY_BOT)+18:.1f}" stroke="{C["muted"]}" stroke-width="1.8"/>')
    b.text_px(fx(smax), dy(0)-18, "應力 (kPa)", 12, C["muted"], "end")
    b.text_px(fx(0)-12, dy(0)-40, "深度", 11.5, C["muted"], "end")
    b.text_px(fx(0)-12, dy(0)-24, "z (m)", 11.5, C["muted"], "end")
    for zt in (0, 2, 4, 6, 8, 10):
        b.text_px(fx(0)-12, dy(zt), f"{zt}", 11.5, C["muted"], "end")
        hline_px(b, fx(0), fx(smax), dy(zt), C["border"], 1.0)
    for sv in (50, 100, 150, 200):
        vline_px(b, fx(sv), dy(0), dy(CLAY_BOT), C["border"], 1.0)
        b.text_px(fx(sv), dy(0)-6, f"{sv}", 10.5, C["muted"])
    zs = [i/20.0 for i in range(0, int(CLAY_BOT*20)+1)]
    def polyline(pts, col, w, dash=None):
        s2 = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        b.parts.append(f'<polyline points="{s2}" fill="none" stroke="{col}" '
                       f'stroke-width="{w}" stroke-linejoin="round"{d}/>')
    polyline([(dpx(sigma_total(z)), dy(z)) for z in zs], C["member"], 3.2)
    polyline([(dpx(u_w(z)), dy(z)) for z in zs], C["compr"], 3.2, "7 5")
    polyline([(dpx(sigma_eff(z)), dy(z)) for z in zs], C["load"], 3.6)
    b.text_px(dpx(u_w(9.4))-10, dy(9.4), "u", 16, C["compr"], "end", weight="700")
    b.text_px(dpx(sigma_eff(9.4))+10, dy(9.4)-14, "σ'", 16, C["load"], "start", weight="700")
    b.text_px(dpx(sigma_total(9.4))+10, dy(9.4), "σ", 16, C["member"], "start", weight="700")
    # 中點標示
    b.parts.append(f'<line x1="{fx(0):.1f}" y1="{dy(Z_MID):.1f}" '
                   f'x2="{dpx(sigma_total(Z_MID)):.1f}" y2="{dy(Z_MID):.1f}" '
                   f'stroke="{C["accent"]}" stroke-width="1.8" stroke-dasharray="5 4"/>')
    b.dot(PX(b, dpx(sigma_eff(Z_MID)), dy(Z_MID)), 6.6, fill=C["load"], stroke="#FFFFFF", w=2.4)
    b.text_px(dpx(sigma_eff(Z_MID)), dy(Z_MID)-18, f"{P0:.1f}", 12, C["load"], weight="700")
    b.rect_px(46, 484, PW-92, 92, C["fill_t"], 10, C["load"], 1.8)
    b.text_px(PW/2, 508, f"p_{{0}}' = σ'(z = {Z_MID:.0f} m) = {P0:.1f} kPa", 17, C["load"], weight="700")
    b.text_px(PW/2, 536, "水位以下一律用浮單位重 γ' = γ_{sat} - γ_{w}", 12.5, C["text"], weight="700")
    b.text_px(PW/2, 558,
              f"= {2.0*18.0:.0f} + {4.0*(19.5-GW):.2f} + {2.0*(17.5-GW):.2f} = {P0:.1f} kPa",
              12, C["muted"])

    compose([a, b],
            title="壓密題的第一步：算出中點的現況有效應力 p0'",
            sub="p0' 算錯，後面 Case A/B/C 一定判錯",
            note="總應力用飽和單位重逐層累加，孔隙水壓由地下水位起算，兩者相減就是有效應力。"
                 "等效做法是水位以下直接用浮單位重 γ' = γsat − γw，兩種寫法答案完全相同。",
            path=f"{OUT}/sm13-fig-7-effective-stress.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 8　e-log p' 曲線：土壤的記憶
# ═══════════════════════════════════════════════════════════════
def fig8():
    W, H = 1200, 560
    p_lo, p_hi = 20.0, 600.0
    xr, yr = (LOG(p_lo), LOG(p_hi)), (0.72, 1.14)
    cv, fx, fy, P = plotbox(W, H, xr, yr, (150, W-430, 96, 470))
    cv.rect_px(0, 0, W, H, "#FFFFFF", 0)
    cv.arrow((fx(xr[0]), fy(yr[0])), (fx(xr[1])+16, fy(yr[0])), C["muted"], 1.8, 9)
    cv.arrow((fx(xr[0]), fy(yr[0])), (fx(xr[0]), fy(yr[1])+16), C["muted"], 1.8, 9)
    cv.text_px(fx(xr[1]), H-fy(yr[0])+40, "log p'  (kPa)", 13, C["muted"], "end")
    cv.text_px(fx(xr[0]), H-fy(yr[1])-30, "孔隙比 e", 13, C["muted"])
    for pv in (20, 50, 100, 200, 400):
        vline_px(cv, fx(LOG(pv)), H-fy(yr[1]), H-fy(yr[0]), C["border"], 1.0)
        cv.text_px(fx(LOG(pv)), H-fy(yr[0])+18, f"{pv}", 11.5, C["muted"])
    for ev in (0.8, 0.9, 1.0, 1.1):
        hline_px(cv, fx(xr[0]), fx(xr[1]), H-fy(ev), C["border"], 1.0)
        cv.text_px(fx(xr[0])-10, H-fy(ev), f"{ev:.1f}", 11.5, C["muted"], "end")

    def e_at(p):
        if p <= PC:
            return E0 - CR*LOG(p/P0)
        return E0 - CR*LOG(PC/P0) - CC*LOG(p/PC)
    # 再壓縮線（延伸到 pc' 左右）
    seg1 = [P(LOG(p), e_at(p)) for p in [p_lo + i for i in range(0, int(PC-p_lo)+1, 2)]]
    cv.poly(seg1, C["compr"], 4.0)
    seg2 = [P(LOG(p), e_at(p)) for p in [PC + i*4 for i in range(0, int((p_hi-PC)/4)+1)]]
    cv.poly(seg2, C["load"], 4.4)
    # 迴彈線（虛線示意）
    cv.poly([P(LOG(p), e_at(p_hi) + CR*LOG(p_hi/p)) for p in [p_hi - i*8 for i in range(0, 46)]],
            C["muted"], 2.2, dash="7 5")
    cv.text_px(fx(LOG(300)), H-fy(e_at(p_hi)+CR*LOG(p_hi/300))+22, "迴彈（卸載）",
               11.5, C["muted"], "start")
    # 關鍵點
    for p, col, lab, dyy in ((P0, C["bmd"], f"p_{{0}}' = {P0:.1f}", -22),
                             (PC, C["accent"], f"p_{{c}}' = {PC:.0f}", -22),
                             (PF, C["load"], f"p_{{f}}' = {PF:.1f}", 26)):
        cv.dot(P(LOG(p), e_at(p)), 6.6, fill=col, stroke="#FFFFFF", w=2.4)
        vline_px(cv, fx(LOG(p)), H-fy(e_at(p)), H-fy(yr[0]), col, 1.6, "5 4")
        cv.text_px(fx(LOG(p)), H-fy(e_at(p))+dyy, lab, 12.5, col, weight="700")
    # 斜率標示
    cv.text_px(fx(LOG(58)), H-fy(e_at(58))-30, "再壓縮線 C_{r}（彈性）",
               13.5, C["compr"], weight="700")
    cv.text_px(fx(LOG(58)), H-fy(e_at(58))-10, f"C_{{r}} = {CR:.3f}", 12, C["compr"])
    cv.text_px(fx(LOG(300)), H-fy(e_at(300))-30, "處女壓縮線 C_{c}（結構崩塌）",
               13.5, C["load"], weight="700")
    cv.text_px(fx(LOG(300)), H-fy(e_at(300))-10, f"C_{{c}} = {CC:.3f}", 12, C["load"])

    # 右側說明卡
    xk = W-400
    cv.rect_px(xk, 84, 352, 132, C["fill_m"], 10, C["bmd"], 1.8)
    cv.text_px(xk+176, 110, "土壤有記憶：預壓密應力 p_{c}'", 14, C["bmd"], weight="700")
    cv.text_px(xk+176, 136, "這一層土在地質史上曾經承受過的最大有效應力", 11.5, C["muted"])
    cv.math_px(xk+176, 172, f"OCR = p_{{c}}' / p_{{0}}' = {OCR:.2f}", 18, C["bmd"], weight="700")
    cv.text_px(xk+176, 200, "OCR = 1 正常壓密 NC　／　OCR ＞ 1 過壓密 OC", 11.5, C["text"], weight="700")
    cards = [("記憶內　p' ≤ p_{c}'", "走 C_{r}：只是把先前被壓過的結構再壓一次，",
              "彈性為主，沉陷極小", C["compr"]),
             ("超過記憶　p' ＞ p_{c}'", "走 C_{c}：顆粒結構首次崩塌重排，不可回復，",
              "沉陷大得多", C["load"]),
             (f"兩者差 {CC_OVER_CR:.0f} 倍",
              f"本例 C_{{c}} / C_{{r}} = {CC:.3f} / {CR:.3f} = {CC_OVER_CR:.1f}",
              "一般在 5~10 倍之間", C["accent"])]
    for i, (t1, t2, t3, col) in enumerate(cards):
        y = 236 + i*88
        cv.rect_px(xk, y, 352, 76, C["panel"], 9, C["border"], 1.4)
        cv.rect_px(xk, y, 8, 76, col, 3)
        cv.text_px(xk+26, y+20, t1, 13, col, "start", weight="700")
        cv.text_px(xk+26, y+44, t2, 11.5, C["text"], "start")
        cv.text_px(xk+26, y+62, t3, 11.5, C["text"], "start")
    cv.rect_px(150, 500, 640, 44, C["fill_t"], 9, C["load"], 1.8)
    cv.text_px(470, 522,
               "判斷 Case 的唯一依據：把 p0'、pc'、pf' 排在這條對數軸上",
               13.5, C["load"], weight="700")

    compose([cv],
            title="e-log p' 曲線：土壤記得自己被壓過多重",
            sub="兩條斜率不同的直線，決定了沉陷量會差好幾倍",
            note="Cr 段是彈性再壓縮，Cc 段是顆粒結構首次崩塌。分界點就是預壓密應力 pc'，"
                 "由 Casagrande 作圖法從曲率最大點求得。OCR 只是 pc' 與 p0' 的比值。",
            path=f"{OUT}/sm13-fig-8-e-logp.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 9　Case A / B / C：把三個應力排在對數軸上  ★
# ═══════════════════════════════════════════════════════════════
def fig9():
    W, H = 1240, 740
    cv = pxcv(W, H)
    cv.rect_px(0, 0, W, H, "#FFFFFF", 0)
    x0, x1 = 96, W - 470
    p_lo, p_hi = 60.0, 260.0
    fx = lambda p: x0 + (LOG(p)-LOG(p_lo))/(LOG(p_hi)-LOG(p_lo))*(x1-x0)

    cases = [
        ("Case A　正常壓密 NC", "p_{0}' = p_{c}'，全程走 C_{c}",
         P0, P0, P0+DSIG, [(P0, P0+DSIG, C["load"], "C_{c}")], C["load"],
         ["S_{c} = C_{c}H/(1+e_{0}) · log[(p_{0}'+Δσ)/p_{0}']"],
         "p_{0}' 與 p_{c}' 重合 ⇒ 一跨越就進入處女壓縮線"),
        ("Case B　過壓密、未跨越", "p_{0}'+Δσ ≤ p_{c}'，全程走 C_{r}",
         P0, PC, P0+28.0, [(P0, P0+28.0, C["compr"], "C_{r}")], C["compr"],
         ["S_{c} = C_{r}H/(1+e_{0}) · log[(p_{0}'+Δσ)/p_{0}']"],
         "仍在記憶範圍內 ⇒ 彈性變形，沉陷極小"),
        ("Case C　過壓密且跨越", "p_{0}'+Δσ ＞ p_{c}'，必須分兩段相加",
         P0, PC, PF, [(P0, PC, C["compr"], "C_{r}"), (PC, PF, C["load"], "C_{c}")],
         C["accent"],
         ["S_{c} = C_{r}H/(1+e_{0}) · log(p_{c}'/p_{0}')",
          "    + C_{c}H/(1+e_{0}) · log(p_{f}'/p_{c}')"],
         "歷屆最愛考的一型 —— 只用一條公式算完全程就整題報銷"),
    ]
    for i, (head, sub, p0, pc, pf, segs, col, forms, tip) in enumerate(cases):
        yb = 132 + i*184
        cv.rect_px(56, yb-80, W-112, 162,
                   C["panel"] if i != 2 else "rgba(180,83,9,0.09)", 12,
                   C["border"] if i != 2 else C["accent"], 1.4 if i != 2 else 2.4)
        cv.text_px(80, yb-56, head, 15.5, col, "start", weight="700")
        cv.text_px(80, yb-34, sub, 12, C["muted"], "start")
        # 對數軸
        cv.parts.append(f'<line x1="{x0:.1f}" y1="{yb:.1f}" x2="{x1:.1f}" y2="{yb:.1f}" '
                        f'stroke="{C["muted"]}" stroke-width="2.0"/>')
        for pv in (60, 80, 100, 130, 170, 220, 260):
            cv.parts.append(f'<line x1="{fx(pv):.1f}" y1="{yb-5:.1f}" x2="{fx(pv):.1f}" '
                            f'y2="{yb+5:.1f}" stroke="{C["muted"]}" stroke-width="1.4"/>')
            cv.text_px(fx(pv), yb+20, f"{pv}", 10.5, C["muted"])
        cv.text_px(x1, yb+40, "log p'", 12, C["muted"], "end")
        # 走過的路徑
        for (pa, pb, ccol, lab) in segs:
            cv.rect_px(fx(pa), yb-17, fx(pb)-fx(pa), 12,
                       "rgba(192,57,43,0.55)" if ccol == C["load"] else "rgba(29,78,216,0.55)", 4)
            cv.text_px((fx(pa)+fx(pb))/2, yb-32, lab, 13.5, ccol, weight="700")
        # 三個標記
        marks = sorted([(p0, C["bmd"], "p_{0}'"), (pc, C["accent"], "p_{c}'"),
                        (pf, C["load"], "p_{f}'")], key=lambda t: t[0])
        placed = []
        for pv, mcol, lab in marks:
            xx = fx(pv)
            dyy = 46
            while any(abs(xx - xp) < 62 and abs(dyy - dp) < 12 for xp, dp in placed):
                dyy += 22
            placed.append((xx, dyy))
            cv.parts.append(f'<line x1="{xx:.1f}" y1="{yb+6:.1f}" x2="{xx:.1f}" '
                            f'y2="{yb+dyy-13:.1f}" stroke="{mcol}" stroke-width="1.6" '
                            f'stroke-dasharray="4 3"/>')
            cv.dot(PX(cv, xx, yb), 5.6, fill=mcol, stroke="#FFFFFF", w=2.0)
            cv.text_px(xx, yb+dyy, f"{lab} = {pv:.0f}", 12, mcol, weight="700")
        # 右欄公式
        xk = W - 440
        cv.rect_px(xk, yb-62, 368, 126, "#FFFFFF", 9, col, 1.6)
        cv.text_px(xk+184, yb-42, "沉陷量公式", 11.5, C["muted"], weight="700")
        for j, fstr in enumerate(forms):
            cv.text_px(xk+14, yb-16+j*24, fstr, 12.5, C["text"], "start", weight="700")
        cv.text_px(xk+184, yb+44, tip, 11.5, col, weight="700")

    # 驗算技巧
    yv = 132 + 3*184 - 66
    cv.rect_px(56, yv, W-112, 100, C["fill_m"], 12, C["bmd"], 2.0)
    cv.text_px(W/2, yv+26, "Case C 的一秒驗算：答案必定夾在「全套 Cc」與「全套 Cr」之間",
               15, C["bmd"], weight="700")
    bx0, bx1 = 260, W-260
    fb = lambda v: bx0 + v/SC_CC*(bx1-bx0)
    cv.parts.append(f'<line x1="{bx0:.1f}" y1="{yv+62:.1f}" x2="{bx1:.1f}" y2="{yv+62:.1f}" '
                    f'stroke="{C["border"]}" stroke-width="5" stroke-linecap="round"/>')
    for val, mcol, lab in ((SC_CR, C["compr"], f"全套 C_{{r}}　{SC_CR:.1f} mm"),
                           (SC, C["accent"], f"本例 Case C　{SC:.1f} mm"),
                           (SC_CC, C["load"], f"全套 C_{{c}}　{SC_CC:.1f} mm")):
        cv.dot(PX(cv, fb(val), yv+62), 6.4, fill=mcol, stroke="#FFFFFF", w=2.2)
        cv.text_px(fb(val), yv+84, lab, 12, mcol, weight="700")

    compose([cv],
            title="Case A / B / C：把 p0'、pc'、pf' 排在對數軸上就分完了",
            sub="不需要背三條公式 —— 看路徑走過哪幾段，就把哪幾段加起來",
            note="Case C 是歷屆最愛考的一型：跨越 pc' 時，前半段走 Cr、後半段走 Cc，兩段必須相加。"
                 "只用一條公式算完全程，是本單元最高頻的扣分點。",
            path=f"{OUT}/sm13-fig-9-case-abc.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 10　Δσ：2:1 傳佈 vs 大面積不折減
# ═══════════════════════════════════════════════════════════════
def fig10():
    TOP, SCZ, ZMAX = 156, 20.0, 8.6            # 基底像素 y、每公尺像素、繪圖深度
    def yz(z): return TOP + z*SCZ
    ZC = Z_BELOW                               # 黏土中點在基底下的深度

    a = pxcv(W3, H3)
    a.panel("有限尺寸基礎", "2:1 應力傳佈法：應力會擴散、會折減")
    cxx = W3/2
    bw = 52
    a.text_px(cxx, 84, f"Q = {Q_FTG:.0f} kN", 13, C["load"], weight="700")
    a.text_px(cxx, 104, f"B × L = {B_FTG:.0f} × {L_FTG:.0f} m", 11, C["muted"])
    vdown(a, cxx, 114, TOP-24, C["load"], 3.0)
    hline_px(a, 26, W3-26, TOP, C["member"], 2.0)
    a.rect_px(cxx-bw/2, TOP-22, bw, 22, "rgba(63,74,90,0.45)", 2, C["member"], 1.6)
    a.text_px(30, TOP-10, "基底", 11, C["muted"], "start")
    half = lambda z: bw/2 + z*SCZ/2.0
    a.polygon([PX(a, cxx-bw/2, TOP), PX(a, cxx+bw/2, TOP),
               PX(a, cxx+half(ZMAX), yz(ZMAX)), PX(a, cxx-half(ZMAX), yz(ZMAX))],
              "rgba(180,83,9,0.12)", "none", 0)
    for sgn in (-1, 1):
        a.parts.append(f'<line x1="{cxx+sgn*bw/2:.1f}" y1="{TOP:.1f}" '
                       f'x2="{cxx+sgn*half(ZMAX):.1f}" y2="{yz(ZMAX):.1f}" '
                       f'stroke="{C["accent"]}" stroke-width="2.2" stroke-dasharray="6 4"/>')
    a.text_px(cxx+half(3.4)+8, yz(3.4), "2 垂直 : 1 水平", 11.5, C["accent"], "start", weight="700")
    hline_px(a, 30, W3-30, yz(ZC), C["compr"], 1.8, "6 4")
    a.dot(PX(a, cxx, yz(ZC)), 6.0, fill=C["load"], stroke="#FFFFFF", w=2.2)
    a.text_px(32, yz(ZC)-13, f"黏土中點 z = {ZC:.1f} m", 11.5, C["compr"], "start", weight="700")
    a.rect_px(26, 350, W3-52, 70, C["fill_t"], 9, C["load"], 1.8)
    a.math_px(W3/2, 372, "Δσ = Q / [(B+z)(L+z)]", 16, C["load"], weight="700")
    a.text_px(W3/2, 398, f"= {Q_FTG:.0f} / ({B_FTG+ZC:.1f} × {L_FTG+ZC:.1f})"
              f" = {DSIG_21:.1f} kPa", 12, C["text"], weight="700")
    a.text_px(W3/2, 444, "z 必須從「基礎底面」起算，不是地表", 12.5, C["accent"], weight="700")

    b = pxcv(W3, H3)
    b.panel("大面積均布載重", "全深度完全不折減")
    b.text_px(W3/2, 88, "預壓覆土／大範圍回填／水位下降", 11.5, C["muted"])
    for k in range(7):
        xx = 46 + k*(W3-92)/6
        vdown(b, xx, 100, TOP-46, C["load"], 2.4)
    b.rect_px(30, TOP-42, W3-60, 26, "rgba(192,57,43,0.22)", 3, C["load"], 1.8)
    b.text_px(W3/2, TOP-29, f"Δσ = {DSIG:.0f} kPa", 13, C["load"], weight="700")
    hline_px(b, 26, W3-26, TOP, C["member"], 2.0)
    for z in (1.6, 3.4, 5.2, 7.4):
        for k in range(7):
            xx = 46 + k*(W3-92)/6
            vdown(b, xx, yz(z)-20, yz(z), "rgba(192,57,43,0.55)", 1.8)
    hline_px(b, 30, W3-30, yz(ZC), C["compr"], 1.8, "6 4")
    b.text_px(32, yz(ZC)-13, "黏土中點", 11.5, C["compr"], "start", weight="700")
    b.text_px(W3-32, yz(ZC)-13, f"Δσ 仍為 {DSIG:.0f} kPa", 11.5, C["load"], "end", weight="700")
    b.rect_px(26, 350, W3-52, 70, C["fill_m"], 9, C["bmd"], 1.8)
    b.text_px(W3/2, 372, "載重面積 ≫ 影響深度", 13, C["bmd"], weight="700")
    b.text_px(W3/2, 398, "應力無處可擴散 ⇒ 不折減", 12.5, C["text"], weight="700")
    b.text_px(W3/2, 444, "水位下降也屬此類（全深度加 Δσ）", 12.5, C["accent"], weight="700")

    c = pxcv(W3, H3)
    c.panel("同樣的載重，深度效應天差地別", "Δσ 隨深度的變化")
    dmax, ZP = 210.0, 10.0
    px0, px1 = 84, W3-40
    cy0, cy1 = TOP, TOP + 172
    fxd = lambda d: px0 + d/dmax*(px1-px0)
    fyz = lambda z: cy0 + z/ZP*(cy1-cy0)
    hline_px(c, px0, px1, cy0, C["muted"], 1.8)
    vline_px(c, px0, cy0, cy1+14, C["muted"], 1.8)
    c.text_px(px1, cy0-36, "Δσ (kPa)", 11.5, C["muted"], "end")
    c.text_px(px0-8, cy1+26, "z (m)", 11.5, C["muted"], "end")
    for dv in (50, 100, 150, 200):
        vline_px(c, fxd(dv), cy0, cy1, C["border"], 1.0)
        c.text_px(fxd(dv), cy0-14, f"{dv}", 10.5, C["muted"])
    for zv in (2, 4, 6, 8, 10):
        c.text_px(px0-8, fyz(zv), f"{zv}", 10.5, C["muted"], "end")
    pts = " ".join(f"{fxd(min(d_sigma_21(z), dmax)):.1f},{fyz(z):.1f}"
                   for z in [i/20.0 for i in range(0, int(ZP*20)+1)])
    c.parts.append(f'<polyline points="{pts}" fill="none" stroke="{C["accent"]}" stroke-width="3.4"/>')
    vline_px(c, fxd(DSIG), cy0, cy1, C["load"], 3.4)
    c.text_px(fxd(DSIG)+8, fyz(8.6), "大面積：垂直線", 11.5, C["load"], "start", weight="700")
    c.text_px(fxd(96), fyz(1.9), "2:1 法：急速衰減", 11.5, C["accent"], "start", weight="700")
    c.dot(PX(c, fxd(DSIG_21), fyz(ZC)), 5.6, fill=C["accent"], stroke="#FFFFFF", w=2.0)
    c.text_px(fxd(DSIG_21)+12, fyz(ZC)+14, f"{DSIG_21:.1f} kPa", 11, C["accent"], "start", weight="700")
    c.rect_px(26, 380, W3-52, 66, C["fill_t"], 9, C["load"], 1.8)
    c.text_px(W3/2, 400, "同為外加載重，黏土中點的 Δσ 差", 12, C["muted"])
    c.text_px(W3/2, 426, f"{DSIG_21:.1f} kPa　vs　{DSIG:.0f} kPa", 16, C["load"], weight="700")
    c.text_px(W3/2, 462, "判錯載重型式 ⇒ 沉陷量錯一個數量級", 12, C["accent"], weight="700")

    compose([a, b, c],
            title="應力增量 Δσ：先判斷是「有限基礎」還是「大面積」",
            sub="這一步判錯，Case A/B/C 與沉陷量全部跟著錯",
            note="2:1 法的 z 從基礎底面起算（不是地表），這是最常見的計算失誤。"
                 "預壓覆土、大範圍回填、地下水位下降都屬於大面積載重，全深度不折減。",
            path=f"{OUT}/sm13-fig-10-delta-sigma.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 11　排水路徑 Hdr：判錯差 4 倍  ★
# ═══════════════════════════════════════════════════════════════
def fig11():
    def panel(cv, title, sub, double):
        cv.panel(title, sub)
        top, bot = 132, 380
        x0, x1 = 60, PW-60
        # 上覆砂層
        cv.rect_px(x0, top-40, x1-x0, 40, "rgba(180,83,9,0.16)", 0, C["member"], 1.6)
        cv.text_px(x0+10, top-20, "透水砂層", 12, C["accent"], "start", weight="700")
        # 黏土層
        cv.rect_px(x0, top, x1-x0, bot-top, "rgba(46,125,111,0.16)", 0, C["member"], 1.8)
        cv.text_px(x0+50, (top+bot)/2, f"黏土 H = {H_CLAY:.0f} m", 12.5, C["bmd"], "start", weight="700")
        # 下層
        if double:
            cv.rect_px(x0, bot, x1-x0, 40, "rgba(180,83,9,0.16)", 0, C["member"], 1.6)
            cv.text_px(x0+10, bot+20, "透水砂層", 12, C["accent"], "start", weight="700")
        else:
            cv.rect_px(x0, bot, x1-x0, 40, "rgba(63,74,90,0.45)", 0, C["member"], 1.6)
            cv.text_px(x0+10, bot+20, "不透水岩盤", 12, "#FFFFFF", "start", weight="700")
        # 排水箭頭
        for k in range(5):
            xx = x0 + 60 + k*(x1-x0-120)/4
            vup(cv, xx, top+6, top-30, C["compr"], 2.4)
            if double:
                vdown(cv, xx, bot-6, bot+30, C["compr"], 2.4)
        # 等時線（孔隙水壓分佈）
        import math as _m
        umax = (x1-x0)*0.30
        xc = (x0+x1)/2 + 30
        for Tv, op in ((0.05, 0.35), (0.20, 0.55), (0.50, 0.80)):
            pts = []
            for i in range(41):
                zz = i/40.0
                s = 0.0
                for m in range(0, 12):
                    M = _m.pi/2*(2*m+1)
                    zz2 = 2.0*zz if double else zz
                    s += 2.0/M*_m.sin(M*zz2)*_m.exp(-M*M*Tv)
                pts.append((xc - umax/2 + s*umax, top + (bot-top)*zz))
            s2 = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
            cv.parts.append(f'<polyline points="{s2}" fill="none" stroke="{C["compr"]}" '
                            f'stroke-width="2.6" opacity="{op}"/>')
        cv.text_px(xc + umax*0.62, top+26, "孔隙水壓", 11, C["compr"], "start", weight="700")
        cv.text_px(xc + umax*0.62, top+44, "消散過程", 11, C["compr"], "start")
        # Hdr 標示
        hdr = HDR_DOUBLE if double else HDR_SINGLE
        hy = bot if not double else (top+bot)/2
        vline_px(cv, x1-26, top, hy, C["load"], 2.8)
        for yy in (top, hy):
            hline_px(cv, x1-34, x1-18, yy, C["load"], 2.2)
        cv.text_px(x1-38, (top+hy)/2, f"H_{{dr}} = {hdr:.0f} m", 12.5, C["load"], "end", weight="700")
        return top, bot

    a = pxcv(PW, PH)
    panel(a, "雙面排水", "上、下都是透水層 ⇒ H_{dr} = H / 2", True)
    a.rect_px(46, 440, PW-92, 122, C["fill_m"], 10, C["bmd"], 1.8)
    a.math_px(PW/2, 466, f"H_{{dr}} = H/2 = {HDR_DOUBLE:.0f} m", 17, C["bmd"], weight="700")
    a.text_px(PW/2, 498, f"U = 90% 所需時間", 12, C["muted"])
    a.text_px(PW/2, 524, f"t = {T90_DOUBLE:.2f} 年", 20, C["bmd"], weight="700")
    a.text_px(PW/2, 550, f"（c_{{v}} = {CV:.2f} m^{{2}}/yr, T_{{v}} = 0.848）", 11, C["muted"])
    a.text_px(PW/2, PH-16, "水只要走一半厚度就能逃出去", 12, C["text"], weight="700")

    b = pxcv(PW, PH)
    panel(b, "單面排水", "一側為岩盤或不透水層 ⇒ H_{dr} = H", False)
    b.rect_px(46, 440, PW-92, 122, C["fill_t"], 10, C["load"], 1.8)
    b.math_px(PW/2, 466, f"H_{{dr}} = H = {HDR_SINGLE:.0f} m", 17, C["load"], weight="700")
    b.text_px(PW/2, 498, f"U = 90% 所需時間", 12, C["muted"])
    b.text_px(PW/2, 524, f"t = {T90_SINGLE:.2f} 年", 20, C["load"], weight="700")
    b.text_px(PW/2, 550, f"整整是雙面排水的 {T_RATIO:.0f} 倍", 12.5, C["load"], weight="700")
    b.text_px(PW/2, PH-16, "水必須走完整層厚度才能逃出去", 12, C["text"], weight="700")

    compose([a, b],
            title="最貴的一句話：排水路徑 Hdr 必帶平方",
            sub="Tv = cv·t / Hdr²　—— 判錯單面／雙面，時間直接差 4 倍",
            note="判斷只看黏土層上下邊界：兩側都透水就是雙面，一側是岩盤或不透水層就是單面。"
                 "實驗室試體多為雙面排水 —— 換算現場時，先用實驗室的 Hdr 反推 cv，再代現場的 Hdr。",
            path=f"{OUT}/sm13-fig-11-drainage-path.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 12　U ~ Tv 關係與 60% 切換
# ═══════════════════════════════════════════════════════════════
def fig12():
    xr, yr = (0.0, 1.2), (0.0, 100.0)
    a, fx, fy, P = plotbox(PW, PH, xr, yr, (96, PW-56, 150, 470))
    a.panel("壓密度 U 與時間因數 T_{v}", "60% 是兩條近似式的接點")
    def ay(U): return PH - fy(U)
    a.arrow((fx(0), fy(0)), (fx(xr[1])+16, fy(0)), C["muted"], 1.8, 9)
    a.arrow((fx(0), fy(0)), (fx(0), fy(yr[1])+16), C["muted"], 1.8, 9)
    a.text_px(fx(xr[1])+24, ay(0)+4, "T_{v}", 13, C["muted"], "start")
    a.text_px(fx(0), ay(yr[1])-30, "U (%)", 13, C["muted"])
    for tv in (0.2, 0.4, 0.6, 0.8, 1.0, 1.2):
        vline_px(a, fx(tv), ay(0), ay(yr[1]), C["border"], 1.0)
        a.text_px(fx(tv), ay(0)+18, f"{tv:.1f}", 11.5, C["muted"])
    for uv in (20, 40, 60, 80, 100):
        hline_px(a, fx(0), fx(xr[1]), ay(uv), C["border"], 1.0)
        a.text_px(fx(0)-10, ay(uv), f"{uv}", 11.5, C["muted"], "end")
    # 兩段曲線
    seg1 = [(Tv_of_U(u/1000.0), u/10.0) for u in range(1, 600)]
    seg2 = [(Tv_of_U(u/1000.0), u/10.0) for u in range(600, 990)]
    a.poly([P(t, u) for t, u in seg1 if t <= xr[1]], C["compr"], 4.0)
    a.poly([P(t, u) for t, u in seg2 if t <= xr[1]], C["load"], 4.0)
    a.dot(P(TV60_A, 60.0), 6.6, fill=C["accent"], stroke="#FFFFFF", w=2.4)
    vline_px(a, fx(TV60_A), ay(60), ay(0), C["accent"], 1.8, "5 4")
    hline_px(a, fx(0), fx(TV60_A), ay(60), C["accent"], 1.8, "5 4")
    a.text_px(fx(0.305), ay(53), f"U = 60%　T_{{v}} = {TV60_A:.3f}",
              12.5, C["accent"], "start", weight="700")
    a.rect_px(186, 298, 302, 96, "#FFFFFF", 8, C["border"], 1.3)
    a.text_px(202, 324, "U ＜ 60%", 13, C["compr"], "start", weight="700")
    a.math_px(300, 324, "T_{v} = (π/4) U^{2}", 14, C["compr"], "start")
    a.text_px(202, 370, "U ≥ 60%", 13, C["load"], "start", weight="700")
    a.math_px(300, 370, "T_{v} = 1.781 - 0.933 log(100-U)", 12, C["load"], "start")
    # 90% 與 100% 標示
    a.dot(P(Tv_of_U(0.90), 90.0), 6.0, fill=C["load"], stroke="#FFFFFF", w=2.2)
    a.text_px(fx(Tv_of_U(0.90))+8, ay(90)+16, f"U = 90%　T_{{v}} = {Tv_of_U(0.90):.3f}",
              11.5, C["load"], "start", weight="700")
    hline_px(a, fx(0), fx(xr[1]), ay(100), C["muted"], 1.6, "6 5")
    a.text_px(fx(xr[1]), ay(100)-14, "U = 100% 需要無限久", 11.5, C["muted"], "end", weight="700")
    a.text_px(PW/2, PH-92, f"兩式在 60% 幾乎接上：{TV60_A:.3f} vs {TV60_B:.3f}",
              12.5, C["accent"], weight="700")
    a.text_px(PW/2, PH-64, "考場切換規則", 13, C["muted"], weight="700")
    a.text_px(PW/2, PH-38, "已知 U 求 t ⇒ 先看 U 有沒有過 60%", 13, C["text"], weight="700")
    a.text_px(PW/2, PH-14, "已知 t 求 U ⇒ 先算 T_{v}，再看有沒有過 0.286", 13, C["text"], weight="700")

    b = pxcv(PW, PH)
    b.panel("這條曲線的形狀在說什麼", "壓密末期為什麼「等不起」")
    rows = [(50, HDR_SINGLE), (60, HDR_SINGLE), (70, HDR_SINGLE),
            (80, HDR_SINGLE), (90, HDR_SINGLE), (95, HDR_SINGLE)]
    b.rect_px(56, 112, PW-112, 34, C["fill_m"], 6, C["bmd"], 1.4)
    for x, s in ((136, "U (%)"), (260, "T_{v}"), (396, "t (年)")):
        b.text_px(x, 129, s, 12.5, C["bmd"], weight="700")
    prev_t = None
    for i, (u, hdr) in enumerate(rows):
        y = 152 + i*40
        tv = Tv_of_U(u/100.0)
        tt = tv*hdr**2/CV
        b.rect_px(56, y, PW-112, 34, C["panel"] if i % 2 == 0 else "#FFFFFF", 5, C["border"], 1.1)
        b.text_px(136, y+17, f"{u}", 13, C["text"], weight="700")
        b.text_px(260, y+17, f"{tv:.3f}", 12.5, C["muted"])
        b.text_px(396, y+17, f"{tt:.2f}", 13, C["load"], weight="700")
        if prev_t is not None:
            b.text_px(PW-64, y+17, f"+{tt-prev_t:.2f}", 11.5, C["accent"], "end")
        prev_t = tt
    b.text_px(PW-64, 129, "增量", 12, C["bmd"], "end", weight="700")
    b.text_px(PW/2, 404, f"（單面排水 H_{{dr}} = {HDR_SINGLE:.0f} m, c_{{v}} = {CV:.2f} m^{{2}}/yr）",
              11.5, C["muted"])
    b.rect_px(46, 428, PW-92, 140, C["fill_t"], 10, C["load"], 1.8)
    b.text_px(PW/2, 454, "從 90% 走到 95%，比從 0 走到 50% 還久", 14, C["load"], weight="700")
    b.text_px(PW/2, 484, "因為末期孔隙水壓梯度已經很小，滲流極慢", 12, C["text"])
    b.text_px(PW/2, 512, "所以工程上不會等 U = 100%", 12.5, C["muted"], weight="700")
    b.text_px(PW/2, 538, "而是用「超載預壓」把目標 U 拉低", 13.5, C["accent"], weight="700")

    compose([a, b],
            title="壓密速率：U 與 Tv 的兩段近似式",
            sub="60% 是分界，過了就要換公式",
            note="U ＜ 60% 走拋物線近似 Tv = (π/4)U²；U ≥ 60% 走對數近似。兩式在 60% 幾乎重合，"
                 "所以切換不會有跳階。注意 U 在式中是百分比或小數要一致，最常錯在這裡。",
            path=f"{OUT}/sm13-fig-12-u-tv.svg")


# ═══════════════════════════════════════════════════════════════
# 圖 13　超載預壓：把目標 U 降下來
# ═══════════════════════════════════════════════════════════════
def fig13():
    W, H = 1200, 560
    t_hi = 5.2
    s_hi = SCF*1.12
    cv, fx, fy, P = plotbox(W, H, (0, t_hi), (0, s_hi), (140, W-420, 96, 440))
    cv.rect_px(0, 0, W, H, "#FFFFFF", 0)
    def sy(s): return H - fy(s)
    cv.parts.append(f'<line x1="{fx(0):.1f}" y1="{sy(0):.1f}" x2="{fx(t_hi)+16:.1f}" '
                    f'y2="{sy(0):.1f}" stroke="{C["muted"]}" stroke-width="1.8"/>')
    cv.parts.append(f'<line x1="{fx(0):.1f}" y1="{sy(0):.1f}" x2="{fx(0):.1f}" '
                    f'y2="{sy(s_hi):.1f}" stroke="{C["muted"]}" stroke-width="1.8"/>')
    cv.text_px(fx(t_hi), sy(0)+40, "時間 t（年）", 13, C["muted"], "end")
    cv.text_px(fx(0)+4, sy(s_hi)-26, "沉陷量 S（mm）", 13, C["muted"], "start")
    for tv in (1, 2, 3, 4, 5):
        vline_px(cv, fx(tv), sy(0), sy(s_hi), C["border"], 1.0)
        cv.text_px(fx(tv), sy(0)+18, f"{tv}", 11.5, C["muted"])
    for sv in (50, 100, 150):
        hline_px(cv, fx(0), fx(t_hi), sy(sv), C["border"], 1.0)
        cv.text_px(fx(0)-10, sy(sv), f"{sv}", 11.5, C["muted"], "end")

    def U_of_t(t, Hdr=HDR_SINGLE):
        Tv = CV*t/Hdr**2
        if Tv <= 0: return 0.0
        U = math.sqrt(4*Tv/math.pi)
        if U < 0.60:
            return U
        return min(0.999, 1.0 - 10**((1.781 - Tv)/0.933)/100.0)

    ts = [i/200.0*t_hi for i in range(1, 201)]
    cv.poly([P(t, SC*U_of_t(t)) for t in ts], C["compr"], 4.0)
    cv.poly([P(t, SCF*U_of_t(t)) for t in ts], C["load"], 4.0)
    # 水平終值線
    hline_px(cv, fx(0), fx(t_hi), sy(SC), C["compr"], 1.8, "7 5")
    hline_px(cv, fx(0), fx(t_hi), sy(SCF), C["load"], 1.8, "7 5")
    cv.text_px(fx(t_hi), sy(SC)-14, f"設計載重最終沉陷 S_{{c}} = {SC:.1f} mm",
               12.5, C["compr"], "end", weight="700")
    cv.text_px(fx(t_hi), sy(SCF)-14, f"預壓載重最終沉陷 S_{{cf}} = {SCF:.1f} mm",
               12.5, C["load"], "end", weight="700")
    # 目標沉陷達成的兩個時間
    cv.dot(P(T_PRE, SC), 7.0, fill=C["accent"], stroke="#FFFFFF", w=2.4)
    vline_px(cv, fx(T_PRE), sy(SC), sy(0), C["accent"], 2.0, "5 4")
    cv.text_px(fx(T_PRE), sy(0)+38, f"t = {T_PRE:.2f} 年", 13, C["accent"], weight="700")
    cv.text_px(fx(T_PRE), sy(0)+58, "（預壓）", 11.5, C["accent"])
    t90 = T90_SINGLE
    cv.dot(P(t90, SC*0.90), 6.4, fill=C["compr"], stroke="#FFFFFF", w=2.2)
    vline_px(cv, fx(t90), sy(SC*0.90), sy(0), C["compr"], 2.0, "5 4")
    cv.text_px(fx(t90), sy(0)+38, f"t = {t90:.2f} 年", 13, C["compr"], weight="700")
    cv.text_px(fx(t90), sy(0)+58, "（不預壓，U = 90%）", 11.5, C["compr"])
    harrow(cv, fx(T_PRE)+6, fx(t90)-6, sy(SC*0.45), C["accent"], 2.6)
    cv.text_px((fx(T_PRE)+fx(t90))/2, sy(SC*0.45)-16,
               f"省下 {T_SAVE*100:.0f}% 的工期", 13.5, C["accent"], weight="700")

    # 右側說明
    xk = W-392
    cv.rect_px(xk, 84, 344, 118, C["fill_m"], 10, C["bmd"], 1.8)
    cv.text_px(xk+172, 110, "預壓工法沒有改變土", 14, C["bmd"], weight="700")
    cv.text_px(xk+172, 136, "c_{v} 沒變、H_{dr} 沒變、k 也沒變", 12, C["text"], weight="700")
    cv.text_px(xk+172, 166, "改變的只有「目標壓密度 U」", 13, C["accent"], weight="700")
    cv.text_px(xk+172, 188, "把終點線往前搬，不是把車開快", 11.5, C["muted"])
    steps = [("① 設計載重下的最終沉陷", f"S_{{c}} = {SC:.1f} mm（必須先消化掉的量）", C["compr"]),
             ("② 加大預壓載重", f"Δσ 由 {DSIG:.0f} 提高到 {DSIG_PRE:.0f} kPa "
              f"⇒ S_{{cf}} = {SCF:.1f} mm", C["load"]),
             ("③ 只需達到部分壓密度", f"U = S_{{c}} / S_{{cf}} = {SC:.1f}/{SCF:.1f} = "
              f"{U_REQ*100:.0f}%", C["accent"]),
             ("④ 卸載並施工", f"T_{{v}} = {Tv_of_U(U_REQ):.3f} ⇒ t = {T_PRE:.2f} 年", C["bmd"])]
    for i, (t1, t2, col) in enumerate(steps):
        y = 220 + i*84
        cv.rect_px(xk, y, 344, 70, C["panel"], 9, C["border"], 1.4)
        cv.rect_px(xk, y, 8, 70, col, 3)
        cv.text_px(xk+26, y+22, t1, 12.5, col, "start", weight="700")
        cv.text_px(xk+26, y+48, t2, 12, C["text"], "start")
    cv.text_px(460, H-18,
               "追問：要不要加排水砂樁？那才是真的改 H_{dr}（徑向排水），與超載是兩件事",
               12.5, C["muted"], weight="700")

    compose([cv],
            title="超載預壓：不是把土變快，而是把目標壓密度降下來",
            sub="施加更大的載重讓 Scf ＞ Sc，於是只要 U = Sc / Scf 就收工",
            note="壓密末期極為漫長（90% → 95% 比 0% → 50% 還久），所以工程上不等 100%。"
                 "超載預壓省下的正是這一段。若要同時改變排水路徑，那要靠排水砂樁或塑膠排水帶。",
            path=f"{OUT}/sm13-fig-13-preloading.svg")


if __name__ == "__main__":
    for fn in (fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10, fig11, fig12, fig13):
        fn()
        print("ok", fn.__name__)
    print(f"""
── 示範數值總表 ────────────────────────────────
夯實  標準 E = {PROCTOR['std']['E']:.0f} kJ/m3 , 修正 E = {PROCTOR['mod']['E']:.0f} kJ/m3 (x{E_RATIO:.2f})
      Dr = {DR_FIELD*100:.1f}%  <->  RC = {RC_FIELD*100:.1f}%  ; RC(Dr=0) = {RC_AT_DR0*100:.1f}%
土方  Ws = {WS_TOTAL:,.0f} kN , V借 = {V_BORROW:,.0f} m3 (脹縮比 {SHRINK:.3f}) , 加水 {W_ADD_M3:,.0f} m3
壓密  p0' = {P0:.2f} kPa , pc' = {PC:.0f} , OCR = {OCR:.3f} , pf' = {PF:.2f}
      Sc(Case C) = {SC:.2f} mm  ( 全Cr {SC_CR:.2f} < {SC:.2f} < 全Cc {SC_CC:.2f} )
      2:1 法中點 Δσ = {DSIG_21:.2f} kPa  vs 大面積 {DSIG:.0f} kPa
速率  雙面 t90 = {T90_DOUBLE:.3f} yr , 單面 t90 = {T90_SINGLE:.3f} yr (x{T_RATIO:.1f})
預壓  Scf = {SCF:.2f} mm , U需求 = {U_REQ*100:.1f}% , t = {T_PRE:.2f} yr (省 {T_SAVE*100:.0f}%)
""")
