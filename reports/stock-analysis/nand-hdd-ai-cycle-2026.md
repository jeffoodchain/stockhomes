---
title: AI 時代下的 NAND × HDD：誰有訂價權？NAND 廠商地圖與投資觀察
date: 2026-05-28
category: semiconductors
tags: [NAND, HDD, Seagate, AI, 記憶體]
description: 從希捷 CEO 與財報狗整理切入，盤點 NAND 主要廠商，並拆解「NAND 漲價 → HDD 相對競爭力提升」的邏輯與風險。
---

> 先講結論：
> 在 AI 帶動儲存需求、且 NAND 價格上行的環境下，HDD 並不是「被淘汰的舊技術」，而是資料中心分層儲存架構中、對成本最敏感那一層的核心基礎設施。只要 NAND 供給維持紀律，HDD（尤其 nearline）的議價能力確實有機會延續。

## 一、NAND 有哪些主要廠商？

以下先列「全球主流 NAND 供給端」，用產業常見分組方式（不含模組品牌商）：

1. **Samsung Electronics（三星）**
2. **SK hynix（含 Solidigm）**
3. **Micron（美光）**
4. **Kioxia（鎧俠）**
5. **SanDisk / Western Digital NAND 業務體系**（近年公司架構有調整，閱讀財報時要確認口徑）
6. **YMTC（長江存儲）**（中國供應鏈）

【補充】NAND 供給長期是寡佔市場，重點不是「有幾家」，而是「每家 capex / 產能利用率 / 節點切換速度 / 產品組合（enterprise vs consumer）」如何變化。

## 二、你提到的核心敘事：NAND 漲價，反而讓 HDD 變重要

### 1) 來自 Seagate 管理層的訊號

根據你提供的 Futu 轉述（引述 Seagate CEO Dave Mosley 在美銀投資人會議說法）：

- NAND 價格上升時，HDD 在 **TCO（總持有成本）**優勢更明顯。
- 客戶在高性能需求上，會回頭要求 HDD 提供更多性能（例如 dual actuator）。
- Mosley 引述近線 HDD 需求約 **1.5 ZB，且朝 2 ZB 前進**，量體顯著大於資料中心 NAND 容量。

這段敘事背後其實是資料中心現實：

- **熱資料**：高性能層（DRAM / 高階 SSD）
- **暖冷資料**：容量與成本優先（nearline HDD）

當 NAND 價格上行太快，企業會更積極把「不必常態低延遲」的資料往 HDD 層移。

### 2) 財報狗脈絡（補上你指定的 Industry Report #44）

除了 Podcast（S2E400，美光季報）外，你補的這篇更直接：

- 財報狗產業報告 #44 指出，2026Q1 NAND 主要原廠營收普遍強勁季增（文中列舉三星、海力士、鎧俠、美光、SanDisk）。
- 報告把驅動力指向 **AI 推理帶動企業級 SSD 需求**，並認為 2026 下半年供需偏緊風險仍在。
- 同一篇也把 HDD（STX/WDC）放在同一個框架觀察，代表市場正在用「NAND 與 HDD 的相對經濟性」而非單一路線看儲存架構。

這點對你的觀察很關鍵：

- **NAND 廠若供給紀律存在**（減產、控產、產品結構上移），
- HDD 廠就更有機會維持價格與毛利韌性（尤其是雲端近線容量層）。
- 但若 enterprise SSD 供給突然放大、或 NAND 價格轉向，這個聯動就會反轉。

## 三、哪些公司是這個「NAND × HDD 聯動」的關鍵觀察標的？

### A. NAND 供給端（價格紀律的源頭）

- Samsung
- SK hynix / Solidigm
- Micron
- Kioxia
- SanDisk / WD NAND 體系
- YMTC

你要看的不是單季漲跌，而是：

1. 減產是否鬆動？
2. Enterprise SSD vs Consumer SSD 比重是否持續拉高？
3. ASP 上漲是否來自真需求、還是短期補庫存？

### B. HDD 受益端（你說的訂價權）

- **Seagate (STX)**
- **Western Digital（HDD 業務）**
- **Toshiba（HDD 業務）**

重點指標：

1. nearline exabyte 出貨
2. 單位容量價格（$/TB）
3. 企業/雲端客戶合約談價節奏
4. HAMR 導入速度與成本下降曲線（對 Seagate 特別重要）

## 四、我對這個投資命題的「支持」與「反證」

### 【支持命題】

- AI 推理 + 資料治理讓「可負擔大容量儲存」需求變長期化。
- NAND 若維持供給紀律，HDD 作為容量層的替代彈性會上升。
- 大型資料中心分層架構短期內難以被單一媒介完全取代。

### 【反證風險】

- NAND 廠若重新激進擴產，價格回落，HDD 議價能力會被稀釋。
- 企業若加速把工作負載往高性能 SSD 收斂，HDD 成長斜率可能不如預期。
- 雲端 capex 節奏轉弱時，HDD/NAND 都可能同時承壓，不是單向受惠。

## 五、可直接追蹤的 6 個月觀察清單

1. NAND 合約價（月/季）方向是否持續上行。  
2. Seagate / WD 近線出貨（Exabyte）是否維持高成長。  
3. HDD 單位價格（$/TB）是否續升、且毛利率同步改善。  
4. 雲端客戶 capex 指引（AWS/Azure/GCP）是否維持擴張。  
5. Enterprise SSD 出貨是否出現「超預期擴張」而擠壓 HDD。  
6. 記憶體廠 capex 與減產紀律是否鬆動。  

---

## 參考來源（含你指定）

1. Futu 轉載華爾街見聞：Seagate CEO 談 NAND 價格與 HDD TCO/需求
   - https://news.futunn.com/post/73721938/seagate-ceo-the-higher-nand-prices-go-the-more-competitive?level=1&data_ticket=1771992646421971
2. 財報狗產業報告 #44（NAND Flash 產業追蹤：AI 推理需求帶動企業級 SSD，並納入 HDD/STX/WDC 觀察）
   - https://statementdog.com/industry_reports/44
3. 財報狗 Podcast S2E400（美光季報：DRAM 與 NAND 週期節奏）
   - https://statementdog.com/blog/archives/14656
4. Micron FY25 Q2 新聞稿（公司對 DRAM/NAND 需求展望）
   - https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-second-quarter-fiscal-2025
5. TrendForce：NAND Flash Revenue Ranking（供給集中度與產業追蹤入口）
   - https://www.trendforce.com/search?query=Revenue%20Ranking%20among%20NAND%20Flash%20Suppliers

---

如果你要，我下一版可以直接升級成「可發佈版」：
- 加一段 **NAND 6 大廠 vs HDD 3 強** 的「情境矩陣（牛/基準/熊）」
- 每家公司加上 **最關鍵 2 個財報指標**
- 轉成你 stockhomes 可直接貼上的 front matter 格式（繁中、描述、底部 tags）。
