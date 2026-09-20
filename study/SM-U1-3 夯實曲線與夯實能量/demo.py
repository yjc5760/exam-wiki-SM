"""
demo.py — 示範案例：全篇唯一的數字來源（圖、表、公式頁都從這裡取值）
改這裡任何一個輸入，重跑 gen_figs.py / build_deck.js，全篇數字一起變。
"""
import numpy as np
from scipy.interpolate import PchipInterpolator

GS = 2.70          # 土粒比重
GW = 9.81          # kN/m^3
V_MOLD = 944.0     # cm^3（標準、修正共用 944 cm^3 夯模）

# ── 試驗數據：以「濕土質量 g」為原始觀測值（題目給的就是這個） ──
# 由目標 γd 反推質量後四捨五入到 0.1 g，之後一切由質量重算，確保可對帳
_STD_TARGET = [(10.0, 16.20), (13.0, 17.05), (16.0, 17.50), (19.0, 17.05), (22.0, 16.20)]
_MOD_TARGET = [(8.5, 17.90), (10.5, 18.60), (12.5, 19.00), (14.5, 18.60), (16.5, 17.85)]


def _mass(w_pct, gd):
    rho = gd * (1 + w_pct / 100) / GW      # g/cm^3
    return round(rho * V_MOLD, 1)


def _rows(target):
    rows = []
    for w, gd_t in target:
        M = _mass(w, gd_t)
        gam = M * GW / V_MOLD                # kN/m^3
        gd = gam / (1 + w / 100)
        e = GS * GW / gd - 1
        S = (w / 100) * GS / e
        zav = zav_gd(w)
        rows.append(dict(w=w, M=M, gam=gam, gd=gd, e=e, S=S, zav=zav))
    return rows


def zav_gd(w_pct):
    return GS * GW / (1 + (w_pct / 100) * GS)


def s_line(w_pct, S):
    return GS * GW / (1 + (w_pct / 100) * GS / S)


STD = _rows(_STD_TARGET)
MOD = _rows(_MOD_TARGET)


def curve(rows):
    x = np.array([r["w"] for r in rows]); y = np.array([r["gd"] for r in rows])
    return PchipInterpolator(x, y)


def peak(rows):
    f = curve(rows)
    ws = np.linspace(rows[0]["w"], rows[-1]["w"], 4001)
    g = f(ws); i = int(np.argmax(g))
    return float(ws[i]), float(g[i])


def check_below_zav(rows, margin=0.05):
    """鐵則：夯實曲線不得碰到 ZAVC。這個 assert 就是圖二原圖那個錯的攔截器。"""
    f = curve(rows)
    ws = np.linspace(rows[0]["w"], rows[-1]["w"], 2001)
    gap = zav_gd(ws) - f(ws)
    assert gap.min() > margin, f"曲線穿越 ZAVC！最小間距 {gap.min():.3f} @ w={ws[gap.argmin()]:.2f}%"
    return float(gap.min())


# ── 夯實能量 ──
def energy(W_N, h_m, N, L, V_cm3=V_MOLD):
    return W_N * h_m * N * L / (V_cm3 * 1e-6) / 1000.0     # kJ/m^3


E_STD = energy(24.5, 0.305, 25, 3)
E_MOD = energy(44.5, 0.457, 25, 5)

W_OPT_S, GD_MAX_S = peak(STD)
W_OPT_M, GD_MAX_M = peak(MOD)
S_OPT_S = (W_OPT_S / 100) * GS / (GS * GW / GD_MAX_S - 1)
S_OPT_M = (W_OPT_M / 100) * GS / (GS * GW / GD_MAX_M - 1)

# ── 三相：單位固體體積 Vs = 1 ──
GD_LOOSE = 14.0                      # 夯實前鬆散狀態（示範值）
W_PHASE = W_OPT_S                    # 同一含水量 16%
E_LOOSE = GS * GW / GD_LOOSE - 1
E_COMP = GS * GW / GD_MAX_S - 1
E_ZAV = (W_PHASE / 100) * GS         # Va = 0 的極限

# ── 算錯示範：忘了除以 (1+w) ──
BAD_ROW = STD[3]                     # w = 19%
BAD_GD = BAD_ROW["gam"]              # 誤把 γ 當 γd

# ── 現地檢測：相對夯實度 ──
GD_FIELD = 16.80
RC_FIELD = GD_FIELD / GD_MAX_S * 100

if __name__ == "__main__":
    for name, rows in (("標準", STD), ("修正", MOD)):
        print(name)
        for r in rows:
            print(f"  w={r['w']:5.1f}  M={r['M']:7.1f} g  γ={r['gam']:6.2f}  γd={r['gd']:6.2f}  "
                  f"e={r['e']:.3f}  S={r['S']*100:5.1f}%  ZAV={r['zav']:6.2f}")
        print("  最小ZAV間距", check_below_zav(rows))
    print(f"std peak w={W_OPT_S:.2f} gd={GD_MAX_S:.3f} S={S_OPT_S:.3f}")
    print(f"mod peak w={W_OPT_M:.2f} gd={GD_MAX_M:.3f} S={S_OPT_M:.3f}")
    print(f"E std={E_STD:.1f} mod={E_MOD:.1f} ratio={E_MOD/E_STD:.3f}")
    print(f"e loose={E_LOOSE:.3f} comp={E_COMP:.3f} zav={E_ZAV:.3f} zav_gd={zav_gd(W_PHASE):.2f}")
    print(f"bad gd={BAD_GD:.2f} vs zav {zav_gd(BAD_ROW['w']):.2f}")
    print(f"RC={RC_FIELD:.1f}%")
