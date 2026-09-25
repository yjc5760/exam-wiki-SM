"""公式 → 向量 SVG（matplotlib mathtext，文字轉路徑）"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, json
from PIL import Image
plt.rcParams["svg.fonttype"] = "path"; plt.rcParams["mathtext.fontset"] = "cm"
M = {
 "m_eff": r"$\sigma' = \sigma - u$",
 "m_skp": r"$\Delta u = B\,[\,\Delta\sigma_3 + A\,(\Delta\sigma_1-\Delta\sigma_3)\,]$",
 "m_af": r"$u_f = A_f\,\Delta\sigma_d \;\Rightarrow\; A_f = \dfrac{u_f}{\Delta\sigma_d}$",
 "m_shift": r"$\sigma'_1 = \sigma_1 - u_f,\qquad \sigma'_3 = \sigma_3 - u_f$",
 "m_center": r"$C' = \dfrac{\sigma'_1+\sigma'_3}{2} = C - u_f$",
 "m_rad": r"$R' = \dfrac{(\sigma_1-u_f)-(\sigma_3-u_f)}{2} = \dfrac{\sigma_1-\sigma_3}{2} = R$",
 "m_su": r"$S_u = \dfrac{(\sigma_1-\sigma_3)_f}{2} = \dfrac{\Delta\sigma_d}{2} = R$",
 "m_qu": r"$q_u = 2\,S_u$",
 "m_surat": r"$\dfrac{S_u}{\sigma'_{v0}} = \dfrac{\sin\phi'}{1+\sin\phi'}$",
 "m_surgen": r"$\dfrac{S_u}{\sigma'_{v0}} = \dfrac{\sin\phi'}{1+(2A_f-1)\sin\phi'}$",
 "m_sin": r"$\sin\phi' = \dfrac{\sigma'_1-\sigma'_3}{\sigma'_1+\sigma'_3}$",
 "m_ratio": r"$\dfrac{(\Delta\sigma_d)_2}{(\sigma_3)_2} = \dfrac{(\Delta\sigma_d)_1}{(\sigma_3)_1},\qquad \dfrac{(u_f)_2}{(\sigma_3)_2} = \dfrac{(u_f)_1}{(\sigma_3)_1}$",
 "m_th": r"$\theta = 45^\circ + \dfrac{\phi'}{2}$",
 "m_uu": r"$\Delta u = \Delta\sigma_3\quad(B=1)$",
 "m_gen1": r"$\sigma'_3 = \sigma_3 - A_f\,\Delta\sigma_d,\qquad \sigma'_1 = \sigma_3 + (1-A_f)\,\Delta\sigma_d$",
 "m_gen2": r"$\Delta\sigma_d = (\sigma'_1+\sigma'_3)\sin\phi'$",
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
