"""公式 → 向量 SVG（matplotlib mathtext，文字轉路徑）"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, json
from PIL import Image
plt.rcParams["svg.fonttype"] = "path"; plt.rcParams["mathtext.fontset"] = "cm"
M = {
 "m_ka_r": r"$K_a = \tan^2\!\left(45^\circ - \dfrac{\phi}{2}\right)$",
 "m_kp_r": r"$K_p = \tan^2\!\left(45^\circ + \dfrac{\phi}{2}\right)$",
 "m_ka_c": r"$K_a = \dfrac{\cos^2(\phi-\theta)}{\cos^2\theta\,\cos(\delta+\theta)\,(1+\sqrt{A_a})^2}$",
 "m_A_a": r"$A_a = \dfrac{\sin(\delta+\phi)\,\sin(\phi-\beta)}{\cos(\delta+\theta)\,\cos(\theta-\beta)}$",
 "m_kp_c": r"$K_p = \dfrac{\cos^2(\phi+\theta)}{\cos^2\theta\,\cos(\delta-\theta)\,(1-\sqrt{A_p})^2}$",
 "m_A_p": r"$A_p = \dfrac{\sin(\delta+\phi)\,\sin(\phi+\beta)}{\cos(\delta-\theta)\,\cos(\theta-\beta)}$",
 "m_ka_rs": r"$K_a = \cos\beta\,\dfrac{\cos\beta-\sqrt{\cos^2\beta-\cos^2\phi}}{\cos\beta+\sqrt{\cos^2\beta-\cos^2\phi}}$",
 "m_pa": r"$P_a = \dfrac{1}{2}\,K_a\,\gamma H^2$",
 "m_pp": r"$P_p = \dfrac{1}{2}\,K_p\,\gamma D_f^{\,2}$",
 "m_comp": r"$P_h = P_a\cos\beta,\quad P_v = P_a\sin\beta$",
 "m_compc": r"$P_h = P_a\cos(\delta+\theta),\quad P_v = P_a\sin(\delta+\theta)$",
 "m_degen": r"$\theta=\delta=\beta=0\ \Rightarrow\ K_a=\dfrac{\cos^2\phi}{(1+\sin\phi)^2}=\dfrac{1-\sin\phi}{1+\sin\phi}$",
}
man = {}
for k, v in M.items():
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, v, fontsize=28, color="#1F2A37")
    fig.savefig(f"figs/{k}.svg", bbox_inches="tight", pad_inches=0.06, transparent=True)
    fig.savefig(f"figs/{k}.png", bbox_inches="tight", pad_inches=0.06, transparent=True, dpi=200)
    plt.close(fig)
    w, h = Image.open(f"figs/{k}.png").size; man[k] = [w / 200, h / 200]
json.dump(man, open("figs/math.json", "w"), indent=1); print(man)
