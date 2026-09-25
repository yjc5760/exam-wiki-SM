"""公式 → 向量 SVG（matplotlib mathtext，文字轉路徑）"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, json
from PIL import Image
plt.rcParams["svg.fonttype"] = "path"; plt.rcParams["mathtext.fontset"] = "cm"
M = {
 "m_s1": r"$\sigma'_1 = \sigma'_3 + \Delta\sigma_d$",
 "m_C": r"$C = \dfrac{\sigma'_1+\sigma'_3}{2}$",
 "m_R": r"$R = \dfrac{\sigma'_1-\sigma'_3}{2} = \dfrac{\Delta\sigma_d}{2}$",
 "m_trs": r"$\sigma_\theta = C + R\cos 2\theta$",
 "m_trt": r"$\tau_\theta = R\sin 2\theta$",
 "m_f1": r"$\sigma'_1 = \sigma'_3\,K_p + 2c'\sqrt{K_p}$",
 "m_kp": r"$K_p = \tan^2\!\left(45^\circ+\dfrac{\phi'}{2}\right) = \dfrac{1+\sin\phi'}{1-\sin\phi'}$",
 "m_f2": r"$R = C\sin\phi' + c'\cos\phi'$",
 "m_f3": r"$\sin\phi' = \dfrac{R}{C} = \dfrac{\sigma'_1-\sigma'_3}{\sigma'_1+\sigma'_3}$",
 "m_d1": r"$\dfrac{\sigma'_1-\sigma'_3}{2} = \dfrac{\sigma'_1+\sigma'_3}{2}\sin\phi' + c'\cos\phi'$",
 "m_d2": r"$\sigma'_1(1-\sin\phi') = \sigma'_3(1+\sin\phi') + 2c'\cos\phi'$",
 "m_d3": r"$\sigma'_1 = \sigma'_3\,\dfrac{1+\sin\phi'}{1-\sin\phi'} + 2c'\,\dfrac{\cos\phi'}{1-\sin\phi'}$",
 "m_d4": r"$\dfrac{\cos\phi'}{1-\sin\phi'} = \sqrt{\dfrac{1+\sin\phi'}{1-\sin\phi'}} = \sqrt{K_p}$",
 "m_th": r"$\theta = 45^\circ + \dfrac{\phi'}{2}$",
 "m_2th": r"$2\theta = 90^\circ + \phi'$",
 "m_sff": r"$\sigma'_{ff} = C - R\sin\phi'$",
 "m_tff": r"$\tau_{ff} = R\cos\phi'$",
 "m_q1": r"$340 = 100\,y^2 + 2(25)\,y,\qquad y=\sqrt{K_p}$",
 "m_q2": r"$10y^2 + 5y - 34 = 0$",
 "m_q3": r"$y = \dfrac{-5+\sqrt{5^2+4(10)(34)}}{2(10)} = \dfrac{-5+\sqrt{1385}}{20} = 1.6108$",
 "m_chk1": r"$c' + \sigma'_{ff}\tan\phi' = 25 + 166.77\,(0.4950) = 107.55 = \tau_{ff}$",
 "m_chk2": r"$C\sin\phi' + c'\cos\phi' = 220(0.4436) + 25(0.8962) = 120.00 = R$",
 "m_chk3": r"$C + R\cos 2\theta = 220 + 120\cos 116.33^\circ = 166.77$",
}
man = {}
for k, v in M.items():
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, v, fontsize=28, color="#1F2A37")
    fig.savefig(f"figs/{k}.svg", bbox_inches="tight", pad_inches=0.06, transparent=True)
    fig.savefig(f"figs/{k}.png", bbox_inches="tight", pad_inches=0.06, transparent=True, dpi=200)
    plt.close(fig)
    w, h = Image.open(f"figs/{k}.png").size; man[k] = [w / 200, h / 200]
json.dump(man, open("figs/math.json", "w"), indent=1); print(len(man))
