import cairosvg, glob
for f in sorted(glob.glob("figs/fig*.svg")):
    cairosvg.svg2png(url=f, write_to=f[:-4]+".png", scale=2, background_color="white")
print("ok")
