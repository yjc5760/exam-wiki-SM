const pptxgen = require("pptxgenjs");
const fs = require("fs");
const N = JSON.parse(fs.readFileSync("nums.json", "utf8"));
const MJ = JSON.parse(fs.readFileSync("figs/math.json", "utf8"));
const pres = new pptxgen(); pres.layout = "LAYOUT_WIDE"; pres.title = "SM-U3-1 側向土壓力 四步解題 SOP";
const FT = "Noto Sans CJK TC";
const C = { ink: "1F2A37", muted: "6B7280", panel: "F4F6F9", line: "D5DAE1", ka: "2F54C8", s2: "B8520E",
            s3: "2E7D6B", s4: "C0392B", res: "E4572E", rec: "3B6FD4", tri: "2E9C7A", wat: "0891B2",
            dark: "1B2432", white: "FFFFFF", okbg: "E6F2EF", badbg: "FBECEA", pcbg: "FBF1EA" };
const f1 = v => v.toFixed(1), f2 = v => v.toFixed(2);

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
// 公式：以固定「字級」縮放（0.72 = 投影片上 ~20pt）
function eq(s, name, x, y, H, scale = 0.72, align = "left") {
  const [w, h] = MJ[name]; let iw = w * scale, ih = h * scale;
  if (ih > H) { iw *= H / ih; ih = H; }
  const ix = align === "center" ? x - iw / 2 : x;
  s.addImage({ path: `figs/${name}.svg`, x: ix, y: y + (H - ih) / 2, w: iw, h: ih, altText: name });
  return iw;
}
function header(s, eyebrow, title, col = C.s2) {
  T(s, eyebrow, 0.6, 0.38, 9, 0.3, { fontSize: 12, bold: true, color: col, charSpacing: 2 });
  T(s, title, 0.6, 0.68, 12.2, 0.6, { fontSize: 27, bold: true });
}
function panel(s, x, y, w, h, fill = C.panel, line = C.line) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { color: line, width: 1 }, rectRadius: 0.12 });
}
function pageNo(s, n) { T(s, `${n}`, 12.3, 7.05, 0.5, 0.25, { fontSize: 10, color: "9AA3AE", align: "right" }); }
function newSlide() { const s = pres.addSlide(); s.background = { color: C.white }; return s; }
let pg = 1;

// ───── 1 封面 ─────
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  T(s, "SM-U3-1　側向土壓力理論｜觀念講義・拼圖三", 0.8, 1.3, 11, 0.4, { fontSize: 16, color: "9FB3C8", bold: true });
  T(s, "四步解題 SOP：切方塊 ＋ 對牆底取矩", 0.8, 1.9, 11.8, 1.1, { fontSize: 44, bold: true, color: C.white });
  T(s, "超載、地下水、分層、張力裂縫再多，都走同一條流程——不漏算、不迷路", 0.8, 3.05, 11.5, 0.5, { fontSize: 20, color: "D6DEE8" });
  const dots = [["1", "確定 K", C.ka], ["2", "列轉折點", C.s2], ["3", "逐點算 σ_a", C.s3], ["4", "切方塊取矩", C.s4]];
  dots.forEach(([n, lab, col], i) => {
    const x = 0.8 + i * 3.0;
    s.addShape(pres.shapes.OVAL, { x, y: 4.3, w: 0.62, h: 0.62, fill: { color: col }, line: { color: col } });
    T(s, n, x, 4.3, 0.62, 0.62, { fontSize: 20, bold: true, color: C.white, align: "center", valign: "middle" });
    T(s, lab, x + 0.78, 4.35, 1.9, 0.55, { fontSize: 21, bold: true, color: C.white, valign: "middle" });
    if (i < 3) T(s, "→", x + 2.5, 4.35, 0.4, 0.55, { fontSize: 22, color: "6B7C90", valign: "middle" });
  });
  T(s, `示範題貫穿全篇：H = 7 m、q = 20 kPa、雙層土（K_{a1} = 1/3、K_{a2} = 0.26）；圖上數字全部可對帳`,
    0.8, 6.3, 11.8, 0.4, { fontSize: 14, color: "9FB3C8" });
}
// ───── 2 總覽 ─────
{
  const s = newSlide(); pg++;
  header(s, "OVERVIEW · 四步 SOP", "四步一條龍：每一步的輸出，就是下一步的輸入");
  img(s, "fig01_sop", 0.6, 1.45, 12.1, 3.55);
  panel(s, 0.6, 5.3, 12.1, 1.5);
  T(s, paras([
    { t: "為什麼一定要照順序？", o: { bold: true, fontSize: 17, color: C.s2 } },
    { t: "K 選錯，後面每個數字都錯；轉折點漏一個（最常漏「層界下側」），σ_a 圖就少一塊；", o: { fontSize: 15 } },
    { t: "圖畫對了，最後一步只剩幾何：切成矩形＋三角形，全部對「牆底」取矩——不需要背任何作用點公式。", o: { fontSize: 15 } },
  ]), 0.9, 5.45, 11.5, 1.3, { paraSpaceAfter: 4 });
  pageNo(s, pg);
}
// ───── 3 Step 1 ─────
{
  const s = newSlide(); pg++;
  header(s, "STEP 1 · 確定 K", "先看牆「能不能動、往哪動」，再決定 K_a、K_0 或 K_p", C.ka);
  img(s, "fig02_k", 0.5, 1.35, 12.3, 4.55);
  const cells = [["m_ka", C.ka, "主動：土推牆、牆退開"], ["m_k0", C.s3, "靜止：正常壓密土的近似"], ["m_kp", C.s4, "被動：牆推土、土抵抗"]];
  cells.forEach(([m, col, cap], i) => {
    const x = 0.6 + i * 4.1;
    panel(s, x, 6.0, 3.9, 1.0);
    eq(s, m, x + 0.2, 6.05, 0.62, 0.6);
    T(s, cap, x + 0.2, 6.65, 3.6, 0.3, { fontSize: 12, color: col, bold: true });
  });
  pageNo(s, pg);
}
// ───── 4 Step 2 ─────
{
  const s = newSlide(); pg++;
  header(s, "STEP 2 · 列轉折點", "兩個轉折點之間 σ_a 必為直線——只要算端點", C.s2);
  img(s, "fig03_breaks", 0.4, 1.35, 9.4, 5.15, "left");
  panel(s, 9.95, 1.45, 2.9, 5.45);
  T(s, paras([
    { t: "為什麼只算端點？", o: { bold: true, fontSize: 16, color: C.s2 } },
    { t: "每段內 γ、K、c 都不變，σ_v 隨 z 線性增加 → σ_a 也是直線。", o: { fontSize: 13 } },
    { t: " ", o: { fontSize: 8 } },
    { t: "張力裂縫深度", o: { bold: true, fontSize: 16, color: "7A5C3A" } },
  ]), 10.15, 1.6, 2.6, 2.1, { paraSpaceAfter: 3 });
  eq(s, "m_zc", 10.15, 3.55, 0.75, 0.62);
  T(s, paras([
    { t: "令 σ_a = 0 解出；裂縫內可能積水，題目有說就要加水壓。", o: { fontSize: 13 } },
    { t: " ", o: { fontSize: 8 } },
    { t: "層界＝兩個點", o: { bold: true, fontSize: 16, color: C.s4 } },
    { t: "同一深度、兩個 σ_a：上側用上層 K，下側用下層 K。", o: { fontSize: 13 } },
  ]), 10.15, 4.4, 2.6, 2.4, { paraSpaceAfter: 3 });
  T(s, "①～⑤ 就是完整清單：題目有幾個，σ_a 圖就有幾個「節點」（左圖為示意剖面，曲線由公式實算）。", 0.6, 6.6, 9.3, 0.4, { fontSize: 14, bold: true, color: C.s2 });
  pageNo(s, pg);
}
// ───── 5 Step 3 ─────
{
  const s = newSlide(); pg++;
  header(s, "STEP 3 · 逐點算 σ_a", "有效應力乘 K，孔隙水壓全額另加（不乘 K）", C.s3);
  img(s, "fig04_water", 0.5, 1.35, 12.3, 4.85);
  panel(s, 0.6, 6.2, 12.1, 0.85, C.okbg, "9CC7BC");
  eq(s, "m_sa", 0.85, 6.27, 0.7, 0.62);
  T(s, "K 只管「土粒骨架」傳過來的力；水沒有剪力強度，垂直多少、水平就多少。黏土才有 −2c√K 項。", 3.65, 6.3, 8.9, 0.7, { fontSize: 14, valign: "middle" });
  pageNo(s, pg);
}
// ───── 6 Step 4 原理 ─────
{
  const s = newSlide(); pg++;
  header(s, "STEP 4 · 切方塊取矩", "任何折線分布都拆得成「矩形＋三角形」", C.s4);
  img(s, "fig05_rule", 0.5, 1.4, 12.3, 4.5);
  panel(s, 0.6, 5.95, 5.9, 1.05);
  T(s, "合力", 0.8, 6.05, 1.0, 0.3, { fontSize: 13, bold: true, color: C.s4 });
  eq(s, "m_P", 1.7, 6.08, 0.8, 0.6);
  T(s, "每塊面積就是那一塊的力（kN/m）", 3.2, 6.28, 3.2, 0.4, { fontSize: 13, color: C.muted });
  panel(s, 6.75, 5.95, 5.95, 1.05, C.badbg, "E6B0AA");
  T(s, "作用點", 6.95, 6.05, 1.0, 0.3, { fontSize: 13, bold: true, color: C.s4 });
  eq(s, "m_y", 7.95, 6.0, 0.95, 0.55);
  T(s, "y_i 一律從牆底量——基準只有一個", 9.6, 6.28, 3.0, 0.4, { fontSize: 13, color: C.s4, bold: true });
  pageNo(s, pg);
}
// ───── 7 示範題 ─────
{
  const s = newSlide(); pg++;
  header(s, "WORKED EXAMPLE · 題目", "綜合算例：地表超載 ＋ 雙層土剖面", C.s2);
  img(s, "fig06_problem", 0.4, 1.35, 7.4, 5.6);
  panel(s, 8.0, 1.45, 4.85, 2.25);
  T(s, paras([
    { t: "題目條件", o: { bold: true, fontSize: 17, color: C.s2 } },
    { t: "牆高 H = 7 m，光滑垂直牆背，牆頂可位移", o: { fontSize: 14 } },
    { t: "地表均布超載 q = 20 kPa", o: { fontSize: 14 } },
    { t: "土層 1（0～3 m）：γ_1 = 17 kN/m³，K_{a1} = 1/3", o: { fontSize: 14 } },
    { t: "土層 2（3～7 m）：γ_2 = 19 kN/m³，K_{a2} = 0.26", o: { fontSize: 14 } },
    { t: "求：總側向合力 P 與作用點高度", o: { fontSize: 14, bold: true } },
  ]), 8.2, 1.6, 4.5, 2.05, { paraSpaceAfter: 3 });
  panel(s, 8.0, 3.85, 4.85, 1.35, "EEF2FB", "B9C6EA");
  T(s, paras([
    { t: "Step 1　K 的種類", o: { bold: true, fontSize: 15, color: C.ka } },
    { t: "牆頂可外傾 → 全深度主動，上層 K_{a1} = 1/3、下層 K_{a2} = 0.26", o: { fontSize: 14 } },
  ]), 8.2, 3.97, 4.5, 1.15, { paraSpaceAfter: 3 });
  panel(s, 8.0, 5.35, 4.85, 1.6, C.pcbg, "E3B894");
  T(s, paras([
    { t: "Step 2　轉折點", o: { bold: true, fontSize: 15, color: C.s2 } },
    { t: "z = 0（地表）、z = 3 m 上側、z = 3 m 下側、z = 7 m（牆底）", o: { fontSize: 14 } },
    { t: "本題無水位、無凝聚力 → 沒有 u、沒有裂縫", o: { fontSize: 13, color: C.muted } },
  ]), 8.2, 5.47, 4.5, 1.45, { paraSpaceAfter: 3 });
  pageNo(s, pg);
}
// ───── 8 Step 3 逐點 ─────
{
  const s = newSlide(); pg++;
  header(s, "WORKED EXAMPLE · STEP 3", "先畫 σ_v（連續），再乘各層的 K 得 σ_a", C.s3);
  img(s, "fig07_points", 0.35, 1.45, 8.6, 5.4);
  const rows = [
    ["① z = 0", "σ_v = q = 20", `σ_a = 1/3 × 20 = ${f2(N.SA0)}`],
    ["② z = 3 m 上側", "σ_v = 20 + 17×3 = 71", `σ_a = 1/3 × 71 = ${f2(N.SA3m)}`],
    ["③ z = 3 m 下側", "σ_v 仍為 71", `σ_a = 0.26 × 71 = ${f2(N.SA3p)}`],
    ["④ z = 7 m", "σ_v = 71 + 19×4 = 147", `σ_a = 0.26 × 147 = ${f2(N.SA7)}`],
  ];
  rows.forEach(([a, b, c], i) => {
    const y = 1.5 + i * 1.3;
    panel(s, 9.15, y, 3.7, 1.18, i === 2 ? C.badbg : C.panel, i === 2 ? "E6B0AA" : C.line);
    T(s, paras([
      { t: a, o: { bold: true, fontSize: 14, color: C.s4 } },
      { t: b, o: { fontSize: 13, color: C.muted } },
      { t: c + " kPa", o: { fontSize: 15, bold: true } },
    ]), 9.3, y + 0.1, 3.45, 1.0, { paraSpaceAfter: 2 });
  });
  T(s, "牆底也可寫成 18.46 + 0.26×(19×4) = 18.46 + 19.76 = 38.22，兩種算法同值。", 0.6, 6.8, 8.4, 0.35, { fontSize: 12, color: C.muted });
  pageNo(s, pg);
}
// ───── 9 界面跳動 ─────
{
  const s = newSlide(); pg++;
  header(s, "WORKED EXAMPLE · 關鍵", "界面上下：σ_v 連續，σ_a 跳動", C.s4);
  img(s, "fig08_jump", 0.5, 1.4, 12.3, 5.0);
  T(s, "口訣：「垂直看土重、水平看 K」——土重不會突然變，K 會。", 0.6, 6.5, 12, 0.45, { fontSize: 17, bold: true, color: C.s3 });
  pageNo(s, pg);
}
// ───── 10 切方塊圖 ─────
{
  const s = newSlide(); pg++;
  header(s, "WORKED EXAMPLE · STEP 4", "切成 A、B、C、D 四塊，每塊的形心高度都從牆底量", C.s4);
  img(s, "fig09_blocks", 0.4, 1.35, 9.6, 5.7);
  const pts = [
    ["A　上層矩形", "超載 q 在上層造成的均布段", C.rec],
    ["B　上層三角形", "上層土重 17×z 的增量", C.tri],
    ["C　下層矩形", "上覆 71 kPa（q＋上層土）× K_{a2}", C.rec],
    ["D　下層三角形", "下層土重 19×z 的增量", C.tri],
  ];
  pts.forEach(([h, b, col], i) => {
    const y = 1.5 + i * 1.3;
    panel(s, 10.15, y, 2.7, 1.15);
    T(s, h, 10.3, y + 0.12, 2.5, 0.35, { fontSize: 15, bold: true, color: col });
    T(s, b, 10.3, y + 0.5, 2.45, 0.6, { fontSize: 12 });
  });
  pageNo(s, pg);
}
// ───── 11 取矩表 ─────
{
  const s = newSlide(); pg++;
  header(s, "WORKED EXAMPLE · 取矩表", "一張表算完：P = ΣP_i，ȳ = ΣP_i·y_i / ΣP_i", C.s4);
  const hd = { bold: true, color: C.white, fill: { color: C.dark }, fontFace: FT, fontSize: 14, align: "center", valign: "middle" };
  const cl = { fontFace: FT, fontSize: 14, color: C.ink, align: "center", valign: "middle" };
  const exprs = {
    A: `${f2(N.SA0)} × 3`, B: `½ × (${f2(N.SA3m)} − ${f2(N.SA0)}) × 3`,
    C: `${f2(N.SA3p)} × 4`, D: `½ × (${f2(N.SA7)} − ${f2(N.SA3p)}) × 4`,
  };
  const yexp = { A: "4 + 3/2", B: "4 + 3/3", C: "4/2", D: "4/3" };
  const rows = [[
    { text: "方塊", options: hd }, { text: "合力算式", options: hd }, { text: runs("P_i (kN/m)", hd), options: hd },
    { text: runs("y_i 算式", hd), options: hd }, { text: runs("y_i (m)", hd), options: hd }, { text: runs("P_i·y_i (kN·m/m)", hd), options: hd }]];
  N.BLOCKS.forEach((b, i) => {
    const col = b.shape === "rect" ? C.rec : C.tri;
    const fill = { color: i % 2 ? "F7F8FA" : C.white };
    rows.push([
      { text: b.k, options: { ...cl, bold: true, color: col, fill } },
      { text: exprs[b.k], options: { ...cl, fill } },
      { text: f2(b.P), options: { ...cl, bold: true, fill } },
      { text: yexp[b.k], options: { ...cl, color: C.muted, fill } },
      { text: f2(b.y), options: { ...cl, fill } },
      { text: f2(b.P * b.y), options: { ...cl, bold: true, fill } },
    ]);
  });
  const sm = { ...cl, bold: true, color: C.res, fill: { color: "FDF0EB" } };
  rows.push([{ text: "Σ", options: sm }, { text: "", options: sm }, { text: f2(N.P), options: sm },
             { text: "", options: sm }, { text: "", options: sm }, { text: f2(N.M), options: sm }]);
  s.addTable(rows, { x: 0.6, y: 1.5, w: 12.1, colW: [0.9, 3.6, 1.6, 1.8, 1.4, 2.8], rowH: 0.52,
                     border: { type: "solid", pt: 0.75, color: "D5DAE1" } });
  panel(s, 0.6, 5.0, 6.6, 1.9, "1B2432", "1B2432");
  T(s, "作用點（自牆底起算）", 0.85, 5.12, 4, 0.3, { fontSize: 13, bold: true, color: "9FB3C8" });
  const iw = eq(s, "m_ynum_w", 0.85, 5.45, 1.0, 0.72);
  T(s, `P = ${f1(N.P)} kN/m　ȳ = ${f2(N.YBAR)} m`, 0.85, 6.45, 6.2, 0.38, { fontSize: 17, bold: true, color: "F2A65A" });
  panel(s, 7.4, 5.0, 5.3, 1.9, C.okbg, "9CC7BC");
  T(s, paras([
    { t: "對帳：直接積分", o: { bold: true, fontSize: 15, color: C.s3 } },
    { t: `∫σ_a dz = ${f2(N.P)} kN/m、∫σ_a(H−z) dz = ${f2(N.M)} kN·m/m`, o: { fontSize: 13 } },
    { t: "與切方塊結果完全相同——切法只是把積分換成幾何。", o: { fontSize: 13, color: C.muted } },
  ]), 7.6, 5.15, 5.0, 1.7, { paraSpaceAfter: 4 });
  pageNo(s, pg);
}
// ───── 12 H/3 對照 ─────
{
  const s = newSlide(); pg++;
  header(s, "WARNING · 反射性寫 H/3", `ȳ 寫成 H/3：作用點低 ${f2(N.YBAR - N.Y_H3)} m，傾覆力矩少算 ${(N.UNDER * 100).toFixed(0)}%`, C.s4);
  img(s, "fig10_h3", 0.5, 1.4, 12.3, 4.7);
  panel(s, 0.6, 6.05, 12.1, 0.95, C.badbg, "E6B0AA");
  T(s, paras([
    { t: "H/3 只屬於「單層、無超載、無水」的純三角形。", o: { bold: true, fontSize: 15, color: C.s4 } },
    { t: "超載的矩形塊作用在 H/2、上層方塊又墊高了 4 m——合力自然被往上拉。", o: { fontSize: 14 } },
  ]), 0.85, 6.13, 11.7, 0.85, { paraSpaceAfter: 3 });
  pageNo(s, pg);
}
// ───── 13 一秒驗算 ─────
{
  const s = newSlide(); pg++;
  header(s, "CHECK · 一秒驗算", "什麼時候能直接寫 H/3、H/2？其餘一律切方塊", C.s3);
  img(s, "fig11_when", 0.5, 1.4, 12.3, 4.45);
  panel(s, 0.6, 6.0, 5.2, 1.0);
  T(s, "梯形公式", 0.8, 6.08, 1.4, 0.3, { fontSize: 13, bold: true, color: C.s3 });
  eq(s, "m_trap", 2.1, 6.05, 0.9, 0.62);
  T(s, "a：頂端壓力\nb：底端壓力", 4.1, 6.15, 1.6, 0.7, { fontSize: 12, color: C.muted });
  panel(s, 6.0, 6.0, 6.7, 1.0, C.okbg, "9CC7BC");
  T(s, "無張力裂縫、σ_a 大致隨深度增加時，ȳ 應落在 H/3～H/2 之間；算出來跑出這個範圍，先回頭檢查切塊與 y_i。",
    6.2, 6.08, 6.35, 0.85, { fontSize: 13, valign: "middle" });
  pageNo(s, pg);
}
// ───── 14 常見錯誤 ─────
{
  const s = newSlide(); pg++;
  header(s, "MISTAKES · 六個失分點", "每一步各有一個陷阱，對照 SOP 逐項檢查", C.s4);
  const items = [
    ["STEP 1", "地下室外牆用了 K_a", "受樓板約束不能動 → 應用 K_0；K_a 會低估側壓", C.ka],
    ["STEP 2", "層界只算一次", `23.67 直接往下接，本例 P 變成 ${f1(N.P_wrong_iface)}，多算 ${((N.P_wrong_iface - N.P) / N.P * 100).toFixed(0)}%`, C.s2],
    ["STEP 2", "漏掉張力裂縫", "黏土頂部 σ_a 為負，不能當成拉力抵銷下方推力", C.s2],
    ["STEP 3", "水壓也乘了 K", `小例中牆底少算 ${f1(N.tot - N.wrong)} kPa（${((N.tot - N.wrong) / N.tot * 100).toFixed(0)}%）`, C.s3],
    ["STEP 3", "下層忘了上覆壓力", "C 塊是 K_{a2} × 71，不是 K_{a2} × 20（超載）而已", C.s3],
    ["STEP 4", "y_i 從層底量、或直接寫 H/3", `作用點基準只有牆底；H/3 使 M 少算 ${(N.UNDER * 100).toFixed(0)}%`, C.s4],
  ];
  items.forEach(([tag, h, b, col], i) => {
    const x = 0.6 + (i % 3) * 4.1, y = 1.55 + Math.floor(i / 3) * 2.7;
    panel(s, x, y, 3.9, 2.5);
    s.addShape(pres.shapes.RECTANGLE, { x, y: y + 0.2, w: 0.09, h: 2.1, fill: { color: col }, line: { color: col } });
    T(s, tag, x + 0.3, y + 0.2, 3.4, 0.3, { fontSize: 12, bold: true, color: col, charSpacing: 2 });
    T(s, h, x + 0.3, y + 0.55, 3.45, 0.75, { fontSize: 18, bold: true });
    T(s, b, x + 0.3, y + 1.35, 3.45, 1.05, { fontSize: 13, color: C.muted });
  });
  pageNo(s, pg);
}
// ───── 15 重點回顧 ─────
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  T(s, "重點回顧", 0.8, 0.8, 11, 0.8, { fontSize: 36, bold: true, color: C.white });
  const pts = [
    ["1", "確定 K：牆外傾 K_a、受約束 K_0、推向土 K_p", C.ka],
    ["2", "列轉折點：地表、裂縫 z_c、水位、層界（上下各一次）、牆底", C.s2],
    ["3", "逐點算 σ_a：有效應力 × K，孔隙水壓 u 全額另加", C.s3],
    ["4", `切方塊對牆底取矩：本例 P = ${f1(N.P)} kN/m、ȳ = ${f2(N.YBAR)} m（不是 H/3）`, C.s4],
  ];
  pts.forEach(([n, t, col], i) => {
    const y = 1.95 + i * 1.02;
    s.addShape(pres.shapes.OVAL, { x: 0.8, y, w: 0.6, h: 0.6, fill: { color: col }, line: { color: col } });
    T(s, n, 0.8, y, 0.6, 0.6, { fontSize: 20, bold: true, color: C.white, align: "center", valign: "middle" });
    T(s, t, 1.65, y, 11, 0.6, { fontSize: 19, color: C.white, valign: "middle" });
  });
  T(s, "下一塊拼圖：黏土張力裂縫 ＋ 地下水位的綜合題——轉折點清單會多出 ② 與 ③", 0.8, 6.3, 11.5, 0.45, { fontSize: 16, bold: true, color: "F2A65A" });
}
pres.writeFile({ fileName: "SM-U3-1_四步解題SOP.pptx" }).then(() => console.log("written"));
