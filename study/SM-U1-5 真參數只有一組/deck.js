const pptxgen = require("pptxgenjs");
const fs = require("fs");
const N = JSON.parse(fs.readFileSync("nums.json", "utf8"));
const MJ = JSON.parse(fs.readFileSync("figs/math.json", "utf8"));
const pres = new pptxgen(); pres.layout = "LAYOUT_WIDE"; pres.title = "SM-U1-5 拼圖一：真參數只有一組";
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
let pg = 1;
function newSlide() { const s = pres.addSlide(); s.background = { color: C.white }; pg++; return s; }
const TFS = [N.TF1, N.TF2, N.TF3].map(f1).join("、");
const TFPS = [N.TFP1, N.TFP2, N.TFP3].map(f1).join("、");
// ───── 1 封面 ─────
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  T(s, "SM-U1-5　土壤強度｜觀念講義・拼圖一", 0.8, 1.2, 11, 0.4, { fontSize: 16, color: "9FB3C8", bold: true });
  T(s, "真參數只有一組", 0.8, 1.8, 11.8, 1.1, { fontSize: 48, bold: true, color: C.white });
  T(s, "水不承剪，所以抗剪強度只聽有效應力；φ_u、φ_{cu} 是試驗條件的產物，(c′, φ′) 才是土的性質", 0.8, 3.0, 11.8, 0.9, { fontSize: 20, color: "D6DEE8" });
  const dots = [["機制", "有效應力控制一切", "F08A6E"], ["路徑", "K_f 線與 φ_{cu} 的真面目", "8FA8F0"], ["解題", "三條破壞式＋相減法", "7CC4AE"]];
  dots.forEach(([n, lab, col], i) => {
    const x = 0.8 + i * 4.0;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 4.35, w: 3.7, h: 0.8, fill: { color: "243044" }, line: { color: col, width: 2 }, rectRadius: 0.1 });
    T(s, n, x + 0.25, 4.35, 0.9, 0.8, { fontSize: 16, bold: true, color: col, valign: "middle" });
    T(s, lab, x + 1.05, 4.35, 2.6, 0.8, { fontSize: 16, bold: true, color: C.white, valign: "middle" });
  });
  T(s, `兩個示範案例貫穿全篇：黏土 A（NC，φ′ = ${N.PHI_A}°，p′_0 = ${N.S3} kPa，A_f = ${N.AF}）、黏土 B（OC，兩組 CD 試驗）；圖上數字全部可對帳`,
    0.8, 6.3, 11.8, 0.4, { fontSize: 14, color: "9FB3C8" });
}
// ───── 2 總覽 ─────
{
  const s = newSlide();
  header(s, "OVERVIEW · 一句話講完拼圖一", "同一塊土做四種試驗，得到四個角度——扣掉孔隙水壓後只剩一組");
  img(s, "fig01_map", 0.6, 1.4, 12.1, 4.6);
  panel(s, 0.6, 6.1, 12.1, 0.95);
  T(s, paras([
    { t: "為什麼這件事重要？", o: { bold: true, fontSize: 15, color: C.eff } },
    { t: `考卷會同時給你 φ_{cu}、u_f、Δσ_d，陷阱就在「拿錯角度去算」：破壞面、長期穩定、K_f 換算，一律要回到 φ′。`, o: { fontSize: 14 } },
  ]), 0.85, 6.18, 11.6, 0.85, { paraSpaceAfter: 3 });
  pageNo(s, pg);
}
// ───── 3 微觀 ─────
{
  const s = newSlide();
  header(s, "機制 ① · 微觀", "剪力只能靠顆粒接觸點的摩擦傳遞，水一點也幫不上忙");
  img(s, "fig02_micro", 0.6, 1.35, 12.1, 4.3);
  panel(s, 0.6, 5.8, 5.95, 1.25, C.panel);
  T(s, "有效應力原理", 0.85, 5.9, 3, 0.3, { fontSize: 13, bold: true, color: C.muted });
  eq(s, "m_eff", 0.85, 6.22, 0.7, 0.62);
  T(s, "u 是各向同性的壓力，只把顆粒「撐開」，不提供摩擦", 3.3, 6.25, 3.1, 0.7, { fontSize: 13, color: C.muted, valign: "middle" });
  panel(s, 6.75, 5.8, 5.95, 1.25, C.effbg, "F2B8A6");
  T(s, "唯一的真破壞準則", 7.0, 5.9, 3, 0.3, { fontSize: 13, bold: true, color: C.eff });
  eq(s, "m_mc", 7.0, 6.22, 0.7, 0.62);
  T(s, "c′、φ′ 由骨架決定，與怎麼試驗無關", 9.8, 6.25, 2.8, 0.7, { fontSize: 13, color: C.eff, bold: true, valign: "middle" });
  pageNo(s, pg);
}
// ───── 4 巨觀：三條包絡線 ─────
{
  const s = newSlide();
  header(s, "機制 ② · 巨觀", "示範黏土 A：一條實線是土的性質，兩條虛線是試驗的產物");
  img(s, "fig03_envelopes", 0.6, 1.35, 12.1, 4.75);
  const cells = [
    ["CD：σ′_3 不變", `σ′_1 = 3 × ${N.S3} = ${f0(N.S1_CD)}`, `圓切在 φ′ = ${N.PHI_A}° 上`, C.ok, C.okbg, "9CC7BC"],
    ["CU：u_f 讓圓左移", `總應力 ${f0(N.S3)}～${f0(N.S1_AC)} → 有效 ${f0(N.S3E_AC)}～${f0(N.S1E_AC)}`, `總應力連線只有 ${f1(N.PHI_CU_AC)}°`, C.tot, C.totbg, "B9C6EA"],
    ["UU：圓一樣大", `s_u = Δσ_d / 2 = ${f0(N.SU)} kPa`, "換圍壓只是 u 等量上升", "5B6573", "F1F3F6", "C9CFD8"],
  ];
  cells.forEach(([a, b, c, col, bg, ln], i) => {
    const x = 0.6 + i * 4.1;
    panel(s, x, 6.2, 3.9, 0.9, bg, ln);
    T(s, a, x + 0.2, 6.25, 3.6, 0.3, { fontSize: 13, bold: true, color: col });
    T(s, b, x + 0.2, 6.5, 3.6, 0.3, { fontSize: 13, bold: true });
    T(s, c, x + 0.2, 6.78, 3.6, 0.28, { fontSize: 12, color: C.muted });
  });
  pageNo(s, pg);
}
// ───── 5 u 只平移 ─────
{
  const s = newSlide();
  header(s, "機制 ③ · 孔隙水壓的角色", "u 只會把莫爾圓左右平移，永遠不會改變圓的大小");
  img(s, "fig04_shift", 0.6, 1.35, 12.1, 4.3);
  panel(s, 0.6, 5.8, 4.2, 1.25);
  T(s, "Skempton 孔壓式（飽和 B = 1）", 0.8, 5.88, 3.9, 0.3, { fontSize: 13, bold: true, color: C.muted });
  eq(s, "m_skp", 0.8, 6.2, 0.7, 0.5, "left", 3.8);
  panel(s, 4.95, 5.8, 3.8, 1.25, C.totbg, "B9C6EA");
  T(s, paras([
    { t: "AC：σ_3 固定、σ_1 加大", o: { bold: true, fontSize: 14, color: C.tot } },
    { t: `u_f = A_f Δσ_d = ${N.AF} × ${f0(N.DSD_AC)} = ${sg(N.UF_AC)}`, o: { fontSize: 14 } },
    { t: "正孔壓 → 圓往左推", o: { fontSize: 12, color: C.muted } },
  ]), 5.15, 5.88, 3.5, 1.15, { paraSpaceAfter: 2 });
  panel(s, 8.9, 5.8, 3.8, 1.25, C.lebg, "C9BCEB");
  T(s, paras([
    { t: "LE：σ_1 固定、σ_3 減小", o: { bold: true, fontSize: 14, color: C.le } },
    { t: `u_f = −(1 − A)Δσ_3 = −${1 - N.AF} × ${f0(N.DL)} = ${sg(N.UF_LE)}`, o: { fontSize: 14 } },
    { t: "負孔壓 → 圓往右拉（假設 A 相同）", o: { fontSize: 12, color: C.muted } },
  ]), 9.1, 5.88, 3.5, 1.15, { paraSpaceAfter: 2 });
  pageNo(s, pg);
}
// ───── 6 應力路徑 ─────
{
  const s = newSlide();
  header(s, "路徑 ① · p–q 圖", "CD、CU 走不同的路，終點卻停在同一條有效 K_f 線上", C.tot);
  img(s, "fig05_path", 0.6, 1.35, 12.1, 5.05);
  panel(s, 0.6, 6.45, 12.1, 0.62, C.totbg, "B9C6EA");
  T(s, `φ_{cu} 只是「總應力路徑終點」和原點的連線角度：終點隨 u_f 左右移動，角度就跟著跳（AC ${f1(N.PHI_CU_AC)}°、LE ${f1(N.PHI_CU_LE)}°）`,
    0.85, 6.45, 11.7, 0.62, { fontSize: 14, bold: true, color: C.tot, valign: "middle" });
  pageNo(s, pg);
}
// ───── 7 鐵證 ─────
{
  const s = newSlide();
  header(s, "路徑 ② · 鐵證", "同一塊土只改加載方式：φ_{cu} 差了兩倍多，φ′ 一動也不動", C.tot);
  const hd = { bold: true, color: C.white, fill: { color: C.dark }, fontFace: FT, fontSize: 14, align: "center", valign: "middle" };
  const cl = { fontFace: FT, fontSize: 14, color: C.ink, align: "center", valign: "middle" };
  const rowsData = [
    ["加載方式", "σ_3 固定，σ_1 往上加", "σ_1 固定，σ_3 往下減"],
    ["破壞時總應力", `σ_3 = ${f0(N.S3)}、σ_1 = ${f0(N.S1_AC)}`, `σ_3 = ${f0(N.S3_LE)}、σ_1 = ${f0(N.S1_LE)}`],
    ["u_f", `${sg(N.UF_AC)} kPa`, `${sg(N.UF_LE)} kPa`],
    ["破壞時有效應力", `σ′_3 = ${f0(N.S3E_AC)}、σ′_1 = ${f0(N.S1E_AC)}`, `σ′_3 = ${f0(N.S3E_LE)}、σ′_1 = ${f0(N.S1E_LE)}`],
    ["φ_{cu}（總應力）", `${f1(N.PHI_CU_AC)}°`, `${f1(N.PHI_CU_LE)}°`],
    ["φ′（有效應力）", `${f1(N.PHI_A)}°`, `${f1(N.PHI_A)}°`],
  ];
  const rows = [[{ text: "示範黏土 A", options: hd }, { text: "CU 軸壓 AC", options: { ...hd, fill: { color: C.tot } } }, { text: "CU 側向伸張 LE", options: { ...hd, fill: { color: C.le } } }]];
  rowsData.forEach((r, i) => {
    const fill = { color: i === 5 ? C.effbg : i === 4 ? "F1F3F6" : (i % 2 ? "F7F8FA" : C.white) };
    const em = i >= 4;
    rows.push([
      { text: runs(r[0], { bold: true }), options: { ...cl, bold: true, fill } },
      { text: runs(r[1], { bold: em, color: i === 5 ? C.eff : i === 4 ? C.tot : C.ink, fontSize: em ? 18 : 14 }), options: { ...cl, fill } },
      { text: runs(r[2], { bold: em, color: i === 5 ? C.eff : i === 4 ? C.le : C.ink, fontSize: em ? 18 : 14 }), options: { ...cl, fill } },
    ]);
  });
  s.addTable(rows, { x: 0.6, y: 1.5, w: 7.4, colW: [2.2, 2.6, 2.6], rowH: [0.5, 0.55, 0.55, 0.55, 0.55, 0.62, 0.62],
                     border: { type: "solid", pt: 0.75, color: "D5DAE1" } });
  panel(s, 8.3, 1.5, 4.4, 3.95, C.goldbg, "E3C48F");
  T(s, paras([
    { t: "考古題對照：SM-2013-3", o: { bold: true, fontSize: 16, color: C.gold } },
    { t: "同一土樣", o: { fontSize: 14, color: C.muted } },
    { t: "AC 試驗：φ_{cu} = 19.23°", o: { fontSize: 16, bold: true, color: C.tot } },
    { t: "LE 試驗：φ_{cu} = 31.59°", o: { fontSize: 16, bold: true, color: C.le } },
    { t: "兩者的 φ′ = 28.04°", o: { fontSize: 18, bold: true, color: C.eff } },
    { t: "數字不同、結構完全一樣：總應力角度跟著路徑跑，有效角度不變。", o: { fontSize: 13 } },
  ]), 8.55, 1.65, 3.95, 3.7, { paraSpaceAfter: 6 });
  panel(s, 0.6, 5.7, 12.1, 1.35);
  T(s, paras([
    { t: "為什麼兩條路回到同一個有效圓？", o: { bold: true, fontSize: 15, color: C.eff } },
    { t: `AC 把總應力圓往右推、正孔壓把它拉回來；LE 把總應力圓往左推、負孔壓把它拉回來。骨架「感受到」的永遠是 ${f0(N.S3E_AC)}～${f0(N.S1E_AC)} kPa 這個圓。`, o: { fontSize: 14 } },
    { t: "本頁示範數字假設兩種試驗的 A_f 相同；實際 A_f 會隨路徑略變，但「φ′ 不變」的結論不受影響。", o: { fontSize: 12, color: C.muted } },
  ]), 0.85, 5.8, 11.6, 1.2, { paraSpaceAfter: 3 });
  pageNo(s, pg);
}
// ───── 8 K_f ↔ M-C ─────
{
  const s = newSlide();
  header(s, "路徑 ③ · K_f 線換算", "K_f 線過圓頂、M–C 線切圓邊：斜率和截距都要換算", C.tot);
  img(s, "fig06_kf", 0.6, 1.35, 12.1, 4.55);
  panel(s, 0.6, 6.0, 12.1, 1.05, C.totbg, "B9C6EA");
  eq(s, "m_kf", 0.85, 6.1, 0.85, 0.5, "left", 4.9);
  const w2 = eq(s, "m_qf", 6.1, 6.1, 0.85, 0.5, "left", 3.8);
  T(s, "NC 時 c′ = 0 直接退化；考題常給 K_f 線要你反推 c′、φ′", 10.0, 6.1, 2.6, 0.85, { fontSize: 12, color: C.tot, bold: true, valign: "middle" });
  pageNo(s, pg);
}
// ───── 9 砂土 ─────
{
  const s = newSlide();
  header(s, "機制 ④ · 砂土的補充", "密砂的尖峰是「咬合」多出來的強度，大變形後一律回到 φ_{cv}", C.gold);
  img(s, "fig07_sand", 0.6, 1.35, 12.1, 4.3);
  const cells = [
    ["尖峰來自咬合", "密砂要剪動就得讓顆粒互相「翻越」，額外的功表現成 φ_p", C.ps, C.psbg, "E6B0AA"],
    ["臨界狀態是共同終點", "大變形時密砂鬆開、鬆砂壓實，孔隙比收斂到 e_{cv}，強度同為 φ_{cv}", C.ok, C.okbg, "9CC7BC"],
    ["與黏土的對應", "密砂 ≈ OC 黏土（剪脹、負孔壓）；鬆砂 ≈ NC 黏土（壓縮、正孔壓）", C.tot, C.totbg, "B9C6EA"],
  ];
  cells.forEach(([a, b, col, bg, ln], i) => {
    const x = 0.6 + i * 4.1;
    panel(s, x, 5.75, 3.9, 1.3, bg, ln);
    T(s, a, x + 0.2, 5.83, 3.5, 0.3, { fontSize: 14, bold: true, color: col });
    T(s, b, x + 0.2, 6.15, 3.55, 0.85, { fontSize: 12 });
  });
  pageNo(s, pg);
}
// ───── 10 砂土：考試與設計 ─────
{
  const s = newSlide();
  header(s, "機制 ④ · 砂土的考點", "同一種砂在不同密度量到不同 φ：材料常數是 φ_{cv}", C.gold);
  panel(s, 0.6, 1.5, 12.1, 1.6, C.goldbg, "E3C48F");
  T(s, paras([
    { t: "考試常問：為什麼同一種砂在不同相對密度下量到不同 φ？", o: { bold: true, fontSize: 17, color: C.gold } },
    { t: "答：φ_{cv} 才是材料常數；φ_p = φ_{cv} + 剪脹貢獻，剪脹貢獻由相對密度與圍壓共同決定。", o: { fontSize: 16 } },
    { t: "講義常簡寫為 φ_p = φ_{cv} + ψ（ψ 為剪脹角）；Bolton 的經驗式在平面應變下取約 0.8ψ——作答時寫「剪脹貢獻」最安全。", o: { fontSize: 13, color: C.muted } },
  ]), 0.85, 1.62, 11.6, 1.4, { paraSpaceAfter: 5 });
  const cards = [
    ["密度越高", "咬合越緊 → 要翻越的高度越大 → 剪脹越明顯 → φ_p 越高", C.ps],
    ["圍壓越高", "顆粒被壓住、翻越受抑制 → 剪脹變小 → φ_p 往 φ_{cv} 靠近", C.tot],
    ["設計取值", "長期或大變形問題（既有滑動面、擋土牆後的鬆動區）用 φ_{cv} 較安全", C.ok],
  ];
  cards.forEach(([a, b, col], i) => {
    const x = 0.6 + i * 4.1;
    panel(s, x, 3.35, 3.9, 1.9);
    bar(s, x, 3.5, 1.6, col);
    T(s, a, x + 0.3, 3.5, 3.4, 0.4, { fontSize: 18, bold: true, color: col });
    T(s, b, x + 0.3, 4.0, 3.45, 1.15, { fontSize: 14 });
  });
  panel(s, 0.6, 5.5, 12.1, 1.5);
  T(s, paras([
    { t: "和「真參數只有一組」怎麼連起來？", o: { bold: true, fontSize: 15, color: C.eff } },
    { t: `砂的 φ_p 看起來也「隨試驗變」，但變的是土的狀態（密度、圍壓），不是排水條件造成的總應力假象。狀態固定，有效應力參數仍只有一組；剪到臨界狀態時，連狀態的差別都消失，只剩 φ_{cv}。`, o: { fontSize: 14 } },
  ]), 0.85, 5.62, 11.6, 1.35, { paraSpaceAfter: 4 });
  pageNo(s, pg);
}
// ───── 11 直剪 ─────
{
  const s = newSlide();
  header(s, "機制 ⑤ · 直剪試驗", "快，但破壞面是你指定的：只能得到包絡線上的點", C.ps);
  img(s, "fig08_direct", 0.6, 1.35, 12.1, 4.7);
  panel(s, 0.6, 6.15, 12.1, 0.9);
  T(s, paras([
    { t: `示範砂：σ′_n = 50、100、200 kPa → τ_f = ${TFS}（φ_{cv} = ${N.PHI_CV}°）；密砂尖峰 ${TFPS}（φ_p = ${N.PHI_P}°）`, o: { bold: true, fontSize: 14 } },
    { t: "直剪不能量孔壓，所以量到的一定要是排水強度（慢剪），才能直接當 c′、φ′ 用。", o: { fontSize: 13, color: C.muted } },
  ]), 0.85, 6.2, 11.6, 0.82, { paraSpaceAfter: 3 });
  pageNo(s, pg);
}
// ───── 12 直剪 vs 三軸 ─────
{
  const s = newSlide();
  header(s, "機制 ⑤ · 怎麼選試驗", "直剪 vs 三軸：差在破壞面、排水與孔壓三件事", C.ps);
  const hd = { bold: true, color: C.white, fill: { color: C.dark }, fontFace: FT, fontSize: 14, align: "center", valign: "middle" };
  const cl = { fontFace: FT, fontSize: 14, color: C.ink, align: "left", valign: "middle", margin: [2, 10, 2, 10] };
  const rowsData = [
    ["破壞面", "強制水平面", `自然弱面 θ = 45° + φ′/2（示範砂 ${N.TH_C}°）`],
    ["排水控制", "靠加載速率，難嚴格控制", "閥門＋反壓，可精確控制"],
    ["量測孔隙水壓", "不能", "可以（CU 的關鍵）"],
    ["應力狀態", "只知破壞面上的 σ_n、τ", "σ_1、σ_3 完整已知"],
    ["莫爾圓", "只得到包絡線上的一個點", "每組都能畫出完整的圓"],
    ["常見用途", "砂土 φ′、殘餘強度 φ_r", "黏土 UU／CU／CD 全系列"],
  ];
  const rows = [[{ text: "比較項目", options: hd }, { text: "直剪試驗", options: { ...hd, fill: { color: C.ps } } }, { text: "三軸試驗", options: { ...hd, fill: { color: C.tot } } }]];
  rowsData.forEach((r, i) => {
    const fill = { color: i % 2 ? "F7F8FA" : C.white };
    rows.push([{ text: runs(r[0], { bold: true }), options: { ...cl, bold: true, align: "center", fill } },
               { text: runs(r[1]), options: { ...cl, fill } }, { text: runs(r[2]), options: { ...cl, fill } }]);
  });
  s.addTable(rows, { x: 0.6, y: 1.5, w: 12.1, colW: [2.3, 4.4, 5.4], rowH: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], border: { type: "solid", pt: 0.75, color: "D5DAE1" } });
  const items = [
    ["破壞面不自由", "結果偏向那個水平面的強度；土若有明顯異向性，φ′ 會偏高或偏低。"],
    ["殘餘強度的利器", "反覆剪（reversal）可量到殘餘摩擦角 φ_r，是既有滑動面分析的必要參數。"],
    ["不能做 UU", "無法封閉排水、也量不到 u；飽和黏土的不排水強度要靠三軸或現地試驗。"],
  ];
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 5.2, w: 12.1, h: 1.85, fill: { color: C.dark }, line: { color: C.dark }, rectRadius: 0.12 });
  T(s, "三個容易被問倒的點", 0.85, 5.3, 5, 0.35, { fontSize: 15, bold: true, color: "F2A65A" });
  items.forEach(([a, b], i) => {
    const x = 0.85 + i * 3.97;
    T(s, a, x, 5.72, 3.7, 0.35, { fontSize: 15, bold: true, color: C.white });
    T(s, b, x, 6.08, 3.7, 0.9, { fontSize: 12, color: "C9D3DF" });
  });
  pageNo(s, pg);
}
// ───── 13 莫爾圓幾何 ─────
{
  const s = newSlide();
  header(s, "解題 ① · 幾何基礎", "所有破壞條件式都來自同一個直角三角形", C.ok);
  img(s, "fig09_geom", 0.6, 1.35, 12.1, 4.7);
  panel(s, 0.6, 6.15, 12.1, 0.9, C.okbg, "9CC7BC");
  eq(s, "m_cr", 0.85, 6.2, 0.8, 0.52, "left", 6.2);
  T(s, `示範黏土 B 試驗 A：σ′_3 = ${f0(N.S3A)}、σ′_1 = ${f0(N.S1A)} → C = ${f0(N.CA)}、R = ${f0(N.RA)}`, 7.3, 6.15, 5.3, 0.9, { fontSize: 14, bold: true, color: C.ok, valign: "middle" });
  pageNo(s, pg);
}
// ───── 14 三條破壞條件式 ─────
{
  const s = newSlide();
  header(s, "解題 ② · 三條破壞條件式", "同一件事的三種寫法：看題目給什麼，挑最短的那條", C.ok);
  const P = [
    ["①  萬能式（最常用）", "m_f1", "給 σ′_3 求 σ′_1、或兩組試驗聯立", `黏土 B：${f0(N.S3A)} × ${f2(N.KP_B)} + 2 × ${f2(N.C_B)} × ${f4(N.SKP_B)} = ${f0(N.S1A)} ✓`, C.ok, C.okbg, "9CC7BC"],
    ["②  幾何式", "m_f2", "已知圓心 C、半徑 R 時最快", `黏土 B：${f0(N.CA)} sin φ′ + ${f2(N.C_B)} cos φ′ = ${f2(N.R_CHECK)} = R ✓`, C.le, C.lebg, "C9BCEB"],
    ["③  NC 專用（c′ = 0）", "m_f3", "包絡線過原點 → 直角三角形斜邊就是 C", `黏土 A：sin φ′ = ${f0(N.DSD_AC / 2)} / ${f0((N.S1E_AC + N.S3E_AC) / 2)} = 0.5 → φ′ = ${N.PHI_A}° ✓`, C.eff, C.effbg, "F2B8A6"],
  ];
  P.forEach(([t, m, use, ex, col, bg, ln], i) => {
    const y = 1.45 + i * 1.5;
    panel(s, 0.6, y, 12.1, 1.35, bg, ln);
    T(s, t, 0.85, y + 0.12, 3.6, 0.35, { fontSize: 16, bold: true, color: col });
    T(s, use, 0.85, y + 0.55, 3.6, 0.7, { fontSize: 13, color: C.muted });
    eq(s, m, 4.5, y + 0.12, 1.1, 0.62, "left", 4.2);
    T(s, ex, 8.85, y + 0.12, 3.7, 1.1, { fontSize: 13, bold: true, valign: "middle" });
  });
  panel(s, 0.6, 5.95, 12.1, 1.1);
  T(s, "被動土壓係數", 0.85, 6.03, 2.5, 0.3, { fontSize: 13, bold: true, color: C.muted });
  eq(s, "m_kp", 0.85, 6.32, 0.7, 0.5, "left", 6);
  T(s, "①式就是把「σ′_1 與 σ′_3 的比例」寫成 K_p；③式是 ①式在 c′ = 0 時的特例。", 7.2, 6.05, 5.3, 0.95, { fontSize: 13, valign: "middle" });
  pageNo(s, pg);
}
// ───── 15 選式流程 ─────
{
  const s = newSlide();
  header(s, "解題 ③ · 考場選式流程", "先換有效應力，再問兩個問題：c′ 是不是 0？有幾組試驗？", C.ok);
  img(s, "fig10_flow", 0.6, 1.4, 12.1, 5.1);
  T(s, "所有路徑的起點都是「扣 u」：題目給的是總應力時，先算 σ′ = σ − u_f 再進流程。",
    0.6, 6.65, 12.1, 0.4, { fontSize: 14, bold: true, color: C.ps });
  pageNo(s, pg);
}
// ───── 16 破壞面角度 ─────
{
  const s = newSlide();
  header(s, "解題 ④ · 破壞面角度", "黃金鐵律：θ = 45° + φ′/2，絕對不能代 φ_{cu} 或 φ_u", C.ps);
  img(s, "fig11_plane", 0.6, 1.35, 12.1, 4.7);
  panel(s, 0.6, 6.15, 12.1, 0.9, C.psbg, "E6B0AA");
  T(s, `圓心到切點的連線與 σ′ 軸夾 2θ；示範黏土 A 若誤代 φ_{cu} = ${f1(N.PHI_CU_AC)}°，會把 ${f0(N.TH_A)}° 的破壞面算成 ${f1(N.TH_WRONG)}°。`,
    0.85, 6.15, 11.7, 0.9, { fontSize: 14, bold: true, color: C.ps, valign: "middle" });
  pageNo(s, pg);
}
// ───── 17 技巧 A ─────
{
  const s = newSlide();
  header(s, "解題 ⑤ · 技巧 A", "保留 K_p、√K_p 當主線，不要先轉成角度再轉回來", C.ok);
  panel(s, 0.6, 1.5, 5.95, 3.9, C.okbg, "9CC7BC");
  T(s, paras([
    { t: "✓ 主線保留 K_p", o: { bold: true, fontSize: 18, color: C.ok } },
    { t: `K_p = ${f2(N.KP_B)}，√K_p = ${f4(N.SKP_B)}`, o: { fontSize: 15 } },
    { t: `c′ = (${f0(N.S1A)} − ${f0(N.S3A)} × ${f2(N.KP_B)}) / (2 × ${f4(N.SKP_B)}) = ${f2(N.C_B)}`, o: { fontSize: 15 } },
    { t: `預測試驗 B：σ′_1 = ${f0(N.S3B)} × ${f2(N.KP_B)} + 2 × ${f2(N.C_B)} × ${f4(N.SKP_B)}`, o: { fontSize: 15 } },
    { t: `= ${f1(N.S1B)} kPa（與實測 ${f0(N.S1B)} 完全吻合）`, o: { fontSize: 17, bold: true, color: C.ok } },
  ]), 0.85, 1.65, 5.5, 3.65, { paraSpaceAfter: 8 });
  panel(s, 6.75, 1.5, 5.95, 3.9, C.psbg, "E6B0AA");
  T(s, paras([
    { t: "✗ 先轉角度、四捨五入再轉回", o: { bold: true, fontSize: 18, color: C.ps } },
    { t: `φ′ = ${f2(N.PHI_B)}° → 取 25° → K_p = ${f4(N.KP_ROUND)}`, o: { fontSize: 15 } },
    { t: `c′ = (${f0(N.S1A)} − ${f0(N.S3A)} × ${f4(N.KP_ROUND)}) / (2√K_p) = ${f2(N.C_ROUND)}`, o: { fontSize: 15 } },
    { t: `預測試驗 B：σ′_1 = ${f1(N.S1B_ROUND)} kPa`, o: { fontSize: 15 } },
    { t: `少了 ${f1(N.S1B - N.S1B_ROUND)} kPa（${f1((1 - N.S1B_ROUND / N.S1B) * 100)}%），c′ 也偏了 ${f1((N.C_ROUND / N.C_B - 1) * 100)}%`, o: { fontSize: 17, bold: true, color: C.ps } },
  ]), 7.0, 1.65, 5.5, 3.65, { paraSpaceAfter: 8 });
  panel(s, 0.6, 5.6, 12.1, 1.45);
  T(s, paras([
    { t: "為什麼有效？", o: { bold: true, fontSize: 15, color: C.ok } },
    { t: "K_p 是從試驗數據直接相除得到的「精確值」；轉成角度要經過反三角函數，再四捨五入一次，誤差就被 K_p 放大回來。題目最後才問 φ′ 時，再從 sin φ′ = (K_p − 1)/(K_p + 1) 一次算出即可。", o: { fontSize: 14 } },
  ]), 0.85, 5.7, 11.6, 1.3, { paraSpaceAfter: 4 });
  pageNo(s, pg);
}
// ───── 18 技巧 B ─────
{
  const s = newSlide();
  header(s, "解題 ⑥ · 技巧 B：相減法", "兩組試驗的 ①式直接相減，c′ 項整個消失，一步得到 K_p", C.ok);
  img(s, "fig12_subtract", 0.6, 1.35, 12.1, 4.6);
  panel(s, 0.6, 6.05, 12.1, 1.0, C.okbg, "9CC7BC");
  eq(s, "m_sub", 0.85, 6.1, 0.9, 0.55, "left", 3.2);
  T(s, `示範黏土 B：K_p = (${f0(N.S1B)} − ${f0(N.S1A)}) / (${f0(N.S3B)} − ${f0(N.S3A)}) = ${f2(N.KP_B)}；破壞面 θ = 45° + ${f2(N.PHI_B)}°/2 = ${f1(N.TH_B)}°`,
    4.3, 6.05, 8.3, 1.0, { fontSize: 14, bold: true, color: C.ok, valign: "middle" });
  pageNo(s, pg);
}
// ───── 19 陷阱 ─────
{
  const s = newSlide();
  header(s, "MISTAKES · 四大高頻陷阱", "每一個都用示範土量化給你看", C.ps);
  const items = [
    ["陷阱 1", "Δσ_d 當成 σ_1", `示範黏土 A 的 CU：Δσ_d = ${f0(N.DSD_AC)}，σ_1 = ${f0(N.S3)} + ${f0(N.DSD_AC)} = ${f0(N.S1_AC)}；把 ${f0(N.DSD_AC)} 當 σ_1 會連圓都畫錯`, C.tot],
    ["陷阱 2", "破壞面代錯角度", `給了 φ_{cu} = ${f1(N.PHI_CU_AC)}° 要先扣 u_f 求 φ′ = ${N.PHI_A}°；θ 應為 ${f0(N.TH_A)}°，不是 ${f1(N.TH_WRONG)}°`, C.ps],
    ["陷阱 3", "OC 土用比例法", `黏土 B 各組單算 sin φ = R/C：${f1(N.PHI_WRONG_A)}°、${f1(N.PHI_WRONG_B)}°，真值 ${f2(N.PHI_B)}°——c′ ≠ 0 圓不相似`, C.le],
    ["陷阱 4", "K_f 線斜率當 φ′", `α′ = ${f1(N.ALPHA_A)}° 不是 φ′；要用 sin φ′ = tan α′ 換回 ${N.PHI_A}°，截距 a 也要除以 cos φ′`, C.gold],
  ];
  items.forEach(([tag, h, b, col], i) => {
    const x = 0.6 + (i % 2) * 6.15, y = 1.5 + Math.floor(i / 2) * 2.8;
    panel(s, x, y, 5.95, 2.6);
    bar(s, x, y + 0.2, 2.2, col);
    T(s, tag, x + 0.3, y + 0.2, 3, 0.3, { fontSize: 12, bold: true, color: col, charSpacing: 2 });
    T(s, h, x + 0.3, y + 0.55, 5.4, 0.5, { fontSize: 22, bold: true });
    T(s, b, x + 0.3, y + 1.2, 5.45, 1.3, { fontSize: 14, color: C.muted });
  });
  pageNo(s, pg);
}
// ───── 20 比例法 ─────
{
  const s = newSlide();
  header(s, "陷阱 3 · 圖解", "只有包絡線過原點，莫爾圓才互為相似形", C.le);
  img(s, "fig13_ncoc", 0.6, 1.4, 12.1, 4.7);
  panel(s, 0.6, 6.2, 12.1, 0.85, C.lebg, "C9BCEB");
  T(s, "NC 黏土：σ′_3 加倍，σ′_1 就加倍（比值固定 = K_p）。OC 黏土多了 2c′√K_p 這個常數項，比值隨圍壓改變，只能用兩組聯立。",
    0.85, 6.2, 11.7, 0.85, { fontSize: 14, bold: true, color: C.le, valign: "middle" });
  pageNo(s, pg);
}
// ───── 21 自我檢查 ─────
{
  const s = newSlide();
  header(s, "CHECK · 算完 30 秒自我檢查", "兩個驗算：切點要落在包絡線上、A_f 要落在合理區間", C.ok);
  panel(s, 0.6, 1.5, 5.95, 4.2, C.okbg, "9CC7BC");
  T(s, "檢查 1：切點應力", 0.85, 1.65, 5, 0.35, { fontSize: 17, bold: true, color: C.ok });
  eq(s, "m_tff", 0.85, 2.1, 0.75, 0.5, "left", 5.4);
  T(s, paras([
    { t: `黏土 B 試驗 A：σ′_{ff} = ${f0(N.CA)} − ${f0(N.RA)} × ${f4(Math.sin(N.PHI_B * Math.PI / 180))} = ${f2(N.SFF)}`, o: { fontSize: 14 } },
    { t: `τ_{ff} = ${f0(N.RA)} × ${f4(Math.cos(N.PHI_B * Math.PI / 180))} = ${f2(N.TFF)}`, o: { fontSize: 14 } },
    { t: `c′ + σ′_{ff} tan φ′ = ${f2(N.C_B)} + ${f2(N.SFF)} × ${f4(Math.tan(N.PHI_B * Math.PI / 180))} = ${f2(N.TFF_MC)} ✓`, o: { fontSize: 14, bold: true, color: C.ok } },
    { t: "兩邊不相等 → c′ 或 φ′ 算錯了", o: { fontSize: 13, color: C.muted } },
  ]), 0.85, 3.0, 5.5, 2.6, { paraSpaceAfter: 8 });
  panel(s, 6.75, 1.5, 5.95, 4.2, C.totbg, "B9C6EA");
  T(s, "檢查 2：回推孔壓參數", 7.0, 1.65, 5, 0.35, { fontSize: 17, bold: true, color: C.tot });
  eq(s, "m_af", 7.0, 2.05, 0.9, 0.5, "left", 3);
  T(s, paras([
    { t: `黏土 A：A_f = ${f0(N.UF_AC)} / ${f0(N.DSD_AC)} = ${N.AF} ✓`, o: { fontSize: 15, bold: true, color: C.tot } },
    { t: "NC 黏土：A_f ≈ 0.5～1.0（剪縮、正孔壓）", o: { fontSize: 14 } },
    { t: "OC 黏土：A_f 小，重壓密可為負（剪脹、負孔壓）", o: { fontSize: 14 } },
    { t: "NC 題目算出負的 A_f → 多半是 u_f 正負號或 Δσ_d 用錯", o: { fontSize: 13, color: C.muted } },
  ]), 7.0, 3.0, 5.5, 2.6, { paraSpaceAfter: 8 });
  panel(s, 0.6, 5.9, 12.1, 1.15);
  T(s, paras([
    { t: "順手再驗第三件事：破壞面角度", o: { bold: true, fontSize: 15, color: C.ps } },
    { t: `θ 一定大於 45°、而且用 φ′ 算：黏土 A ${f0(N.TH_A)}°、黏土 B ${f1(N.TH_B)}°、示範砂 ${N.TH_C}°。算出小於 45° 或和 φ_{cu} 有關，就是代錯了。`, o: { fontSize: 14 } },
  ]), 0.85, 6.0, 11.6, 1.0, { paraSpaceAfter: 3 });
  pageNo(s, pg);
}
// ───── 22 重點回顧 ─────
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  T(s, "重點回顧", 0.8, 0.8, 11, 0.8, { fontSize: 36, bold: true, color: C.white });
  const pts = [
    ["1", "水不承剪 → 抗剪強度只由 σ′ 控制，一種土只有一組 (c′, φ′)", C.eff],
    ["2", `u 只平移莫爾圓：φ_{cu} 隨路徑跳動（AC ${f1(N.PHI_CU_AC)}°、LE ${f1(N.PHI_CU_LE)}°），φ′ 固定 ${N.PHI_A}°`, C.tot],
    ["3", "K_f 線 ≠ M–C 線：tan α′ = sin φ′、a = c′ cos φ′；砂的材料常數是 φ_{cv}", C.gold],
    ["4", "三條破壞式挑最短；兩組試驗用相減法；K_p 保留到最後", C.ok],
    ["5", "θ = 45° + φ′/2；OC 不可用比例法；算完驗切點與 A_f", C.ps],
  ];
  pts.forEach(([n, t, col], i) => {
    const y = 1.85 + i * 0.9;
    s.addShape(pres.shapes.OVAL, { x: 0.8, y, w: 0.58, h: 0.58, fill: { color: col }, line: { color: col } });
    T(s, n, 0.8, y, 0.58, 0.58, { fontSize: 19, bold: true, color: C.white, align: "center", valign: "middle" });
    T(s, t, 1.6, y, 11.2, 0.58, { fontSize: 18, color: C.white, valign: "middle" });
  });
  T(s, "下一步：拿「相減法」實際解一題 OC 黏土的兩組 CD 試驗考題", 0.8, 6.5, 11.5, 0.45, { fontSize: 16, bold: true, color: "F2A65A" });
}
pres.writeFile({ fileName: "SM-U1-5_真參數只有一組.pptx" }).then(() => console.log("written"));
