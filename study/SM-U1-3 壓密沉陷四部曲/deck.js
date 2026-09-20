const pptxgen = require("pptxgenjs");
const fs = require("fs");
const P = JSON.parse(fs.readFileSync("nums.json", "utf8"));
const pres = new pptxgen(); pres.layout = "LAYOUT_WIDE"; pres.title = "SM-U1-3 壓密沉陷計算四部曲";
const FT = "Noto Sans CJK TC";
const C = { ink: "1F2A37", muted: "6B7280", panel: "F4F6F9", line: "D5DAE1", cr: "2F54C8", cc: "C0392B",
            pc: "B8520E", p0: "2E7D6B", dark: "1B2432", white: "FFFFFF", okbg: "E6F2EF", pcbg: "FBF1EA" };

// "p_0'" → runs with subscript
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
// 多段落：[{t, o}] → runs with breakLine
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
// 置入 SVG，等比縮放後在框內置中
function img(s, name, x, y, W, H, align = "center") {
  const f = `figs/${name}.svg`; const [w, h] = vb(f); const k = Math.min(W / w, H / h);
  const iw = w * k, ih = h * k;
  const ix = align === "left" ? x : x + (W - iw) / 2;
  s.addImage({ path: f, x: ix, y: y + (H - ih) / 2, w: iw, h: ih, altText: name });
  return { x: ix, y: y + (H - ih) / 2, w: iw, h: ih };
}
function header(s, eyebrow, title, col = C.pc) {
  T(s, eyebrow, 0.6, 0.38, 9, 0.3, { fontSize: 12, bold: true, color: col, charSpacing: 2 });
  T(s, title, 0.6, 0.68, 12.2, 0.6, { fontSize: 28, bold: true });
}
function panel(s, x, y, w, h, fill = C.panel, line = C.line) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { color: line, width: 1 }, rectRadius: 0.12 });
}
function pageNo(s, n) { T(s, `${n}`, 12.3, 7.05, 0.5, 0.25, { fontSize: 10, color: "9AA3AE", align: "right" }); }
const f1 = v => v.toFixed(1);
const MJ = JSON.parse(fs.readFileSync("figs/math.json", "utf8"));

// ───── 1 封面 ─────
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  T(s, "SM-U1-3　土壤夯實與壓密｜觀念講義", 0.8, 1.35, 11, 0.4, { fontSize: 16, color: "9FB3C8", bold: true });
  T(s, "壓密沉陷計算四部曲", 0.8, 1.95, 11.5, 1.1, { fontSize: 50, bold: true, color: C.white });
  T(s, "算現況 → 算增量 → 看歷史 → 選公式：順著決策鏈，選對公式不靠背", 0.8, 3.15, 11.5, 0.5, { fontSize: 20, color: "D6DEE8" });
  const dots = [["1", "p_0'", C.p0], ["2", "Δσ", C.cc], ["3", "p_c'", C.pc], ["4", "S_c", C.cr]];
  dots.forEach(([n, lab, col], i) => {
    const x = 0.8 + i * 2.35;
    s.addShape(pres.shapes.OVAL, { x, y: 4.35, w: 0.62, h: 0.62, fill: { color: col }, line: { color: col } });
    T(s, n, x, 4.35, 0.62, 0.62, { fontSize: 20, bold: true, color: C.white, align: "center", valign: "middle" });
    T(s, lab, x + 0.78, 4.4, 1.3, 0.55, { fontSize: 22, bold: true, color: C.white, valign: "middle" });
    if (i < 3) T(s, "→", x + 1.72, 4.4, 0.5, 0.55, { fontSize: 22, color: "6B7C90", valign: "middle" });
  });
  T(s, `示範案例貫穿全篇：黏土層 H = 4 m、e_0 = ${P.E0}、C_c = ${P.CC}、C_r = ${P.CR}、p_c' = ${P.PC} kPa；圖上數字全部可對帳`,
    0.8, 6.3, 11.8, 0.4, { fontSize: 14, color: "9FB3C8" });
}
// ───── 2 總覽 ─────
{
  const s = pres.addSlide(); s.background = { color: C.white };
  header(s, "OVERVIEW · 決策鏈", "一條決策鏈：每一步的輸出，都是下一步的輸入");
  img(s, "fig01_overview", 0.6, 1.5, 12.1, 3.4);
  panel(s, 0.6, 5.25, 12.1, 1.55);
  T(s, paras([
    { t: "為什麼要照順序？", o: { bold: true, fontSize: 17, color: C.pc } },
    { t: "p_0' 算錯 → OCR 與 Case 一定判錯；Δσ 的載重型式判錯 → 沉陷量差一個數量級（本例 5.8 mm vs 86.9 mm）。", o: { fontSize: 15 } },
    { t: "所以不背三條長公式，只要把 p_0'、p_c'、p_f' 排上同一條對數軸，看路徑走過哪幾段。", o: { fontSize: 15 } },
  ]), 0.9, 5.4, 11.5, 1.3, { paraSpaceAfter: 4 });
  pageNo(s, 2);
}
// ───── 3 Step1 ─────
{
  const s = pres.addSlide(); s.background = { color: C.white };
  header(s, "STEP 1 · 算現況", "先定「黏土層中點」，再算現況有效應力 p_0'", C.p0);
  img(s, "fig02_profile", 0.45, 1.45, 8.3, 5.4);
  panel(s, 8.95, 1.55, 3.9, 5.3);
  T(s, "逐層累加（水位下用 γ'）", 9.2, 1.75, 3.5, 0.35, { fontSize: 16, bold: true, color: C.p0 });
  img(s, "m_p0", 9.15, 2.2, 3.5, 0.5);
  T(s, paras([
    { t: "砂（水位上） 18.0 × 2", o: { fontSize: 14, color: C.muted } },
    { t: "= 36.00", o: { fontSize: 16, bold: true } },
    { t: "砂（飽和） (19.5 − 9.81) × 4", o: { fontSize: 14, color: C.muted } },
    { t: "= 38.76", o: { fontSize: 16, bold: true } },
    { t: "黏土上半 (17.5 − 9.81) × 2", o: { fontSize: 14, color: C.muted } },
    { t: "= 15.38", o: { fontSize: 16, bold: true } },
  ]), 9.2, 2.9, 3.5, 2.3, { paraSpaceAfter: 2 });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 9.2, y: 5.25, w: 3.4, h: 0.62, fill: { color: "FBECEA" }, line: { color: C.cc, width: 1.5 }, rectRadius: 0.08 });
  T(s, `p_0' = ${f1(P.P0)} kPa`, 9.2, 5.25, 3.4, 0.62, { fontSize: 22, bold: true, color: C.cc, align: "center", valign: "middle" });
  T(s, `對帳：σ − u = ${f1(P.SIG8)} − ${f1(P.U8)} = ${f1(P.P0)}，兩種算法答案相同`, 9.2, 6.05, 3.5, 0.65, { fontSize: 13, color: C.muted });
  pageNo(s, 3);
}
// ───── 4 為什麼中點 ─────
{
  const s = pres.addSlide(); s.background = { color: C.white };
  header(s, "STEP 1 · 為什麼取中點", "中點一次算，和分 8 層積分只差 0.2%", C.p0);
  img(s, "fig03_midpoint", 0.5, 1.5, 8.2, 4.5);
  const pts = [
    ["為什麼中點能代表全層？", "σ' 沿深度線性變化，中點應力代表全層的平均壓縮行為；頂、底兩端的偏差大致互相抵消。"],
    ["本例的證據", `中點一次算 ${f1(P.SUB[0])} mm，分 8 層 ${P.SUB[3].toFixed(2)} mm——考場上中點法完全足夠。`],
    ["什麼時候要分層？", "黏土很厚，或 Δσ 隨深度劇烈變化（如小基腳的 2:1 法）時，才分薄層各自算再加總。"],
  ];
  pts.forEach(([h, b], i) => {
    const y = 1.6 + i * 1.62;
    panel(s, 8.95, y, 3.9, 1.45);
    T(s, h, 9.15, y + 0.15, 3.5, 0.4, { fontSize: 15, bold: true, color: C.p0 });
    T(s, b, 9.15, y + 0.55, 3.55, 0.85, { fontSize: 13 });
  });
  T(s, "取頂或底代替中點：p_0' 會變成 74.8 或 105.5 kPa，後面 OCR、Case 全部跟著偏。", 0.6, 6.35, 8.1, 0.45, { fontSize: 14, color: C.cc, bold: true });
  pageNo(s, 4);
}
// ───── 5 Step2 ─────
{
  const s = pres.addSlide(); s.background = { color: C.white };
  header(s, "STEP 2 · 算增量", "Δσ：先判斷「有限基礎」還是「大面積」", C.cc);
  img(s, "fig04_21geom", 0.45, 1.4, 6.3, 4.35);
  img(s, "fig05_depth", 6.9, 1.4, 5.9, 4.35);
  panel(s, 0.6, 5.95, 5.95, 1.0);
  img(s, "m_21", 0.75, 6.02, 2.4, 0.85);
  T(s, paras([
    { t: "有限尺寸基礎：2:1 法", o: { bold: true, color: C.pc, fontSize: 14 } },
    { t: `1200 / (8.5 × 9.5) = ${f1(P.DSF)} kPa`, o: { fontSize: 14 } },
    { t: "z 從「基礎底面」起算", o: { fontSize: 13, color: C.cc, bold: true } },
  ]), 3.35, 6.05, 3.1, 0.9);
  panel(s, 6.8, 5.95, 5.95, 1.0, C.okbg, "9CC7BC");
  T(s, paras([
    { t: "大面積均布載重：全深度不折減", o: { bold: true, color: C.p0, fontSize: 14 } },
    { t: "預壓覆土、大範圍回填、地下水位下降 → Δσ = 80 kPa 直達黏土中點", o: { fontSize: 13 } },
    { t: "載重面積 ≫ 影響深度，應力無處擴散", o: { fontSize: 13, color: C.muted } },
  ]), 7.0, 6.05, 5.6, 0.9);
  pageNo(s, 5);
}
// ───── 6 Step3 e-log p' ─────
{
  const s = pres.addSlide(); s.background = { color: C.white };
  header(s, "STEP 3 · 看歷史", "e-log p' 曲線：土壤記得自己被壓過多重", C.pc);
  img(s, "fig06_elogp", 0.4, 1.45, 8.4, 5.1);
  panel(s, 9.0, 1.55, 3.85, 1.7, C.okbg, "9CC7BC");
  T(s, "預壓密應力 p_c'", 9.2, 1.68, 3.5, 0.35, { fontSize: 15, bold: true, color: C.p0 });
  img(s, "m_ocr", 9.2, 2.05, 1.5, 0.6, "left");
  T(s, `= 130 / ${f1(P.P0)} = ${P.OCR.toFixed(2)}`, 10.75, 2.15, 2.0, 0.45, { fontSize: 16, bold: true, valign: "middle" });
  T(s, "OCR = 1 正常壓密 NC；> 1 過壓密 OC", 9.2, 2.75, 3.6, 0.35, { fontSize: 12, color: C.muted });
  const cards = [
    ["記憶內　p' ≤ p_c'", "走 C_r：把以前壓過的結構再壓一次，彈性為主，沉陷極小。", C.cr],
    ["超過記憶　p' > p_c'", "走 C_c：顆粒結構首次崩塌重排、不可回復，沉陷大得多。", C.cc],
    [`斜率差 ${P.RATIO.toFixed(1)} 倍`, `本例 C_c / C_r = ${P.CC} / ${P.CR}；一般在 5～10 倍之間。`, C.pc],
  ];
  cards.forEach(([h, b, col], i) => {
    const y = 3.45 + i * 1.12;
    panel(s, 9.0, y, 3.85, 1.0);
    T(s, h, 9.2, y + 0.1, 3.5, 0.35, { fontSize: 15, bold: true, color: col });
    T(s, b, 9.2, y + 0.45, 3.55, 0.55, { fontSize: 12 });
  });
  T(s, "判斷 Case 的唯一依據：把 p_0'、p_c'、p_f' 排在這條對數軸上。", 0.6, 6.6, 8.2, 0.4, { fontSize: 14, bold: true, color: C.cc });
  pageNo(s, 6);
}
// ───── 7 公式從哪來 ─────
{
  const s = pres.addSlide(); s.background = { color: C.white };
  header(s, "STEP 3 → 4 · 公式的來源", "三條公式其實只是同一件事：S = 孔隙比減少量換算成厚度", C.pc);
  img(s, "fig07_phase", 0.5, 1.5, 6.0, 4.6);
  T(s, "土粒體積不變，只有孔隙被擠掉", 0.7, 6.3, 5.8, 0.4, { fontSize: 14, bold: true, color: C.muted, align: "center" });
  panel(s, 6.85, 1.55, 5.95, 1.35);
  T(s, "① 應變 = 孔隙減少 / 原總高", 7.05, 1.65, 5.5, 0.35, { fontSize: 15, bold: true, color: C.pc });
  img(s, "m_S", 7.05, 2.05, 2.6, 0.75, "left");
  panel(s, 6.85, 3.05, 5.95, 1.55);
  T(s, "② Δe 由 e-log p' 路徑逐段讀出", 7.05, 3.15, 5.5, 0.35, { fontSize: 15, bold: true, color: C.pc });
  img(s, "m_de", 7.05, 3.55, 5.0, 0.95, "left");
  panel(s, 6.85, 4.75, 5.95, 1.95, C.pcbg, "E3B894");
  T(s, paras([
    { t: "③ 代入本例", o: { bold: true, color: C.pc, fontSize: 15 } },
    { t: `Δe = ${P.DER.toFixed(4)} + ${P.DEC.toFixed(4)} = ${(P.DER + P.DEC).toFixed(4)}`, o: { fontSize: 15 } },
    { t: `S_c = ${(P.DER + P.DEC).toFixed(4)} / 2.05 × 4000 = ${f1(P.SC)} mm`, o: { fontSize: 15, bold: true } },
    { t: "把 C·log(…) 代入 ① 就得到 Case A / B / C 三條公式——不必背，推得出來。", o: { fontSize: 13, color: C.muted } },
  ]), 7.05, 4.88, 5.6, 1.75, { paraSpaceAfter: 3 });
  pageNo(s, 7);
}
// ───── 8 三種 Case ─────
{
  const s = pres.addSlide(); s.background = { color: C.white };
  header(s, "STEP 4 · 選公式", "Case A / B / C：路徑不同，沉陷量可差 30 倍", C.cr);
  img(s, "fig08_cases", 0.6, 1.35, 12.1, 5.55);
  pageNo(s, 8);
}
// ───── 9 判斷流程 ─────
{
  const s = pres.addSlide(); s.background = { color: C.white };
  header(s, "STEP 4 · 判斷流程", "兩個判斷就分完：OCR 是否為 1？p_f' 有沒有衝破 p_c'？", C.cr);
  img(s, "fig09_flow", 0.4, 1.4, 8.1, 5.5);
  const fs_ = [["Case A（NC）", "m_A", C.cc], ["Case B（OC、未跨越）", "m_B", C.cr], ["Case C（OC、跨越）", "m_C", C.pc]];
  fs_.forEach(([lab, m, col], i) => {
    const y = 1.5 + i * 1.8;
    panel(s, 8.7, y, 4.15, 1.62);
    T(s, lab, 8.9, y + 0.12, 3.8, 0.35, { fontSize: 15, bold: true, color: col });
    img(s, m, 8.85, y + 0.5, 3.85, 1.0);
  });
  pageNo(s, 9);
}
// ───── 10 Case C 完整計算 ─────
{
  const s = pres.addSlide(); s.background = { color: C.white };
  header(s, "WORKED EXAMPLE · Case C", "示範案例完整計算：大面積預壓 80 kPa", C.pc);
  img(s, "fig10_split", 0.4, 1.45, 7.9, 4.0);
  T(s, "關鍵觀念：沉陷量由「斜率 × 對數長度」決定；C_c 段即使較短，仍貢獻 84%。", 0.6, 5.7, 7.6, 0.8, { fontSize: 15, bold: true, color: C.cc });
  panel(s, 8.5, 1.55, 4.35, 5.25);
  const K = (4 / 2.05).toFixed(3);
  T(s, paras([
    { t: "① 判型", o: { bold: true, color: C.pc, fontSize: 15 } },
    { t: `p_0' = ${f1(P.P0)} < p_c' = 130 < p_f' = ${f1(P.PF)}`, o: { fontSize: 14 } },
    { t: "→ Case C，拆兩段", o: { fontSize: 14, bold: true } },
    { t: " ", o: { fontSize: 6 } },
    { t: "② C_r 段（p_0' → p_c'）", o: { bold: true, color: C.cr, fontSize: 15 } },
    { t: `0.045 × 4000 / 2.05 × log(130 / ${f1(P.P0)})`, o: { fontSize: 13 } },
    { t: `= ${f1(P.SCR)} mm`, o: { fontSize: 15, bold: true } },
    { t: " ", o: { fontSize: 6 } },
    { t: "③ C_c 段（p_c' → p_f'）", o: { bold: true, color: C.cc, fontSize: 15 } },
    { t: `0.320 × 4000 / 2.05 × log(${f1(P.PF)} / 130)`, o: { fontSize: 13 } },
    { t: `= ${f1(P.SCC)} mm`, o: { fontSize: 15, bold: true } },
    { t: " ", o: { fontSize: 6 } },
    { t: `④ S_c = ${f1(P.SCR)} + ${f1(P.SCC)} = ${f1(P.SC)} mm`, o: { bold: true, color: C.pc, fontSize: 18 } },
  ]), 8.75, 1.75, 3.95, 4.9, { paraSpaceAfter: 2 });
  pageNo(s, 10);
}
// ───── 11 一秒驗算 ─────
{
  const s = pres.addSlide(); s.background = { color: C.white };
  header(s, "SANITY CHECK · 一秒驗算", "Case C 的答案必定夾在「全套 C_r」與「全套 C_c」之間", C.p0);
  img(s, "fig11_check", 0.6, 1.45, 12.1, 3.65);
  const cards = [
    ["下限：全套 C_r", `${f1(P.ALLCR)} mm`, "假設從頭到尾都在記憶內", C.cr],
    ["上限：全套 C_c", `${f1(P.ALLCC)} mm`, "假設一加載就進入處女壓縮線", C.cc],
    ["同地換成基腳", `${f1(P.SB)} mm`, `2:1 法 Δσ 只剩 ${f1(P.DSF)} kPa，未達 p_c'，為 Case C 的 1/15`, C.muted],
  ];
  cards.forEach(([h, v, d, col], i) => {
    const x = 0.6 + i * 4.1;
    panel(s, x, 5.3, 3.9, 1.55);
    T(s, h, x + 0.2, 5.4, 3.5, 0.35, { fontSize: 14, bold: true, color: col });
    T(s, v, x + 0.2, 5.75, 3.5, 0.5, { fontSize: 24, bold: true, color: col });
    T(s, d, x + 0.2, 6.3, 3.55, 0.5, { fontSize: 12, color: C.muted });
  });
  pageNo(s, 11);
}
// ───── 12 陷阱 ─────
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  T(s, "REVIEW · 高頻陷阱", 0.6, 0.38, 9, 0.3, { fontSize: 12, bold: true, color: "F2A65A", charSpacing: 2 });
  T(s, "六個最常見的扣分點（皆以示範案例量化）", 0.6, 0.68, 12, 0.6, { fontSize: 28, bold: true, color: C.white });
  const traps = [
    ["2:1 法的 z 從地表起算", `z 應為 6.5 m（基礎底面起）；誤用 8 m 得 ${f1(P.DSFW)} kPa，低估 ${Math.round((1 - P.DSFW / P.DSF) * 100)}%。`],
    ["大面積載重也拿去折減", "預壓覆土、大範圍回填、水位下降一律全深度不折減，Δσ = 80 kPa。"],
    ["水位下忘記扣 γ_w", `用總應力 ${f1(P.SIG8)} 當 p_0'，會誤判 p_0' > p_c'，整個 Case 判錯。`],
    ["取黏土頂或底代替中點", "p_0' 變成 74.8 或 105.5 kPa，OCR 與沉陷量全部跟著偏。"],
    ["Case C 只用一條公式", `全套 C_r 得 ${f1(P.ALLCR)}、全套 C_c 得 ${f1(P.ALLCC)}，正解 ${f1(P.SC)} mm。`],
    ["log 按成 ln", `自然對數會放大 2.303 倍：${f1(P.SC)} → ${f1(P.SC * Math.LN10)} mm。`],
  ];
  traps.forEach(([h, d], i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = 0.6 + col * 6.15, y = 1.55 + row * 1.8;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 5.95, h: 1.6, fill: { color: "263244" }, line: { color: "3A4A60", width: 1 }, rectRadius: 0.1 });
    s.addShape(pres.shapes.OVAL, { x: x + 0.22, y: y + 0.22, w: 0.46, h: 0.46, fill: { color: "C0392B" }, line: { color: "C0392B" } });
    T(s, String(i + 1), x + 0.22, y + 0.22, 0.46, 0.46, { fontSize: 15, bold: true, color: C.white, align: "center", valign: "middle" });
    T(s, h, x + 0.85, y + 0.24, 4.9, 0.42, { fontSize: 17, bold: true, color: C.white, valign: "middle" });
    T(s, d, x + 0.85, y + 0.75, 4.9, 0.75, { fontSize: 13, color: "C8D3E0" });
  });
}
// ───── 13 公式速查 ─────
{
  const s = pres.addSlide(); s.background = { color: C.white };
  header(s, "CHEAT SHEET · 考前速查", "四部曲全公式一頁速查", C.pc);
  const cells = [
    ["① 現況有效應力", "m_p0", 0.6, 1.45, 4.55], ["② 2:1 應力傳佈（z 從基底起）", "m_21", 5.3, 1.45, 3.65], ["③ 過壓密比", "m_ocr", 9.1, 1.45, 3.65],
    ["② 最終有效應力", "m_pf", 0.6, 2.95, 4.55], ["沉陷的本質", "m_S", 5.3, 2.95, 3.65], ["④ Δe 分段讀取", "m_de", 9.1, 2.95, 3.65],
    ["Case A（NC，全程 C_c）", "m_A", 0.6, 4.45, 6.0], ["Case B（OC 未跨越，全程 C_r）", "m_B", 6.75, 4.45, 6.0],
  ];
  cells.forEach(([lab, m, x, y, w]) => {
    panel(s, x, y, w, 1.35);
    T(s, lab, x + 0.18, y + 0.1, w - 0.3, 0.3, { fontSize: 13, bold: true, color: C.pc });
    const iw = Math.min(w - 0.3, MJ[m][0] * 0.72);
    img(s, m, x + 0.15 + (w - 0.3 - iw) / 2, y + 0.42, iw, 0.85);
  });

  panel(s, 0.6, 5.95, 12.15, 1.0, C.pcbg, "E3B894");
  T(s, "Case C（OC 跨越）", 0.8, 6.02, 2.5, 0.3, { fontSize: 13, bold: true, color: C.pc });
  img(s, "m_C", 3.0, 6.0, 7.8, 0.9);
  pageNo(s, 13);
}
// ───── 14 結尾 ─────
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  T(s, "重點回顧", 0.8, 0.8, 11, 0.8, { fontSize: 36, bold: true, color: C.white });
  const pts = [
    ["1", "p_0' 取黏土層中點，水位下用浮單位重逐層累加", C.p0],
    ["2", "Δσ 先判型式：基腳 2:1 法（z 從基底起算），大面積全深度不折減", C.cc],
    ["3", "OCR = p_c' / p_0' 判 NC / OC；C_c 約為 C_r 的 5～10 倍", C.pc],
    ["4", "三點排上對數軸看路徑；Case C 拆兩段，答案必夾在全套 C_r 與全套 C_c 之間", C.cr],
  ];
  pts.forEach(([n, t, col], i) => {
    const y = 1.95 + i * 1.02;
    s.addShape(pres.shapes.OVAL, { x: 0.8, y, w: 0.6, h: 0.6, fill: { color: col }, line: { color: col } });
    T(s, n, 0.8, y, 0.6, 0.6, { fontSize: 20, bold: true, color: C.white, align: "center", valign: "middle" });
    T(s, t, 1.65, y, 11, 0.6, { fontSize: 19, color: C.white, valign: "middle" });
  });
  T(s, "建議演練：SM-2003-2（2:1 應力傳佈 ＋ Case C 跨越段）", 0.8, 6.3, 11.5, 0.45, { fontSize: 16, bold: true, color: "F2A65A" });
}
pres.writeFile({ fileName: "SM-U1-3_壓密沉陷四部曲.pptx" }).then(() => console.log("written"));
