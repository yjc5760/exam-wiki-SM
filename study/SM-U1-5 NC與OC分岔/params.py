# ── SM-U1-5 拼圖四：NC / OC 分岔 ── 全篇唯一數據來源
import math, json
r, d = math.radians, math.degrees
sn, cs, tn = (lambda a: math.sin(r(a))), (lambda a: math.cos(r(a))), (lambda a: math.tan(r(a)))
kp_of = lambda phi: (1 + sn(phi))/(1 - sn(phi))
phi_of = lambda kp: d(math.asin((kp - 1)/(kp + 1)))

# ═════ NC 示範題 [SM-2018-2] CU：σ3 = 100、Δσd = 85、uf = 67；第二試體 σ3 = 250 ═════
N_S3, N_DSD, N_UF, N_S3B = 100.0, 85.0, 67.0, 250.0
N_S1 = N_S3 + N_DSD                                   # 185
N_S3E, N_S1E = N_S3 - N_UF, N_S1 - N_UF               # 33、118
N_SIN_CU = N_DSD/(N_S1 + N_S3)                        # 85/285
N_SIN_E = (N_S1E - N_S3E)/(N_S1E + N_S3E)             # 85/151
N_PHICU, N_PHI = d(math.asin(N_SIN_CU)), d(math.asin(N_SIN_E))   # 17.35°、34.26°
N_TH, N_TH_WRONG = 45 + N_PHI/2, 45 + N_PHICU/2       # 62.13°、53.68°
N_AF = N_UF/N_DSD                                     # 0.788
N_K = N_S3B/N_S3                                      # 位似比 2.5
N_DSDB = N_DSD*N_K                                    # 212.5
N_S1B, N_UFB = N_S3B + N_DSDB, N_UF*N_K               # 462.5、167.5
N_S3BE, N_S1BE = N_S3B - N_UFB, N_S1B - N_UFB         # 82.5、295
N_KP_E, N_KP_CU = kp_of(N_PHI), kp_of(N_PHICU)        # 3.5758、1.85
N_SU = N_DSD/2                                        # 42.5
N_SU_RATIO = N_SU/N_S3                                # 0.425（σc' = 100）
N_SU_GEN = N_SIN_E/(1 + (2*N_AF - 1)*N_SIN_E)         # 一般式
N_SU_AF1 = N_SIN_E/(1 + N_SIN_E)                      # 課本式（A_f = 1）
N_DSD_CHK = N_S3*(N_KP_E - 1)/(1 - N_AF + N_AF*N_KP_E)

# ═════ OC 示範題 ① [SM-2024-1] CD：σ3' = 100、Δσd = 240、c' = 25（單組 → 一元二次） ═════
O_S3, O_DSD, O_C = 100.0, 240.0, 25.0
O_S1 = O_S3 + O_DSD                                   # 340
O_Y = (-2*O_C + math.sqrt(4*O_C*O_C + 4*O_S3*O_S1))/(2*O_S3)   # √Kp = 1.6108
O_KP = O_Y*O_Y                                        # 2.5946
O_PHI = phi_of(O_KP)                                  # 26.33°
O_ICPT = 2*O_C*O_Y                                    # 2c'√Kp = 80.54
O_S3B = 200.0
O_S1B = O_S3B*O_KP + O_ICPT                           # 599.46
O_DSDB = O_S1B - O_S3B                                # 399.46
O_DSD_PROP = O_DSD*O_S3B/O_S3                         # 480（錯）
O_OVER = (O_DSD_PROP - O_DSDB)/O_DSDB*100             # 20.2 %

# ═════ OC 示範題 ② [SM-2025-2] CU 兩組 → 相減法 → CD 外推 ═════
Q_S3A, Q_DA, Q_UA = 75.0, 40.0, 35.0
Q_S3B, Q_DB, Q_UB = 150.0, 70.0, 70.0
Q_S3AE, Q_S1AE = Q_S3A - Q_UA, Q_S3A + Q_DA - Q_UA    # 40、80
Q_S3BE, Q_S1BE = Q_S3B - Q_UB, Q_S3B + Q_DB - Q_UB    # 80、150
Q_KP = (Q_S1BE - Q_S1AE)/(Q_S3BE - Q_S3AE)            # 70/40 = 1.75
Q_ICPT = Q_S1AE - Q_S3AE*Q_KP                         # 2c'√Kp = 10
Q_Y = math.sqrt(Q_KP)
Q_PHI = phi_of(Q_KP)                                  # 15.83°
Q_C = Q_ICPT/(2*Q_Y)                                  # 3.78
Q_S3C = 200.0
Q_S1C = Q_S3C*Q_KP + Q_ICPT                           # 360
Q_DC = Q_S1C - Q_S3C                                  # 160
Q_DB_PROP = Q_DA*Q_S3B/Q_S3A                          # 80（比例法硬套，實測 70）
Q_DC_PROP_E = Q_S3C*(Q_S1AE/Q_S3AE - 1)               # 有效圓硬套比例：200×(2−1) = 200（錯）

# ═════ 陷阱 2：取樣後壓密壓力 < 現地 σ'v0 → 虛擬凝聚力（示意數值） ═════
F_PHI = 30.0; F_KP = kp_of(F_PHI)                     # 現地真 NC：c' = 0、φ' = 30°
F_SP = 150.0                                          # σ'v0 = σ'p
F_S1P = F_SP*F_KP                                     # 450
F_KPO = 2.5                                           # 過壓密段斜率（示意）
F_ICPT = F_S1P - F_SP*F_KPO                           # 75
F_C = F_ICPT/(2*math.sqrt(F_KPO)); F_PHIO = phi_of(F_KPO)
F_T1, F_T2 = 50.0, 100.0                              # 實驗室壓密壓力（< 150）
F_S1T1, F_S1T2 = F_T1*F_KPO + F_ICPT, F_T2*F_KPO + F_ICPT     # 200、325
F_NC_T1 = F_T1*F_KP                                   # 150（真 NC）
F_OVER = (F_S1T1 - F_NC_T1)/F_NC_T1*100               # 高估 33 %

# ═════ 應力歷史示意（e–log σ'） ═════
H_SP, H_S0 = 200.0, 50.0; H_OCR = H_SP/H_S0

# ═════ Kp–φ' 對照 ═════
KP_TABLE = [(20, kp_of(20)), (25, kp_of(25)), (30, kp_of(30)), (35, kp_of(35))]

N = {k: v for k, v in globals().items() if k.isupper() and isinstance(v, (int, float))}
if __name__ == "__main__":
    for k, v in N.items(): print(f"{k:12s} {v:.4f}")
    assert abs(N_PHICU - 17.35) < 0.01 and abs(N_PHI - 34.26) < 0.01
    assert abs(N_TH - 62.13) < 0.01 and abs(N_DSDB - 212.5) < 1e-9
    assert abs(N_S1B - N_S3B*N_KP_CU) < 0.2                     # 總應力法驗算 462.5
    assert abs((N_S1BE - N_S3BE)/(N_S1BE + N_S3BE) - N_SIN_E) < 1e-12   # 第二試體 φ' 相同
    assert abs(N_SU_GEN - N_SU_RATIO) < 1e-9                    # 一般式 = 42.5/100
    assert abs(N_DSD_CHK - N_DSD) < 1e-9
    assert abs(O_S3*O_KP + O_ICPT - O_S1) < 1e-9
    assert abs(O_DSDB - 399.46) < 0.01 and abs(O_OVER - 20.2) < 0.05
    assert abs(Q_KP - 1.75) < 1e-12 and abs(Q_ICPT - 10) < 1e-9 and abs(Q_DC - 160) < 1e-9
    assert abs(Q_S3BE*Q_KP + Q_ICPT - Q_S1BE) < 1e-9
    # SM-2025-2 包絡線與兩個有效圓相切：R = C sinφ' + c' cosφ'
    for s3, s1 in [(Q_S3AE, Q_S1AE), (Q_S3BE, Q_S1BE), (Q_S3C, Q_S1C)]:
        assert abs((s1 - s3)/2 - ((s1 + s3)/2*sn(Q_PHI) + Q_C*cs(Q_PHI))) < 1e-9
    json.dump({k: round(v, 4) for k, v in N.items()}, open("nums.json", "w"), indent=1)
    print("asserts ok")
