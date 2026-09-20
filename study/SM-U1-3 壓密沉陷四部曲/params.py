# ── 示範案例：全篇唯一數據來源（所有圖與簡報數字皆由此算出）──
from math import log10
GW = 9.81
LAYERS = [  # (頂, 底, γ 或 γsat, 名稱)
    (0.0, 2.0, 18.0, "砂（水位以上）"),
    (2.0, 6.0, 19.5, "砂（飽和）"),
    (6.0, 10.0, 17.5, "黏土"),
]
Z_WT = 2.0
CLAY_TOP, CLAY_BOT = 6.0, 10.0
H = CLAY_BOT - CLAY_TOP            # 4 m
Z_MID = (CLAY_TOP + CLAY_BOT) / 2  # 8 m
E0, CC, CR = 1.05, 0.320, 0.045
PC = 130.0

def sigma(z):
    s = 0.0
    for t, b, g, _ in LAYERS:
        if z <= t: break
        s += g * (min(z, b) - t)
    return s
def u(z): return max(0.0, z - Z_WT) * GW
def sig_eff(z): return sigma(z) - u(z)

P0 = sig_eff(Z_MID)
TERMS = [18.0*2, (19.5-GW)*4, (17.5-GW)*2]   # 36 + 38.76 + 15.38

# 載重情境
DS_AREA = 80.0                       # 大面積預壓覆土
Q, B, L, DF = 1200.0, 2.0, 3.0, 1.5  # 矩形基腳，基礎底面在地表下 1.5 m
Z_FROM_BASE = Z_MID - DF             # 6.5 m
def ds21(z): return Q / ((B + z) * (L + z))
DS_FOOT = ds21(Z_FROM_BASE)
DS_FOOT_WRONG = ds21(Z_MID)          # 誤用地表起算 z = 8 m

K = H * 1000 / (1 + E0)              # mm
def settle(p0, pf, pc=PC, cc=CC, cr=CR):
    if pf <= pc: return cr*K*log10(pf/p0), 0.0
    if p0 >= pc: return 0.0, cc*K*log10(pf/p0)
    return cr*K*log10(pc/p0), cc*K*log10(pf/pc)

PF = P0 + DS_AREA
S_C_r, S_C_c = settle(P0, PF)
S_C = S_C_r + S_C_c
S_ALL_CR = CR*K*log10(PF/P0)
S_ALL_CC = CC*K*log10(PF/P0)
PF_FOOT = P0 + DS_FOOT
S_B = sum(settle(P0, PF_FOOT))
OCR = PC / P0
DE_R = CR*log10(PC/P0); DE_C = CC*log10(PF/PC)

def sublayer(n):
    """黏土分 n 層，各層取其中點；pc' 取定值 130（示範用）"""
    tot = 0.0; h = H/n
    for i in range(n):
        zm = CLAY_TOP + h*(i+0.5)
        p0 = sig_eff(zm); r, c = settle(p0, p0+DS_AREA)
        tot += (r+c) * h / H
    return tot

if __name__ == "__main__":
    print(f"p0'={P0:.2f} terms={[round(t,2) for t in TERMS]}")
    print(f"clay top/bot σ' = {sig_eff(6):.2f} / {sig_eff(10):.2f}")
    print(f"Δσ foot={DS_FOOT:.2f} wrong={DS_FOOT_WRONG:.2f}  pf_foot={PF_FOOT:.2f} S_B={S_B:.2f}")
    print(f"pf={PF:.2f} OCR={OCR:.3f}  S_C={S_C_r:.2f}+{S_C_c:.2f}={S_C:.2f}  allCr={S_ALL_CR:.2f} allCc={S_ALL_CC:.2f}")
    print(f"Δe_r={DE_R:.4f} Δe_c={DE_C:.4f} check={(DE_R+DE_C)/(1+E0)*H*1000:.2f} K={K:.1f}")
    for n in (1,2,4,8,32): print(n, round(sublayer(n),2))
    print("NC case A:", round(sum(settle(P0,PF,pc=P0)),2))
