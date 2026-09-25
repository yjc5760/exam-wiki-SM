const pptxgen = require("pptxgenjs");
const fs = require("fs");
const N = JSON.parse(fs.readFileSync("nums.json", "utf8"));
const MJ = JSON.parse(fs.readFileSync("figs/math.json", "utf8"));
const pres = new pptxgen(); pres.layout = "LAYOUT_WIDE"; pres.title = "SM-U1-5 拼圖四：NC / OC 分岔";
const FT = "Noto Sans CJK TC";
const C = { ink: "1F2A37", muted: "6B7280", panel: "F4F6F9", line: "D5DAE1", eff: "E4572E", tot: "2F54C8", le: "6D4BC2",
            ps: "C0392B", ok: "2E7D6B", dark: "1B2432", white: "FFFFFF", gold: "B7791F",
            effbg: "FDEDE8", totbg: "EEF2FB", psbg: "FBECEA", okbg: "E6F2EF", lebg: "F1EDFA", goldbg: "FBF3E4" };
const f1 = v => (v + 1e-9).toFixed(1), f2 = v => (v + 1e-9).toFixed(2), f3 = v => (v + 1e-9).toFixed(3), f4 = v => (v + 1e-9).toFixed(4);
const f0 = v => Math.round(v).toString();
const sg = v => (v < 0 ? "−" + f0(-v) : "+" + f0(v));

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
function eq(s, name, x, y, H, scale = 0.72, align = "left", maxW = 99) {
  const [w, h] = MJ[name]; let iw = w * scale, ih = h * scale;
  if (ih > H) { iw *= H / ih; ih = H; }
  if (iw > maxW) { ih *= maxW / iw; iw = maxW; }
  const ix = align === "center" ? x - iw / 2 : x;
  s.addImage({ path: `figs/${name}.svg`, x: ix, y: y + (H - ih) / 2, w: iw, h: ih, altText: name });
  return iw;
}
function header(s, eyebrow, title, col = C.eff) {
  T(s, eyebrow, 0.6, 0.38, 11, 0.3, { fontSize: 12, bold: true, color: col, charSpacing: 2 });
  T(s, title, 0.6, 0.68, 12.2, 0.6, { fontSize: 26, bold: true });
}
function panel(s, x, y, w, h, fill = C.panel, line = C.line) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { color: line, width: 1 }, rectRadius: 0.12 });
}
function bar(s, x, y, h, col) { s.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.08, h, fill: { color: col }, line: { color: col } }); }
function pageNo(s, n) { T(s, `${n}`, 12.3, 7.08, 0.5, 0.25, { fontSize: 10, color: "9AA3AE", align: "right" }); }
Object.assign(C, { uu: "C0392B", cu: "E07B39", cd: "2E7D6B", uubg: "FBECEA", cubg: "FDF1E7", cdbg: "E6F2EF", pur: "6D4BC2", purbg: "F1EDFA", water: "2C6E9E" });
let pg = 1;
function newSlide() { const s = pres.addSlide(); s.background = { color: C.white }; pg++; return s; }
// 圖＋底部 1～3 格說明
function figSlide(eyebrow, title, fig, cells, col = C.eff, figH = 4.45) {
  const s = newSlide();
  header(s, eyebrow, title, col);
  img(s, fig, 0.6, 1.4, 12.1, figH);
  const n = cells.length, gap = 0.15, w = (12.1 - gap * (n - 1)) / n, y = 1.5 + figH, h = 7.05 - y;
  cells.forEach(([hd, body, c, bg, ln], i) => {
    const x = 0.6 + i * (w + gap);
    panel(s, x, y, w, h, bg || C.panel, ln || C.line);
    T(s, paras([{ t: hd, o: { bold: true, fontSize: 14, color: c || C.ink } }, ...body.map(t => ({ t, o: { fontSize: 13 } }))]),
      x + 0.2, y + 0.08, w - 0.35, h - 0.12, { paraSpaceAfter: 2 });
  });
  pageNo(s, pg);
  return s;
}


// 公式面板：標題＋一條公式
function eqPanel(s, x, y, w, h, title, name, col, bg, ln, note) {
  panel(s, x, y, w, h, bg || C.panel, ln || C.line);
  T(s, title, x + 0.2, y + 0.1, w - 0.4, 0.32, { fontSize: 14, bold: true, color: col || C.ink });
  const eh = note ? h - 0.95 : h - 0.55;
  eq(s, name, x + 0.2, y + 0.45, eh, 0.6, "left", w - 0.4);
  if (note) T(s, note, x + 0.2, y + h - 0.42, w - 0.4, 0.34, { fontSize: 12, color: C.muted });
}
const n2 = v => f2(v);
// ───── 1 封面 ─────
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  T(s, "SM-U1-5　土壤強度｜觀念講義・拼圖四", 0.8, 1.2, 11, 0.4, { fontSize: 16, color: "9FB3C8", bold: true });
  T(s, "NC 還是 OC？決定 c′ 是不是 0", 0.8, 1.8, 11.8, 1.1, { fontSize: 44, bold: true, color: C.white });
  T(s, "包絡線過不過原點，決定你能不能用「相似形比例法」秒殺整題；c′ ≠ 0 時，回到萬能式與相減法", 0.8, 3.0, 11.8, 0.9, { fontSize: 20, color: "D6DEE8" });
  const dots = [["NC", "c′ = 0 → 過原點 → 三大捷徑", "7FC8B4"], ["OC", "c′ ≠ 0 → 有截距 → 萬能式", "F08A7E"], ["共用", "K_p 互推＋兩組相減", "F2A65A"]];
  dots.forEach(([n, lab, col], i) => {
    const x = 0.8 + i * 4.0;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 4.35, w: 3.7, h: 0.8, fill: { color: "243044" }, line: { color: col, width: 2 }, rectRadius: 0.1 });
    T(s, n, x + 0.15, 4.35, 0.85, 0.8, { fontSize: 20, bold: true, color: col, valign: "middle" });
    T(s, runs(lab, { color: C.white, bold: true, fontSize: 14 }), x + 1.0, 4.35, 2.65, 0.8, { valign: "middle" });
  });
  T(s, "示範題：NC [SM-2018-2]、OC [SM-2024-1]（單組）、[SM-2025-2]（兩組相減）；圖上數字全部由同一支程式算出，可逐一對帳",
    0.8, 6.3, 11.8, 0.4, { fontSize: 14, color: "9FB3C8" });
}
// ───── 2 總覽 ─────
figSlide("OVERVIEW · 解題大分岔", "讀題第一件事：這顆黏土的包絡線過不過原點？", "fig01_fork", [
  ["關鍵字 → NC", ["「正常壓密」「OCR = 1」「首次加載」→ 立刻寫下 c′ = 0、c_{cu} = 0"], C.ok, C.okbg, "9CC7BC"],
  ["沒寫、或給了 c′ → OC", ["題目給 c′、或兩組數據不成比例 → 走萬能式，不准用比例法"], C.ps, C.psbg, "EBB4AE"],
], C.eff, 4.55);
// ───── 3 應力歷史 ─────
figSlide("底層物理 ① · 應力歷史", "NC 與 OC 的差別，在於土壤「記不記得」更大的應力", "fig02_history", [
  ["NC：OCR = 1", ["現在的 σ′_0 就是歷史最大有效應力，站在原始壓縮線上"], C.ok, C.okbg, "9CC7BC"],
  ["OC：OCR > 1", ["曾經壓到 σ′_p 再卸載：同樣 σ′_0 之下，孔隙比更小、更密實"], C.ps, C.psbg, "EBB4AE"],
], C.eff, 4.5);
// ───── 4 微觀 ─────
figSlide("底層物理 ② · 微觀真相", "「壓密記憶」在包絡線上表現為截距 c′", "fig03_micro", [
  ["NC 顆粒", ["沒有被更大應力擠壓過 → 無額外咬合 → c′ = 0，包絡線過原點"], C.ok, C.okbg, "9CC7BC"],
  ["OC 顆粒", ["緊密嵌鎖的排列被保留下來 → 重新剪切時多出強度截距 c′ ≠ 0"], C.ps, C.psbg, "EBB4AE"],
], C.eff, 4.5);
// ───── 5 位似 ─────
figSlide("莫爾圓幾何 ① · NC 位似", "包絡線過原點 → 所有破壞圓以原點為位似中心，互為相似形", "fig04_homo", [
  ["幾何相似代表什麼", ["σ′_3、σ′_1、C、R、Δσ_d、u_f 全部成固定比例：圍壓 × k，整張圖 × k"], C.ok, C.okbg, "9CC7BC"],
  ["[SM-2018-2] 驗證", [`有效圓 33～118 與 82.5～295：每一格比值都是 2.5，sin φ′ 完全相同`], C.gold, C.goldbg, "E6CFA0"],
], C.ok, 4.5);
// ───── 6 OC 不相似 ─────
figSlide("莫爾圓幾何 ② · OC 不相似", "有截距 c′：圍壓加倍，軸差應力不會加倍", "fig05_oc", [
  ["[SM-2024-1] 正解", [`σ′_3 = 200：σ′_1 = ${n2(N.O_S1B)}，Δσ_d = ${n2(N.O_DSDB)} kPa`], C.ok, C.okbg, "9CC7BC"],
  ["硬套比例法", [`240 × 2 = 480：高估 ${f1(N.O_OVER)}%，圓衝出包絡線，物理上不可能`], C.ps, C.psbg, "EBB4AE"],
], C.ps, 4.5);
// ───── 7 σ1–σ3 平面 ─────
figSlide("換個座標看 · σ′_1–σ′_3 平面", "比例法 = 假設破壞線過原點；OC 的誤差剛好是一個截距", "fig06_lines", [
  ["一條直線兩個參數", ["斜率 K_p（摩擦）、截距 2c′√K_p（凝聚）：c′ = 0 才過原點"], C.gold, C.goldbg, "E6CFA0"],
  ["誤差 = 截距", [`2 × 340 − ${n2(N.O_S1B)} = ${n2(N.O_ICPT)} = 2c′√K_p：圍壓加倍時截距被多算一次`], C.ps, C.psbg, "EBB4AE"],
], C.gold, 4.5);
// ───── 8 捷徑矩陣 ─────
figSlide("四大捷徑 · 適用範圍", "捷徑 1～3 是 NC 專用；捷徑 4 兩邊通用", "fig07_matrix", [
  ["一句話記住", ["只要用到「過原點」這個性質的捷徑（正弦式、比例法、S_u 比值）就是 NC 專用；相減法本來就是為了消去 c′ 而生"], C.ink],
], C.eff, 4.85);
// ───── 9 捷徑 1 ─────
{
  const s = figSlide("捷徑 1 · 正弦式", "c′ = 0：半徑 ÷ 圓心距 = sin φ，一秒出角度", "fig08_sine", [], C.eff, 4.3);
  eqPanel(s, 0.6, 5.85, 4.1, 1.2, "有效應力", "m_sin", C.eff, C.effbg, "F2B8A6");
  eqPanel(s, 4.85, 5.85, 3.6, 1.2, "總應力（NC 的 c_{cu} = 0）", "m_sincu", C.tot, C.totbg, "B9C6EA");
  panel(s, 8.6, 5.85, 4.1, 1.2, C.panel);
  T(s, paras([
    { t: "[SM-2018-2] 第二小題", o: { bold: true, fontSize: 14 } },
    { t: `φ_{cu} = ${n2(N.N_PHICU)}°、φ′ = ${n2(N.N_PHI)}°`, o: { fontSize: 14, bold: true, color: C.eff } },
    { t: "OC 硬套：R/C 不等於 sin φ′（拼圖三）", o: { fontSize: 12, color: C.ps } },
  ]), 8.8, 5.93, 3.8, 1.05, { paraSpaceAfter: 2 });
}
// ───── 10 捷徑 2 ─────
{
  const s = figSlide("捷徑 2 · 相似形比例法", "換圍壓求新軸差應力：不查角度，3 秒比例放大", "fig09_ratio", [], C.gold, 4.35);
  eqPanel(s, 0.6, 5.9, 5.0, 1.15, "比例式（c′ = 0 才成立）", "m_ratio", C.gold, C.goldbg, "E6CFA0");
  eqPanel(s, 5.75, 5.9, 6.95, 1.15, "[SM-2018-2] 第一小題", "m_n3", C.ok, C.okbg, "9CC7BC");
}
// ───── 11 捷徑 3 ─────
{
  const s = figSlide("捷徑 3 · 不排水強度比", "S_u/σ′_{v0} 固定：NC 黏土的 S_u 隨深度線性成長（SHANSEP 雛形）", "fig10_su", [], C.ok, 4.3);
  eqPanel(s, 0.6, 5.85, 3.9, 1.2, "課本式（A_f = 1）", "m_su", C.ok, C.okbg, "9CC7BC");
  eqPanel(s, 4.65, 5.85, 4.4, 1.2, "一般式（拼圖二推導延伸）", "m_sug", C.tot, C.totbg, "B9C6EA");
  panel(s, 9.2, 5.85, 3.5, 1.2, C.panel);
  T(s, paras([
    { t: "物理前提", o: { bold: true, fontSize: 14 } },
    { t: "課本式假設破壞時有效圓右緣 = σ′_{v0}", o: { fontSize: 12 } },
    { t: "題目給了 u_f 或 A_f → 用一般式", o: { fontSize: 12, bold: true, color: C.tot } },
  ]), 9.4, 5.93, 3.2, 1.05, { paraSpaceAfter: 2 });
}
// ───── 12 捷徑 4a ─────
{
  const s = figSlide("捷徑 4a · K_p ↔ φ′ 互推", "有 K_p 就有 φ′：純三角恆等式，NC、OC 都成立", "fig11_kp", [], C.gold, 4.3);
  eqPanel(s, 0.6, 5.85, 6.6, 1.2, "正向", "m_kp", C.gold, C.goldbg, "E6CFA0");
  eqPanel(s, 7.35, 5.85, 5.35, 1.2, "反向（最後報告時才用）", "m_phi", C.eff, C.effbg, "F2B8A6");
}
// ───── 13 捷徑 4b ─────
{
  const s = figSlide("捷徑 4b · 兩組試驗相減法", "兩點決定一條直線：相減消去截距，一步得到 K_p", "fig12_subtract", [], C.gold, 4.3);
  panel(s, 0.6, 5.85, 5.6, 1.2, C.panel);
  eq(s, "m_sa", 0.85, 5.92, 0.5, 0.5, "left", 5.2);
  eq(s, "m_sb", 0.85, 6.47, 0.5, 0.5, "left", 5.2);
  eqPanel(s, 6.35, 5.85, 3.3, 1.2, "兩式相減", "m_sub", C.gold, C.goldbg, "E6CFA0");
  panel(s, 9.8, 5.85, 2.9, 1.2, C.okbg, "9CC7BC");
  T(s, paras([
    { t: "再回代任一式", o: { bold: true, fontSize: 14, color: C.ok } },
    { t: "得截距 2c′√K_p", o: { fontSize: 13 } },
    { t: "需要時才拆出 c′", o: { fontSize: 13, color: C.muted } },
  ]), 10.0, 5.93, 2.6, 1.05, { paraSpaceAfter: 2 });
}
// ───── 14 OC SOP ─────
figSlide("代公式 SOP ① · OC 黏土（c′ ≠ 0）", "列萬能式 → 看數據組數 → 保留 K_p 往下代 → 最後才轉角度", "fig14_ocsop", [
  ["口訣", ["兩組相減、單組解二次；K_p 不離手，角度最後走"], C.ink],
], C.ps, 4.85);
// ───── 15 SM-2025-2 ─────
{
  const s = figSlide("實戰 · [SM-2025-2] 兩組 CU → CD 外推", "先扣 u 變有效應力，兩式相減，保留 K_p 與截距直接代", "fig13_2025", [], C.gold, 3.75);
  panel(s, 0.6, 5.3, 12.1, 1.75, C.panel);
  eq(s, "m_q1", 0.85, 5.36, 0.46, 0.5, "left", 5.8);
  eq(s, "m_q2", 0.85, 5.86, 0.66, 0.5, "left", 5.8);
  eq(s, "m_q3", 0.85, 6.5, 0.48, 0.5, "left", 5.8);
  panel(s, 7.0, 5.42, 5.55, 1.5, C.goldbg, "E6CFA0");
  T(s, "若題目還要報告參數（非本題所問）", 7.2, 5.5, 5.2, 0.3, { fontSize: 13, bold: true, color: C.gold });
  eq(s, "m_q4", 7.2, 5.85, 0.95, 0.5, "left", 5.2);
}
// ───── 16 SM-2024-1 ─────
{
  const s = newSlide();
  header(s, "實戰 · [SM-2024-1] 單組 CD → 圍壓 200 外推", "只有一組數據但已知 c′：令 y = √K_p 解二次式", C.ps);
  const rows = [["Step 1–2　萬能式代入第一組", "m_o1", C.ps, C.psbg, "EBB4AE"],
                ["Step 3　保留 √K_p 代新圍壓", "m_o2", C.gold, C.goldbg, "E6CFA0"],
                ["答案", "m_o3", C.ok, C.okbg, "9CC7BC"]];
  rows.forEach(([t, m, col, bg, ln], i) => {
    const y = 1.5 + i * 1.45;
    panel(s, 0.6, y, 12.1, 1.3, bg, ln);
    T(s, t, 0.85, y + 0.12, 3.6, 1.0, { fontSize: 16, bold: true, color: col, valign: "middle" });
    eq(s, m, 4.75, y + 0.2, 0.9, 0.62, "left", 7.75);
  });
  panel(s, 0.6, 5.95, 12.1, 1.1, C.dark, C.dark);
  T(s, paras([
    { t: `對照：硬套比例法 240 × 2 = 480（高估 ${f1(N.O_OVER)}%）`, o: { fontSize: 15, bold: true, color: "F08A7E" } },
    { t: `φ′ = ${n2(N.O_PHI)}° 只在最後報告時計算；若先取 26° 再轉回 K_p，σ′_1 會少 3.9 kPa（拼圖三）`, o: { fontSize: 13, color: "D6DEE8" } },
  ]), 0.85, 6.0, 11.6, 1.0, { valign: "middle", paraSpaceAfter: 4 });
  pageNo(s, pg);
}
// ───── 17 NC SOP ─────
figSlide("代公式 SOP ② · NC 黏土（c′ = 0）", "[SM-2018-2]：宣告 c′ = 0 之後，四小題全部秒殺", "fig15_ncsop", [
  ["先後順序", ["先做第二小題（角度），第一小題用比例法 3 秒；破壞面只用 φ′；最後 A_f 一併做閉合檢核"], C.ok, C.okbg, "9CC7BC"],
], C.ok, 4.85);
// ───── 18 陷阱 1 ─────
figSlide("高頻陷阱 1", "OC 黏土硬套比例法：三個考題的實際代價", "fig16_trap1", [
  ["為什麼一定高估", ["比例法把固定截距 2c′√K_p 也一起放大；c′ > 0 時放大越多、錯越多"], C.ps, C.psbg, "EBB4AE"],
  ["考場判斷", ["兩組數據若 Δσ_d/σ_3 不相等（75→40、150→70），就證明不是 NC"], C.gold, C.goldbg, "E6CFA0"],
], C.ps, 4.5);
// ───── 19 陷阱 2 ─────
figSlide("高頻陷阱 2", "取樣擾動與壓密不足：量到的 c′ > 0 可能是「虛擬凝聚力」", "fig17_fake", [
  ["先算 σ′_{v0}", ["題目給取樣深度 z → σ′_{v0} = Σγ′h，再和實驗室壓密壓力 σ′_c 比較"], C.gold, C.goldbg, "E6CFA0"],
  ["σ′_c < σ′_{v0}", ["試體形同人造 OC：拿假 c′ 去設計現地 NC 土，會高估強度（偏不安全）"], C.ps, C.psbg, "EBB4AE"],
], C.ps, 4.5);
// ───── 20 陷阱 3 ─────
figSlide("高頻陷阱 3 ＋ 免費雙重驗算", "比值有天花板、切點要在線上、A_f 要落在合理區間", "fig18_checks", [
  ["S_u/σ′_{v0} 天花板", ["課本式 < 0.5；一般 NC 約 0.2～0.35"], C.ink],
  ["切點檢核", ["τ_{ff} = c′ + σ′_{ff} tan φ′"], C.ok, C.okbg, "9CC7BC"],
  ["A_f 檢核", ["NC：A_f = u_f/Δσ_d 在 0.5～1.0"], C.tot, C.totbg, "B9C6EA"],
], C.ps, 4.5);
// ───── 21 速查 ─────
{
  const s = newSlide();
  header(s, "考場速查", "寫答案前，四格各花 5 秒", C.ps);
  const cards = [
    ["1", "NC 還是 OC？", ["關鍵字：正常壓密、OCR = 1、首次加載", "不確定 → 看兩組 Δσ_d/σ_3 是否相等"], C.ok, C.okbg, "9CC7BC"],
    ["2", "比例法用對了嗎？", ["只有 c′ = 0 才能用", `OC 硬套：[SM-2024-1] 高估 ${f1(N.O_OVER)}%`], C.ps, C.psbg, "EBB4AE"],
    ["3", "c′ 是真的嗎？", ["σ′_c < σ′_{v0} → 虛擬凝聚力", "設計會偏於不安全"], C.gold, C.goldbg, "E6CFA0"],
    ["4", "驗算過了嗎？", ["S_u/σ′_{v0} < 0.5、A_f 0.5～1.0", "切點落在包絡線上"], C.tot, C.totbg, "B9C6EA"],
  ];
  cards.forEach(([n, hd, body, col, bg, ln], i) => {
    const x = 0.6 + i * 3.05;
    panel(s, x, 1.55, 2.9, 5.0, bg, ln);
    s.addShape(pres.shapes.OVAL, { x: x + 0.25, y: 1.8, w: 0.7, h: 0.7, fill: { color: col }, line: { color: col } });
    T(s, n, x + 0.25, 1.8, 0.7, 0.7, { fontSize: 24, bold: true, color: C.white, align: "center", valign: "middle" });
    T(s, hd, x + 0.25, 2.7, 2.5, 0.9, { fontSize: 18, bold: true, color: col });
    T(s, paras(body.map((t, k) => ({ t, o: { fontSize: 14, bold: k === 0, color: k === 1 ? C.muted : C.ink } }))), x + 0.25, 3.7, 2.45, 2.7, { paraSpaceAfter: 10 });
  });
  T(s, "拼圖四的核心只有一句：先判斷包絡線過不過原點，再決定可以用哪些捷徑", 0.6, 6.65, 12.1, 0.4, { fontSize: 15, bold: true, color: C.muted, align: "center" });
  pageNo(s, pg);
}
// ───── 22 回顧 ─────
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  T(s, "重點回顧：四塊拼圖全景", 0.8, 0.7, 11, 0.8, { fontSize: 34, bold: true, color: C.white });
  const pts = [
    ["1", "拼圖一 真參數只有一組：強度只由有效應力決定，φ′、c′ 才是土壤本性", C.gold],
    ["2", "拼圖二 兩個閥門定生死：CD / CU / UU 只是讓莫爾圓平移 u", C.ok],
    ["3", "拼圖三 一張莫爾圓走天下：C、R、T 推出萬能式、幾何式、正弦式", C.eff],
    ["4", "拼圖四 NC / OC 分岔：c′ = 0 → 相似形三大捷徑；c′ ≠ 0 → 萬能式＋相減法", C.ps],
    ["5", "手算主線：保留 K_p、√K_p 往下代，最後才轉 φ′；交卷前做切點與 A_f 檢核", C.tot],
  ];
  pts.forEach(([n, t, col], i) => {
    const y = 1.8 + i * 0.9;
    s.addShape(pres.shapes.OVAL, { x: 0.8, y, w: 0.58, h: 0.58, fill: { color: col }, line: { color: col } });
    T(s, n, 0.8, y, 0.58, 0.58, { fontSize: 19, bold: true, color: C.white, align: "center", valign: "middle" });
    T(s, runs(t, { color: C.white, fontSize: 17 }), 1.6, y - 0.1, 11.2, 0.78, { valign: "middle" });
  });
  T(s, "下一步：挑一題歷屆考題（[SM-2018-2] 或 [SM-2024-1]）在紙上動筆列式，按本篇 SOP 自己走一遍", 0.8, 6.45, 11.8, 0.45, { fontSize: 16, bold: true, color: "F2A65A" });
}
pres.writeFile({ fileName: "SM-U1-5_NC與OC分岔.pptx" }).then(() => console.log("written"));
