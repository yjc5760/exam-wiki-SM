# ── SM-U1-5 拼圖三：一張 Mohr 圓走天下 ── 全篇唯一數據來源
import math, json
r, d = math.radians, math.degrees
sn, cs, tn = (lambda a: math.sin(r(a))), (lambda a: math.cos(r(a))), (lambda a: math.tan(r(a)))

# 示範題 [SM-2024-1] CD：σ3' = 100、Δσd = 240、c' = 25
S3, DSD, CC = 100.0, 240.0, 25.0
S1 = S3 + DSD                                   # 340
C, R = (S1 + S3)/2, (S1 - S3)/2                 # 220、120
# 萬能式：S1 = S3·y² + 2c'·y，y = √Kp → S3 y² + 2c' y − S1 = 0
qa, qb, qc = S3, 2*CC, -S1                      # 100y² + 50y − 340 = 0（÷10 → 10y² + 5y − 34）
Y = (-qb + math.sqrt(qb*qb - 4*qa*qc))/(2*qa)  # 1.6108
Y_NEG = (-qb - math.sqrt(qb*qb - 4*qa*qc))/(2*qa)
KP = Y*Y
TH = d(math.atan(Y))                            # θ = 45 + φ'/2 = arctan √Kp
PHI = 2*(TH - 45)                               # 26.34°
SF = C - R*sn(PHI)                              # 破壞面正向應力
TF = R*cs(PHI)                                  # 破壞面剪應力
TF_CHK = CC + SF*tn(PHI)                        # 包絡線驗算
R_CHK = C*sn(PHI) + CC*cs(PHI)                  # 公式② 驗算
A0 = CC/tn(PHI)                                 # c' cotφ'：包絡線與 σ 軸交點在 −A0
HYP = C + A0                                    # 直角三角形斜邊
# 破壞面點也可用 2θ 直接算
SF_2T, TF_2T = C + R*cs(2*TH), R*sn(2*TH)
# 錯誤示範：Δσd 當成 σ1
S1_WRONG = DSD; C_WRONG, R_WRONG = (S1_WRONG + S3)/2, (S1_WRONG - S3)/2
# 陷阱：誤把 Δσd 當 σ1 再用萬能式反推 φ'
_yw = (-2*CC + math.sqrt(4*CC*CC + 4*S3*S1_WRONG))/(2*S3)
PHI_TRAP = 2*(d(math.atan(_yw)) - 45)
# 技巧對照：φ' 先取整 26° 再轉回 Kp
PHI_RND = 26.0; KP_RND = tn(45 + PHI_RND/2)**2
S1_RND = S3*KP_RND + 2*CC*math.sqrt(KP_RND)
# 三軸加載動畫用：Δσd 四個階段（最後一個 = 破壞）
STAGES = [0.0, 80.0, 160.0, DSD]
# 任意平面示例：θ = 30°
TH_EX = 30.0
SX_EX, TX_EX = C + R*cs(2*TH_EX), R*sn(2*TH_EX)
# 黃金鐵律示例（沿用拼圖二黏土 A：φ' = 30°、φcu = 16.6°）
PHI_A, PHI_CU_A = 30.0, d(math.asin(80/280))
TH_A, TH_WRONG_A = 45 + PHI_A/2, 45 + PHI_CU_A/2
# NC 公式③ 示例（拼圖二黏土 A CD：σ3' = 100 → σ1' = 300）
NC_S3, NC_S1 = 100.0, 300.0
NC_SIN = (NC_S1 - NC_S3)/(NC_S1 + NC_S3)
NC_PHI = d(math.asin(NC_SIN))
# 若示範題誤用公式③（忽略 c'）
PHI_NC_WRONG = d(math.asin(R/C))

N = {k: v for k, v in globals().items() if k.isupper() and isinstance(v, (int, float))}
if __name__ == "__main__":
    for k, v in N.items(): print(f"{k:12s} {v:.4f}")
    assert abs(10*Y*Y + 5*Y - 34) < 1e-9
    assert abs(S3*KP + 2*CC*Y - S1) < 1e-9
    assert abs(TF_CHK - TF) < 1e-9 and abs(R_CHK - R) < 1e-9
    assert abs(SF_2T - SF) < 1e-9 and abs(TF_2T - TF) < 1e-9
    assert abs(NC_PHI - 30) < 1e-9
    json.dump({k: round(v, 4) for k, v in N.items()}, open("nums.json", "w"), indent=1)
