"""公式 → 向量 SVG（matplotlib mathtext，文字轉路徑）；數字一律取自 params.py"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, json
from PIL import Image
from params import *
plt.rcParams["svg.fonttype"] = "path"; plt.rcParams["mathtext.fontset"] = "cm"
M = {
 "m_f1": r"$\sigma'_1 = \sigma'_3\,K_p + 2c'\sqrt{K_p}$",
 "m_nc": r"$c'=0:\quad \sigma'_1 = \sigma'_3\,K_p$",
 "m_sin": r"$\sin\phi' = \dfrac{R}{C} = \dfrac{\sigma'_1-\sigma'_3}{\sigma'_1+\sigma'_3}$",
 "m_sincu": r"$\sin\phi_{cu} = \dfrac{\sigma_1-\sigma_3}{\sigma_1+\sigma_3}$",
 "m_ratio": r"$\dfrac{(\Delta\sigma_d)_2}{(\sigma_3)_2} = \dfrac{(\Delta\sigma_d)_1}{(\sigma_3)_1}$",
 "m_su": r"$\dfrac{S_u}{\sigma'_{v0}} = \dfrac{\sin\phi'}{1+\sin\phi'}$",
 "m_sud": r"$\dfrac{S_u}{\sigma'_{v0}-S_u} = \sin\phi'$",
 "m_sug": r"$\dfrac{S_u}{\sigma'_c} = \dfrac{\sin\phi'}{1+(2A_f-1)\sin\phi'}$",
 "m_kp": r"$K_p = \tan^2\!\left(45^\circ+\dfrac{\phi'}{2}\right) = \dfrac{1+\sin\phi'}{1-\sin\phi'}$",
 "m_phi": r"$\phi' = \arcsin\dfrac{K_p-1}{K_p+1}$",
 "m_sa": r"$\sigma'_{1a} = \sigma'_{3a}K_p + 2c'\sqrt{K_p}$",
 "m_sb": r"$\sigma'_{1b} = \sigma'_{3b}K_p + 2c'\sqrt{K_p}$",
 "m_sub": r"$K_p = \dfrac{\sigma'_{1a}-\sigma'_{1b}}{\sigma'_{3a}-\sigma'_{3b}}$",
 "m_q1": rf"$80 = 40\,K_p + 2c'\sqrt{{K_p}}\qquad 150 = 80\,K_p + 2c'\sqrt{{K_p}}$",
 "m_q2": rf"$K_p = \dfrac{{150-80}}{{80-40}} = {Q_KP:.2f},\qquad 2c'\sqrt{{K_p}} = 80-40({Q_KP:.2f}) = {Q_ICPT:.0f}$",
 "m_q3": rf"$\sigma'_1 = 200({Q_KP:.2f}) + {Q_ICPT:.0f} = {Q_S1C:.0f}\ \Rightarrow\ \Delta\sigma = {Q_DC:.0f}\ \mathrm{{kN/m^2}}$",
 "m_q4": rf"$\phi' = \arcsin\dfrac{{{Q_KP:.2f}-1}}{{{Q_KP:.2f}+1}} = {Q_PHI:.2f}^\circ,\quad c' = \dfrac{{{Q_ICPT:.0f}}}{{2\sqrt{{{Q_KP:.2f}}}}} = {Q_C:.2f}$",
 "m_o1": rf"$340 = 100\,y^2 + 50\,y\ \Rightarrow\ 10y^2+5y-34=0,\quad y=\sqrt{{K_p}}={O_Y:.4f}$",
 "m_o2": rf"$\sigma'_1 = 200({O_KP:.4f}) + 2(25)({O_Y:.4f}) = {O_S1B:.2f}$",
 "m_o3": rf"$\Delta\sigma_d = {O_S1B:.2f} - 200 = {O_DSDB:.2f}\ \mathrm{{kPa}}$",
 "m_o4": rf"$\mathrm{{\times}}\ \ 240 \times 2 = 480\ \ (\mathrm{{+{O_OVER:.1f}\%}})$",
 "m_n1": rf"$\sin\phi_{{cu}} = \dfrac{{85}}{{285}}\Rightarrow \phi_{{cu}} = {N_PHICU:.2f}^\circ$",
 "m_n2": rf"$\sin\phi' = \dfrac{{85}}{{151}}\Rightarrow \phi' = {N_PHI:.2f}^\circ$",
 "m_n3": rf"$(\Delta\sigma_d)_2 = 85\times\dfrac{{250}}{{100}} = {N_DSDB:g}\ \mathrm{{kPa}}$",
 "m_chk": r"$\tau_{ff} = c' + \sigma'_{ff}\tan\phi'$",
 "m_af": r"$A_f = \dfrac{u_f}{\Delta\sigma_d}$",
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
