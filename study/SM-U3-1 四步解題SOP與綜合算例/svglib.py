import re
from xml.sax.saxutils import escape
from PIL import ImageFont
_FC = {}
def _font(size, bold):
    k = (round(size*4), bold)
    if k not in _FC:
        f = "/usr/share/fonts/opentype/noto/NotoSansCJK-%s.ttc" % ("Bold" if bold else "Regular")
        _FC[k] = ImageFont.truetype(f, size=k[0]/4*10)   # 10× 精度
    return _FC[k]
def measure(s, size, bold=False):
    s = s.replace("'", "′"); w = 0.0
    for p in re.split(r"(_\{[^}]*\}|_.)", s):
        if not p: continue
        if p.startswith("_"):
            t = p[2:-1] if p.startswith("_{") else p[1:]
            w += _font(size*0.68, bold).getlength(t)/10
        else:
            w += _font(size, bold).getlength(p)/10
    return w
FONT = "Noto Sans CJK TC, Microsoft JhengHei, PingFang TC, sans-serif"
INK, MUTED, GRID, PANEL = "#1F2A37", "#6B7280", "#E3E7EC", "#F4F6F9"
CRc, CCc, PCc, P0c, WATER, OK = "#2F54C8", "#C0392B", "#B8520E", "#2E7D6B", "#1D4ED8", "#2E7D6B"
SAND1, SAND2, CLAY, ROCK = "#EADCD2", "#EFE4DE", "#D5E4E4", "#A3A9B2"

def rich(s, size):
    """'p_0′' → tspans；_x 或 _{xx} 為下標"""
    s = s.replace("'", "′")
    out, i, sub_on = [], 0, False
    parts = re.split(r"(_\{[^}]*\}|_.)", s)
    for p in parts:
        if not p: continue
        if p.startswith("_"):
            t = p[2:-1] if p.startswith("_{") else p[1:]
            out.append(f'<tspan font-size="{size*0.68:.1f}" dy="{size*0.28:.1f}">{escape(t)}</tspan>')
            sub_on = True
        else:
            if sub_on:
                out.append(f'<tspan dy="{-size*0.28:.1f}">{escape(p)}</tspan>'); sub_on = False
            else:
                out.append(escape(p))
    return "".join(out)

class SVG:
    def __init__(s, w, h, bg=None, ts=1.0):
        s.w, s.h, s.el, s.ts = w, h, [], ts
        if bg: s.rect(0, 0, w, h, fill=bg, stroke="none")
    def add(s, e): s.el.append(e); return s
    def text(s, x, y, t, size=18, color=INK, anchor="start", weight="normal", italic=False, raw=False, bg=None):
        size = size * s.ts
        if bg:
            wd = measure(t, size, weight == "bold")
            bx = x - (wd/2 if anchor == "middle" else wd if anchor == "end" else 0)
            s.rect(bx-4, y-size*0.9, wd+8, size*1.2, fill=bg, stroke="none", rx=3)
        body = t if raw else rich(t, size)
        if anchor != "start" and not raw:
            wd = measure(t, size, weight == "bold")
            x = x - (wd/2 if anchor == "middle" else wd); anchor = "start"
        st = ' font-style="italic"' if italic else ''
        if "ȳ" in t and not raw:           # 字型缺 ȳ：畫 y 再自繪上橫線
            parts = t.split("ȳ"); acc = ""
            for i, p_ in enumerate(parts[:-1]):
                acc += p_
                x1 = x + measure(acc, size, weight == "bold"); wy = measure("y", size, weight == "bold")
                s.line(x1 + wy*0.15, y - size*0.80, x1 + wy*0.95, y - size*0.80, color, max(1.2, size*0.07))
                acc += "y"
            t = t.replace("ȳ", "y"); body = rich(t, size)
        return s.add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}"{st}>{body}</text>')
    def rect(s, x, y, w, h, fill="none", stroke=INK, sw=1.5, rx=0, dash=None, op=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        o = f' fill-opacity="{op}"' if op is not None else ''
        return s.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{o}/>')
    def line(s, x1, y1, x2, y2, color=INK, sw=2, dash=None, cap="butt"):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        return s.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{sw}" stroke-linecap="{cap}"{d}/>')
    def poly(s, pts, color=INK, sw=2, fill="none", dash=None, closed=False, op=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        o = f' fill-opacity="{op}"' if op is not None else ''
        tag = "polygon" if closed else "polyline"
        P = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        return s.add(f'<{tag} points="{P}" fill="{fill}" stroke="{color}" stroke-width="{sw}" stroke-linejoin="round"{d}{o}/>')
    def circle(s, x, y, r, fill=INK, stroke="#FFFFFF", sw=2.5):
        return s.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def arrow(s, x1, y1, x2, y2, color=INK, sw=2.2, head=11, dash=None):
        import math
        a = math.atan2(y2-y1, x2-x1)
        bx, by = x2 - head*math.cos(a), y2 - head*math.sin(a)
        s.line(x1, y1, bx, by, color, sw, dash)
        p1 = (x2, y2)
        p2 = (bx + head*0.5*math.sin(a), by - head*0.5*math.cos(a))
        p3 = (bx - head*0.5*math.sin(a), by + head*0.5*math.cos(a))
        return s.poly([p1, p2, p3], color=color, sw=1, fill=color, closed=True)
    def dim(s, x1, y1, x2, y2, label, color=INK, size=16, off=(0, -8), anchor="middle"):
        s.arrow((x1+x2)/2, (y1+y2)/2, x1, y1, color, 1.4, 8)
        s.arrow((x1+x2)/2, (y1+y2)/2, x2, y2, color, 1.4, 8)
        return s.text((x1+x2)/2+off[0], (y1+y2)/2+off[1], label, size, color, anchor, "bold")
    def save(s, path):
        body = "\n".join(s.el)
        open(path, "w", encoding="utf-8").write(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s.w} {s.h}" width="{s.w}" height="{s.h}">\n{body}\n</svg>\n')
