# 結構工程技師考試知識庫 — 土壤力學與基礎設計（SM）

> 科目代碼：SM｜資料夾：`exam-wiki-SM`｜其他科目另建獨立資料庫

## 專案說明

本資料庫專門收錄「專門職業及技術人員高等考試結構工程技師」**土壤力學與基礎設計**科目的考古題解析知識庫。

- **科目代碼：** SM（Soil Mechanics & Foundation Design）
- **題目編號格式：** SM-YYYY-N（如 SM-2015-1）
- **其他科目：** 各自建立獨立資料庫（exam-wiki-RC、exam-wiki-SS 等）

**核心工作流程：**
```
在 Cowork 開啟 exam-wiki-SM/ 資料夾（Project）
    ↓
說：「解析 XXXX 年考卷」
Cowork 讀取 CLAUDE.md + 考卷 PDF + question_index.json
  → 建立所有尚無解析的題目資料夾（已有解析者跳過）
  → 提醒你將各題附圖截圖存入對應資料夾
  → 等待你通知「截圖完成，請開始解題」
    ↓
【你做】依提醒截圖存檔，完成後告知 Cowork
    ↓
【重要】Cowork 一次只解一題，解完存檔後再繼續下一題
    ↓
你加入補充截圖（chart/eqn/hand）
請 Cowork 更新 question_index.json（tags、verified）
    ↓
說：「ingest SM-XXXX-N」→ Cowork 直接執行，wiki 自動更新
```

---

## 兩個環境分工

| 環境 | 負責什麼 |
|------|---------|
| **你（使用者）** | PDF 題目附圖截圖（fig-N.png）、chart/eqn/hand 補充截圖、人工驗算後通知 Cowork 更新 verificationStatus |
| **Cowork** | 解題（SOLVE，**一次一題**）、存檔（.md + viz.html）、更新 question_index.json、**所有 wiki 操作指令**（ingest / compile-all / lint / status / reindex / add-concept / add-method / refresh-dashboard / frequency / analyze / predict / study / find / related / unverified / query，共 16 個，詳見 CLAUDE-CODE.md）、直接維護 wiki/diagnosis/ · wiki/failure-modes/ · wiki/materials/ · wiki/code-ref/ · wiki/queries/ · study/（study 指令輸出） |

---

## 單向資料流

```
raw/solutions/SM-XXXX-N/SM-XXXX-N.md  ──→  wiki/problems/      （Cowork: ingest）
raw/json/concepts.json                 ──→  wiki/concepts/      （Cowork: compile-all）
raw/solutions/methods/                 ──→  wiki/methods/       （Cowork: compile-all）
Cowork 查詢結果                        ──→  wiki/queries/       （Cowork 直接存入）
Cowork study 指令輸出                  ──→  study/              （Cowork 直接存入）
Cowork 跨層知識工具                    ──→  wiki/diagnosis/     （Cowork 直接存入）
                                       ──→  wiki/failure-modes/ （Cowork 直接存入）
                                       ──→  wiki/materials/     （Cowork 直接存入）
                                       ──→  wiki/code-ref/      （Cowork 直接存入）

解題內容唯一來源：raw/solutions/ 下的 .md 檔案
索引資訊唯一來源：raw/json/question_index.json
wiki/queries/、study/（study 輸出）及四個跨層知識目錄：由 Cowork 直接寫入，不走 ingest 流程
```

---

## 資料夾結構

```
exam-wiki-SM/
├── README.md                        ← 冷啟動快速導覽
├── CLAUDE.md                        ← 本檔（身份層：分工、資料流、重要規則）
├── CLAUDE-SOLVE.md                  ← Cowork 解題 Skill
├── CLAUDE-CODE.md                   ← Claude Code 操作指令（Runbook）
├── CLAUDE-SPEC.md                   ← 規格驗證層（格式、命名、完成標準）
│
├── study/                           ← 讀書筆記、講義、study 指令 HTML 輸出（study-SM-UN.html / study-SM-UN-n.html）
│
├── raw/                             ← 所有原始資料（唯讀，絕對不可修改）
│   ├── exams/                       ← 原始考卷 PDF（命名：SM-YYYY_土壤力學與基礎設計.pdf）
│   ├── json/
│   │   ├── concepts.json            ← 概念定義（供 compile-all）
│   │   └── question_index.json      ← ⭐ 題目總索引（唯一需要人工維護的 JSON）
│   └── solutions/                   ← AI 解析 + 補充截圖（每題一個資料夾）
│       ├── SM-YYYY-N/
│       │   ├── SM-YYYY-N.md
│       │   ├── SM-YYYY-N-fig-1.png
│       │   ├── SM-YYYY-N-[內容碼]-viz.html
│       │   └── *.pdf                    ← 補充筆記（選用，命名無限制）
│       └── methods/                 ← 解題方法論
│
└── wiki/                            ← 知識庫輸出
    ├── index.md                     ← 主導航（七層架構）
    ├── by-year.md                   ← 依考年分類
    ├── log.md                       ← 操作紀錄（append only）
    ├── concepts/                    ← 概念頁         ← Cowork (compile-all)
    ├── methods/                     ← 方法論頁       ← Cowork (compile-all)
    ├── traps/                       ← 陷阱頁         ← Cowork (compile-all)（補充目錄，非七層架構核心）
    ├── problems/                    ← 題目頁         ← Cowork (ingest)
    ├── philosophy/                  ← 設計哲學頁     ← Cowork (compile-all)
    ├── queries/                     ← 查詢結果頁     ← Cowork (直接存入)
    ├── diagnosis/                   ← 題型診斷層     ← Cowork (直接存入)
    ├── failure-modes/               ← 失敗模式層     ← Cowork (直接存入)
    ├── materials/                   ← 材料行為層     ← Cowork (直接存入)
    └── code-ref/                    ← 規範條文對應層 ← Cowork (直接存入)
```

---

## 知識分類骨架（七層）

Wiki 導航依七層知識架構組織（前三層由 Cowork 透過 compile-all/ingest 生成，後四層由 Cowork 直接維護）：

| 層 | 目錄 | 維護者 | 內容 |
|----|------|:------:|------|
| Layer 1 | `concepts/` + `problems/` | Cowork (ingest/compile) | 核心土力/基礎觀念（土壤基本性質/滲透/壓密/土體應力/剪力強度/承載力/樁基/土壓力/邊坡穩定） |
| Layer 2 | `philosophy/` | Cowork (compile-all) | 設計哲學與實務（總應力法 vs 有效應力法、容許應力設計 vs 極限狀態設計、安全係數選取哲學） |
| Layer 3 | `methods/` | Cowork (compile-all) | 解題方法論（Terzaghi/Meyerhof承載力理論、Rankine/Coulomb土壓力理論、Fellenius/Bishop邊坡穩定法、壓密沉陷計算） |
| Layer 4 | `diagnosis/` | Cowork (直接存入) | 題型診斷決策樹 |
| Layer 5 | `failure-modes/` | Cowork (直接存入) | 失敗模式（承載力破壞/過大沉陷/滲流破壞（管湧砂湧）/邊坡滑動/擋土結構失穩） |
| Layer 6 | `materials/` | Cowork (直接存入) | 材料行為（土壤分類特性/滲透特性/壓密特性/剪力強度特性） |
| Layer 7 | `code-ref/` | Cowork (直接存入) | 規範條文對應（建築物基礎構造設計規範、大地工程手冊、建築物耐震設計規範） |

> **補充目錄 `wiki/traps/`：** 不屬於七層架構，由 compile-all 從題目解析萃取陷阱頁面，與 concepts/ 並列為輔助導航。

---

## 命題大綱分類（依官方命題大綱，93年3月公告）

> topicId 格式：`SM-UN-n`，U = 單元號，n = 子項號。
> `primaryTopicId` 填最主要考點；跨子項時用 `secondaryTopicIds` 列出。
> 最新鮮的官方分類請直接查閱 `raw/json/syllabus_taxonomy.json` 中 `id: "SM"` 的段落。

### 第一單元（SM-U1）

| topicId | 命題大綱子項 |
|---------|------------|
| SM-U1-1 | 土壤基本性質 |
| SM-U1-2 | 土壤滲透 |
| SM-U1-3 | 土壤夯實及壓密 |
| SM-U1-4 | 土體內應力 |
| SM-U1-5 | 土壤強度特性與變形性 |

### 第二單元（SM-U2）

| topicId | 命題大綱子項 |
|---------|------------|
| SM-U2-1 | 淺基礎之支承力與沉陷量 |
| SM-U2-2 | 深基礎之支承力與沉陷量 |
| SM-U2-3 | 開挖之穩定性分析 |
| SM-U2-4 | 基礎型式之選擇與評估 |
| SM-U2-5 | 地層改良方法 |

### 第三單元（SM-U3）

| topicId | 命題大綱子項 |
|---------|------------|
| SM-U3-1 | 側向土壓力理論 |
| SM-U3-2 | 擋土結構物穩定分析 |
| SM-U3-3 | 坡地工程 |
| SM-U3-4 | 生態工法在邊坡工程之應用 |

---

## 重要規則

1. **`raw/` 目錄下所有檔案絕對不可修改**（`question_index.json` 除外）
2. **`verifiedSolution` 是最終答案，不可質疑或重新計算**
3. **`wiki/log.md` 只可 append，不可刪除已有紀錄**
4. **wiki/ 大多數目錄是 compile 輸出，不可手動修改**；例外：diagnosis/ · failure-modes/ · materials/ · code-ref/ · queries/ 由 Cowork 直接維護
5. **ingest 前必須確認 verificationStatus = "verified"**
6. 概念連結使用 `[[concept_id]]`（Obsidian 相容）
7. 每次 ingest 同時更新 index.md 和 by-year.md
8. **格式與命名規範見 CLAUDE-SPEC.md；操作指令（ingest/compile/lint/status）見 CLAUDE-CODE.md，全部由 Cowork 執行**

---

## CHANGELOG

| 日期 | 變更 | 原因 |
|------|------|------|
| 2026-07-11 | 從 exam-wiki-RC 克隆，全面改寫為 SM 科目（土壤力學與基礎設計） | 建立土壤力學與基礎設計獨立知識庫；沿用 RC 版本已驗證的兩層（User/Cowork）工作流程與 16 個 Cowork 指令架構；清空 RC 領域專屬的 wiki 內容（題目解析、概念、方法論等），重置為空白索引，等待依「解析 XXXX 年考卷」流程逐年建立 SM 題庫 |
