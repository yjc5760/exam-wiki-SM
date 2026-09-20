const pptxgen = require("pptxgenjs");
const fs = require("fs");
const { imageSize } = (() => {
  // 讀 PNG 尺寸（IHDR）
  return { imageSize: (p) => { const b = fs.readFileSync(p); return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) }; } };
})();

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.title = "萬用鑰匙：固體顆粒體積永遠不變";
const F = "Microsoft JhengHei";
const K = { ink: "1F2733", muted: "5B6573", navy: "1F2733", red: "C0392B", blue: "1D4ED8", green: "2E7D6F",
  amber: "B45309", panel: "F5F7FA", border: "E1E6ED", white: "FFFFFF" };
const FIG = "figs/", EQ = "eq/";

function img(s, path, x, y, maxW, maxH, align = "c") {
  const { w, h } = imageSize(path);
  let W = maxW, H = maxW * h / w;
  if (H > maxH) { H = maxH; W = maxH * w / h; }
  const X = align === "c" ? x + (maxW - W) / 2 : x;
  s.addImage({ path, x: X, y: y + (maxH - H) / 2, w: W, h: H });
  return { X, W, H };
}
function eq(s, key, x, y, scale = 0.62, align = "l", boxW = 0) {
  const { w, h } = imageSize(EQ + key + ".png");
  const W = w / 250 * scale, H = h / 250 * scale;
  const X = align === "c" ? x + (boxW - W) / 2 : x;
  s.addImage({ path: EQ + key + ".png", x: X, y, w: W, h: H });
  return H;
}
function title(s, t, sub) {
  s.addText(t, { x: 0.6, y: 0.35, w: 12.1, h: 0.7, fontFace: F, fontSize: 30, bold: true, color: K.ink, margin: 0, isTextBox: true });
  if (sub) s.addText(sub, { x: 0.6, y: 1.05, w: 12.1, h: 0.4, fontFace: F, fontSize: 16, color: K.muted, margin: 0, isTextBox: true });
}
function para(s, runs, x, y, w, h, size = 17) {
  const arr = [];
  runs.forEach((r, i) => {
    const o = typeof r === "string" ? { text: r } : r;
    arr.push({ text: o.text, options: { bold: !!o.b, color: o.c || K.ink, fontSize: o.size || size,
      breakLine: i < runs.length - 1 && !o.inline, paraSpaceAfter: o.gap ?? 8 } });
  });
  s.addText(arr, { x, y, w, h, fontFace: F, valign: "top", margin: 0, isTextBox: true });
}
function card(s, x, y, w, h, fill = K.panel, line = K.border) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12, fill: { color: fill }, line: { color: line, width: 1.25 } });
}
function badge(s, n, x, y, col) {
  s.addShape(pres.shapes.OVAL, { x, y, w: 0.42, h: 0.42, fill: { color: col }, line: { color: col } });
  s.addText(String(n), { x, y, w: 0.42, h: 0.42, fontFace: "Arial", fontSize: 15, bold: true, color: K.white, align: "center", valign: "middle", margin: 0, isTextBox: true });
}
function pageno(s, n) {
  s.addText(`${n}`, { x: 12.3, y: 7.0, w: 0.5, h: 0.3, fontFace: "Arial", fontSize: 11, color: "9AA3AF", align: "right", margin: 0, isTextBox: true });
}
let n = 0;
const S = () => { const s = pres.addSlide(); s.background = { color: K.white }; n++; if (n > 1) pageno(s, n); return s; };

// 1 封面
{ const s = pres.addSlide(); n++; s.background = { color: K.navy };
  s.addText("SM-U1-3 土壤夯實與壓密 · 觀念專題", { x: 0.8, y: 1.5, w: 11.5, h: 0.5, fontFace: F, fontSize: 18, color: "AEB8C6", margin: 0, isTextBox: true });
  s.addText("萬用鑰匙：固體顆粒體積永遠不變", { x: 0.8, y: 2.1, w: 11.5, h: 1.1, fontFace: F, fontSize: 44, bold: true, color: K.white, margin: 0, isTextBox: true });
  s.addText("所有厚度與體積的變化，100% 來自孔隙的變化", { x: 0.8, y: 3.25, w: 11.5, h: 0.6, fontFace: F, fontSize: 22, color: "F2C38B", margin: 0, isTextBox: true });
  const items = [["①", "γd ⇄ e", "E27A6E"], ["②", "Se = wGs", "8FB0F2"], ["③", "Sc ⇄ Δe", "7CC4B4"]];
  items.forEach(([a, b, c], i) => {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.8 + i * 3.1, y: 4.6, w: 2.8, h: 1.1, rectRadius: 0.12, fill: { color: "2B3545" }, line: { color: c, width: 2 } });
    s.addText([{ text: a + "  ", options: { color: c, bold: true } }, { text: b, options: { color: K.white } }],
      { x: 0.8 + i * 3.1, y: 4.6, w: 2.8, h: 1.1, fontFace: F, fontSize: 22, align: "center", valign: "middle", margin: 0, isTextBox: true });
  });
  s.addText("示範數字全篇貫穿：案例 A 壓密黏土、案例 B 砂土、案例 C 夯實土", { x: 0.8, y: 6.4, w: 11.5, h: 0.4, fontFace: F, fontSize: 15, color: "AEB8C6", margin: 0, isTextBox: true });
}

// 2 全局
{ const s = S(); title(s, "一把鑰匙，長出三個關係式", "夯實與壓密共用同一套三相關係：先把土切成「固體 1 份 + 孔隙 e 份」");
  img(s, FIG + "SM-key-fig-01-key-map.png", 0.6, 1.6, 8.3, 5.3);
  card(s, 9.2, 1.9, 3.5, 4.7);
  para(s, [{ text: "本講義的讀法", b: true, size: 19, gap: 14 },
    { text: "先建立模型：Vs = 1 不變", gap: 10 }, { text: "再逐一推出 ①②③", gap: 10 },
    { text: "最後用同一組示範數字對帳", gap: 18 },
    { text: "三條式子都不必背，考場上 30 秒可以重推", c: K.amber, b: true }], 9.45, 2.15, 3.05, 4.3, 16);
}

// 3 為什麼 Vs 不變
{ const s = S(); title(s, "為什麼可以假設 Vs 永遠不變？", "物理直覺：加壓只會把顆粒擠得更緊，不會把顆粒壓小");
  img(s, FIG + "SM-key-fig-03-particles.png", 5.0, 1.6, 7.8, 4.9);
  const pts = [["顆粒幾乎不可壓縮", "土粒礦物的勁度遠大於土骨架，一般應力範圍內體積變化可忽略"],
    ["水也視為不可壓縮", "飽和黏土的體積減少 = 被排出的水量，這正是壓密要「等」的原因"],
    ["所以變的只有孔隙", "ΔV = ΔVv；把 Vs 定為 1，孔隙就直接等於 e"]];
  pts.forEach(([h, b], i) => {
    badge(s, i + 1, 0.6, 1.85 + i * 1.6, [K.ink, K.blue, K.green][i]);
    para(s, [{ text: h, b: true, size: 19, gap: 4 }, { text: b, size: 15, c: K.muted }], 1.2, 1.82 + i * 1.6, 3.6, 1.4);
  });
}

// 4 三相圖
{ const s = S(); title(s, "三相圖：把土切成「固體 1 份 + 孔隙 e 份」", "所有定義都是比值，所以可以任選一個基準量 —— 選 Vs = 1 最省事");
  img(s, FIG + "SM-key-fig-02-phase.png", 6.3, 1.5, 6.5, 5.6);
  const defs = [["孔隙比", "e = Vv / Vs = Vv", K.blue], ["含水量", "w = Ww / Ws", K.blue], ["飽和度", "S = Vw / Vv", K.blue], ["比重", "Gs = γs / γw → Ws = Gsγw", K.ink]];
  defs.forEach(([a, b, c], i) => {
    card(s, 0.6, 1.75 + i * 1.12, 5.4, 0.9, i % 2 ? K.white : K.panel);
    s.addText([{ text: a + "　", options: { bold: true, color: c } }, { text: b, options: { color: K.ink } }],
      { x: 0.85, y: 1.75 + i * 1.12, w: 5.0, h: 0.9, fontFace: F, fontSize: 18, valign: "middle", margin: 0, isTextBox: true });
  });
  para(s, [{ text: "案例 C 的數字（右圖）會在 ZAVC 那一頁再出現", c: K.amber, b: true }], 0.6, 6.4, 5.4, 0.5, 15);
}

// 5 壓縮前後
{ const s = S(); title(s, "壓縮前後：模型裡 ΔH 就是 Δe", "案例 A：正常壓密黏土 H0 = 4.00 m、e0 = 1.10，加壓後 e = 0.949");
  img(s, FIG + "SM-key-fig-04-columns.png", 0.5, 1.5, 8.4, 5.1);
  card(s, 9.2, 1.7, 3.6, 4.9, "FFF4E5", "F2C38B");
  para(s, [{ text: "精確講法", b: true, c: K.amber, size: 19, gap: 12 },
    { text: "「ΔH = Δe」只在模型裡成立：高度的單位是「份」。", gap: 12 },
    { text: "現場換算要乘同一個比例：", gap: 4 },
    { text: "H0 / (1 + e0) = 4.00 / 2.10 = 1.905 m/份", b: true, gap: 12 },
    { text: "Sc = 0.1505 × 1.905 = 0.287 m", b: true, c: K.red }], 9.45, 1.95, 3.15, 4.5, 16);
}

// 6 推導 εv
{ const s = S(); title(s, "推導：體積應變的分母為何是 1 + e0", "應變 = 變化量 ÷ 原始量；原始量只有一個，就是受壓前的體積");
  const steps = [["原始體積", "v0"], ["應變定義（側向束制，體積應變 = 垂直應變）", "eps"]];
  badge(s, 1, 0.6, 1.8, K.ink);
  para(s, [{ text: "原始體積與體積變化", b: true, size: 19 }], 1.2, 1.82, 6, 0.5);
  eq(s, "v0", 1.2, 2.45, 0.55);
  badge(s, 2, 0.6, 3.35, K.green);
  para(s, [{ text: "應變定義（側向束制：體積應變 = 垂直應變）", b: true, size: 19 }], 1.2, 3.37, 8, 0.5);
  eq(s, "eps", 1.2, 4.1, 0.85);
  card(s, 8.6, 4.8, 4.1, 1.9, "EAF3F1", K.green);
  para(s, [{ text: "案例 A 代入", b: true, c: K.green, size: 18, gap: 10 },
    { text: "εv = 0.1505 / 2.10 = 7.17%", gap: 8 }, { text: "ΔH = 7.17% × 4.00 m = 0.287 m", b: true }], 8.85, 5.0, 3.7, 1.6, 17);
  para(s, [{ text: "分母永遠是「初始狀態」的 1 + e0", b: true, c: K.amber, size: 20 }], 1.2, 6.0, 7.2, 0.6);
}

// 7 關係式①
{ const s = S(); title(s, "關係式 ①　孔隙比 ⇄ 乾單位重", "Ws 永遠是 Gsγw（1 份固體），總體積 1 + e，一除就出來");
  badge(s, 1, 0.6, 1.8, K.red);
  eq(s, "gd", 1.2, 1.7, 0.7);
  para(s, [{ text: "反過來求 e（題目給 γd 時）", b: true, size: 17 }], 1.2, 2.85, 5.4, 0.4);
  eq(s, "e_from_gd", 1.2, 3.3, 0.6);
  card(s, 0.6, 4.55, 5.6, 2.2);
  para(s, [{ text: "案例 A（Gs = 2.70）", b: true, size: 17, gap: 8 },
    { text: "受壓前 e = 1.100 → γd = 12.61 kN/m³", gap: 6 }, { text: "受壓後 e = 0.949 → γd = 13.59 kN/m³", gap: 10 },
    { text: "e 變小，γd 變大：同一件事的兩種講法", c: K.red, b: true }], 0.85, 4.75, 5.2, 1.9, 16);
  img(s, FIG + "SM-key-fig-05-gd-e.png", 6.5, 1.5, 6.3, 5.4);
}

// 8 RC vs Dr
{ const s = S(); title(s, "應用：RC 與 Dr 不能直接對接，只能經由 e", "案例 B：砂土 Gs = 2.65、emax = 0.90、emin = 0.45，要求 Dr = 70%");
  img(s, FIG + "SM-key-fig-06-rc-dr.png", 0.5, 1.5, 8.3, 4.1);
  card(s, 9.1, 1.6, 3.7, 3.9);
  eq(s, "dr", 9.3, 1.8, 0.5); eq(s, "rc", 9.3, 2.7, 0.5);
  para(s, [{ text: "兩者的「0%」不在同一個位置", b: true, c: K.amber, size: 16 }], 9.3, 3.7, 3.3, 1.5);
  const chain = ["Dr = 70%", "e = 0.585", "γd = 16.40", "RC = 91.5%"];
  chain.forEach((t, i) => {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.8 + i * 3.05, y: 5.95, w: 2.45, h: 0.75, rectRadius: 0.1, fill: { color: i == 3 ? "FBE3E0" : K.panel }, line: { color: i == 3 ? K.red : K.border, width: 1.25 } });
    s.addText(t, { x: 0.8 + i * 3.05, y: 5.95, w: 2.45, h: 0.75, fontFace: F, fontSize: 18, bold: true, color: i == 3 ? K.red : K.ink, align: "center", valign: "middle", margin: 0, isTextBox: true });
    if (i < 3) s.addShape(pres.shapes.RIGHT_ARROW, { x: 3.33 + i * 3.05, y: 6.17, w: 0.42, h: 0.32, fill: { color: K.muted }, line: { color: K.muted } });
  });
}

// 9 關係式②
{ const s = S(); title(s, "關係式 ②　含水量 ⇄ 飽和度", "水的體積 Vw = S·e，水的重量 ÷ 固體重量 = w");
  badge(s, 2, 0.6, 1.72, K.blue);
  eq(s, "se", 1.2, 1.6, 0.55);
  img(s, FIG + "SM-key-fig-07-saturation.png", 0.6, 2.4, 7.4, 4.7);
  card(s, 8.4, 2.6, 4.3, 3.9);
  para(s, [{ text: "考場用法", b: true, c: K.blue, size: 19, gap: 12 },
    { text: "飽和土（S = 1）：e = wGs，知道 w 就知道 e", gap: 10 },
    { text: "案例 A 受壓前 w = 1.10 / 2.70 = 40.7%，受壓後 35.2%", gap: 10 },
    { text: "飽和黏土壓密 = 排水，w 下降量正對應 Δe", c: K.amber, b: true }], 8.65, 2.85, 3.85, 3.5, 16);
}

// 10 ZAVC
{ const s = S(); title(s, "由 ② 代入 ①：零空氣孔隙線 ZAVC", "把 e = wGs / S 代入 γd = Gsγw / (1 + e)，令 S = 1 即為上限");
  eq(s, "zav", 0.8, 1.75, 0.62);
  card(s, 0.6, 3.0, 5.2, 3.7);
  para(s, [{ text: "讀圖要點", b: true, size: 19, gap: 12 },
    { text: "ZAVC 是物理上限：夯實曲線不可能穿過它", gap: 10 },
    { text: "S 越低，曲線越往左下移", gap: 10 },
    { text: "案例 C：w = 15%、e = 0.60 → γd = 16.55，S = 67.5%，落在 S = 80% 線下方", c: K.red, b: true }], 0.85, 3.2, 4.75, 3.4, 16);
  img(s, FIG + "SM-key-fig-08-zavc.png", 6.1, 1.5, 6.7, 5.4);
}

// 11 關係式③
{ const s = S(); title(s, "關係式 ③　孔隙比 ⇄ 沉陷量", "e-log p' 曲線給的是 Δe（份），乘上 H0 / (1 + e0) 才是公尺");
  img(s, FIG + "SM-key-fig-09-elogp.png", 0.5, 1.5, 8.4, 4.7);
  card(s, 9.2, 1.6, 3.6, 4.7);
  badge(s, 3, 9.4, 1.8, K.green);
  eq(s, "de", 9.4, 2.4, 0.43); eq(s, "sc", 9.4, 3.35, 0.55);
  para(s, [{ text: "案例 A", b: true, c: K.green, gap: 6 }, { text: "Cc = 0.50，p' 由 100 → 200 kPa", gap: 4 },
    { text: "Δe = 0.50 × log 2 = 0.1505", gap: 4 }, { text: "Sc = 4.00 × 0.1505 / 2.10 = 0.287 m", b: true }], 9.4, 4.45, 3.3, 1.8, 14);
  para(s, [{ text: "H 用的是 H0（初始層厚）；e 用的是 e0（初始孔隙比）—— 兩個「初始」要成對出現", b: true, c: K.amber }], 0.6, 6.4, 12.2, 0.5, 16);
}

// 12 對帳
{ const s = S(); title(s, "示範案例對帳：γd·H 前後守恆", "每平方公尺土柱裡的固體重量不會變 —— 這就是 Vs 不變的驗證方式");
  img(s, FIG + "SM-key-fig-11-check.png", 0.5, 1.5, 7.6, 4.3);
  const rows = [["", "受壓前", "受壓後"], ["e", "1.100", "0.949"], ["H（m）", "4.000", "3.713"], ["γd（kN/m³）", "12.61", "13.59"],
    ["w（飽和）", "40.7%", "35.2%"], ["γd·H（kN/m²）", "50.45", "50.45"]];
  s.addTable(rows.map((r, i) => r.map((c, j) => ({ text: c, options: { bold: i == 0 || j == 0 || i == 5, color: i == 5 ? K.green : K.ink,
    fill: { color: i == 0 ? "E8ECF2" : (i == 5 ? "EAF3F1" : K.white) }, align: j ? "center" : "left" } }))),
    { x: 8.4, y: 1.7, w: 4.4, colW: [2.1, 1.15, 1.15], rowH: 0.52, fontFace: F, fontSize: 15, border: { type: "solid", color: K.border, pt: 1 } });
  para(s, [{ text: "自我檢查：算完 Sc 後，若 γd0·H0 ≠ γd·H，代表 e 或 H 有一個算錯", b: true, c: K.amber }], 0.6, 6.2, 12.2, 0.6, 17);
}

// 13 自殺式錯誤
{ const s = S(); title(s, "考場最常見的自殺式錯誤：分母寫成 1 + e", "錯誤的分母會讓沉陷量系統性高估，壓縮越大錯越多");
  eq(s, "sc", 0.8, 1.7, 0.6); eq(s, "scw", 4.0, 1.72, 0.6);
  s.addText("正確", { x: 0.8, y: 2.65, w: 2.5, h: 0.4, fontFace: F, fontSize: 16, bold: true, color: K.green, margin: 0, isTextBox: true });
  s.addText("錯誤", { x: 4.0, y: 2.65, w: 2.5, h: 0.4, fontFace: F, fontSize: 16, bold: true, color: K.red, margin: 0, isTextBox: true });
  img(s, FIG + "SM-key-fig-10-error.png", 0.5, 3.1, 7.6, 3.9);
  card(s, 8.5, 1.7, 4.3, 5.0, "FBE3E0", "E7A79E");
  para(s, [{ text: "為什麼錯", b: true, c: K.red, size: 19, gap: 10 },
    { text: "1 + e 是受壓後的體積；應變定義是相對於「原始」體積", gap: 14 },
    { text: "錯多少", b: true, c: K.red, size: 19, gap: 10 },
    { text: "高估比例 = εv / (1 − εv)", gap: 6 }, { text: "案例 A：30.9 cm vs 28.7 cm，+7.7%", b: true, gap: 14 },
    { text: "防呆", b: true, c: K.red, size: 19, gap: 10 }, { text: "寫分母時唸出「初始」兩個字" }], 8.75, 1.95, 3.85, 4.6, 16);
}

// 14 三式互推
{ const s = S(); title(s, "三式互推：題目給哪個，就從哪個切入", "所有路線都經過 e —— 先換成孔隙比，再走到題目要的量");
  img(s, FIG + "SM-key-fig-12-hub.png", 0.9, 1.5, 11.5, 5.5);
}

// 15 總結
{ const s = pres.addSlide(); n++; s.background = { color: K.navy };
  s.addText("帶走三件事", { x: 0.8, y: 0.6, w: 11.5, h: 0.8, fontFace: F, fontSize: 36, bold: true, color: K.white, margin: 0, isTextBox: true });
  const cards = [["1", "模型", "Vs = 1 不變；孔隙 = e；總體積 = 1 + e", "8FB0F2"],
    ["2", "三式", "① γd = Gsγw/(1+e)　② Se = wGs　③ Sc = H0·Δe/(1+e0)", "7CC4B4"],
    ["3", "陷阱", "分母只能用初始的 1 + e0；RC 與 Dr 必須經 e 換算", "F2A097"]];
  cards.forEach(([a, h, b, c], i) => {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.8, y: 1.8 + i * 1.6, w: 11.7, h: 1.3, rectRadius: 0.12, fill: { color: "2B3545" }, line: { color: c, width: 2 } });
    s.addShape(pres.shapes.OVAL, { x: 1.1, y: 2.15 + i * 1.6, w: 0.6, h: 0.6, fill: { color: c }, line: { color: c } });
    s.addText(a, { x: 1.1, y: 2.15 + i * 1.6, w: 0.6, h: 0.6, fontFace: "Arial", fontSize: 20, bold: true, color: K.navy, align: "center", valign: "middle", margin: 0, isTextBox: true });
    s.addText([{ text: h + "　", options: { bold: true, color: c } }, { text: b, options: { color: K.white } }],
      { x: 2.0, y: 1.8 + i * 1.6, w: 10.3, h: 1.3, fontFace: F, fontSize: 20, valign: "middle", margin: 0, isTextBox: true });
  });
  s.addText("忘了公式時：畫一個 1 份固體 + e 份孔隙的方塊，30 秒重推", { x: 0.8, y: 6.65, w: 11.7, h: 0.45, fontFace: F, fontSize: 16, color: "F2C38B", margin: 0, isTextBox: true });
}

pres.writeFile({ fileName: "SM-U1-3-萬用鑰匙.pptx" }).then(() => console.log("done", n));
