import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, json
plt.rcParams["mathtext.fontset"]="cm"
EQ={
"eps":r"$\varepsilon_v=\dfrac{\Delta H}{H_0}=\dfrac{\Delta V}{V_0}=\dfrac{\Delta e}{1+e_0}$",
"v0":r"$V_0=V_s+V_{v0}=1+e_0,\quad \Delta V=\Delta V_v=\Delta e$",
"gd":r"$\gamma_d=\dfrac{W_s}{V}=\dfrac{G_s\gamma_w\cdot 1}{1+e}$",
"e_from_gd":r"$e=\dfrac{G_s\gamma_w}{\gamma_d}-1$",
"se":r"$w=\dfrac{W_w}{W_s}=\dfrac{V_w\gamma_w}{G_s\gamma_w}=\dfrac{Se}{G_s}\ \Rightarrow\ Se=wG_s$",
"zav":r"$\gamma_{d,\mathrm{zav}}=\dfrac{G_s\gamma_w}{1+wG_s}$",
"dr":r"$D_r=\dfrac{e_{max}-e}{e_{max}-e_{min}}$",
"rc":r"$RC=\dfrac{\gamma_d}{\gamma_{d,max}}$",
"de":r"$\Delta e=C_c\log\dfrac{p'_0+\Delta p}{p'_0}$",
"sc":r"$S_c=H_0\,\dfrac{\Delta e}{1+e_0}$",
"scw":r"$S_c\neq H_0\,\dfrac{\Delta e}{1+e}$",
}
size={}
for k,t in EQ.items():
    f=plt.figure(figsize=(0.01,0.01)); f.text(0,0,t,fontsize=30,color="#1F2733")
    p=f"eq/{k}.png"; f.savefig(p,dpi=250,transparent=True,bbox_inches="tight",pad_inches=0.04); plt.close(f)
    from PIL import Image; im=Image.open(p); size[k]=im.size
json.dump(size,open("eq/sizes.json","w")); print(size)
