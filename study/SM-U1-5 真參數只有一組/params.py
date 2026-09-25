# ── SM-U1-5 拼圖一：真參數只有一組 ── 全篇唯一數據來源
import math, json
r, d = math.radians, math.degrees
kp = lambda phi: math.tan(r(45 + phi/2))**2

# 示範土 A：NC 黏土（c' = 0、φ' = 30°），p'0 = σ3 = 100 kPa，A_f = 0.75
PHI_A, S3 = 30.0, 100.0
KP_A = kp(PHI_A)                              # 3.0
AF = 0.75
# CU 軸壓（AC）：u_f = A_f·Δσ_d，σ3' = S3 − u_f，σ1' = K_p σ3'
UF_AC = AF*2*S3/(1 + 2*AF) if abs(KP_A-3) < 1e-9 else None   # Δσd = 2σ3' → u = A·2(S3−u)
S3E_AC = S3 - UF_AC; S1E_AC = KP_A*S3E_AC
DSD_AC = S1E_AC - S3E_AC
S1_AC = S3 + DSD_AC
PHI_CU_AC = d(math.asin(DSD_AC/(S1_AC + S3)))
# CD：σ3' = 100 不變
S1_CD = KP_A*S3; DSD_CD = S1_CD - S3
# UU（同一 p'0 的試體）：s_u = Δσd/2 與圍壓無關
SU = DSD_AC/2
# CU 側向伸張（LE）：σ_a = 100 不動（變成 σ1），側向 σ3 降 Δ；Δu = Δσ3 + A(Δσ1 − Δσ3) = −(1−A)Δ
#   σ3' = 100 − Δ + (1−A)Δ = 100 − AΔ；σ1' = 100 + (1−A)Δ；σ1' = 3σ3'
DL = (KP_A*S3 - S3)/((1 - AF) + KP_A*AF)
UF_LE = -(1 - AF)*DL
S1_LE, S3_LE = S3, S3 - DL
S1E_LE, S3E_LE = S1_LE - UF_LE, S3_LE - UF_LE
PHI_CU_LE = d(math.asin((S1_LE - S3_LE)/(S1_LE + S3_LE)))
TH_A = 45 + PHI_A/2                            # 60°
TH_WRONG = 45 + PHI_CU_AC/2                    # 誤用 φcu
# p–q（MIT：p = (σ1+σ3)/2，q = (σ1−σ3)/2）
P0 = S3
P_CD, Q_CD = (S1_CD + S3)/2, DSD_CD/2
P_AC, Q_AC = (S1_AC + S3)/2, DSD_AC/2
PE_AC = P_AC - UF_AC
P_LE, Q_LE = (S1_LE + S3_LE)/2, (S1_LE - S3_LE)/2
PE_LE = P_LE - UF_LE
ALPHA_A = d(math.atan(math.sin(r(PHI_A))))     # 26.57°

# 示範土 B：OC 黏土，兩組 CD（相減法）
S3A, S1A, S3B, S1B = 50.0, 170.0, 150.0, 420.0
KP_B = (S1A - S1B)/(S3A - S3B)                 # 2.5
SKP_B = math.sqrt(KP_B)
PHI_B = d(math.asin((KP_B - 1)/(KP_B + 1)))
C_B = (S1A - S3A*KP_B)/(2*SKP_B)
TH_B = 45 + PHI_B/2
CA, RA = (S1A + S3A)/2, (S1A - S3A)/2
CB, RB = (S1B + S3B)/2, (S1B - S3B)/2
R_CHECK = CA*math.sin(r(PHI_B)) + C_B*math.cos(r(PHI_B))
SFF = CA - RA*math.sin(r(PHI_B)); TFF = RA*math.cos(r(PHI_B))
TFF_MC = C_B + SFF*math.tan(r(PHI_B))
PHI_WRONG_A = d(math.asin(RA/CA)); PHI_WRONG_B = d(math.asin(RB/CB))
# 技巧 A：先轉角度（四捨五入到 1°）再轉回 K_p 的誤差
KP_ROUND = kp(round(PHI_B, 0))
C_ROUND = (S1A - S3A*KP_ROUND)/(2*math.sqrt(KP_ROUND))
S1B_ROUND = S3B*KP_ROUND + 2*C_ROUND*math.sqrt(KP_ROUND)

# 示範砂 C：直剪，φ' = 32°、c' = 0；密砂尖峰 40°
PHI_CV, PHI_P = 32.0, 40.0
SN = [50.0, 100.0, 200.0]
TF = [s*math.tan(r(PHI_CV)) for s in SN]
TFP = [s*math.tan(r(PHI_P)) for s in SN]
TH_C = 45 + PHI_CV/2
TF1, TF2, TF3 = TF
TFP1, TFP2, TFP3 = TFP

N = {k: v for k, v in globals().items() if k.isupper() and isinstance(v, (int, float))}
if __name__ == "__main__":
    for k, v in N.items(): print(f"{k:12s} {v:.4f}")
    assert abs(R_CHECK - RA) < 1e-9 and abs(TFF - TFF_MC) < 1e-9
    assert abs(S1E_LE - S1E_AC) < 1e-9 and abs(S3E_LE - S3E_AC) < 1e-9
    assert 0.5 <= AF <= 1.0
    json.dump(N, open("nums.json", "w"), indent=1)
    print("TF", [round(t, 1) for t in TF], "TFP", [round(t, 1) for t in TFP])
