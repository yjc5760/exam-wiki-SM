"""公式 → 向量 SVG（matplotlib mathtext，文字轉路徑）"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["svg.fonttype"] = "path"; plt.rcParams["mathtext.fontset"] = "cm"
M = {
 "m_p0":  r"$p_0' = \sum \gamma_i' h_i,\quad \gamma' = \gamma_{sat} - \gamma_w$",
 "m_21":  r"$\Delta\sigma = \dfrac{Q}{(B+z)(L+z)}$",
 "m_ocr": r"$\mathrm{OCR} = \dfrac{p_c'}{p_0'}$",
 "m_S":   r"$S_c = \dfrac{\Delta e}{1+e_0}\,H$",
 "m_de":  r"$\Delta e = C_r \log\dfrac{p_c'}{p_0'} + C_c \log\dfrac{p_f'}{p_c'}$",
 "m_A":   r"$S_c = \dfrac{C_c H}{1+e_0}\,\log\dfrac{p_0'+\Delta\sigma}{p_0'}$",
 "m_B":   r"$S_c = \dfrac{C_r H}{1+e_0}\,\log\dfrac{p_0'+\Delta\sigma}{p_0'}$",
 "m_C":   r"$S_c = \dfrac{C_r H}{1+e_0}\log\dfrac{p_c'}{p_0'} + \dfrac{C_c H}{1+e_0}\log\dfrac{p_0'+\Delta\sigma}{p_c'}$",
 "m_pf":  r"$p_f' = p_0' + \Delta\sigma$",
}
import json; man = {}
for k, v in M.items():
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, v, fontsize=28, color="#1F2A37")
    fig.savefig(f"figs/{k}.svg", bbox_inches="tight", pad_inches=0.06, transparent=True)
    fig.savefig(f"figs/{k}.png", bbox_inches="tight", pad_inches=0.06, transparent=True, dpi=200)
    plt.close(fig)
    from PIL import Image
    w, h = Image.open(f"figs/{k}.png").size; man[k] = [w/200, h/200]   # 以 inch 計的原始尺寸
json.dump(man, open("figs/math.json", "w"), indent=1); print(man)
