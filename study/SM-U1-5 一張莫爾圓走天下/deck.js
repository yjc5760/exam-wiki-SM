const pptxgen = require("pptxgenjs");
const fs = require("fs");
const N = JSON.parse(fs.readFileSync("nums.json", "utf8"));
const MJ = JSON.parse(fs.readFileSync("figs/math.json", "utf8"));
const pres = new pptxgen(); pres.layout = "LAYOUT_WIDE"; pres.title = "SM-U1-5 拼圖三：一張 Mohr 圓走天下";
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

const PHI = f2(N.PHI), TH = f2(N.TH), SF = f2(N.SF), TF = f2(N.TF), Y = f4(N.Y);
// 公式面板：標題＋一條公式
function eqPanel(s, x, y, w, h, title, name, col, bg, ln, note) {
  panel(s, x, y, w, h, bg || C.panel, ln || C.line);
  T(s, title, x + 0.2, y + 0.1, w - 0.4, 0.32, { fontSize: 14, bold: true, color: col || C.ink });
  const eh = note ? h - 0.95 : h - 0.55;
  eq(s, name, x + 0.2, y + 0.45, eh, 0.6, "left", w - 0.4);
  if (note) T(s, note, x + 0.2, y + h - 0.42, w - 0.4, 0.34, { fontSize: 12, color: C.muted });
}
// ───── 1 封面 ─────
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  T(s, "SM-U1-5　土壤強度｜觀念講義・拼圖三", 0.8, 1.2, 11, 0.4, { fontSize: 16, color: "9FB3C8", bold: true });
  T(s, "一張 Mohr 圓走天下", 0.8, 1.8, 11.8, 1.1, { fontSize: 48, bold: true, color: C.white });
  T(s, "莫爾圓不是公式，是「應力轉換的幾何圖解」：圓心 C、半徑 R、切點 T 三樣東西，推出所有破壞條件式", 0.8, 3.0, 11.8, 0.9, { fontSize: 20, color: "D6DEE8" });
  const dots = [["C", "圓心 = 平均有效應力", "9FB3C8"], ["R", "半徑 = 最大剪應力", "7FA7D9"], ["T", "切點 = 破壞面 (σ, τ)", "F2A65A"]];
  dots.forEach(([n, lab, col], i) => {
    const x = 0.8 + i * 4.0;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 4.35, w: 3.7, h: 0.8, fill: { color: "243044" }, line: { color: col, width: 2 }, rectRadius: 0.1 });
    T(s, n, x + 0.2, 4.35, 0.6, 0.8, { fontSize: 24, bold: true, color: col, valign: "middle" });
    T(s, lab, x + 0.85, 4.35, 2.8, 0.8, { fontSize: 15, bold: true, color: C.white, valign: "middle" });
  });
  T(s, `示範題 [SM-2024-1] CD 試驗：σ′_3 = ${N.S3}、Δσ_d = ${N.DSD}、c′ = ${N.CC} kPa；圖上數字全部由同一支程式算出，可逐一對帳`,
    0.8, 6.3, 11.8, 0.4, { fontSize: 14, color: "9FB3C8" });
}
// ───── 2 總覽 ─────
figSlide("OVERVIEW · 三把鑰匙", "只要主應力確定，莫爾圓就唯一確定：C、R、T 決定一切", "fig01_map", [
  ["C 與 R：所有題目共用", ["由 σ′_1、σ′_3 直接算出，第一步永遠先把它們寫出來"], C.ink],
  ["T：破壞的那一瞬間", ["圓長大到剛好切到包絡線；切點就是實體破壞面上的應力"], C.eff, C.effbg, "F2B8A6"],
  ["三條公式 = 同一張圖", ["① 萬能式、② 幾何式、③ 正弦式只是不同寫法，不必各自死背"], C.tot, C.totbg, "B9C6EA"],
], C.eff, 4.5);
// ───── 3 應力轉換 ─────
{
  const s = figSlide("底層觀念 ① · 應力轉換", "圓上每一點，都是試體內某個方向平面上的 (σ, τ)", "fig02_transform", [], C.eff, 4.35);
  panel(s, 0.6, 5.9, 5.2, 1.15, C.totbg, "B9C6EA");
  eq(s, "m_trs", 0.85, 5.98, 0.46, 0.55, "left", 4.8);
  eq(s, "m_trt", 0.85, 6.5, 0.46, 0.55, "left", 4.8);
  panel(s, 5.95, 5.9, 6.75, 1.15, C.panel);
  T(s, paras([
    { t: `驗算 θ = ${N.TH_EX}°：σ = 220 + 120 cos 60° = ${f0(N.SX_EX)}、τ = 120 sin 60° = ${f1(N.TX_EX)}`, o: { fontSize: 14, bold: true } },
    { t: "θ = 0 → σ_1 面（τ = 0）；θ = 90° → σ_3 面；θ = 45° → 圓頂 τ_{max} = R", o: { fontSize: 13, color: C.muted } },
  ]), 6.15, 5.98, 6.4, 1.0, { paraSpaceAfter: 4, valign: "middle" });
}
// ───── 4 三軸加載 ─────
figSlide("底層觀念 ② · 三軸加載", "先圍壓、再軸差：圓從一個點長大，碰到包絡線就破壞", "fig03_loading", [
  ["階段① 施加圍壓 σ_3", ["各向同性：σ_1 = σ_3，圓縮成 σ 軸上一點"], C.tot, C.totbg, "B9C6EA"],
  ["階段② 施加軸差 Δσ_d", ["σ_3 不動、σ_1 往右推：圓心與半徑同時變大"], C.ink],
  ["破壞瞬間", ["圓周剛好切到包絡線：切點 T = 實體破壞面的應力狀態"], C.eff, C.effbg, "F2B8A6"],
], C.eff, 4.5);
// ───── 5 陷阱 Δσd ─────
{
  const s = figSlide("高頻第一大陷阱", "題目給的 Δσ_d 是「應力差」，不是大主應力", "fig04_trap", [], C.ps, 4.35);
  panel(s, 0.6, 5.9, 5.0, 1.15, C.goldbg, "E6CFA0");
  T(s, "第一步永遠先做", 0.8, 5.96, 4.6, 0.3, { fontSize: 13, bold: true, color: C.gold });
  eq(s, "m_s1", 0.8, 6.28, 0.62, 0.6, "left", 4.6);
  panel(s, 5.75, 5.9, 6.95, 1.15, C.psbg, "EBB4AE");
  T(s, paras([
    { t: "為什麼會搞混？", o: { bold: true, fontSize: 14, color: C.ps } },
    { t: "三軸儀的活塞只「額外」推 Δσ_d，圍壓 σ_3 同時也作用在試體頂面。", o: { fontSize: 13 } },
    { t: "題目寫「破壞時軸差應力」「deviator stress」都是 Δσ_d。", o: { fontSize: 13 } },
  ]), 5.95, 5.96, 6.6, 1.05, { paraSpaceAfter: 2 });
}
// ───── 6 C、R ─────
{
  const s = figSlide("核心幾何 · 所有題目共用的兩個量", "C 決定圓在哪、R 決定圓多大", "fig05_cr", [], C.eff, 4.3);
  panel(s, 0.6, 5.85, 6.0, 1.2, C.panel);
  eq(s, "m_C", 0.85, 5.92, 1.06, 0.62, "left", 5.5);
  panel(s, 6.75, 5.85, 5.95, 1.2, C.totbg, "B9C6EA");
  eq(s, "m_R", 7.0, 5.92, 1.06, 0.62, "left", 5.5);
}
// ───── 7 相切三角形 ─────
{
  const s = figSlide("三條式 ② · 幾何關係式", "相切 = 圓心到切線的垂直距離等於 R：一個直角三角形", "fig06_triangle", [], C.tot, 4.45);
  eqPanel(s, 0.6, 5.95, 5.4, 1.1, "② 幾何式（已知 C、R 時最快）", "m_f2", C.tot, C.totbg, "B9C6EA");
  panel(s, 6.15, 5.95, 6.55, 1.1, C.panel);
  T(s, paras([
    { t: "三角形三個角色", o: { bold: true, fontSize: 14 } },
    { t: `斜邊 = C + c′ cot φ′ = ${f0(N.C)} + ${f1(N.A0)} = ${f1(N.HYP)}；對邊 = R = ${f0(N.R)}；夾角 = φ′`, o: { fontSize: 13 } },
    { t: `驗算：${f0(N.R)} / ${f1(N.HYP)} = ${f4(N.R / N.HYP)} = sin ${PHI}° ✓`, o: { fontSize: 13, bold: true, color: C.ok } },
  ]), 6.35, 6.0, 6.2, 1.0, { paraSpaceAfter: 1 });
}
// ───── 8 推導 ① ─────
{
  const s = newSlide();
  header(s, "三條式 ① · 萬能表示式", "把 C、R 代回 ② 式，四行代數就得到萬能式", C.eff);
  panel(s, 0.6, 1.5, 7.3, 5.55);
  const steps = [["① 代入 C、R", "m_d1", C.tot], ["② 同乘 2、移項整理", "m_d2", C.ink], ["③ 兩邊除以 (1 − sin φ′)", "m_d3", C.ink], ["④ 三角恆等式", "m_d4", C.ok]];
  steps.forEach(([t, m, col], i) => {
    const y = 1.62 + i * 1.33;
    T(s, t, 0.85, y, 6.8, 0.32, { fontSize: 15, bold: true, color: col });
    eq(s, m, 0.85, y + 0.36, 0.86, 0.5, "left", 6.8);
  });
  panel(s, 8.1, 1.5, 4.6, 2.55, C.effbg, "F2B8A6");
  T(s, "得到 ① 萬能式（任何土壤適用）", 8.3, 1.62, 4.2, 0.35, { fontSize: 15, bold: true, color: C.eff });
  eq(s, "m_f1", 8.3, 2.05, 0.6, 0.55, "left", 4.2);
  eq(s, "m_kp", 8.3, 2.8, 0.95, 0.5, "left", 4.2);
  panel(s, 8.1, 4.2, 4.6, 2.85, C.panel);
  T(s, paras([
    { t: "物理意義", o: { bold: true, fontSize: 15 } },
    { t: "σ′_3 K_p：摩擦把圍壓「放大」K_p 倍", o: { fontSize: 14 } },
    { t: "2c′√K_p：凝聚力額外撐住的部分", o: { fontSize: 14 } },
    { t: `示範題：K_p = ${f4(N.KP)}`, o: { fontSize: 14, bold: true, color: C.eff } },
    { t: `100 × ${f4(N.KP)} + 50 × ${Y} = ${f2(N.S3 * N.KP + 2 * N.CC * N.Y)} ✓`, o: { fontSize: 14, bold: true, color: C.ok } },
  ]), 8.3, 4.32, 4.2, 2.65, { paraSpaceAfter: 6 });
  pageNo(s, pg);
}
// ───── 9 NC 正弦 ─────
{
  const s = figSlide("三條式 ③ · NC 黏土專用", "c′ = 0：包絡線過原點，斜邊直接就是 C", "fig07_nc", [], C.ok, 4.3);
  eqPanel(s, 0.6, 5.85, 6.3, 1.2, "③ 正弦式（僅限 c′ = 0）", "m_f3", C.ok, C.okbg, "9CC7BC");
  panel(s, 7.05, 5.85, 5.65, 1.2, C.panel);
  T(s, paras([
    { t: "適用：正常壓密（NC）黏土、乾淨砂土", o: { bold: true, fontSize: 14, color: C.ok } },
    { t: "例子來自拼圖二黏土 A 的 CD 試驗：σ′_3 = 100 → σ′_1 = 300", o: { fontSize: 13 } },
    { t: "OC 黏土（c′ ≠ 0）硬套 → φ′ 高估", o: { fontSize: 13, color: C.ps, bold: true } },
  ]), 7.25, 5.93, 5.3, 1.05, { paraSpaceAfter: 2 });
}
// ───── 10 選式流程 ─────
figSlide("三條式怎麼選", "看題目給了什麼、缺什麼：四個問題決定用哪一條", "fig08_flow", [
  ["口訣", ["過原點用 ③；已知 φ′ 用 ②；已知 c′ 用 ①；什麼都不知道就兩組試驗相減"], C.ink],
], C.eff, 4.85);
// ───── 11 破壞面角度 ─────
{
  const s = figSlide("破壞面 ① · 角度", "θ = 45° + φ′/2：兩行幾何證明", "fig09_angle", [], C.ps, 4.3);
  eqPanel(s, 0.6, 5.85, 3.9, 1.2, "第一步：半徑 ⊥ 切線", "m_2th", C.ink);
  eqPanel(s, 4.65, 5.85, 3.9, 1.2, "第二步：圓上角 ÷ 2", "m_th", C.ps, C.psbg, "EBB4AE");
  panel(s, 8.7, 5.85, 4.0, 1.2, C.panel);
  T(s, paras([
    { t: "示範題", o: { bold: true, fontSize: 14 } },
    { t: `2θ = 90° + ${PHI}° = ${f2(2 * N.TH)}°`, o: { fontSize: 13 } },
    { t: `θ = ${TH}° = arctan √K_p`, o: { fontSize: 13, bold: true, color: C.ps } },
  ]), 8.9, 5.93, 3.7, 1.05, { paraSpaceAfter: 2 });
}
// ───── 12 切點應力 ─────
{
  const s = figSlide("破壞面 ② · 切點座標", "破壞面上的應力：從圓心沿半徑走到 T", "fig10_point", [], C.eff, 4.5);
  eqPanel(s, 0.6, 6.05, 5.95, 1.0, "正向應力（往左 R sin φ′）", "m_sff", C.eff, C.effbg, "F2B8A6");
  eqPanel(s, 6.75, 6.05, 5.95, 1.0, "剪應力（往上 R cos φ′）", "m_tff", C.gold, C.goldbg, "E6CFA0");
}
// ───── 13 黃金鐵律 ─────
figSlide("黃金鐵律", "問破壞面角度或破壞面上的 σ、τ：一律只用有效 φ′", "fig11_rule", [
  ["為什麼", ["土壤破壞是顆粒間的摩擦滑動，摩擦由有效應力控制；同一試體的實體破壞面只有一個角度"], C.ps, C.psbg, "EBB4AE"],
  ["φ_{cu} 只是表觀角度", ["它隨加載路徑跳動（拼圖一：AC、LE 不同）；代入會把 θ 低估 (φ′ − φ_{cu})/2"], C.tot, C.totbg, "B9C6EA"],
  ["只給 φ_{cu} 怎麼辦", ["用 u_f 把總應力圓左移成有效圓 → 求 φ′ → 再算 θ"], C.ok, C.okbg, "9CC7BC"],
], C.ps, 4.4);
// ───── 14 示範題 Step 1 ─────
{
  const s = newSlide();
  header(s, "實戰 SOP · [SM-2024-1] CD 試驗", "Step 1：建立主應力與莫爾圓基礎參數", C.gold);
  panel(s, 0.6, 1.45, 12.1, 0.75, C.goldbg, "E6CFA0");
  T(s, `題目已知：圍壓 σ′_3 = ${N.S3} kPa、破壞軸差應力 Δσ_d = ${N.DSD} kPa、凝聚力 c′ = ${N.CC} kPa　　→ 求 φ′、θ、σ′_{ff}、τ_{ff}`,
    0.85, 1.45, 11.7, 0.75, { fontSize: 15, bold: true, valign: "middle" });
  img(s, "fig12_setup", 0.6, 2.35, 12.1, 4.45);
  pageNo(s, pg);
}
// ───── 15 Step 2 ─────
{
  const s = figSlide("實戰 SOP · Step 2", "解 φ′：令 y = √K_p，一元二次式一次解完", "fig13_chain", [], C.gold, 4.35);
  panel(s, 0.6, 5.9, 12.1, 1.15, C.panel);
  eq(s, "m_q1", 0.85, 5.98, 0.46, 0.5, "left", 5.6);
  eq(s, "m_q2", 0.85, 6.5, 0.46, 0.5, "left", 5.6);
  eq(s, "m_q3", 6.3, 6.02, 0.95, 0.5, "left", 6.2);
}
// ───── 16 Step 3 ─────
figSlide("實戰 SOP · Step 3", "破壞面角度與破壞面應力：全部在同一張圖上", "fig14_full", [
  ["破壞面夾角", [`θ = arctan ${Y} = ${TH}°`, "（由水平面量起）"], C.ps, C.psbg, "EBB4AE"],
  ["正向應力", [`σ′_{ff} = 220 − 120 sin ${PHI}° = ${SF} kPa`], C.eff, C.effbg, "F2B8A6"],
  ["剪應力", [`τ_{ff} = 120 cos ${PHI}° = ${TF} kPa`], C.gold, C.goldbg, "E6CFA0"],
], C.gold, 4.45);
// ───── 17 Step 4 雙向檢核 ─────
{
  const s = newSlide();
  header(s, "實戰 SOP · Step 4", "免費雙向檢核：同一個切點，三條路都要走得到", C.ok);
  const rows = [
    ["檢核 A：切點在包絡線上", "m_chk1", "代入 τ = c′ + σ′ tan φ′", C.ok, C.okbg, "9CC7BC"],
    ["檢核 B：② 幾何式", "m_chk2", "圓心到切線距離 = R", C.tot, C.totbg, "B9C6EA"],
    ["檢核 C：2θ 轉換式", "m_chk3", "與 C − R sin φ′ 同答案", C.gold, C.goldbg, "E6CFA0"],
  ];
  rows.forEach(([t, m, note, col, bg, ln], i) => {
    const y = 1.5 + i * 1.55;
    panel(s, 0.6, y, 12.1, 1.4, bg, ln);
    T(s, t, 0.85, y + 0.12, 3.6, 0.4, { fontSize: 16, bold: true, color: col });
    T(s, note, 0.85, y + 0.6, 3.6, 0.6, { fontSize: 13, color: C.muted });
    eq(s, m, 4.4, y + 0.22, 0.95, 0.62, "left", 8.1);
  });
  panel(s, 0.6, 6.2, 12.1, 0.85, C.dark, C.dark);
  T(s, `三項全過（差 < 0.01 kPa）才交卷。φ′ 精確值 ${f3(N.PHI)}°，寫 ${PHI}°；若先把 θ 取到 58.17° 再乘 2，會得 26.34°——兩者都算對，但驗算請用未取整的數字。`,
    0.85, 6.2, 11.6, 0.85, { fontSize: 14, bold: true, color: C.white, valign: "middle" });
  pageNo(s, pg);
}
// ───── 18 避坑清單 ─────
{
  const s = newSlide();
  header(s, "考場避坑速查", "四個最常見的失分點", C.ps);
  const cards = [
    ["1", "軸差當成大主應力", [`先做 σ_1 = σ_3 + Δσ_d`, `示範題誤用：φ′ = ${f2(N.PHI_TRAP)}°（真值 ${PHI}°）`], C.ps, C.psbg, "EBB4AE"],
    ["2", "圓上角當成實體角", ["圓上切點圓心角是 2θ", `θ = ${TH}°，不是 ${f2(2 * N.TH)}°`], C.tot, C.totbg, "B9C6EA"],
    ["3", "用 φ_{cu} 算破壞面", ["實體破壞面只由 φ′ 決定", `黏土 A：${f0(N.TH_A)}° vs 誤算 ${f1(N.TH_WRONG_A)}°`], C.eff, C.effbg, "F2B8A6"],
    ["4", "過早轉角度", ["解出 √K_p 後直接往下代", `先取 26° 再轉回：σ′_1 少 ${f1(N.S1 - N.S1_RND)} kPa`], C.gold, C.goldbg, "E6CFA0"],
  ];
  cards.forEach(([n, hd, body, col, bg, ln], i) => {
    const x = 0.6 + i * 3.05;
    panel(s, x, 1.55, 2.9, 5.0, bg, ln);
    s.addShape(pres.shapes.OVAL, { x: x + 0.25, y: 1.8, w: 0.7, h: 0.7, fill: { color: col }, line: { color: col } });
    T(s, n, x + 0.25, 1.8, 0.7, 0.7, { fontSize: 24, bold: true, color: C.white, align: "center", valign: "middle" });
    T(s, hd, x + 0.25, 2.7, 2.5, 0.9, { fontSize: 18, bold: true, color: col });
    T(s, paras(body.map((t, k) => ({ t, o: { fontSize: 14, bold: k === 0, color: k === 1 ? C.muted : C.ink } }))), x + 0.25, 3.7, 2.45, 2.7, { paraSpaceAfter: 10 });
  });
  T(s, "寫答案前，對照這四格各花 5 秒", 0.6, 6.65, 12.1, 0.4, { fontSize: 15, bold: true, color: C.muted, align: "center" });
  pageNo(s, pg);
}
// ───── 19 重點回顧 ─────
{
  const s = pres.addSlide(); s.background = { color: C.dark };
  T(s, "重點回顧", 0.8, 0.8, 11, 0.8, { fontSize: 36, bold: true, color: C.white });
  const pts = [
    ["1", "莫爾圓 = 應力轉換圖：實體平面轉 θ，圓上轉 2θ", C.gold],
    ["2", "先 σ_1 = σ_3 + Δσ_d，再算 C = (σ′_1 + σ′_3)/2、R = Δσ_d/2", C.ok],
    ["3", "三條式同一張圖：① σ′_1 = σ′_3 K_p + 2c′√K_p　② R = C sin φ′ + c′ cos φ′　③ sin φ′ = R/C（c′ = 0）", C.eff],
    ["4", "破壞面：θ = 45° + φ′/2 = arctan √K_p；σ′_{ff} = C − R sin φ′、τ_{ff} = R cos φ′", C.ps],
    ["5", "只用 φ′ 算破壞面；保留 √K_p 往下代；最後用包絡線與 ② 式雙向檢核", C.tot],
  ];
  pts.forEach(([n, t, col], i) => {
    const y = 1.85 + i * 0.9;
    s.addShape(pres.shapes.OVAL, { x: 0.8, y, w: 0.58, h: 0.58, fill: { color: col }, line: { color: col } });
    T(s, n, 0.8, y, 0.58, 0.58, { fontSize: 19, bold: true, color: C.white, align: "center", valign: "middle" });
    T(s, t, 1.6, y - 0.1, 11.2, 0.78, { fontSize: 17, color: C.white, valign: "middle" });
  });
  T(s, "下一步：拼圖四（NC / OC 分岔）——包絡線過原點時，正弦式、比例法與 S_u/σ′_{v0} 三大秒殺捷徑", 0.8, 6.5, 11.8, 0.45, { fontSize: 16, bold: true, color: "F2A65A" });
}
pres.writeFile({ fileName: "SM-U1-5_一張莫爾圓走天下.pptx" }).then(() => console.log("written"));
