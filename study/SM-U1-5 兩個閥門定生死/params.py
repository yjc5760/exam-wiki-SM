# ── SM-U1-5 拼圖二：兩個閥門定生死 ── 全篇唯一數據來源
import math, json
r, d = math.radians, math.degrees
kp = lambda phi: math.tan(r(45 + phi/2))**2
sn = lambda phi: math.sin(r(phi))

# 示範黏土 A（沿用拼圖一）：NC、c'=0、φ'=30°、壓密後 p'0 = σ3 = 100 kPa、A_f = 0.75
PHI, S3, AF = 30.0, 100.0, 0.75
KP = kp(PHI)                                   # 3.0

def cu(s3, A, phi=PHI):
    """CU 軸壓（AC）：σ3' = s3 − AΔ，σ1' = s3 + (1−A)Δ，且 Δ = (σ1'+σ3') sinφ'"""
    D = 2*s3*sn(phi)/(1 - (1 - 2*A)*sn(phi))
    return D, A*D                              # Δσ_d, u_f

# ① CD（兩閥門都開）：u = 0
S1_CD = KP*S3; DSD_CD = S1_CD - S3; C_CD, R_CD = (S1_CD + S3)/2, DSD_CD/2
# ② CU（壓密開、剪切關）
DSD, UF = cu(S3, AF)                           # 80, 60
S1 = S3 + DSD; S3E, S1E = S3 - UF, S1 - UF     # 180；40、120
C_T, C_E, R = (S1 + S3)/2, (S1E + S3E)/2, DSD/2
PHI_CU = d(math.asin(DSD/(S1 + S3)))           # 16.6°
SIN_E = (S1E - S3E)/(S1E + S3E)                # 0.5
AF_BACK = UF/DSD
RATIO_CU = PHI_CU/PHI
# ③ UU（兩閥門都關）：試體有效應力鎖在 100，換三種室壓
SU = R                                         # 40
QU = 2*SU                                      # 80（UC：σ3 = 0）
UU_S3 = [100.0, 200.0, 300.0]
UU_U = [s - S3E for s in UU_S3]                # 破壞時 u：60、160、260
UU_U1, UU_U2, UU_U3 = UU_U
# Skempton B：不飽和 B = 0.8 → 室壓增量 100 只有 80 進水
DS3_B, B_UNSAT = 100.0, 0.8
DU_B = B_UNSAT*DS3_B; DSE_B = DS3_B - DU_B
# NC 比例法：σ3 = 200
S3_2 = 200.0; DSD_2, UF_2 = cu(S3_2, AF)       # 160、120
# 重過壓密（示意，c' 取 0 簡化）：A_f = −0.2
AF_OC = -0.2; DSD_OC, UF_OC = cu(S3, AF_OC)
S3E_OC, S1E_OC = S3 - UF_OC, S3 + DSD_OC - UF_OC
PHI_CU_OC = d(math.asin(DSD_OC/(2*S3 + DSD_OC)))
# S_u / σ'v0：A_f = 1 捷徑 vs 一般式
SUR_A1 = sn(PHI)/(1 + sn(PHI))                 # 0.333
SUR_GEN = sn(PHI)/(1 + (2*AF - 1)*sn(PHI))     # 0.400
S3E_A1 = S3*(1 - sn(PHI))/(1 + sn(PHI))        # 33.3（A_f=1 時破壞 σ3'）
SU_A1 = SUR_A1*S3                              # 33.3
# 深度剖面：γ' = 8 kN/m³、地下水位在地表
GAM = 8.0; ZS = [0, 5, 10, 15, 20]
SV = [GAM*z for z in ZS]; SU_Z = [SUR_A1*s for s in SV]
SV10, SU10 = GAM*10, SUR_A1*GAM*10
# 破壞面
TH = 45 + PHI/2; TH_WRONG = 45 + PHI_CU/2
# 考古題引用（SM-2013-3，拼圖一已用）
PHI_CU_AC13, PHI_CU_LE13 = 19.23, 31.59

N = {k: v for k, v in globals().items() if k.isupper() and isinstance(v, (int, float))}
if __name__ == "__main__":
    for k, v in N.items(): print(f"{k:12s} {v:.4f}")
    assert abs(DSD - 80) < 1e-9 and abs(UF - 60) < 1e-9 and abs(SIN_E - 0.5) < 1e-12
    assert abs(SU/S3 - SUR_GEN) < 1e-12 and 0.5 <= AF_BACK <= 1.0 and SUR_A1 < 0.5
    D1, U1 = cu(S3, 1.0); assert abs(D1/2 - SU_A1) < 1e-9 and abs(S3 + D1 - U1 - S3) < 1e-9  # σ1f' = σv0'
    assert abs(DSD_2/S3_2 - DSD/S3) < 1e-12 and abs(UF_2/S3_2 - UF/S3) < 1e-12
    assert abs((S1E_OC - S3E_OC)/(S1E_OC + S3E_OC) - 0.5) < 1e-12
    json.dump({k: round(v, 4) for k, v in N.items()}, open("nums.json", "w"), indent=1)
