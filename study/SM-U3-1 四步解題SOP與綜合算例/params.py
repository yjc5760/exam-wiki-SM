# ── 示範案例：全篇唯一數據來源（所有圖與簡報數字皆由此算出）──
H = 7.0; Q = 20.0
H1, H2 = 3.0, 4.0
G1, G2 = 17.0, 19.0
KA1, KA2 = 1/3, 0.26

SV0 = Q
SV3 = Q + G1*H1              # 71
SV7 = SV3 + G2*H2            # 147
SA0 = KA1*SV0                # 6.67
SA3m = KA1*SV3               # 23.67
SA3p = KA2*SV3               # 18.46
SA7 = KA2*SV7                # 38.22

# 方塊：(代號, 名稱, 合力, 形心至牆底高度, 形狀)
BLOCKS = [
    ("A", "上層矩形（超載）", SA0*H1,               H2 + H1/2, "rect"),
    ("B", "上層三角形（土重）", 0.5*(SA3m-SA0)*H1,   H2 + H1/3, "tri"),
    ("C", "下層矩形（上覆 71 kPa）", SA3p*H2,        H2/2,      "rect"),
    ("D", "下層三角形（土重）", 0.5*(SA7-SA3p)*H2,   H2/3,      "tri"),
]
P = sum(b[2] for b in BLOCKS)
M = sum(b[2]*b[3] for b in BLOCKS)
YBAR = M/P
Y_H3 = H/3
M_H3 = P*Y_H3
UNDER = (M - M_H3)/M

# 若誤用「全牆單一 Ka1 且忽略超載」等對照
P_NOQ_1K = 0.5*KA1*((G1*H1+G2*H2))*H   # 僅示意，不用於主線

if __name__ == "__main__":
    print(f"σa: {SA0:.3f} {SA3m:.3f} {SA3p:.3f} {SA7:.3f}")
    for b in BLOCKS: print(b[0], round(b[2],3), round(b[3],3), round(b[2]*b[3],3))
    print(f"P={P:.3f} M={M:.3f} ybar={YBAR:.4f} H/3={Y_H3:.4f} M_H3={M_H3:.2f} under={UNDER*100:.2f}%")
    # 對帳：積分法
    import numpy as np
    z = np.linspace(0, H, 700001)
    s = np.where(z<=H1, KA1*(Q+G1*z), KA2*(Q+G1*H1+G2*(z-H1)))
    Pi = np.trapezoid(s, z); Mi = np.trapezoid(s*(H-z), z)
    print(f"積分對帳 P={Pi:.3f} M={Mi:.3f} ybar={Mi/Pi:.4f}")
