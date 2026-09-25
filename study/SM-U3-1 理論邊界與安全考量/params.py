# ── 拼圖四 示範牆：全篇唯一數據來源（所有圖與簡報數字皆由此算出）──
import math, json
from wedge import ka_c, kp_c, ka_rs, trial
r = math.radians
H, G, PHI = 6.0, 18.0, 30.0          # 牆高、單位重、內摩擦角（c = 0）
DELTA = 20.0                          # Coulomb 牆背摩擦角（≈ 2/3 φ）
BETA = 15.0                           # 斜填土坡角
THETA = 10.0                          # 牆背傾角（Das 定義：填土壓在牆背上為正）
DF, DIGNORE = 1.5, 0.5                # 牆趾前埋深、忽略表層深度
RED = 0.5                             # 被動折減係數
half = 0.5*G*H*H                      # ½γH² = 324

KA_R = math.tan(r(45-PHI/2))**2       # 1/3
KP_R = math.tan(r(45+PHI/2))**2       # 3.0
PA_R = KA_R*half                      # 108
KA_C = ka_c(PHI, DELTA, 0, 0)         # 0.2973
PA_C = KA_C*half
PA_C_H, PA_C_V = PA_C*math.cos(r(DELTA)), PA_C*math.sin(r(DELTA))
KA_CT = ka_c(PHI, DELTA, THETA, 0)    # θ = 10°
KA_RS = ka_rs(PHI, BETA)              # 斜填土 Rankine
PA_RS = KA_RS*half
PA_RS_H, PA_RS_V = PA_RS*math.cos(r(BETA)), PA_RS*math.sin(r(BETA))
KA_C_B0 = ka_c(PHI, 0, 0, BETA)       # Coulomb δ=0 斜填土（力垂直牆背）
KA_C_DB = ka_c(PHI, BETA, 0, BETA)    # Coulomb δ=β → 等於 Rankine 斜填土
KA_RS_LIM = math.cos(r(PHI))          # β = φ 時的極限值
_, RHO_R, *_ = trial(H, G, PHI, 0, 0, 0)
_, RHO_C, *_ = trial(H, G, PHI, DELTA, 0, 0)

KP_R40 = math.tan(r(45+40/2))**2
KA_R40 = math.tan(r(45-40/2))**2
KP_C = kp_c(PHI, DELTA, 0, 0)         # 6.105
KP_C_PHI = kp_c(PHI, PHI, 0, 0)
PP_FULL = 0.5*KP_R*G*DF**2            # 60.75
PP_C = 0.5*KP_C*G*DF**2
PP_40 = 0.5*KP_R40*G*DF**2
PP_IGN = 0.5*KP_R*G*(DF-DIGNORE)**2   # 27.0
PP_DES = PP_IGN*RED                   # 13.5
DA_ACT = 0.001*H*1000                 # 主動所需位移 mm
DP_LO, DP_HI = 0.02*DF*1000, 0.05*DF*1000

N = {k: v for k, v in globals().items() if k.isupper() and isinstance(v, (int, float))}
if __name__ == "__main__":
    for k, v in N.items(): print(f"{k:10s} {v:.4f}")
    print("Coulomb 水平分力較 Rankine 少 %.1f%%" % ((1-PA_C_H/PA_R)*100))
    print("斜填土 Pa +%.1f%%, 水平 +%.1f%%" % ((PA_RS/PA_R-1)*100, (PA_RS_H/PA_R-1)*100))
    print("Kp 30→40 +%.1f%%, Ka 差 %.3f" % ((KP_R40/KP_R-1)*100, KA_R-KA_R40))
    json.dump(N, open("nums.json", "w"), indent=1)
