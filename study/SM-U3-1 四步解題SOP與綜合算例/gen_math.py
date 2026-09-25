"""公式 → 向量 SVG（matplotlib mathtext，文字轉路徑）"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, json
from PIL import Image
from params import *
plt.rcParams["svg.fonttype"] = "path"; plt.rcParams["mathtext.fontset"] = "cm"
M = {
 "m_ka":  r"$K_a = \tan^2\!\left(45^\circ - \dfrac{\phi}{2}\right)$",
 "m_k0":  r"$K_0 = 1 - \sin\phi'$",
 "m_kp":  r"$K_p = \tan^2\!\left(45^\circ + \dfrac{\phi}{2}\right)$",
 "m_sa":  r"$\sigma_a = K\,\sigma_v' - 2c\sqrt{K} + u$",
 "m_zc":  r"$z_c = \dfrac{2c}{\gamma\sqrt{K_a}} - \dfrac{q}{\gamma}$",
 "m_P":   r"$P = \sum P_i$",
 "m_y":   r"$\bar{y} = \dfrac{\sum P_i\,y_i}{\sum P_i}$",
 "m_ynum": r"$\bar{y} = \dfrac{%.1f}{%.1f} = %.2f\ \mathrm{m}$" % (M, P, YBAR),
 "m_trap": r"$\bar{y} = \dfrac{H}{3}\cdot\dfrac{2a+b}{a+b}$",
}
man = {}
WHITE = {"m_ynum_w": M["m_ynum"]}
for k, v in M.items():
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, v, fontsize=28, color="#1F2A37")
    fig.savefig(f"figs/{k}.svg", bbox_inches="tight", pad_inches=0.06, transparent=True)
    fig.savefig(f"figs/{k}.png", bbox_inches="tight", pad_inches=0.06, transparent=True, dpi=200)
    plt.close(fig)
    w, h = Image.open(f"figs/{k}.png").size; man[k] = [w / 200, h / 200]
for k, v in WHITE.items():
    fig = plt.figure(figsize=(0.01, 0.01)); fig.text(0, 0, v, fontsize=28, color="#FFFFFF")
    fig.savefig(f"figs/{k}.svg", bbox_inches="tight", pad_inches=0.06, transparent=True)
    fig.savefig(f"figs/{k}.png", bbox_inches="tight", pad_inches=0.06, transparent=True, dpi=200); plt.close(fig)
    w, h = Image.open(f"figs/{k}.png").size; man[k] = [w / 200, h / 200]
json.dump(man, open("figs/math.json", "w"), indent=1); print(man)
