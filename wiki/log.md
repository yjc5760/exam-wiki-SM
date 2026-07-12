# Wiki 操作紀錄

> append-only，請勿刪除已有紀錄

---

## 2026-07-11

- **[INIT]** 從 exam-wiki-RC 克隆，全面改寫為 SM 科目（土壤力學與基礎設計）
  - 改寫 CLAUDE.md（身份層）、CLAUDE-SOLVE.md（解題規範，含土壤力學/基礎工程設計哲學框架）、CLAUDE-SPEC.md（命名規格）
  - 改寫 CLAUDE-CODE.md（Runbook）、README.md（導覽）、檔案架構索引表.md、知識庫使用說明書.md
  - 清空 RC 領域專屬的 wiki/problems、concepts、methods、diagnosis、failure-modes、materials、code-ref、philosophy、traps、queries 內容與 study/ 講義
  - 重建 wiki/index.md（SM 七層架構，三單元）、wiki/by-year.md（2002–2025 空白表格）
  - 重建 raw/json/question_index.json（空白索引）、concepts.json（24 個 SM 核心種子概念）
  - 重建 dashboard-data.js（SM_TOPICS / SM_UNITS，題目陣列清空）、index.html 品牌字串
  - 科目代碼：SM｜題目編號格式：SM-YYYY-N｜資料範圍：2002–2025（24 份考卷已就位，尚待解析）

## 2026-07-12

- **[BULK-VERIFY]** 使用者將 `raw/json/question_index.json` 全部 96 題 `verificationStatus` 由 `unverified` 改為 `verified`（人工確認）
- **[DATA-FIX]** `compile all` 前置檢查發現 17 筆 `primaryTopicId`/`secondaryTopicIds` 引用了已不存在於三單元命題大綱的 `SM-U4-*`（舊分類殘留）。已依題目內容重新對應至現行 `SM-U1~U3` 分類並修正 `question_index.json`：
  - `SM-U4-1`（淺基礎相關，4 題）→ `SM-U2-1` 淺基礎之支承力與沉陷量
  - `SM-U4-2`（樁基/深基礎相關，8 題）→ `SM-U2-2` 深基礎之支承力與沉陷量
  - `SM-U4-3`（個案判斷）→ SM-2004-4 主分類改 `SM-U2-4`；SM-2003-1 主分類改 `SM-U2-3`；SM-2002-2 副分類改 `SM-U2-5`
  - 此分類調整為依題目內容之合理判斷，建議日後人工複核
- **[COMPILE-ALL]** 執行完整編譯：
  - 生成 `wiki/concepts/*.md`（24 頁，依 `concepts.json`；含定義、前置/相關概念、關鍵公式 LaTeX 化、常見陷阱、出現題目表）
  - 生成 `wiki/problems/*.md`（96 頁，全部 `verificationStatus=verified` 題目；依 `raw/solutions/` 解析內容 + `question_index.json` 分類/標籤資訊）
  - `raw/solutions/methods/` 目前無資料夾，故未生成 `wiki/methods/` 頁面
  - 重新生成 `wiki/index.md`（七層架構 + 24 概念導覽 + 三單元題目分類表）與 `wiki/by-year.md`（2002–2025 全部年份題目連結）
  - 未觸碰 `wiki/diagnosis/`、`wiki/failure-modes/`、`wiki/materials/`、`wiki/code-ref/`、`wiki/queries/`（依規範由 Cowork 直接維護，非 compile-all 生成）
  - 題庫狀態：96/96 題已 ingest
- **[LINT]** 執行 16 項 lint 檢查，發現並修正：
  - `raw/solutions/SM-2020-1/SM-2020-1.md` 應力分布圖缺「圖說：」（已依已計算之 A/B/C/D 點數值補上）
  - `raw/solutions/SM-2017-4/SM-2017-4-fig-２.png` 檔名誤用全形數字（已更名為 ASCII `fig-2.png`）
  - 其餘 14 項檢查（斷開連結、概念缺口、手寫補充/圖形登錄、標籤數、by-year 一致性等）均為 0 問題
- **[OPTIMIZE]** 依使用者要求全面優化知識庫：
  - 概念頁品質強化（24 頁）：修正 11 處前置/相關概念方向錯置（原以命題大綱單元序號判斷，實際邏輯前置關係常與單元序號相反，如有效應力原理應為壓密理論之前置而非反向）；規範來源由單元通用描述改為逐概念具體描述
  - 新建 `wiki/philosophy/`（Layer 2）4 頁：總應力法vs有效應力法、容許應力設計vs極限狀態設計、安全係數選取哲學、排水條件對設計的影響
  - 新建 `wiki/methods/`（Layer 3）8 頁 + 對應 `raw/solutions/methods/[id]/` 原始檔：承載力法、樁基法、壓密沉陷法、側向土壓力法、擋土結構四項檢核、Fellenius法、Bishop簡化法、流網法
  - 新建 `wiki/diagnosis/`（Layer 4）6 頁：改採「跨題型判斷點」決策樹（總應力/有效應力選擇、基礎型式判斷、土壓力理論判斷、邊坡分析法選擇、開挖破壞模式判斷、承載力vs沉陷題型判斷），而非逐一對應命題大綱子項
  - 新建 `wiki/failure-modes/`（Layer 5）5 頁（五大類別齊全）、`wiki/materials/`（Layer 6）4 頁（四大主題齊全）
  - 新建 `wiki/code-ref/`（Layer 7）4 頁：規範主題對照表，**條文號留待使用者提供正式規範原文後填入**，未杜撰條文編號
  - 為 SM-U2-1／SM-U3-3 下 25 題缺互動圖之題目，依各題已計算完成之關鍵數值（安全係數、容許承載力、孔隙水壓等）生成 `-viz.html`（bearing/pressure/slope/seepage/liquidity 五類內容碼，SVG 長條圖呈現，580px 自含檔案），並更新對應 `wiki/problems/*.md` 之「圖形」區塊連結
  - 複查後仍存在的已知落差：`wiki/code-ref/` 條文號待查證；診斷/失敗模式/材料頁為初版種子內容，可持續擴充
- **[REFRESH-DASHBOARD]** 重新生成 `dashboard-data.js`：
  - `window.SM_QUESTIONS`：96 筆全部題目（含 unverified/needs-review，非僅 ingest 題目），每筆含 moduleId、主/副分類縮寫、分析法、viz 前綴陣列、tags、pdf 陣列
  - 25 題附 viz 前綴（bearing/pressure/slope/seepage/liquidity，對應本次新建之 `-viz.html`）；目前無任何題目資料夾內有補充筆記 PDF
  - `window.SM_TOPICS`／`window.SM_UNITS` 依 `syllabus_taxonomy.json` 現行三單元十四子項重新擷取
  - `index.html` 本身未變動
- **[STUDY]** 使用者要求對 5 個子項命題大綱（SM-U1-3、SM-U1-5、SM-U2-1、SM-U2-2、SM-U3-3）產生子項層級複習頁，依規格各生成七區塊自含互動 HTML，存至 `study/`：
  - `study-SM-U1-3.html`（土壤夯實及壓密，23題）：夯實曲線/壓密沉陷分 compaction／consolidation 兩類；含 NC/OC 沉陷量與 Tv-時間 兩組計算器
  - `study-SM-U1-5.html`（土壤強度特性與變形性，10題）：分 triaxial／strength_concept 兩類；含 p-q 法求 c'/φ' 計算器
  - `study-SM-U2-1.html`（淺基礎之支承力與沉陷量，10題）：實際考題約半數為滲流/降水計算而非純承載力，分 bearing／seepage 兩類；含 Terzaghi/Meyerhof 承載力計算器 + 達西定律滲流量計算器
  - `study-SM-U2-2.html`（深基礎之支承力與沉陷量，10題）：分 pile／ground_improve 兩類；含 α法（總應力）與 β法（有效應力）樁承載力計算器
  - `study-SM-U3-3.html`（坡地工程，15題）：實際考題絕大多數為深開挖擋土結構（連續壁/鈑樁）問題而非圓弧滑動邊坡分析，分 wall_stability／heave_seepage 兩類；含懸臂擋土牆 FS 計算器 + Terzaghi 抗隆起 FS 計算器
  - 五頁共通結構：①KPI總覽+子分類篩選+年度長條圖 ②SVG剖面圖解 ③SVG決策樹 ④KaTeX公式卡 ⑤可篩選考題清單（連結至 `wiki/problems/`）⑥高頻陷阱卡（均引用實際題目編號）⑦互動計算器
  - 驗證：所有 `<script>` 區塊經 `node --check` 語法檢查通過；各計算器均以預設參數手算覆核數值正確；確認考題清單中每一 ID 均對應存在的 `wiki/problems/*.md`
  - 已知取捨：SM-U2-1 與 SM-U3-3 之命題大綱名稱與實際考題內容有落差（詳見頁面內說明區塊），計算器設計已依實際題型調整，未強行套用大綱字面（如邊坡圓弧滑動法）
