// SM-U1-3 夯實曲線與夯實能量｜觀念講義
// 數字全部來自 demo.json（由 demo.py 產生），圖來自 gen_figs.py（SVG → 2x PNG）
const L = require("./lib.js");
const { C, FONT_HEAD, FONT_BODY } = L;
const D = require("./demo.json");
const f2 = (x) => x.toFixed(2), f1 = (x) => x.toFixed(1);

const pres = L.newPres("Gibsin 觀念講義");
pres.title = "SM-U1-3 夯實曲線與夯實能量";

// 1 ─ 封面
L.titleSlide(pres, {
  kicker: "SM-U1-3　土壤力學｜觀念講義",
  title: "夯實曲線與夯實能量\n為什麼是鐘形、為什麼往左上移",
  subtitle: "用一組五點 Proctor 試驗數據貫穿全篇：從顆粒尺度的兩個機制，一路推到 ZAVC 檢核與能量換算",
  tag: "示範案例：Gs = 2.70",
  footer: "結構技師考試「土壤力學」觀念講義｜圖解全部為 SVG 向量圖，數字可對帳",
});

// 2 ─ 主題地圖
L.topicMapSlide(pres, {
  eyebrow: "TOPIC MAP",
  title: "本單元四個問題",
  topics: [
    { title: "曲線為什麼是鐘形", desc: "乾側水是潤滑劑、濕側水是阻擋物；兩個相反機制交會出峰值。" },
    { title: "上限在哪裡", desc: "夯實只排氣、不排水。空氣排光（S = 100%）就是 ZAVC，曲線永遠碰不到。" },
    { title: "能量怎麼算、怎麼比", desc: "E = WhNL/V；修正 Proctor 約為標準的 4.5 倍，W、h、L 三個因子連乘。" },
    { title: "能量變大會怎樣", desc: "γd,max 上升、wopt 下降，峰值沿 S ≈ 85% 往左上移，仍在 ZAVC 左下方。" },
  ],
});

// 3 ─ 鐘形
L.diagramSlide(pres, {
  eyebrow: "DIAGRAM 1 · 夯實曲線",
  title: "同一能量下，γd 對 w 為什麼先升後降？",
  diagram: "fig-1-bell",
  insights: [
    "圖上五個點是示範案例的試驗結果，曲線以單調保形內插連起來，峰值直接讀出。",
    `峰值 wopt = ${f1(D.W_OPT_S)}%、γd,max = ${f2(D.GD_MAX_S)} kN/m³，這是「這個能量」下的最佳點，不是土的固定性質。`,
    "左半段加水幫顆粒滑動，右半段加水把顆粒撐開。鐘形是兩個機制的交會，不是經驗曲線。",
  ],
});

// 4 ─ 顆粒尺度
L.diagramSlide(pres, {
  eyebrow: "DIAGRAM 2 · 顆粒尺度",
  title: "同樣加水，兩側的角色完全相反",
  diagram: "fig-2-particles",
  insights: [
    "三相長條由示範數據算出：Vs = γd/(Gsγw)、Vw = wγd/γw，其餘是空氣。",
    "由乾到濕，空氣一路從 0.22 降到 0.03；固體卻在最佳點 0.66 最多，之後反而變少。",
    "濕側的空氣已經幾乎排光，多加的水只能佔掉原本屬於固體的位置，γd 必然下降。",
  ],
});

// 5 ─ 三相圖推 ZAVC
L.diagramSlide(pres, {
  eyebrow: "DIAGRAM 3 · 三相圖",
  title: "夯實只排得掉空氣，排不掉水",
  diagram: "fig-3-phase",
  insights: [
    "夯擊只有幾秒鐘，水來不及滲流排出（那是壓密的事），所以 Vw = wGs 在夯實前後不變。",
    "能被壓掉的只有空氣：e 從 0.892 → 0.514，最多壓到 Va = 0，此時 e = wGs = 0.432。",
    "把 e = wGs 代入 γd = Gsγw/(1+e)，就得到 ZAVC 公式。它是幾何上限，不是試驗曲線。",
  ],
});

// 6 ─ 公式
L.formulaSlide(pres, {
  eyebrow: "FORMULA · 三條基本關係",
  title: "從試驗數據到 ZAVC，只需要這三條",
  formulas: [
    { label: "由秤重算乾單位重", math: "gd" },
    { label: "零空氣孔隙線 ZAVC", math: "zav" },
    { label: "任意飽和度 S 的等值線", math: "sline" },
  ],
  note: "三條都由 Se = wGs 與 γd = Gsγw/(1+e) 推出；S = 1 時第三式退化為 ZAVC。w 一律用小數代入（16% → 0.16）。",
});

// 7 ─ S 等值線
L.diagramSlide(pres, {
  eyebrow: "DIAGRAM 4 · 飽和度等值線",
  title: "峰值落在 S ≈ 85%，而不是 100%",
  diagram: "fig-4-slines",
  insights: [
    "點旁數字是各試驗點的飽和度，由 S = wGs/e 算出：43% → 63% → 84% → 93% → 94%。",
    "濕側的 S 停在 92～94% 附近：殘留的封閉氣泡排不掉，所以曲線與 ZAVC 平行而不相交。",
    `峰值 S ≈ ${Math.round(D.S_OPT_S * 100)}% 是常見值（約 80～90%）。算出峰值 S 接近或超過 100%，先回頭檢查。`,
  ],
});

// 8 ─ 示範案例數據表
(function tableDemo() {
  const s = pres.addSlide(); s.background = { color: C.white };
  s.addText("WORKED EXAMPLE · 示範案例", { x: 0.6, y: 0.4, w: 11, h: 0.4, fontFace: FONT_BODY, fontSize: 13, bold: true, color: C.accent, charSpacing: 1.5, margin: 0 });
  s.addText("標準 Proctor 五點試驗：從濕土質量到 γd", { x: 0.6, y: 0.75, w: 12, h: 0.75, fontFace: FONT_HEAD, fontSize: 28, bold: true, color: C.navy, margin: 0 });
  const hdr = ["w (%)", "濕土質量 M (g)", "γ = Mg/V (kN/m³)", "γd = γ/(1+w)", "e", "S (%)", "ZAVC γzav", "檢核"];
  const rows = [hdr.map((h) => ({ text: h, options: { bold: true, color: C.white, fill: { color: C.navy }, fontSize: 13, align: "center" } }))];
  D.STD.forEach((r) => {
    const pk = Math.abs(r.w - D.W_OPT_S) < 1e-6;
    const o = { fontSize: 13, align: "center", color: pk ? "C0392B" : C.ink, bold: pk, fill: { color: pk ? "FBE1DE" : C.cardBg } };
    rows.push([f1(r.w), f1(r.M), f2(r.gam), f2(r.gd), r.e.toFixed(3), f1(r.S * 100), f2(r.zav), r.gd < r.zav ? "γd < γzav ✓" : "✗"].map((t) => ({ text: t, options: { ...o } })));
  });
  s.addTable(rows, { x: 0.6, y: 1.8, w: 12.1, colW: [1.1, 1.7, 1.9, 1.7, 1.1, 1.1, 1.6, 1.9], rowH: 0.52, fontFace: FONT_BODY, border: { type: "solid", color: "D9E1EA", pt: 0.75 } });
  s.addShape("roundRect", { x: 0.6, y: 5.25, w: 12.1, h: 1.7, rectRadius: 0.08, fill: { color: C.ice }, line: { type: "none" } });
  s.addText([
    { text: "已知：", options: { bold: true, color: C.navy } },
    { text: "V = 944 cm³、Gs = 2.70、γw = 9.81 kN/m³。", options: { breakLine: true } },
    { text: "對帳：", options: { bold: true, color: C.navy } },
    { text: `w = 16%：γ = 1953.4 × 9.81 / 944 = 20.30 → γd = 20.30 / 1.16 = 17.50；e = 26.487/17.50 − 1 = 0.514；S = 0.16 × 2.70 / 0.514 = 84.1%。`, options: { breakLine: true } },
    { text: "單位換算：", options: { bold: true, color: C.navy } },
    { text: "g/cm³ × 9.81 = kN/m³，所以 γ = M(g) × 9.81 / V(cm³) 直接得 kN/m³。", options: {} },
  ], { x: 0.9, y: 5.35, w: 11.5, h: 1.5, fontFace: FONT_BODY, fontSize: 13.5, color: C.ink, valign: "middle", margin: 0, paraSpaceAfter: 4 });
})();

// 9 ─ 解題流程
L.flowMapSlide(pres, {
  eyebrow: "SOLUTION FLOW",
  badge: "流",
  title: "解題流程：從秤重到 wopt、γd,max",
  subtitle: "一條主線，最後一定要做 ZAVC 檢核",
  tag: "SM-U1-3",
  cols: 4,
  nodes: [
    { text: "各點濕土質量 M\n與含水量 w", type: "start" },
    { text: "γ = M·g / V", type: "step" },
    { text: "γd = γ / (1+w)\nw 用小數", type: "step" },
    { text: "γd 是否 ≤ γzav(w)？", type: "decision" },
    { fork: [
      { text: "是：繼續", tint: "green" },
      { text: "否：必有算錯\n回頭查單位", tint: "pink" },
    ] },
    { text: "描點、連平滑曲線\n讀峰值", type: "step" },
    { text: "峰值 S = wGs/e\n約 80～90%？", type: "decision" },
  ],
  result: { text: `wopt = ${f1(D.W_OPT_S)}%，γd,max = ${f2(D.GD_MAX_S)} kN/m³` },
  sideNote: { title: "峰值讀法", text: "數據點間距大時，可用峰值附近三點配拋物線求極值；本例三點對稱，峰值恰在 w = 16%。", color: "blue" },
  checklist: {
    title: "三個必做檢核",
    items: [
      { label: "w 用小數", detail: "16% 代 0.16，不是 16" },
      { label: "γ 與 γd 分清", detail: "表格常給濕單位重" },
      { label: "ZAVC 上限", detail: "每一點 γd < γzav" },
    ],
  },
});

// 10 ─ ZAVC 檢核
L.diagramSlide(pres, {
  eyebrow: "DIAGRAM 5 · 合理性檢核",
  title: "算出來的點若落在 ZAVC 右上方，一定算錯",
  diagram: "fig-5-check",
  insights: [
    `w = 19% 那一點：若忘了除以 (1+w)，會得到 ${f2(D.STD[3].gam)}，比 ZAVC 上限 ${f2(D.STD[3].zav)} 還大。`,
    "S > 100% 代表「水比孔隙還多」，物理上不可能；這不是試驗誤差，是計算或單位錯。",
    `除以 1.19 後得 ${f2(D.STD[3].gd)}，回到曲線上。考場上每算一點就順手比一次 ZAVC，只要幾秒。`,
  ],
});

// 11 ─ 能量公式
L.formulaSlide(pres, {
  eyebrow: "FORMULA · 夯實能量",
  title: "E = WhNL/V：四個輸入各代表什麼",
  formulas: [
    { label: "單位體積夯實能量", math: "E" },
    { label: "標準 Proctor", math: "Estd" },
    { label: "修正 Proctor", math: "Emod" },
  ],
  note: "W 夯錘重 (N)、h 落距 (m)、N 每層夯擊數、L 層數、V 夯模體積 (m³)。N·m/m³ = J/m³，÷1000 得 kJ/m³。常見書本以 2700 kJ/m³ 近似修正值（夯錘 44.48 N 時）。",
});

// 12 ─ 能量連乘
L.diagramSlide(pres, {
  eyebrow: "DIAGRAM 6 · 能量比較",
  title: "修正是標準的 4.5 倍，倍數從哪裡來？",
  diagram: "fig-6-energy",
  insights: [
    "兩者 N 與 V 相同，所以比值只由 W、h、L 決定：1.816 × 1.498 × 1.667 = 4.54。",
    "比較兩種夯實法時不必算出 E，直接算三個比值相乘，最快也最不容易錯單位。",
    "現地對應：W 是滾壓機重量、h 與 N 對應振動與輾壓遍數、L 對應鋪築層數與層厚。",
  ],
});

// 13 ─ 曲線左上移
L.diagramSlide(pres, {
  eyebrow: "DIAGRAM 7 · 能量效應",
  title: "能量變大，曲線為什麼往「左上」移？",
  diagram: "fig-7-shift",
  insights: [
    `往上：更大的衝擊克服乾側的摩擦鎖死，γd,max 由 ${f2(D.GD_MAX_S)} 升到 ${f2(D.GD_MAX_M)}。`,
    `往左：骨架更密、孔隙更少，水墊效應提早出現，wopt 由 ${f1(D.W_OPT_S)}% 降到 ${f1(D.W_OPT_M)}%。`,
    "兩個效應是同一件事的兩面，所以峰值沿 S ≈ 85% 的等值線移動，大致平行於 ZAVC。",
  ],
});

// 14 ─ 錯誤示範
L.diagramSlide(pres, {
  eyebrow: "DIAGRAM 8 · 錯誤示範",
  title: "常見錯圖：修正曲線的濕側畫過 ZAVC",
  diagram: "fig-8-wrong-vs-right",
  note: "左圖把修正曲線畫成對稱拋物線，濕側在 w ≈ 14～20% 穿到 ZAVC 右上方（紅色區域 S > 100%），與「曲線永遠碰不到 ZAVC」矛盾。右圖以試驗點重畫：濕側 S 停在 92% 左右，與 ZAVC 平行下降，並逐漸靠近標準曲線。",
});

// 15 ─ 組構
L.diagramSlide(pres, {
  eyebrow: "DIAGRAM 9 · 黏土組構",
  title: "同樣的 γd，乾側夯與濕側夯的土不一樣",
  diagram: "fig-9-fabric",
  insights: [
    "乾側夯實：板片邊對面隨機接觸（凝聚結構），強度與勁度較高、較脆，透水性較大，遇水易膨脹。",
    "濕側夯實：夯擊的剪動把板片排成平行（分散結構），透水性低、延展性好，但強度較低、乾縮大。",
    "工程取捨：黏土心牆、襯墊要低透水 → 偏濕側；路基、承載層要強度 → 偏乾側或最佳含水量。",
  ],
});

// 16 ─ 現地控制
L.cardGridSlide(pres, {
  eyebrow: "FIELD CONTROL · 現地夯實",
  title: "試驗室曲線怎麼用到工地",
  cols: 2,
  cards: [
    { title: "相對夯實度 RC", bullets: [`RC = γd,field / γd,max；本例現地 ${f2(D.GD_FIELD)} → ${f1(D.RC)}%`, "規範常要求 ≥ 90～95%，並限定含水量在 wopt 附近範圍"] },
    { title: "為什麼要規定層厚", bullets: ["層厚對應公式裡的 L：鋪太厚，能量傳不到底部", "每層先滾壓到規定遍數，檢測合格再鋪下一層"] },
    { title: "能量不是越大越好", bullets: ["超過最佳點會壓碎顆粒、改變級配", "濕側過度輾壓：孔隙水壓升高，形成彈簧土（橡皮土）"] },
    { title: "選哪一種 Proctor", bullets: ["機場跑道、重載路基 → 修正 Proctor（能量高）", "一般填方、堤防 → 標準 Proctor；以設計採用值為準"] },
  ],
});

// 17 ─ 速查
L.cheatSheetSlide(pres, {
  eyebrow: "CHEAT SHEET · 考前速查",
  title: "夯實｜全公式一頁速查",
  cols: 2,
  items: [
    { label: "乾單位重", math: "gd" },
    { label: "ZAVC（S = 100%）", math: "zav" },
    { label: "S 等值線", math: "sline" },
    { label: "夯實能量", math: "E" },
    { label: "合理性檢核（示範 w = 19%）", math: "check" },
    { label: "相對夯實度（示範）", math: "RC" },
  ],
});

// 18 ─ 陷阱
L.trapSlide(pres, {
  eyebrow: "REVIEW",
  title: "高頻陷阱",
  traps: [
    { title: "w 用百分比代入", desc: "γd = γ/(1+w) 與 ZAVC 的 w 都要用小數。代 16 而不是 0.16，γd 會小到離譜。" },
    { title: "把 γ 當成 γd", desc: "題目表格常給濕土重或濕單位重，忘了除以 (1+w)，點就跑到 ZAVC 右上方。" },
    { title: "以為曲線會碰到 ZAVC", desc: "夯實排不掉水、也排不光封閉氣泡；濕側大約停在 S ≈ 90～95%，與 ZAVC 平行。" },
    { title: "wopt 當成土的固定性質", desc: "wopt 與 γd,max 隨能量改變；能量增加時前者降、後者升，說明時要註明是哪一種試驗。" },
    { title: "把夯實和壓密混為一談", desc: "夯實：短時間衝擊、排出空氣。壓密：長時間載重、孔隙水滲流排出。" },
    { title: "能量比值算太久", desc: "N、V 相同時，比值只看 W、h、L 三個比例相乘，不必各自算出 E。" },
  ],
});

// 19 ─ 結尾
L.closingSlide(pres, {
  title: "夯實曲線與夯實能量｜重點回顧",
  points: [
    "鐘形來自兩個機制：乾側水是潤滑劑，濕側水是阻擋物",
    "夯實只排氣不排水；空氣排光就是 ZAVC，γd = Gsγw/(1+wGs)",
    "每算一點就比一次 ZAVC：超過上限，一定是計算或單位錯",
    "E = WhNL/V；修正約為標準的 4.5 倍，曲線往左上移並平行 ZAVC",
  ],
});

pres.writeFile({ fileName: "SM-U1-3_夯實曲線與夯實能量_觀念講義.pptx" }).then(() => console.log("done"));
