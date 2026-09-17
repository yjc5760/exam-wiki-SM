const { newPres, titleSlide, topicMapSlide, formulaSlide, flowchartSlide, flowMapSlide,
        diagramSlide, cheatSheetSlide, trapSlide, tableSlide, closingSlide } = require("./lib.js");

const pres = newPres();
const FOOT = "大地工程「土壤夯實與壓密」觀念講義｜原理 · 公式 · 向量圖解";

/* 1 */
titleSlide(pres, {
  kicker: "SM-U1-3 · 大地工程｜觀念講義",
  title: "土壤夯實與壓密",
  subtitle: "全篇只有一個對立關係：夯實趕「空氣」，壓密擠「水」",
  tag: "壓密佔本單元 60% 以上題數",
  footer: FOOT,
});

/* 2 */
topicMapSlide(pres, {
  eyebrow: "TOPIC MAP",
  title: "一個總開關、一把萬用鑰匙、兩大運算主軸",
  topics: [
    { title: "總開關：夯實 vs 壓密", desc: "非飽和土排空氣、幾秒完成、屬能量問題；飽和土排水、需數月至數十年、屬滲流問題。這一刀切錯，後面全錯。" },
    { title: "萬用鑰匙：Vs 永遠不變", desc: "體積變化 100% 來自孔隙。所有應變公式都是 ΔH/H0 = Δe/(1+e0)，分母永遠是初始狀態的 1+e0。" },
    { title: "主軸一：夯實", desc: "鐘形曲線與 ZAVC、夯實能量 E、品管兩把尺（RC 與 Dr）、土方平衡以乾土重 Ws 守恆。" },
    { title: "主軸二：壓密", desc: "先判土壤記憶（p0'、pc'、OCR）選 Case A/B/C 算沉陷量，再用 Tv = cv·t/Hdr² 算速率。" },
  ],
});

/* 3 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 總開關",
  title: "為什麼要先分邊？因為兩者排掉的東西根本不同",
  diagram: "sm13-fig-1-master-switch",
  insights: [
    "夯實：非飽和土，把「空氣」趕出去。出力就有，幾秒鐘完成 —— 是能量問題。",
    "壓密：飽和土，把「水」擠出去。出力沒用，只能等孔隙水壓消散 —— 是滲流問題。",
    "看到填方、路基、夯實度、含水量 ⇒ 走夯實；看到黏土層、沉陷量、多久沉完 ⇒ 走壓密。",
    "同一個載重作用在非飽和填土與飽和黏土上，完成時間差了六、七個數量級。",
  ],
  note: "這一刀切錯，公式選錯、變數也選錯，整題不會有分。",
});

/* 4 */
formulaSlide(pres, {
  eyebrow: "FORMULA · 萬用鑰匙",
  title: "所有沉陷公式的起點：固體顆粒體積永遠不變",
  formulas: [
    { label: "體積應變 —— 分母永遠是初始狀態的 1+e0", math: "f_eps" },
    { label: "孔隙比 ⇄ 乾單位重（RC 與 Dr 的唯一橋樑）", math: "f_gd" },
    { label: "含水量 ⇄ 飽和度（S=1 代入即得 ZAVC）", math: "f_se" },
    { label: "由 e-log p' 讀到的 Δe 換成沉陷量", math: "f_sce" },
  ],
  note: "最高頻的自殺式錯誤是把分母寫成受壓後的 1+e。應變的定義是「相對於初始體積」，分母只能是初始值。",
});

/* 5 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 觀念圖解",
  title: "為什麼分母是 1+e0？把土切成「固體 1 份 + 孔隙 e 份」就看懂了",
  diagram: "sm13-fig-2-master-key",
  insights: [
    "受壓過程中固體顆粒本身不可壓縮，Vs 從頭到尾不變。",
    "所以 ΔV 全部來自孔隙：ΔV = ΔVv，而 V0 = Vs + Vv0 = 1 + e0。",
    "夯實與壓密共用同一組三相關係式，題目給哪一個就從哪一個切入。",
  ],
});

/* 6 */
formulaSlide(pres, {
  eyebrow: "FORMULA · 夯實（一）",
  title: "夯實曲線的兩個關鍵量：ZAVC 與夯實能量",
  formulas: [
    { label: "零空氣孔隙線 —— 純幾何上限，曲線永遠碰不到", math: "f_zav" },
    { label: "夯實能量 —— 錘重 × 落距 × 每層夯擊數 × 層數 ÷ 模體積", math: "f_energy" },
  ],
  note: "ZAVC 是考場的合理性檢核尺：算出來的 γd 若超過同含水量下的 γzav，代表計算或單位出錯。"
      + "標準 Proctor 約 594 kJ/m³、修正 Proctor 約 2695 kJ/m³，後者是前者的 4.5 倍。",
});

/* 7 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 物理機制",
  title: "鐘形不是經驗規律 —— 水在乾側是潤滑劑，在濕側是阻擋物",
  diagram: "sm13-fig-3-compaction-curve",
  insights: [
    "乾側：水膜太薄，顆粒被摩擦鎖死；加水潤滑讓顆粒重排 ⇒ γd 上升。",
    "濕側：水不可壓縮又來不及排掉，形成水墊把顆粒撐開 ⇒ γd 反而下降。",
    "最佳含水量 wopt 就是兩個相反機制交會的峰值，不是某個材料常數。",
    "夯擊是幾秒鐘的衝擊載重，排得掉空氣但排不掉水 —— 排水那是壓密的事。",
  ],
});

/* 8 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 物理機制",
  title: "能量增加，曲線為什麼是往「左上」移而不是整條上移？",
  diagram: "sm13-fig-4-compaction-energy",
  insights: [
    "能量大 ⇒ 乾側的摩擦鎖死被更大的衝擊克服，故 γd,max 上升。",
    "但更密的骨架代表孔隙更少，水墊效應提早發生，故 wopt 下降。",
    "兩個效應是同一件事的兩面 —— 峰值連線大致平行於 ZAVC 並落在其左側。",
    "現地機具的「能量」= 滾壓機重量 × 振動頻率 × 輾壓遍數 ÷ 鋪築層厚。",
  ],
  note: "能量不是越大越好：超過最佳點會過度夯實、破壞顆粒，濕側還可能產生彈簧土。",
});

/* 9 */
formulaSlide(pres, {
  eyebrow: "FORMULA · 夯實（二）",
  title: "品管兩把尺：細粒土看 RC、粗粒土（砂）看 Dr",
  formulas: [
    { label: "相對夯實度 —— 現地 γd 除以實驗室最大乾密度", math: "f_rc" },
    { label: "相對密度 —— 現地孔隙比在最鬆與最緊之間的百分位", math: "f_dr" },
    { label: "兩者的唯一橋樑（百分比不可直接對接）", math: "f_gd" },
  ],
  note: "Dr 的零點是「最鬆狀態」，RC 的零點是 0。同一根砂在 Dr = 0 時 RC 已經約 77~80%，"
      + "所以 RC 95% 與 Dr 95% 是完全不同的要求。",
});

/* 10 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 觀念圖解",
  title: "同一根土，兩把尺讀出來的數字差很多",
  diagram: "sm13-fig-5-rc-vs-dr",
  insights: [
    "示範砂：emax = 0.85、emin = 0.42、現地 γd = 16.40 ⇒ e = 0.615。",
    "同一根土：Dr = 55%，但 RC 已經是 88%。",
    "要互換一定要繞回 γd = Gs·γw/(1+e)，絕不能直接把兩個百分比對接。",
  ],
});

/* 11 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 土方平衡",
  title: "借土 → 運送 → 夯實，三個狀態唯一守恆的是什麼？",
  diagram: "sm13-fig-6-earthwork-balance",
  insights: [
    "體積會變、含水量會變、單位重會變 —— 只有乾土重 Ws（固體顆粒重量）不變。",
    "圖上三格的固體體積高度完全相同，這就是 Ws 守恆的幾何意義。",
    "千萬不要用「體積守恆」或「總重守恆」列式，運送與夯實都會改變體積與含水量。",
  ],
  note: "本例脹縮比 V借 / V填 = 1.117，代表要挖出比填方多 11.7% 的體積。",
});

/* 12 */
flowMapSlide(pres, {
  eyebrow: "SOLUTION FLOW",
  title: "土方平衡題：三步一路到底",
  subtitle: "一切從「完成填方」倒推回去",
  tag: "SM-U1-3",
  badge: "土",
  cols: 4,
  nodes: [
    { text: "題目給\n填方 V 與 RC", type: "start" },
    { text: "γd,填 = RC × γd,max", type: "step" },
    { text: "Ws = γd,填 · V填\n（唯一守恆量）", type: "decision" },
    { text: "問什麼？", type: "decision" },
    { fork: [
      { text: "問開挖量\nV借 = Ws ÷ γd,借", tint: "blue" },
      { text: "問加水量\nWw = Ws(w目標 − w原)", tint: "green" },
    ] },
    { text: "借土 γd,借 由 e 或 w 反推\nγd = Gsγw/(1+e)\n水重 kN ÷ γw 換成 m³", type: "step" },
  ],
  result: { text: "V借、Ww\n（含脹縮比）" },
  sideNote: {
    title: "鬆方體積",
    text: "運送中的鬆方也用同一個 Ws 除以鬆方的 γd，不必另外設未知數。",
    color: "blue",
  },
  checklist: {
    title: "三個必檢查",
    items: [
      { label: "守恆量選對", detail: "只有 Ws 守恆，不是體積也不是總重" },
      { label: "γd 對應狀態", detail: "借土、鬆方、填方各有各的 γd" },
      { label: "水重換體積", detail: "kN 要除以 γw 才是 m³" },
    ],
  },
});

/* 13 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 壓密（一）",
  title: "壓密題的第一步：算出黏土層中點的現況有效應力 p0'",
  diagram: "sm13-fig-7-effective-stress",
  insights: [
    "一律取黏土層「中點深度」代表全層 —— 因為 e-log p' 是曲線，中點應力代表平均壓縮行為。",
    "總應力逐層累加，孔隙水壓由地下水位起算，相減得有效應力。",
    "等效做法：水位以下直接用浮單位重 γ' = γsat − γw，兩種寫法答案完全相同。",
    "本例 p0' = 36 + 38.76 + 15.38 = 90.1 kPa。",
  ],
  note: "p0' 算錯，後面 Case A/B/C 一定判錯 —— 這是整題最不能省的一步。",
});

/* 14 */
formulaSlide(pres, {
  eyebrow: "FORMULA · 壓密（一）",
  title: "土壤的記憶：預壓密應力 pc' 與過壓密比 OCR",
  formulas: [
    { label: "現況有效應力（取黏土層中點）", math: "f_p0" },
    { label: "過壓密比 —— 只是 pc' 與 p0' 的比值", math: "f_ocr" },
    { label: "壓縮指數的定義；Cc 通常是 Cr 的 5~10 倍", math: "f_cc" },
  ],
  note: "pc' 是這層土在地質史上曾經承受過的最大有效應力，由 Casagrande 作圖法從 e-log p' 曲率最大點求得。",
});

/* 15 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 觀念圖解",
  title: "為什麼沉陷量會差好幾倍？因為土走的是兩條不同斜率的線",
  diagram: "sm13-fig-8-e-logp",
  insights: [
    "記憶內（p' ≤ pc'）：走再壓縮線 Cr，只是把先前被壓過的結構再壓一次，彈性為主、沉陷極小。",
    "超過記憶（p' > pc'）：走處女壓縮線 Cc，顆粒結構首次崩塌重排，不可回復、沉陷大得多。",
    "本例 Cc/Cr = 0.320/0.045 = 7.1 倍 —— 跨不跨越 pc' 的差別就在這裡。",
  ],
});

/* 16 */
formulaSlide(pres, {
  eyebrow: "FORMULA · 壓密（二）",
  title: "沉陷量三式：其實只是「走過哪幾段就加哪幾段」",
  formulas: [
    { label: "Case A　正常壓密 NC（p0' = pc'）：全程走 Cc", math: "f_caseA" },
    { label: "Case B　過壓密、未跨越（p0'+Δσ ≤ pc'）：全程走 Cr", math: "f_caseB" },
    { label: "Case C　過壓密且跨越（p0'+Δσ > pc'）：兩段相加", math: "f_caseC" },
  ],
  note: "驗算技巧：Case C 的答案必定夾在「全套 Cc」與「全套 Cr」之間。"
      + "本例 24.2 mm < 86.9 mm < 172.3 mm，一秒就能確認沒有算錯段。",
});

/* 17 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 核心圖",
  title: "不必背三條公式 —— 把 p0'、pc'、pf' 排在對數軸上就分完了",
  diagram: "sm13-fig-9-case-abc",
  insights: [
    "先把三個應力點在同一條 log p' 軸上標出來，路徑走過 Cr 段就加 Cr 項、走過 Cc 段就加 Cc 項。",
    "Case C 是歷屆最愛考的一型：只用一條公式算完全程，是本單元最高頻的扣分點。",
    "Case C 的兩段分別用 log(pc'/p0') 與 log(pf'/pc')，不要重複計入中間那一段。",
  ],
});

/* 18 */
flowMapSlide(pres, {
  eyebrow: "SOLUTION FLOW",
  title: "壓密沉陷題：從剖面圖到 Sc 的一條路",
  subtitle: "五步，每一步都有一個固定的陷阱",
  tag: "SM-U1-3",
  badge: "沉",
  cols: 5,
  nodes: [
    { text: "黏土層剖面", type: "start" },
    { text: "定中點深度\nz = (top+bot)/2", type: "step" },
    { text: "算 p0'\n水位下用 γ'", type: "step" },
    { text: "載重型式？", type: "decision" },
    { fork: [
      { text: "有限基礎\nΔσ = Q/[(B+z)(L+z)]\nz 從基底起算", tint: "blue" },
      { text: "大面積\nΔσ 全深度不折減", tint: "green" },
    ] },
    { text: "查 pc'、OCR", type: "step" },
    { text: "排對數軸\n判 Case A/B/C", type: "decision" },
    { text: "代對應公式\n（C 要兩段相加）", type: "step" },
  ],
  result: { text: "Sc（mm）" },
  sideNote: {
    title: "一秒驗算",
    text: "Case C 的答案必定夾在全套 Cc 與全套 Cr 之間；不在區間內就是段落切錯了。",
    color: "pink",
  },
  checklist: {
    title: "四個必檢查",
    items: [
      { label: "中點深度", detail: "不是層頂、不是層底" },
      { label: "浮單位重", detail: "水位以下用 γ' = γsat − γw" },
      { label: "2:1 的 z", detail: "從基礎底面起算，不是地表" },
      { label: "分母 1+e0", detail: "初始孔隙比，不是壓後的 e" },
    ],
  },
});

/* 19 */
formulaSlide(pres, {
  eyebrow: "FORMULA · 壓密（三）",
  title: "應力增量 Δσ：先判斷是「有限基礎」還是「大面積」",
  formulas: [
    { label: "有限尺寸基礎 —— 2:1 應力傳佈法（會擴散、會折減）", math: "f_21" },
    { label: "大面積均布載重 —— 全深度完全不折減", math: "f_wide" },
  ],
  note: "2:1 法的 z 從基礎底面起算（不是地表），這是最常見的計算失誤。"
      + "預壓覆土、大範圍回填、地下水位下降都屬於大面積載重。",
});

/* 20 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 觀念圖解",
  title: "同樣是外加載重，深度效應可以差一個數量級",
  diagram: "sm13-fig-10-delta-sigma",
  insights: [
    "有限基礎：應力錐往下擴散，中點的 Δσ 只剩 14.9 kPa。",
    "大面積：載重面積遠大於影響深度，應力無處可擴散，中點仍是 80 kPa。",
    "水位下降也算大面積 —— 它讓全深度的有效應力同時增加，不折減。",
  ],
  note: "判錯載重型式，沉陷量就會錯一個數量級，而且往往連 Case 都跟著判錯。",
});

/* 21 */
formulaSlide(pres, {
  eyebrow: "FORMULA · 壓密（四）",
  title: "壓密速率：最貴的一句話是「排水路徑必帶平方」",
  formulas: [
    { label: "無因次時間因數", math: "f_tv" },
    { label: "排水路徑判斷（判錯差 4 倍）", math: "f_hdr" },
    { label: "壓密度 U 小於 60% —— 拋物線近似", math: "f_u60a" },
    { label: "壓密度 U 大於等於 60% —— 對數近似", math: "f_u60b" },
  ],
  note: "實驗室試體通常是雙面排水。換算現場時，要先用實驗室的 Hdr 反推材料參數 cv，再代入現場的 Hdr 算時間。",
});

/* 22 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 核心圖",
  title: "雙面還是單面？判錯的代價是時間差 4 倍",
  diagram: "sm13-fig-11-drainage-path",
  insights: [
    "判斷只看黏土層的上下邊界：兩側都透水 ⇒ 雙面，Hdr = H/2。",
    "有一側是岩盤、不透水層或對稱面 ⇒ 單面，Hdr = H。",
    "本例 H = 4 m、cv = 3.15 m²/yr：雙面 U=90% 要 1.08 年，單面要 4.30 年。",
    "因為 Hdr 帶平方，路徑加倍時間就變 4 倍 —— 這是本單元 CP 值最高的一個判斷。",
  ],
});

/* 23 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 觀念圖解",
  title: "U 與 Tv 的兩段近似式，以及為什麼壓密末期「等不起」",
  diagram: "sm13-fig-12-u-tv",
  insights: [
    "U < 60% 走拋物線近似、U ≥ 60% 走對數近似；兩式在 60% 幾乎重合（0.283 vs 0.286），切換不會跳階。",
    "已知 U 求 t ⇒ 先看 U 有沒有過 60%；已知 t 求 U ⇒ 先算 Tv 再看有沒有過 0.286。",
    "從 90% 走到 95% 要 1.42 年，比從 0 走到 50% 的 1.00 年還久 —— 末期梯度小、滲流極慢。",
    "所以工程上不會等 U = 100%，而是用超載預壓把目標 U 拉低。",
  ],
});

/* 24 */
diagramSlide(pres, {
  eyebrow: "DIAGRAM · 工法",
  title: "超載預壓：不是把土變快，而是把「目標壓密度」降下來",
  diagram: "sm13-fig-13-preloading",
  insights: [
    "預壓沒有改變 cv、沒有改變 Hdr、也沒有改變 k —— 土的性質一點都沒動。",
    "加大載重讓最終沉陷 Scf > Sc，於是目標壓密度只要 U = Sc/Scf 就夠。",
    "本例 Δσ 由 80 提高到 125 kPa：U 只需 58%，工期從 4.30 年縮到 1.33 年，省下 69%。",
    "若要真的改變排水路徑，那要靠排水砂樁或塑膠排水帶（徑向排水），與超載是兩件事。",
  ],
});

/* 25 */
tableSlide(pres, {
  eyebrow: "KNOWLEDGE CARD · 對照表",
  title: "夯實 vs 壓密：六個維度一次分清",
  header: ["比較項目", "夯實 Compaction", "壓密 Consolidation"],
  colW: [2.6, 4.7, 4.8],
  rows: [
    ["排掉的是什麼", "空氣（非飽和土，S < 100%）", "水（飽和土，S = 100%）"],
    ["完成時間", "幾秒鐘～數分鐘（瞬時）", "數月～數十年（時間相依）"],
    ["物理本質", "能量問題：出力就有", "滲流問題：只能等 u 消散"],
    ["控制變數", "含水量 w、夯實能量 E", "cv、排水路徑 Hdr、應力歷史"],
    ["核心公式", "γd = Gsγw/(1+e)；γzav；E = WhNL/V", "Sc = CH/(1+e0)·log(·)；Tv = cv·t/Hdr²"],
    ["品管／驗收", "RC（細粒土）、Dr（粗粒土）", "沉陷觀測、孔隙水壓計、預壓卸載時機"],
    ["典型工程", "路基、填方、堤防、回填", "軟弱黏土地盤、大面積填土、預壓工法"],
  ],
});

/* 26 */
flowchartSlide(pres, {
  eyebrow: "OVERVIEW · 考場 30 秒分流",
  title: "進考場的第一個動作：先分邊，再選主軸",
  stages: [
    { type: "step", text: "① 掃題目關鍵字：填方／路基／夯實度／含水量　vs　黏土層／沉陷量／多久沉完／預壓" },
    {
      type: "decision", question: "排掉的是空氣，還是水？",
      branches: [
        { label: "空氣 · 夯實", text: "題目要 γd、w 還是 E？\n品管題：細粒土 RC ／ 粗粒土 Dr\n土方題：一律用乾土重 Ws 守恆" },
        { label: "水 · 壓密", text: "沉多少：中點 → p0' → Δσ → 排軸 → Case A/B/C\n要多久：圈上下邊界定 Hdr → Tv → U 過 60% 換式\n等太久：超載預壓把目標 U 拉低" },
      ],
    },
    { type: "result", text: "兩條支線合起來，就能回答「最終沉陷多少、什麼時候沉完、要不要預壓」" },
  ],
  note: "兩邊雖然分流，但共用同一把萬用鑰匙：Vs 不變、ΔH/H0 = Δe/(1+e0)、γd = Gsγw/(1+e)。",
});

/* 27 */
cheatSheetSlide(pres, {
  eyebrow: "CHEAT SHEET · 考前速查（一）",
  title: "萬用鑰匙與夯實主軸｜公式速查",
  cols: 3,
  items: [
    { label: "萬用鑰匙 · 體積應變", math: "f_eps" },
    { label: "三相 · 乾單位重", math: "f_gd" },
    { label: "三相 · 飽和度", math: "f_se" },
    { label: "沉陷量 · 由 Δe 換算", math: "f_sce" },
    { label: "夯實 · 零空氣孔隙線", math: "f_zav" },
    { label: "夯實 · 夯實能量", math: "f_energy" },
    { label: "品管 · 相對夯實度", math: "f_rc" },
    { label: "品管 · 相對密度", math: "f_dr" },
    { label: "土方 · 乾土重守恆", math: "f_ws" },
    { label: "土方 · 加水量", math: "f_water" },
  ],
});

/* 28 */
cheatSheetSlide(pres, {
  eyebrow: "CHEAT SHEET · 考前速查（二）",
  title: "壓密主軸｜沉陷量與速率公式速查",
  cols: 3,
  items: [
    { label: "壓密 · 現況有效應力", math: "f_p0" },
    { label: "壓密 · 過壓密比", math: "f_ocr" },
    { label: "壓密 · 壓縮指數", math: "f_cc" },
    { label: "Case A · 正常壓密", math: "f_caseA" },
    { label: "Case B · 未跨越 pc'", math: "f_caseB" },
    { label: "Case C · 跨越 pc'（兩段相加）", math: "f_caseC" },
    { label: "Δσ · 2:1 應力傳佈", math: "f_21" },
    { label: "Δσ · 大面積不折減", math: "f_wide" },
    { label: "速率 · 時間因數", math: "f_tv" },
    { label: "速率 · 排水路徑", math: "f_hdr" },
    { label: "速率 · U 小於 60%", math: "f_u60a" },
    { label: "速率 · U 大於等於 60%", math: "f_u60b" },
    { label: "速率 · 時間比（Hdr 平方）", math: "f_tratio" },
    { label: "參數 · cv 與體積壓縮係數", math: "f_cv" },
    { label: "預壓 · 目標壓密度", math: "f_pre" },
  ],
});

/* 29 */
trapSlide(pres, {
  eyebrow: "REVIEW",
  title: "高頻陷阱精選",
  traps: [
    { title: "分母寫成 1+e 而不是 1+e0", desc: "應變的定義是「相對於初始體積」。無論是夯實還是壓密、無論用 Δe 還是 ΔH，分母一律是初始狀態的 1+e0。" },
    { title: "把 Dr 與 RC 的百分比直接對接", desc: "兩把尺的零點不同：同一根砂在 Dr = 0 時 RC 已經約 77~80%。互換只能繞回 γd = Gsγw/(1+e)。" },
    { title: "土方題用「體積守恆」或「總重守恆」", desc: "運送與夯實都會改變體積與含水量，唯一守恆的是乾土重 Ws。先由完成填方算 Ws，再回推借土體積與加水量。" },
    { title: "2:1 法的 z 從地表起算", desc: "z 必須從「基礎底面」起算。若基礎埋深 Df = 1.5 m、黏土中點在地表下 8 m，代入的是 6.5 m 而不是 8 m。" },
    { title: "Case C 只用一條公式算完全程", desc: "跨越 pc' 時前半段走 Cr、後半段走 Cc，兩段必須相加。驗算：答案必定夾在全套 Cc 與全套 Cr 之間。" },
    { title: "單面／雙面排水判錯", desc: "Tv = cv·t/Hdr² 的 Hdr 帶平方，判錯時間直接差 4 倍。實驗室數據換算現場，要先用實驗室 Hdr 反推 cv 再代現場 Hdr。" },
  ],
});

/* 30 */
closingSlide(pres, {
  title: "土壤夯實與壓密｜重點回顧",
  points: [
    "一個總開關：夯實趕空氣（能量問題，幾秒）、壓密擠水（滲流問題，數月至數十年）。",
    "一把萬用鑰匙：固體體積 Vs 永遠不變，所有應變都是 Δe/(1+e0)，分母只能是初始值。",
    "夯實三件事：鐘形曲線與 ZAVC 上限、能量 E 讓曲線往左上移、品管分 RC 與 Dr；土方題用 Ws 守恆。",
    "壓密沉陷量：中點 → p0' → Δσ（有限基礎 2:1／大面積不折減）→ 排對數軸 → Case A/B/C。",
    "壓密速率：Tv = cv·t/Hdr²，Hdr 必帶平方；U 過 60% 換公式；預壓工法是把目標 U 降下來。",
    "建議從 SM-2025-1（觀念鏈題）與 SM-2003-2（Case C 雙段式經典題）開始動筆。",
  ],
});

pres.writeFile({ fileName: "SM_土壤夯實與壓密_觀念講義.pptx" }).then(() => console.log("done"));
