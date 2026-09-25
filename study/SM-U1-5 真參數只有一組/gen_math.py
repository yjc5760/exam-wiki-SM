"""公式 → 向量 SVG（matplotlib mathtext，文字轉路徑）"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, json
from PIL import Image
plt.rcParams["svg.fonttype"] = "path"; plt.rcParams["mathtext.fontset"] = "cm"
M = {
 "m_eff": r"$\sigma' = \sigma - u$",
 "m_mc": r"$\tau_f = c' + \sigma'\tan\phi'$",
 "m_f1": r"$\sigma'_1 = \sigma'_3\,K_p + 2c'\sqrt{K_p}$",
 "m_kp": r"$K_p = \tan^2\!\left(45^\circ + \dfrac{\phi'}{2}\right) = \dfrac{1+\sin\phi'}{1-\sin\phi'}$",
 "m_f2": r"$R = C\,\sin\phi' + c'\cos\phi'$",
 "m_f3": r"$\sin\phi' = \dfrac{R}{C} = \dfrac{\sigma'_1-\sigma'_3}{\sigma'_1+\sigma'_3}$",
 "m_cr": r"$C = \dfrac{\sigma'_1+\sigma'_3}{2},\qquad R = \dfrac{\sigma'_1-\sigma'_3}{2} = \dfrac{\Delta\sigma_d}{2}$",
 "m_th": r"$\theta = 45^\circ + \dfrac{\phi'}{2}$",
 "m_sub": r"$K_p = \dfrac{\sigma'_{1a}-\sigma'_{1b}}{\sigma'_{3a}-\sigma'_{3b}}$",
 "m_kf": r"$\tan\alpha' = \sin\phi',\qquad a = c'\cos\phi'$",
 "m_qf": r"$q_f = p'_f\,\sin\phi' + c'\cos\phi'$",
 "m_dil": r"$\phi_p \approx \phi_{cv} + (\mathrm{dilatancy})$",
 "m_af": r"$A_f = \dfrac{u_f}{\Delta\sigma_d}$",
 "m_tff": r"$\tau_{ff} = R\cos\phi',\qquad \sigma'_{ff} = C - R\sin\phi'$",
 "m_skp": r"$\Delta u = B\,[\,\Delta\sigma_3 + A\,(\Delta\sigma_1-\Delta\sigma_3)\,]$",
 "m_pq": r"$p = \dfrac{\sigma_1+\sigma_3}{2},\qquad q = \dfrac{\sigma_1-\sigma_3}{2}$",
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
