const pptxgen = require("pptxgenjs");
const fs = require("fs");
const N = JSON.parse(fs.readFileSync("nums.json", "utf8"));
const MJ = JSON.parse(fs.readFileSync("figs/math.json", "utf8"));
const pres = new pptxgen(); pres.layout = "LAYOUT_WIDE"; pres.title = "SM-U3-1 拼圖四：理論邊界（適用條件與安全考量）";
const FT = "Noto Sans CJK TC";
const C = { ink: "1F2A37", muted: "6B7280", panel: "F4F6F9", line: "D5DAE1", rk: "2F54C8", cl: "B8520E",
            ps: "C0392B", ok: "2E7D6B", res: "E4572E", dark: "1B2432", white: "FFFFFF",
            rkbg: "EEF2FB", clbg: "FBF1EA", psbg: "FBECEA", okbg: "E6F2EF" };
const f1 = v => (v + 1e-9).toFixed(1), f2 = v => (v + 1e-9).toFixed(2), f3 = v => (v + 1e-9).toFixed(3);
const pct = (a, b) => ((a / b - 1) * 100).toFixed(1);

function runs(str, o = {}) {
  const out = []; const re = /(_\{[^}]*\}|_.)/g; let last = 0, m;
  str = str.replace(/'/g, "′");
  while ((m = re.exec(str))) {
    if (m.index > last) out.push({ text: str.slice(last, m.index), options: { ...o } });
    const t = m[0].startsWith("_{") ? m[0].slice(2, -1) : m[0].slice(1);
    out.push({ text: t, options: { ...o, subscript: true } }); last = re.lastIndex;
  }
  if (last < str.length) out.push({ text: str.slice(last), options: { ...o } });
  return out;
}
function paras(list) {
  const out = [];
  list.forEach((p, i) => {
    const r = runs(p.t, p.o || {});
    if (i < list.length - 1) r[r.length - 1].options.breakLine = true;
    out.push(...r);
  });
  return out;
}
function T(s, content, x, y, w, h, o = {}) {
  const base = { fontFace: FT, fontSize: 15, color: C.ink, valign: "top", margin: 0, isTextBox: true };
  const opts = { ...base, ...o, x, y, w, h };
  const body = typeof content === "string" ? runs(content, { bold: o.bold, color: o.color || C.ink, fontSize: o.fontSize || 15 }) : content;
  s.addText(body, opts);
}
function vb(file) {
  const t = fs.readFileSync(file, "utf8"); const m = t.match(/viewBox="([\d.\s-]+)"/);
  const a = m[1].trim().split(/\s+/).map(Number); return [a[2], a[3]];
}
function img(s, name, x, y, W, H, align = "center") {
  const f = `figs/${name}.svg`; let w, h;
  if (MJ[name]) [w, h] = MJ[name]; else [w, h] = vb(f);
  const k = Math.min(W / w, H / h); const iw = w * k, ih = h * k;
  const ix = align === "left" ? x : x + (W - iw) / 2;
  s.addImage({ path: f, x: ix, y: y + (H - ih) / 2, w: iw, h: ih, altText: name });
  return { x: ix, y: y + (H - ih) / 2, w: iw, h: ih };
}
function eq(s, name, x, y, H, scale = 0.72, align = "left") {
  const [w, h] = MJ[name]; let iw = w * scale, ih = h * scale;
  if (ih > H) { iw *= H / ih; ih = H; }
  const ix = align === "center" ? x - iw / 2 : x;
  s.addImage({ path: `figs/${name}.svg`, x: ix, y: y + (H - ih) / 2, w: iw, h: ih, altText: name });
  return iw;
}
function header(s, eyebrow, title, col = C.rk) {
  T(s, eyebrow, 0.6, 0.38, 11, 0.3, { fontSize: 12, bold: true, color: col, charSpacing: 2 });
  T(s, title, 0.6, 0.68, 12.2, 0.6, { fontSize: 27, bold: true });
}
function panel(s, x, y, w, h, fill = C.panel, line = C.line) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { color: line, width: 1 }, rectRadius: 0.12 });
}
function pageNo(s, n) { T(s, `${n}`, 12.3, 7.08, 0.5, 0.25, { fontSize: 10, color: "9AA3AE", align: "right" }); }
let pg = 1;
function newSlide() { const s = pres.addSlide(); s.background = { color: C.white }; pg++; return s; }

// ───── 1 封面 ─────
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  T(s, "SM-U3-1　側向土壓力理論｜觀念講義・拼圖四", 0.8, 1.2, 11, 0.4, { fontSize: 16, color: "9FB3C8", bold: true });
  T(s, "理論邊界：適用條件與安全考量", 0.8, 1.8, 11.8, 1.1, { fontSize: 44, bold: true, color: C.white });
  T(s, "前三塊拼圖給你計算的刀槍；這一塊告訴你公式的物理極限——考場選對公式，設計不過度樂觀", 0.8, 2.95, 11.8, 0.9, { fontSize: 20, color: "D6DEE8" });
  const dots = [["一", "Rankine／Coulomb", C.rk], ["二", "斜填土 β 修正", C.cl], ["三", "被動土壓保護傘", C.ps]];
  dots.forEach(([n, lab, col], i) => {
    const x = 0.8 + i * 4.0;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 4.35, w: 3.7, h: 0.8, fill: { color: "243044" }, line: { color: col, width: 2 }, rectRadius: 0.1 });
    T(s, `邊界${n}`, x + 0.25, 4.35, 1.1, 0.8, { fontSize: 15, bold: true, color: col === C.rk ? "8FA8F0" : col === C.cl ? "F0A36A" : "F08A7E", valign: "middle" });
    T(s, lab, x + 1.25, 4.35, 2.45, 0.8, { fontSize: 17, bold: true, color: C.white, valign: "middle" });
  });
  T(s, `示範牆貫穿全篇：H = ${N.H} m、γ = ${N.G} kN/m³、φ = ${N.PHI}°、c = 0；牆趾前埋深 D_f = ${N.DF} m；圖上數字全部可對帳`,
    0.8, 6.3, 11.8, 0.4, { fontSize: 14, color: "9FB3C8" });
}
// ───── 2 定位 ─────
{
  const s = newSlide();
  header(s, "OVERVIEW · 拼圖四的角色", "最後一片拼圖：不是再多一條公式，而是知道公式能用到哪裡", C.ps);
  img(s, "fig01_map", 0.6, 1.45, 12.1, 4.35);
  panel(s, 0.6, 6.0, 12.1, 1.0);
  T(s, paras([
    { t: "三個邊界各管一件事：", o: { bold: true, fontSize: 15, color: C.ps } },
    { t: "選公式（Rankine／Coulomb）→ 修幾何（斜填土 β）→ 守安全（被動抗力不能全信）。本講每個結論都用同一道示範牆算給你看。", o: { fontSize: 15 } },
  ]), 0.85, 6.1, 11.6, 0.85, { paraSpaceAfter: 3 });
  pageNo(s, pg);
}
// ───── 3 兩種看法 ─────
{
  const s = newSlide();
  header(s, "邊界一 · RANKINE vs COULOMB", "兩大流派差在「看哪裡」：土體內部的應力，還是整塊滑動楔體", C.rk);
  img(s, "fig02_two", 0.6, 1.4, 12.1, 5.45);
  T(s, "右圖依 Das 教科書定義：θ 為牆背與鉛直線夾角，填土壓在牆背上方為正；β 為填土坡角；δ 為牆背摩擦角。",
    0.6, 6.9, 12.1, 0.35, { fontSize: 12, color: C.muted });
  pageNo(s, pg);
}
// ───── 4 比較表 ─────
{
  const s = newSlide();
  header(s, "邊界一 · 比較表", "主動時 Rankine 偏保守，被動時 Coulomb 偏危險", C.rk);
  const hd = { bold: true, color: C.white, fill: { color: C.dark }, fontFace: FT, fontSize: 14, align: "center", valign: "middle" };
  const cl = { fontFace: FT, fontSize: 13, color: C.ink, align: "left", valign: "middle", margin: [2, 8, 2, 8] };
  const rowsData = [
    ["底層假設", "牆背垂直 θ = 0、完全光滑 δ = 0、填土水平 β = 0", "可含斜牆背 θ、牆背摩擦 δ、斜填土 β", "題目給 δ、θ 就是在叫你換公式"],
    ["推導角度", "土體每一點都達極限 → 莫爾圓", "滑動楔體當剛體 → 試算求極值", "三參數歸零時兩者完全一致"],
    ["主動 K_a", "忽略摩擦 → 偏大（保守）", "δ 分擔一部分 → 較小、較貼近實際", `本例 ${f3(N.KA_R)} vs ${f3(N.KA_C)}`],
    ["被動 K_p", "δ = 0 → 偏小（保守）", "平面破壞面 → 高估，δ 大時嚴重", `本例 ${f2(N.KP_R)} vs ${f2(N.KP_C)}`],
    ["合力方向", "平行填土面（水平填土即水平）", "與牆背法線夾 δ 角", "檢核前要先拆水平、垂直分力"],
  ];
  const rows = [[{ text: "項目", options: hd }, { text: "Rankine（應力法）", options: { ...hd, fill: { color: C.rk } } },
                 { text: "Coulomb（楔體法）", options: { ...hd, fill: { color: C.cl } } }, { text: "考試上的意義", options: hd }]];
  rowsData.forEach((r, i) => {
    const fill = { color: i % 2 ? "F7F8FA" : C.white };
    rows.push([
      { text: runs(r[0], { bold: true }), options: { ...cl, bold: true, align: "center", fill } },
      { text: runs(r[1]), options: { ...cl, fill } },
      { text: runs(r[2]), options: { ...cl, fill } },
      { text: runs(r[3], { bold: i >= 2, color: i >= 2 ? C.ps : C.ink }), options: { ...cl, fill } },
    ]);
  });
  s.addTable(rows, { x: 0.6, y: 1.5, w: 12.1, colW: [1.4, 3.8, 3.6, 3.3], rowH: [0.5, 0.72, 0.72, 0.72, 0.72, 0.72],
                     border: { type: "solid", pt: 0.75, color: "D5DAE1" } });
  panel(s, 0.6, 5.85, 5.95, 1.15, C.rkbg, "B9C6EA");
  T(s, paras([
    { t: "為什麼 Rankine 主動偏保守？", o: { bold: true, fontSize: 15, color: C.rk } },
    { t: "真實牆背有摩擦，會「托住」一部分下滑的土；Rankine 當它不存在，推力就算大了。", o: { fontSize: 13 } },
  ]), 0.8, 5.95, 5.6, 1.0, { paraSpaceAfter: 3 });
  panel(s, 6.75, 5.85, 5.95, 1.15, C.psbg, "E6B0AA");
  T(s, paras([
    { t: "為什麼 Coulomb 被動偏危險？", o: { bold: true, fontSize: 15, color: C.ps } },
    { t: "被動破壞面實際上是彎的；假設成平面會找不到真正的最小抗力，K_p 算太大。", o: { fontSize: 13 } },
  ]), 6.95, 5.95, 5.6, 1.0, { paraSpaceAfter: 3 });
  pageNo(s, pg);
}
// ───── 5 楔體試算 ─────
{
  const s = newSlide();
  header(s, "邊界一 · COULOMB 的算法", "切一刀、解三力、找最大：主動土壓就是所有試算刀中最大的推力", C.cl);
  img(s, "fig03_wedge", 0.6, 1.4, 12.1, 5.25);
  T(s, `同一道示範牆：δ = 20° 時最危險的一刀在 ρ = ${N.RHO_C.toFixed(1)}°，P_a = ${f1(N.PA_C)} kN/m；δ = 0 時回到 60° 與 ${f1(N.PA_R)} kN/m。`,
    0.6, 6.72, 12.1, 0.4, { fontSize: 14, bold: true, color: C.cl });
  pageNo(s, pg);
}
// ───── 6 示範牆對照 ─────
{
  const s = newSlide();
  header(s, "邊界一 · 示範牆", `給了 δ = 20°：推力小了，方向也歪了——水平推力少 ${(100 - N.PA_C_H / N.PA_R * 100).toFixed(1)}%`, C.cl);
  img(s, "fig04_demo", 0.6, 1.4, 12.1, 4.75);
  const cells = [
    ["水平推力", `${f1(N.PA_R)} → ${f1(N.PA_C_H)} kN/m`, "滑動、傾覆的主要來源變小", C.rk, C.rkbg, "B9C6EA"],
    ["多了垂直分力", `P_v = ${f1(N.PA_C_V)} kN/m 向下`, "壓在牆背上，反而幫忙抗滑、抗傾", C.ok, C.okbg, "9CC7BC"],
    ["所以 Rankine…", "主動側偏保守", "安全但可能不經濟；題目沒給 δ 就用它", C.cl, C.clbg, "E3B894"],
  ];
  cells.forEach(([a, b, c, col, bg, ln], i) => {
    const x = 0.6 + i * 4.1;
    panel(s, x, 6.2, 3.9, 0.95, bg, ln);
    T(s, a, x + 0.2, 6.27, 3.5, 0.3, { fontSize: 12, bold: true, color: col });
    T(s, b, x + 0.2, 6.5, 3.6, 0.32, { fontSize: 16, bold: true });
    T(s, c, x + 0.2, 6.82, 3.6, 0.3, { fontSize: 11, color: C.muted });
  });
  pageNo(s, pg);
}
// ───── 7 選用流程 ─────
{
  const s = newSlide();
  header(s, "邊界一 · 考場選用指標", "兩個問題決定公式：有沒有 δ、θ？填土斜不斜？", C.rk);
  img(s, "fig05_flow", 0.6, 1.4, 12.1, 5.5);
  pageNo(s, pg);
}
// ───── 8 Coulomb 公式 ─────
{
  const s = newSlide();
  header(s, "邊界一 · COULOMB 公式", "長得嚇人，但只是把 δ、θ、β 三個幾何量放進去", C.cl);
  panel(s, 0.6, 1.45, 5.95, 3.35, C.clbg, "E3B894");
  T(s, "主動（楔體往下滑）", 0.85, 1.58, 5, 0.3, { fontSize: 14, bold: true, color: C.cl });
  eq(s, "m_ka_c", 0.85, 1.95, 1.2, 0.62);
  eq(s, "m_A_a", 0.85, 3.3, 1.2, 0.62);
  panel(s, 6.75, 1.45, 5.95, 3.35, C.psbg, "E6B0AA");
  T(s, "被動（楔體被往上推）", 7.0, 1.58, 5, 0.3, { fontSize: 14, bold: true, color: C.ps });
  eq(s, "m_kp_c", 7.0, 1.95, 1.2, 0.62);
  eq(s, "m_A_p", 7.0, 3.3, 1.2, 0.62);
  panel(s, 0.6, 5.0, 12.1, 1.15, C.rkbg, "B9C6EA");
  T(s, "退化檢查", 0.85, 5.1, 2, 0.3, { fontSize: 14, bold: true, color: C.rk });
  const dw = eq(s, "m_degen", 0.85, 5.38, 0.72, 0.55);
  T(s, "＝ tan²(45° − φ/2)", 0.85 + dw + 0.15, 5.47, 3.6, 0.5, { fontSize: 20, bold: true, color: C.rk, valign: "middle" });
  T(s, paras([
    { t: "符號陷阱：各教科書 θ 的量法、正負不一，甚至有人量「牆背與水平」的夾角。考場先看題目附圖，把角度對到公式的定義再代入。", o: { fontSize: 13 } },
    { t: "合力拆分：P_h = P_a cos(δ + θ)、P_v = P_a sin(δ + θ)（本講 θ 定義下）。", o: { fontSize: 13, bold: true, color: C.cl } },
  ]), 0.6, 6.3, 12.1, 0.8, { paraSpaceAfter: 3 });
  pageNo(s, pg);
}
// ───── 9 退化與對帳 ─────
{
  const s = newSlide();
  header(s, "邊界一 · 退化特性", "三個參數各自歸零，Coulomb 都回到 Rankine 的 1/3——兩者不矛盾", C.rk);
  img(s, "fig06_degen", 0.6, 1.4, 12.1, 4.45);
  panel(s, 0.6, 5.95, 12.1, 1.1, C.okbg, "9CC7BC");
  T(s, paras([
    { t: `漂亮的對帳：Coulomb 取 θ = 0、δ = β = 15° → K_a = ${f3(N.KA_C_DB)}，恰等於 Rankine 斜填土的 ${f3(N.KA_RS)}`, o: { bold: true, fontSize: 15, color: C.ok } },
    { t: `Rankine 斜填土＝「牆背摩擦角剛好等於 β」的 Coulomb；若 Coulomb 取 δ = 0（合力垂直牆背），K_a 反而是 ${f3(N.KA_C_B0)}。`, o: { fontSize: 13 } },
  ]), 0.85, 6.05, 11.7, 0.95, { paraSpaceAfter: 3 });
  pageNo(s, pg);
}
// ───── 10 斜填土 ─────
{
  const s = newSlide();
  header(s, "邊界二 · RANKINE 斜填土", "牆背仍垂直光滑，但地表有坡角 β：K_a 要修正，合力要轉向", C.cl);
  img(s, "fig07_slope", 0.6, 1.35, 12.1, 4.2);
  panel(s, 0.6, 5.7, 6.4, 1.35, C.clbg, "E3B894");
  eq(s, "m_ka_rs", 0.8, 5.78, 1.2, 0.6);
  panel(s, 7.2, 5.7, 5.5, 1.35);
  T(s, paras([
    { t: `β = ${N.BETA}°、φ = ${N.PHI}° → K_a = ${f3(N.KA_RS)}`, o: { bold: true, fontSize: 15, color: C.cl } },
    { t: `P_a = ½ × ${f3(N.KA_RS)} × ${N.G} × ${N.H}² = ${f1(N.PA_RS)} kN/m`, o: { fontSize: 14 } },
    { t: `P_h = ${f1(N.PA_RS_H)}、P_v = ${f1(N.PA_RS_V)}（合力平行坡面）`, o: { fontSize: 14, bold: true } },
  ]), 7.4, 5.8, 5.2, 1.2, { paraSpaceAfter: 3 });
  pageNo(s, pg);
}
// ───── 11 β 的邊界 ─────
{
  const s = newSlide();
  header(s, "邊界二 · 物理邊界 β < φ", "β 越接近 φ，K_a 越陡；β ≥ φ 時公式直接失效", C.cl);
  img(s, "fig08_beta", 0.6, 1.4, 12.1, 4.7);
  const cells = [
    ["水平填土", f3(N.KA_R), `P_h = ${f1(N.PA_R)}`, C.rk],
    [`β = ${N.BETA}°`, f3(N.KA_RS), `P_h = ${f1(N.PA_RS_H)}（+${pct(N.PA_RS_H, N.PA_R)}%）`, C.cl],
    ["β → φ", f3(N.KA_RS_LIM), "填土即將自己滑動", C.ps],
  ];
  cells.forEach(([a, b, c, col], i) => {
    const x = 0.6 + i * 4.1;
    panel(s, x, 6.2, 3.9, 0.9);
    T(s, a, x + 0.2, 6.27, 1.5, 0.35, { fontSize: 13, bold: true, color: col });
    T(s, `K_a = ${b}`, x + 1.6, 6.24, 2.2, 0.4, { fontSize: 17, bold: true, color: col });
    T(s, c, x + 0.2, 6.68, 3.6, 0.35, { fontSize: 13, color: C.muted });
  });
  pageNo(s, pg);
}
// ───── 12 被動：位置與位移 ─────
{
  const s = newSlide();
  header(s, "邊界三 · 被動土壓", "被動抗力很大，但要「推得很多」才出得來", C.ps);
  img(s, "fig09_passive", 0.6, 1.4, 12.1, 5.3);
  T(s, "位移比例依土性而異（砂土密實者較小）；重點是數量級：被動所需位移是主動的數倍到數十倍，牆常在那之前就已失效或超過使用限度。",
    0.6, 6.75, 12.1, 0.4, { fontSize: 13, color: C.muted });
  pageNo(s, pg);
}
// ───── 13 K_p 對 φ 敏感 ─────
{
  const s = newSlide();
  header(s, "邊界三 · 對 φ 極度敏感", `φ 高估 10°：K_p 暴增 ${pct(N.KP_R40, N.KP_R).slice(0, 2)}%，K_a 只變 ${f2(N.KA_R - N.KA_R40)}`, C.ps);
  img(s, "fig10_kphi", 0.6, 1.4, 12.1, 4.85);
  panel(s, 0.6, 6.35, 12.1, 0.7, C.psbg, "E6B0AA");
  T(s, "試驗求得的 φ 本來就有幾度的誤差——在主動側幾乎無感，在被動側卻會讓抗力膨脹一半。所以被動側永遠用保守值。",
    0.85, 6.35, 11.7, 0.7, { fontSize: 14, bold: true, color: C.ps, valign: "middle" });
  pageNo(s, pg);
}
// ───── 14 平面解高估 ─────
{
  const s = newSlide();
  header(s, "邊界三 · 幾何過度樂觀", `Coulomb 算被動：δ = 20° 時 K_p = ${f2(N.KP_C)}，是 Rankine 的 ${(N.KP_C / N.KP_R).toFixed(1)} 倍`, C.ps);
  img(s, "fig11_kpdelta", 0.6, 1.4, 12.1, 4.9);
  panel(s, 0.6, 6.35, 12.1, 0.7);
  T(s, "嚴謹設計：被動側改用對數螺線法（或據此製成的 K_p 圖表）；考題若只給公式，用 Rankine（δ = 0）最穩。",
    0.85, 6.35, 11.7, 0.7, { fontSize: 14, bold: true, valign: "middle" });
  pageNo(s, pg);
}
// ───── 15 設計打折 ─────
{
  const s = newSlide();
  header(s, "邊界三 · 設計保護傘", `算得出 ${f1(N.PP_C)}，敢用的只有 ${f1(N.PP_DES)}：被動抗力要層層打折`, C.ps);
  img(s, "fig12_cut", 0.6, 1.35, 12.1, 4.75);
  const cells = [
    ["① 折減係數", "設計值乘 1/2～1/3，或乾脆不計", C.ps],
    ["② 表層忽略", "開挖、擾動、沖刷後可能不存在", C.cl],
    ["③ 幾何別樂觀", "δ 大時不用 Coulomb 平面解", C.rk],
  ];
  cells.forEach(([a, b, col], i) => {
    const x = 0.6 + i * 4.1;
    panel(s, x, 6.2, 3.9, 0.9);
    s.addShape(pres.shapes.RECTANGLE, { x, y: 6.32, w: 0.08, h: 0.66, fill: { color: col }, line: { color: col } });
    T(s, a, x + 0.25, 6.27, 3.5, 0.35, { fontSize: 15, bold: true, color: col });
    T(s, b, x + 0.25, 6.64, 3.6, 0.35, { fontSize: 13 });
  });
  pageNo(s, pg);
}
// ───── 16 全單元貫通 ─────
{
  const s = newSlide();
  header(s, "SYNTHESIS · 四塊拼圖貫通", "任何側向土壓題，都照這個順序串起四塊拼圖", C.ok);
  img(s, "fig13_chain", 0.6, 1.4, 12.1, 3.9);
  panel(s, 0.6, 5.5, 12.1, 1.5);
  T(s, paras([
    { t: "為什麼「邊界」排在第二步？", o: { bold: true, fontSize: 16, color: C.ps } },
    { t: "K 的種類定了（拼圖一）之後，立刻要決定用哪一套 K 公式——Rankine 還是 Coulomb、要不要斜填土修正。", o: { fontSize: 14 } },
    { t: "這一步錯了，後面畫圖、切方塊再精準也是錯的數字；被動側則在最後檢核時再套一次保護傘。", o: { fontSize: 14 } },
  ]), 0.85, 5.62, 11.7, 1.35, { paraSpaceAfter: 4 });
  pageNo(s, pg);
}
// ───── 17 失分點 ─────
{
  const s = newSlide();
  header(s, "MISTAKES · 六個失分點", "三個邊界各有兩個陷阱，全部用示範牆量化", C.ps);
  const items = [
    ["邊界一", "給了 δ 還用 Rankine", `水平推力 ${f1(N.PA_R)} vs ${f1(N.PA_C_H)}，多算 ${pct(N.PA_R, N.PA_C_H)}%（偏保守但不是題目要的答案）`, C.rk],
    ["邊界一", "Coulomb 合力當水平", `${f1(N.PA_C)} 全當水平推力，比 ${f1(N.PA_C_H)} 高估 ${pct(N.PA_C, N.PA_C_H)}%，且漏掉向下的 ${f1(N.PA_C_V)}`, C.rk],
    ["邊界二", "斜填土合力畫成水平", `應平行坡面：P_h = ${f1(N.PA_RS_H)}、P_v = ${f1(N.PA_RS_V)}，不是 ${f1(N.PA_RS)} 全水平`, C.cl],
    ["邊界二", "β ≥ φ 還硬代公式", "根號內為負 → 邊坡本身不穩，應先檢討邊坡穩定", C.cl],
    ["邊界三", "被動抗力全額計入", `需 ${N.DP_LO.toFixed(0)}～${N.DP_HI.toFixed(0)} mm 位移；本例設計只剩 ${f1(N.PP_DES)}（全額 ${f1(N.PP_FULL)} 的 ${(N.PP_DES / N.PP_FULL * 100).toFixed(0)}%）`, C.ps],
    ["邊界三", "δ 大時用 Coulomb 算 K_p", `${f2(N.KP_C)} 是 Rankine ${f2(N.KP_R)} 的 ${(N.KP_C / N.KP_R).toFixed(1)} 倍，偏不安全`, C.ps],
  ];
  items.forEach(([tag, h, b, col], i) => {
    const x = 0.6 + (i % 3) * 4.1, y = 1.55 + Math.floor(i / 3) * 2.7;
    panel(s, x, y, 3.9, 2.5);
    s.addShape(pres.shapes.RECTANGLE, { x, y: y + 0.2, w: 0.09, h: 2.1, fill: { color: col }, line: { color: col } });
    T(s, tag, x + 0.3, y + 0.2, 3.4, 0.3, { fontSize: 12, bold: true, color: col, charSpacing: 2 });
    T(s, h, x + 0.3, y + 0.55, 3.45, 0.75, { fontSize: 18, bold: true });
    T(s, b, x + 0.3, y + 1.3, 3.45, 1.1, { fontSize: 13, color: C.muted });
  });
  pageNo(s, pg);
}
// ───── 18 重點回顧 ─────
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  T(s, "重點回顧", 0.8, 0.8, 11, 0.8, { fontSize: 36, bold: true, color: C.white });
  const pts = [
    ["1", "沒給 δ、θ → Rankine；給了 → Coulomb；三者歸零時兩者相同", C.rk],
    ["2", `Coulomb 合力偏牆背法線 δ：本例水平推力 ${f1(N.PA_C_H)} < Rankine ${f1(N.PA_R)}`, C.cl],
    ["3", "斜填土：K_a 含 cosβ 修正、合力平行坡面、β 必須 < φ", C.cl],
    ["4", `被動：對 φ 敏感（+${pct(N.KP_R40, N.KP_R).slice(0, 2)}%）、要大位移、平面解高估 → 打折、忽略表層`, C.ps],
  ];
  pts.forEach(([n, t, col], i) => {
    const y = 1.95 + i * 1.02;
    s.addShape(pres.shapes.OVAL, { x: 0.8, y, w: 0.6, h: 0.6, fill: { color: col }, line: { color: col } });
    T(s, n, 0.8, y, 0.6, 0.6, { fontSize: 20, bold: true, color: C.white, align: "center", valign: "middle" });
    T(s, t, 1.65, y, 11, 0.6, { fontSize: 19, color: C.white, valign: "middle" });
  });
  T(s, "四塊拼圖到齊：變形 → 邊界 → 土質 → SOP，任何側向土壓題都走這一條路", 0.8, 6.3, 11.5, 0.45, { fontSize: 16, bold: true, color: "F2A65A" });
}
pres.writeFile({ fileName: "SM-U3-1_理論邊界與安全考量.pptx" }).then(() => console.log("written"));
