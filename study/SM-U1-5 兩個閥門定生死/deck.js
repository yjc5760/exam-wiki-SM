const pptxgen = require("pptxgenjs");
const fs = require("fs");
const N = JSON.parse(fs.readFileSync("nums.json", "utf8"));
const MJ = JSON.parse(fs.readFileSync("figs/math.json", "utf8"));
const pres = new pptxgen(); pres.layout = "LAYOUT_WIDE"; pres.title = "SM-U1-5 拼圖二：兩個閥門定生死";
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

// ───── 1 封面 ─────
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  T(s, "SM-U1-5　土壤強度｜觀念講義・拼圖二", 0.8, 1.2, 11, 0.4, { fontSize: 16, color: "9FB3C8", bold: true });
  T(s, "兩個閥門定生死", 0.8, 1.8, 11.8, 1.1, { fontSize: 48, bold: true, color: C.white });
  T(s, "壓密排不排水 × 剪切排不排水：閥門的開關組合決定孔隙水壓 u 怎麼變，也決定你量到的是哪一組強度參數", 0.8, 3.0, 11.8, 0.9, { fontSize: 20, color: "D6DEE8" });
  const dots = [["CD", "u = 0，直接量 c′、φ′", "7CC4AE"], ["CU", "有效圓 = 總應力圓左移 u_f", "F2A65A"], ["UU", "圓一樣大，φ_u = 0、S_u = R", "F08A6E"]];
  dots.forEach(([n, lab, col], i) => {
    const x = 0.8 + i * 4.0;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 4.35, w: 3.7, h: 0.8, fill: { color: "243044" }, line: { color: col, width: 2 }, rectRadius: 0.1 });
    T(s, n, x + 0.2, 4.35, 0.8, 0.8, { fontSize: 20, bold: true, color: col, valign: "middle" });
    T(s, lab, x + 0.95, 4.35, 2.7, 0.8, { fontSize: 14, bold: true, color: C.white, valign: "middle" });
  });
  T(s, `示範黏土 A 沿用拼圖一：NC、c′ = 0、φ′ = ${N.PHI}°、σ_3 = ${N.S3} kPa、A_f = ${N.AF}；圖上數字全部由同一支程式算出，可逐一對帳`,
    0.8, 6.3, 11.8, 0.4, { fontSize: 14, color: "9FB3C8" });
}
// ───── 2 總覽 ─────
figSlide("OVERVIEW · 兩個閥門", "壓密閥 × 剪切閥：四種組合，實際只有三種試驗", "fig01_valves", [
  ["閥門①：壓密階段", ["決定剪切前骨架有多緊（起跑點）"], C.cd, C.cdbg, "9CC7BC"],
  ["閥門②：剪切階段", ["決定剪切時體積變化會不會變成 u"], C.cu, C.cubg, "F2C7A6"],
  ["讀圖方法", ["先問兩個閥門開或關，再推 u 怎麼走，最後才畫圓"], C.ink],
], C.eff, 4.55);
// ───── 3 三軸儀 ─────
figSlide("機制 ① · 儀器", "其實只有一顆排水閥，只是在兩個階段各決定一次開或關", "fig02_apparatus", [
  ["縮寫的讀法", ["第一個字母 = 壓密階段（C／U）", "第二個字母 = 剪切階段（D／U）"], C.ink],
  ["閥開時量什麼", ["量管讀體積變化 ΔV（u ≈ 0）"], C.cd, C.cdbg, "9CC7BC"],
  ["閥關時量什麼", ["孔壓計讀 u（ΔV = 0）"], C.uu, C.uubg, "EBB4AE"],
], C.eff, 4.55);
// ───── 4 閥門① ─────
figSlide("機制 ② · 壓密閥", "閥門① 決定起跑點：剪切前骨架承受多少有效應力", "fig03_consol", [
  ["開（C）", [`加圍壓 ${N.S3} kPa 後等 u 消散：σ′_3 = σ_3 = ${N.S3}`, "骨架被壓緊 → 強度隨圍壓增加"], C.cd, C.cdbg, "9CC7BC"],
  ["關（U）", ["圍壓增量全部由水扛：Δu = Δσ_3（飽和 B = 1）", "σ′ 維持取樣時的值 → 加再多圍壓也沒用"], C.uu, C.uubg, "EBB4AE"],
]);
// ───── 5 閥門② ─────
figSlide("機制 ③ · 剪切閥", "閥門② 決定體積變化傾向去哪裡：變成 ΔV，還是變成 u", "fig04_shear", [
  ["同一個傾向，兩種表現", ["NC 想剪縮：排水 → 體積縮；不排水 → 正孔壓 +u", "OC 想剪脹：排水 → 體積脹；不排水 → 負孔壓 −u"], C.ink],
  ["考試關鍵", ["不排水時 ΔV = 0，但 u ≠ 0：u 讓有效應力改變", "→ 這就是 CU、UU 強度不同於 CD 的根源"], C.eff, C.effbg, "F2B8A6"],
]);
// ───── 6 UD ─────
figSlide("機制 ④ · 缺席的組合", "為什麼沒有 UD？因為「不壓密卻排水剪」在現場找不到對應", "fig05_noud", [
  ["一句話記住", ["能排水的土早就壓密完了；UD 等於邊壓密邊剪，量到的東西無法解讀"], C.ink],
], C.eff, 4.05);
// ───── 7 總表 ─────
{
  const s = newSlide();
  header(s, "總整理 · 三大試驗", "CD／CU／UU 一張表：閥門、孔壓、莫爾圓、參數、現場");
  const hd = ["試驗", "閥門①／閥門②", "孔隙水壓 u", "莫爾圓行為", "量到的參數", "對應現場"];
  const rows = [
    ["CD", "開／開", "全程 u = 0\n總應力 = 有效應力", "只有一個圓\n不必平移", "c′、φ′\n（真參數）", "長期穩定、砂土、\n緩慢加載", C.cd, C.cdbg],
    ["CU", "開／關", "壓密時歸零\n剪切時累積 u_f", "有效圓 = 總應力圓\n左移 u_f，R 不變", "φ_{cu}（總）\nc′、φ′（有效）", "既有結構上快速加載、\n水位驟降", C.cu, C.cubg],
    ["UU", "關／關", "Δu = Δσ_3\nσ′ 完全不變", "不同圍壓的圓\n一樣大", "φ_u = 0\nS_u = R", "施工期、開挖後立即、\n快速填土", C.uu, C.uubg],
  ];
  const cw = [1.1, 1.7, 2.3, 2.5, 2.1, 2.4]; const X = [0.6]; cw.forEach((w, i) => X.push(X[i] + w + 0));
  s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 1.5, w: 12.1, h: 0.55, fill: { color: C.dark }, line: { color: C.dark } });
  hd.forEach((h, i) => T(s, h, X[i] + 0.15, 1.5, cw[i] - 0.2, 0.55, { fontSize: 14, bold: true, color: C.white, valign: "middle" }));
  rows.forEach((r, j) => {
    const y = 2.15 + j * 1.35, col = r[6], bg = r[7];
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y, w: 12.1, h: 1.25, fill: { color: bg }, line: { color: col, width: 1.5 }, rectRadius: 0.08 });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.7, y: y + 0.12, w: 0.9, h: 1.0, fill: { color: col }, line: { color: col }, rectRadius: 0.08 });
    T(s, r[0], 0.7, y + 0.12, 0.9, 1.0, { fontSize: 22, bold: true, color: C.white, align: "center", valign: "middle" });
    for (let i = 1; i < 6; i++) {
      const lines = r[i].split("\n");
      T(s, paras(lines.map((t, k) => ({ t, o: { fontSize: 14, bold: i === 4 || (i === 1), color: i === 4 ? col : C.ink } }))),
        X[i] + 0.15, y, cw[i] - 0.2, 1.25, { valign: "middle", paraSpaceAfter: 2 });
    }
  });
  panel(s, 0.6, 6.3, 12.1, 0.75, C.panel);
  T(s, "記憶口訣：閥門只管 u；u 只管「圓在哪」，不管「圓多大」。圓多大由骨架的有效應力決定。", 0.85, 6.3, 11.6, 0.75, { fontSize: 15, bold: true, valign: "middle" });
  pageNo(s, pg);
}
// ───── 8 三試驗並排 ─────
figSlide("示範黏土 A · 同一個 σ_3 = 100", "同一塊土、同一個圍壓，三個試驗量到三種破壞圓", "fig06_three", [
  ["CD", [`u = 0，σ′_3 維持 ${N.S3}，可以一路剪到 σ_1 = ${N.S1_CD}`], C.cd, C.cdbg, "9CC7BC"],
  ["CU", [`u_f = +${N.UF} 把 σ′_3 從 ${N.S3} 拉到 ${N.S3E}，只剪到 Δσ_d = ${N.DSD}`], C.cu, C.cubg, "F2C7A6"],
  ["UU", [`試體有效應力同為 ${N.S3}，破壞圓與 CU 相同；只報 S_u = ${N.SU}`], C.uu, C.uubg, "EBB4AE"],
], C.eff, 4.55);
// ───── 9 CD ─────
figSlide("試驗 ① · CD", "CD：u 全程為零，畫一個圓就是有效應力圓", "fig07_cd", [
  ["直接讀出真參數", [`K_p = σ_1/σ_3 = ${N.KP.toFixed(0)} → sin φ′ = (K_p − 1)/(K_p + 1) = 0.5 → φ′ = ${N.PHI}°`], C.cd, C.cdbg, "9CC7BC"],
  ["為什麼不常做", ["黏土透水性低，剪切要夠慢才能讓 u ≈ 0，一組常要數天；工程上多用 CU 加孔壓量測代替"], C.ink],
]);
// ───── 10 CU ─────
figSlide("試驗 ② · CU", "CU：有效應力圓就是總應力圓整個往左平移 u_f", "fig08_cu", [
  ["同一個破壞事件，兩套座標", [`總應力 ${N.S3}～${N.S1}；有效 ${N.S3E}～${N.S1E}；兩者都是 2R = ${N.DSD}`], C.eff, C.effbg, "F2B8A6"],
  ["φ_{cu} 與 φ′ 的比例", [`${N.PHI_CU.toFixed(1)}° / ${N.PHI}° = ${N.RATIO_CU.toFixed(2)}，落在 NC 黏土常見的 0.5～0.7`], C.tot, C.totbg, "B9C6EA"],
], C.eff, 4.35);
// ───── 11 半徑不變代數 ─────
{
  const s = newSlide();
  header(s, "推導 · 黃金跳躍法", "兩邊同扣 u_f：圓心移動、半徑不變，三行代數說完");
  panel(s, 0.6, 1.5, 6.4, 5.5);
  T(s, "① 主應力同時扣掉 u_f", 0.85, 1.65, 6, 0.35, { fontSize: 16, bold: true, color: C.eff });
  eq(s, "m_shift", 0.85, 2.05, 0.6, 0.5, "left", 5.9);
  T(s, "② 圓心往左移 u_f", 0.85, 2.9, 6, 0.35, { fontSize: 16, bold: true, color: C.tot });
  eq(s, "m_center", 0.85, 3.3, 0.9, 0.5, "left", 5.9);
  T(s, "③ 半徑：u_f 相減時抵消", 0.85, 4.4, 6, 0.35, { fontSize: 16, bold: true, color: C.cd });
  eq(s, "m_rad", 0.85, 4.8, 0.9, 0.5, "left", 5.9);
  T(s, "物理意義：水不承剪，所以 u 改變不了「最大剪應力 = R」", 0.85, 6.1, 6, 0.7, { fontSize: 14, bold: true, color: C.muted, valign: "middle" });
  panel(s, 7.2, 1.5, 5.5, 2.6, C.effbg, "F2B8A6");
  T(s, "代入示範黏土 A", 7.45, 1.65, 5, 0.35, { fontSize: 16, bold: true, color: C.eff });
  T(s, paras([
    { t: `σ′_3 = ${N.S3} − ${N.UF} = ${N.S3E}`, o: { fontSize: 16, bold: true } },
    { t: `σ′_1 = ${N.S1} − ${N.UF} = ${N.S1E}`, o: { fontSize: 16, bold: true } },
    { t: `C：${N.C_T} → ${N.C_E}　R：${N.R} → ${N.R}`, o: { fontSize: 16, bold: true, color: C.eff } },
  ]), 7.45, 2.1, 5, 1.9, { paraSpaceAfter: 8 });
  panel(s, 7.2, 4.3, 5.5, 2.7, C.totbg, "B9C6EA");
  T(s, "所以 NC 黏土 φ′ > φ_{cu} 恆成立", 7.45, 4.45, 5, 0.35, { fontSize: 16, bold: true, color: C.tot });
  T(s, paras([
    { t: "兩個圓一樣大、有效圓在左（較靠近原點）", o: { fontSize: 14 } },
    { t: "從原點畫切線，越近的圓切線越陡", o: { fontSize: 14 } },
    { t: `→ φ′ = ${N.PHI}° > φ_{cu} = ${N.PHI_CU.toFixed(1)}°`, o: { fontSize: 15, bold: true, color: C.tot } },
    { t: "檢查：算出的有效圓半徑 ≠ 總應力圓 → 一定只扣了一邊", o: { fontSize: 13, color: C.ps, bold: true } },
  ]), 7.45, 4.9, 5, 2.0, { paraSpaceAfter: 6 });
  pageNo(s, pg);
}
// ───── 12 u_f 符號 ─────
figSlide("CU 延伸 · u_f 的正負", "u_f 的符號決定圓往哪移：NC 往左、重 OC 往右", "fig09_sign", [
  ["NC（A_f > 0）", [`u_f = +${N.UF} → φ_{cu} = ${N.PHI_CU.toFixed(1)}°，比 φ′ 小`], C.tot, C.totbg, "B9C6EA"],
  ["重 OC（A_f < 0）", [`u_f = ${N.UF_OC.toFixed(1)} → φ_{cu} = ${N.PHI_CU_OC.toFixed(1)}°，比 φ′ 大`], C.pur, C.purbg, "C9BCEB"],
  ["結論", ["φ_{cu} 是「土＋試驗路徑」的產物，不是土的性質"], C.ink],
]);
// ───── 13 UU ─────
figSlide("試驗 ③ · UU", "UU：圍壓加再多，圓還是一樣大", "fig10_uu", [
  ["閥門全關", ["室壓增量 100 全進水：Δu = Δσ_3（B = 1），σ′ 一點都沒變"], C.uu, C.uubg, "EBB4AE"],
  ["強度鎖死", [`有效應力不變 → 抗剪強度不變 → 每個圓的半徑都 = S_u = ${N.SU}`], C.ink],
  ["破壞時的 u", [`σ_3 = 100／200／300 → u = ${N.UU_U1}／${N.UU_U2}／${N.UU_U3}`], C.water, "E8F2F9", "A9CBE3"],
]);
// ───── 14 φu = 0 + UC ─────
{
  const s = newSlide();
  header(s, "UU 延伸 · φ_u = 0 與 UC 試驗", "φ_u = 0 不是「土沒有摩擦角」，而是「這個試驗看不到摩擦角」", C.uu);
  img(s, "fig11_uc", 0.6, 1.4, 7.6, 3.4);
  panel(s, 8.4, 1.45, 4.3, 3.35, C.uubg, "EBB4AE");
  T(s, "UU 家族三條公式", 8.6, 1.55, 4, 0.35, { fontSize: 15, bold: true, color: C.uu });
  eq(s, "m_su", 8.6, 1.95, 0.85, 0.5, "left", 3.9);
  eq(s, "m_qu", 8.6, 2.9, 0.55, 0.5, "left", 3.9);
  T(s, "無圍壓壓縮（UC）= σ_3 = 0 的 UU", 8.6, 3.5, 4, 0.3, { fontSize: 13, color: C.muted });
  T(s, `示範黏土 A：q_u = 2 × ${N.SU} = ${N.QU} kPa`, 8.6, 3.95, 4, 0.35, { fontSize: 15, bold: true });
  const cells = [
    ["摩擦其實還在", "骨架仍靠 σ′ tan φ′ 抗剪，只是 σ′ 被「鎖」在同一個值", C.eff, C.effbg, "F2B8A6"],
    ["φ_u = 0 的用法", "只能用在「不排水、總應力」分析：τ_f = S_u，與 σ 無關", C.uu, C.uubg, "EBB4AE"],
    ["不可以", "拿 φ_u = 0 算破壞面（45°）或做長期穩定分析", C.ps, "F4F6F9", C.line],
  ];
  cells.forEach(([a, b, c, bg, ln], i) => {
    const x = 0.6 + i * 4.07;
    panel(s, x, 5.0, 3.95, 2.05, bg, ln);
    T(s, paras([{ t: a, o: { bold: true, fontSize: 15, color: c } }, { t: b, o: { fontSize: 14 } }]), x + 0.2, 5.12, 3.6, 1.85, { paraSpaceAfter: 6 });
  });
  pageNo(s, pg);
}
// ───── 15 Skempton ─────
{
  const s = figSlide("核心公式 · Skempton 孔壓參數", "孔隙水壓從哪來：一個 B 管飽和、一個 A 管剪縮剪脹", "fig12_skempton", [], C.eff, 4.3);
  panel(s, 0.6, 5.85, 6.3, 1.2, C.totbg, "B9C6EA");
  eq(s, "m_skp", 0.85, 5.95, 1.0, 0.62, "left", 5.9);
  panel(s, 7.05, 5.85, 5.65, 1.2, C.panel);
  T(s, paras([
    { t: `不飽和例：B = ${N.B_UNSAT}，室壓加 ${N.DS3_B}`, o: { bold: true, fontSize: 14, color: C.water } },
    { t: `Δu = ${N.DU_B}，Δσ′ = ${N.DSE_B} → UU 的圓會隨圍壓略為變大、包絡線不再水平`, o: { fontSize: 13 } },
  ]), 7.25, 5.93, 5.3, 1.05, { paraSpaceAfter: 3 });
}
// ───── 16 剪縮剪脹 ─────
{
  const s = figSlide("核心公式 · A 參數的物理", "A 的正負：顆粒想「掉進去」還是想「爬過去」", "fig13_dilat", [], C.eff, 4.3);
  panel(s, 0.6, 5.85, 5.4, 1.2, C.panel);
  T(s, paras([
    { t: "常規三軸剪切：σ_3 固定、飽和 B = 1", o: { bold: true, fontSize: 14 } },
    { t: "Δσ_3 = 0，Skempton 式只剩 A 那一項 →", o: { fontSize: 13 } },
  ]), 0.8, 5.93, 5.1, 1.05, { paraSpaceAfter: 4 });
  panel(s, 6.15, 5.85, 6.55, 1.2, C.totbg, "B9C6EA");
  eq(s, "m_af", 6.4, 5.95, 1.0, 0.6, "left", 6.1);
}
// ───── 17 A_f 範圍 ─────
figSlide("核心公式 · A_f 的合理範圍", "A_f 的典型範圍：算完回頭對照，就知道有沒有算錯", "fig14_arange", [
  ["示範黏土 A 回推", [`A_f = u_f / Δσ_d = ${N.UF} / ${N.DSD} = ${N.AF_BACK.toFixed(2)} ✓（NC 範圍內）`], C.tot, C.totbg, "B9C6EA"],
  ["警訊", ["NC 題目算出負的 A_f → 多半是 u_f 正負號或 Δσ_d 用錯"], C.ps, C.uubg, "EBB4AE"],
]);
// ───── 18 Su/σ'v0 ─────
{
  const s = newSlide();
  header(s, "UU 延伸 · NC 黏土的強度比", "S_u / σ′_{v0}：把破壞圓右端釘在 σ′_{v0}，再往左長到切 φ′");
  img(s, "fig15_surat", 0.6, 1.4, 12.1, 4.3);
  panel(s, 0.6, 5.85, 4.0, 1.2, C.effbg, "F2B8A6");
  T(s, "A_f = 1 的捷徑（課本式）", 0.8, 5.9, 3.7, 0.3, { fontSize: 13, bold: true, color: C.eff });
  eq(s, "m_surat", 0.8, 6.2, 0.8, 0.5, "left", 3.6);
  panel(s, 4.75, 5.85, 4.3, 1.2, C.panel);
  T(s, "一般式（任意 A_f）", 4.95, 5.9, 4, 0.3, { fontSize: 13, bold: true, color: C.muted });
  eq(s, "m_surgen", 4.95, 6.2, 0.8, 0.5, "left", 3.95);
  panel(s, 9.2, 5.85, 3.5, 1.2, C.totbg, "B9C6EA");
  T(s, paras([
    { t: "對帳", o: { bold: true, fontSize: 13, color: C.tot } },
    { t: `A_f = 1：${N.SUR_A1.toFixed(3)} → S_u = ${N.SU_A1.toFixed(1)}`, o: { fontSize: 13, bold: true } },
    { t: `A_f = ${N.AF}：${N.SUR_GEN.toFixed(3)} → S_u = ${N.SU}`, o: { fontSize: 13, bold: true } },
  ]), 9.4, 5.92, 3.2, 1.1, { paraSpaceAfter: 2 });
  pageNo(s, pg);
}
// ───── 19 深度 ─────
figSlide("UU 延伸 · 現地剖面", "NC 黏土的不排水強度隨深度線性成長", "fig16_depth", [
  ["前提（完美取樣）", ["試體有效應力 = 現地 σ′_{v0}；A_f = 1 時破壞圓右端 σ′_{1f} = σ′_{v0}"], C.ink],
  ["比值永遠 < 0.5", [`sin φ′/(1 + sin φ′) 在 φ′ → 90° 時才趨近 0.5；φ′ = ${N.PHI}° 只有 ${N.SUR_A1.toFixed(3)}`], C.ps, C.uubg, "EBB4AE"],
]);
// ───── 20 CU 四步 ─────
{
  const s = figSlide("考場速算 ① · CU 題", "兩邊同扣 u_f，直接建有效應力圓：四步收工", "fig17_cuflow", [], C.eff, 4.0);
  panel(s, 0.6, 5.6, 6.0, 1.45, C.panel);
  T(s, "NC 黏土（c′ = 0）的正弦捷徑", 0.8, 5.66, 5.6, 0.3, { fontSize: 13, bold: true, color: C.cd });
  eq(s, "m_sin", 0.8, 6.0, 0.95, 0.55, "left", 5.5);
  panel(s, 6.75, 5.6, 5.95, 1.45, C.effbg, "F2B8A6");
  T(s, paras([
    { t: "為什麼要先扣 u_f 再算角度？", o: { bold: true, fontSize: 14, color: C.eff } },
    { t: "直接用總應力代正弦式得到的是 φ_{cu}，不是 φ′；", o: { fontSize: 13 } },
    { t: `本例會算成 ${N.PHI_CU.toFixed(1)}°，差了 ${(N.PHI - N.PHI_CU).toFixed(1)}°`, o: { fontSize: 13, bold: true } },
  ]), 6.95, 5.68, 5.6, 1.3, { paraSpaceAfter: 3 });
}
// ───── 21 比例法 ─────
{
  const s = figSlide("考場速算 ② · NC 比例法", "同一 NC 黏土換圍壓：整張莫爾圖從原點等比例放大", "fig18_ratio", [], C.eff, 4.3);
  panel(s, 0.6, 5.85, 7.0, 1.2, C.panel);
  eq(s, "m_ratio", 0.8, 5.95, 1.0, 0.5, "left", 6.6);
  panel(s, 7.75, 5.85, 4.95, 1.2, C.goldbg, "E6CFA0");
  T(s, paras([
    { t: "3 秒算出新破壞軸差", o: { bold: true, fontSize: 14, color: C.gold } },
    { t: `σ_3 = ${N.S3_2}：Δσ_d = ${N.DSD / N.S3} × ${N.S3_2} = ${N.DSD_2}、u_f = ${N.UF_2}`, o: { fontSize: 13, bold: true } },
    { t: "OC 黏土（c′ ≠ 0）包絡線不過原點 → 不可用", o: { fontSize: 13, color: C.ps } },
  ]), 7.95, 5.92, 4.6, 1.1, { paraSpaceAfter: 2 });
}
// ───── 22 檢查點 ─────
{
  const s = newSlide();
  header(s, "考場三大檢查點", "算完別急著交：三個 10 秒就能做的檢查");
  const cards = [
    ["1", "兩個圓的半徑必須一樣", ["CU 的總應力圓與有效圓 R 相同", `本例：R = ${N.R}（兩者）`, "不同 → σ_1、σ_3 沒有同時扣 u_f"], C.eff, C.effbg, "F2B8A6"],
    ["2", "A_f 與強度比落在合理範圍", [`NC：A_f = u_f/Δσ_d 應在 0.5～1.0（本例 ${N.AF_BACK.toFixed(2)}）`, `NC：S_u/σ′_{v0} < 0.5（本例 ${N.SUR_A1.toFixed(3)}）`, "超出 → 幾乎一定代錯公式"], C.tot, C.totbg, "B9C6EA"],
    ["3", "破壞面只用 φ′", [`θ = 45° + φ′/2 = ${N.TH}°`, `誤用 φ_{cu} 會得 ${N.TH_WRONG.toFixed(1)}°`, "題目只給 φ_{cu} → 先用 u_f 換回 φ′"], C.uu, C.uubg, "EBB4AE"],
  ];
  cards.forEach(([n, hd, body, col, bg, ln], i) => {
    const x = 0.6 + i * 4.07;
    panel(s, x, 1.55, 3.95, 5.0, bg, ln);
    s.addShape(pres.shapes.OVAL, { x: x + 0.25, y: 1.8, w: 0.7, h: 0.7, fill: { color: col }, line: { color: col } });
    T(s, n, x + 0.25, 1.8, 0.7, 0.7, { fontSize: 24, bold: true, color: C.white, align: "center", valign: "middle" });
    T(s, hd, x + 0.25, 2.7, 3.5, 0.8, { fontSize: 18, bold: true, color: col });
    T(s, paras(body.map((t, k) => ({ t, o: { fontSize: 15, bold: k === 1, color: k === 2 ? C.muted : C.ink } }))), x + 0.25, 3.6, 3.5, 2.8, { paraSpaceAfter: 10 });
  });
  T(s, "三項全過，再寫答案", 0.6, 6.65, 12.1, 0.4, { fontSize: 15, bold: true, color: C.muted, align: "center" });
  pageNo(s, pg);
}
// ───── 23 破壞面陷阱 ─────
figSlide("高頻陷阱", "破壞面角度嚴禁用 φ_{cu} 或 φ_u：實體破壞面只有一個", "fig19_plane", [
  ["為什麼", ["顆粒沿哪個面滑是骨架摩擦決定的，只看有效應力；φ_{cu} 隨加載路徑跳動，不能代表實體面"], C.ps, C.uubg, "EBB4AE"],
  ["標準動作", ["只給 φ_{cu} + u_f → 扣 u_f 建有效圓 → 求 φ′ → θ = 45° + φ′/2"], C.cd, C.cdbg, "9CC7BC"],
], C.ps);
// ───── 24 現場 ─────
figSlide("回到工程 · 選哪種試驗", "現場情境決定閥門：先問「水來不來得及排」", "fig20_field", [
  ["短期（不排水）", ["黏土快速加載：用總應力法 S_u（UU）或 φ_{cu}（CU）"], C.uu, C.uubg, "EBB4AE"],
  ["長期（排水）", ["超額孔壓已消散：用有效應力法 c′、φ′（CD 或 CU 量孔壓）"], C.cd, C.cdbg, "9CC7BC"],
], C.eff, 4.35);
// ───── 25 重點回顧 ─────
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  T(s, "重點回顧", 0.8, 0.8, 11, 0.8, { fontSize: 36, bold: true, color: C.white });
  const pts = [
    ["1", "兩個閥門：壓密閥決定起跑點，剪切閥決定體積傾向變成 ΔV 還是 u", C.gold],
    ["2", "CD：u = 0，一個圓直接量 c′、φ′", C.ok],
    ["3", `CU：σ_1、σ_3 同扣 u_f，圓左移不縮放；NC 的 φ′ > φ_{cu}（${N.PHI}° vs ${N.PHI_CU.toFixed(1)}°）`, C.eff],
    ["4", "UU：Δu = Δσ_3，圓一樣大，φ_u = 0、S_u = R；UC：q_u = 2S_u", C.ps],
    ["5", "Δu = B[Δσ_3 + A(Δσ_1 − Δσ_3)]；NC 的 A_f ≈ 0.5～1.0、S_u/σ′_{v0} < 0.5；θ 只用 φ′", C.tot],
  ];
  pts.forEach(([n, t, col], i) => {
    const y = 1.85 + i * 0.9;
    s.addShape(pres.shapes.OVAL, { x: 0.8, y, w: 0.58, h: 0.58, fill: { color: col }, line: { color: col } });
    T(s, n, 0.8, y, 0.58, 0.58, { fontSize: 19, bold: true, color: C.white, align: "center", valign: "middle" });
    T(s, t, 1.6, y, 11.2, 0.58, { fontSize: 17, color: C.white, valign: "middle" });
  });
  T(s, "下一步：用「同扣 u_f 平移法」與「S_u/σ′_{v0} 捷徑」實際拆解 CU、UU 考古題", 0.8, 6.5, 11.5, 0.45, { fontSize: 16, bold: true, color: "F2A65A" });
}
pres.writeFile({ fileName: "SM-U1-5_兩個閥門定生死.pptx" }).then(() => console.log("written"));
