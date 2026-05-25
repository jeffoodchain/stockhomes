---
title: "台股 / 美股光通、矽光子、CPO 供應鏈研究報告"
date: 2026-05-25
category: optical-cpo
tags: ["optical", "CPO", "silicon photonics", "AI datacenter", "supply chain"]
hackmd_url: ""
description: "AI datacenter 光通、矽光子、CPO 供應鏈研究與台股 / 美股觀察清單。"
---

更新日期：2026-05-25  
定位：產業研究與觀察清單，不是買賣建議。重點是判斷「題材是否能轉成營收、毛利率與 EPS」。

---

## 0. 一頁結論

AI 資料中心的瓶頸正在從單顆 GPU 算力，往 **GPU/ASIC 之間、機櫃之間、資料中心之間的高速互連** 移動。當交換器 ASIC 頻寬升高、機櫃密度增加，傳統銅纜在距離、功耗、散熱、訊號完整性上逐步吃緊，光通訊就從「電信骨幹 / 雲端網路零件」變成 AI infrastructure 的核心升級項目。

目前投資主線可分三層：

1. **800G / 1.6T 光模組放量**：比較接近現在可驗證的營收主線。看 optical transceiver、雷射、DSP/TIA/CDR、mSAP PCB、交換器。
2. **矽光子 / CPO**：比較偏 2026～2027 驗證、2027 以後逐步放量。看外部雷射源、SiPh foundry、光引擎、FAU / microlens、先進封裝。
3. **周邊外溢**：高速板、連接器、光纖、測試設備、封裝設備。營收可受惠，但不一定是純光通股。

**台股較強的是：模組 / 光元件、InP 磊晶、FAU、封裝、交換器 ODM、PCB。**  
**美股較強的是：雷射 / 光源、DSP / SerDes / switching ASIC、網通系統、測試設備、材料與光纖。**

FOMO 檢查：光通 / CPO 很容易先漲估值，再等財報。沒有月營收、產品占比、毛利率或客戶認證證據的公司，應該只放研究清單，不當成已經兌現的受惠股。

---

## 1. 光通題材到底在哪裡用到？

### 1.1 AI 資料中心內部：GPU cluster / AI fabric

AI 訓練與推論需要大量 GPU / ASIC 並行。當節點數增加，資料搬移、同步、checkpoint、參數交換、推論流量都會推高網路需求。

使用位置：

- **GPU / ASIC server 到 top-of-rack switch**
- **機櫃內 switch 到 switch**
- **spine / leaf / super-spine switch 之間**
- **資料中心內部 cluster fabric**

這裡目前主流是 400G / 800G，下一階段往 1.6T、再往 3.2T。高速光模組、光纖、DSP / retimer、switch ASIC、mSAP PCB 都會受惠。

### 1.2 資料中心之間：DCI / coherent optics

雲端業者在不同資料中心之間搬移 AI 資料、備援與模型服務，會用到 DCI（Data Center Interconnect）。距離較長時，需要 coherent optics / DCO。

受惠公司類型：

- Coherent optical module
- DCO / pluggable coherent
- 網通設備商
- 光纖 / 連接器
- 測試設備

### 1.3 CPO / co-packaged optics：把光更靠近 switch ASIC

CPO 的邏輯是：當 switch ASIC 速度繼續上升，電訊號從 ASIC 拉到前面板 pluggable module 的距離造成更高功耗與訊號損失，所以把光引擎放到 ASIC 封裝附近，縮短電連接距離。

關鍵零組件：

- Switch ASIC
- SiPh photonic engine
- External laser source / CW DFB laser
- Fiber array unit, FAU
- Micro-lens / optical coupling
- Optical interposer
- Advanced packaging / hybrid bonding
- Test & burn-in

CPO 的投資重點不是「誰名字沾到矽光子」，而是：誰在光源、耦光、封裝、測試、量產良率上真的有 bottleneck value。

---

## 2. 高階產品有哪些？

### 2.1 高速光模組

- **400G**：現有雲端資料中心主力之一。
- **800G**：AI cluster 升級主線，2026 年多數研究與新聞都指向 800G 占比快速提高。
- **1.6T**：下一代高階產品，2026 起開始出貨 / 驗證，2027 後放量機率較高。
- **3.2T**：更遠期，取決於 switch ASIC 與資料中心架構。

常見型態：

- OSFP / QSFP-DD
- DR / FR / LR / ZR / ZR+
- SR for short reach
- DCI coherent pluggables

### 2.2 光源 / 雷射

- CW DFB laser
- EML / DML
- InP laser
- External laser source for CPO / SiPh

高階化原因：更高速、更低功耗、更穩定溫控、更高可靠度，且 CPO 架構可能把外部雷射源變成關鍵零組件。

### 2.3 DSP / SerDes / TIA / CDR / Linear optics

- DSP：高速訊號處理，但功耗與成本高。
- LPO / Linear pluggable optics：用更少 DSP，降低功耗，但系統設計與相容性要求高。
- TIA / CDR / Driver：光電轉換鏈中的關鍵 IC。
- SerDes / switch ASIC：決定網路速度升級節奏。

### 2.4 SiPh / CPO 光引擎與封裝

- Silicon photonics waveguide / modulator
- Photonic integrated circuit, PIC
- Optical interposer
- Hybrid bonding / advanced packaging
- FAU / micro-lens / coupling
- Co-packaged optical engine

### 2.5 PCB / substrate / mSAP

高速光模組與交換器需要更高頻寬、更低損耗、更細線寬線距。mSAP / 高階 PCB 變成光模組升級的外溢受惠項目。

---

## 3. 產業鏈分層：從最核心到周邊

| 層級 | 零組件 / 環節 | 需求驅動 | 美股 / 國際代表 | 台股代表 |
|---|---|---|---|---|
| 光源 | CW DFB、InP laser、EML | 800G/1.6T、CPO 外部雷射源 | Lumentum, Coherent, MACOM, Broadcom, AAOI | 聯亞、IET-KY、全新、環宇-KY |
| SiPh foundry | Silicon photonics PIC | CPO / 光引擎整合 | Intel, GlobalFoundries, Tower, TSM ADR | 台積電、聯電，純度較低 |
| 光模組 | 800G、1.6T、ZR/ZR+ | AI cluster / DCI | Coherent, Lumentum, Cisco/Acacia, Ciena, Nokia, Fabrinet | 華星光、光聖、眾達-KY、前鼎、聯鈞、光環 |
| DSP / analog IC | DSP, TIA, driver, CDR | 高速訊號處理 | Broadcom, Marvell, MACOM, Semtech, MaxLinear | 台股直接純度較低 |
| CPO 耦光 | FAU、micro-lens、光纖陣列 | 光引擎封裝良率 | Himax ADR, POET 等 | 上詮 |
| 網通系統 | AI switch、router、DCO 系統 | AI fabric 擴張 | Arista, Cisco, Ciena, Nokia | 智邦 |
| 光纖 / 連接器 | Fiber, connector, cable | Rack / DCI 線路增加 | Corning, Amphenol, TE Connectivity | 貿聯-KY、波若威等 |
| 測試設備 | Optical / RF / semiconductor test | 高速良率與認證 | Keysight, Viavi, FormFactor, Aehr | 台股較少純標的 |
| PCB / mSAP | 光模組板、交換器板 | 高速線路升級 | 國際 PCB / substrate 廠 | 華通、欣興、臻鼎-KY |

---

## 4. 美股廠商在做什麼？

### 4.1 NVIDIA / Broadcom / Marvell：需求與 ASIC / networking 核心

- **NVIDIA**：AI GPU、NVLink / Spectrum-X / InfiniBand 生態，是 AI networking 需求的重要推動者。NVIDIA 不是傳統光模組廠，但其 cluster 架構決定高速互連需求。市場關注 NVIDIA 對 Lumentum / Coherent 等先進光學供應商的投資與採購承諾。
- **Broadcom**：switch ASIC、DSP、SerDes、光通訊 IC 與部分光學元件，屬於 AI networking 核心供應商。
- **Marvell**：DSP、SerDes、DPU / custom silicon / interconnect IC，受惠 AI data center 高速互連升級。

### 4.2 Lumentum / Coherent / MACOM / AAOI：雷射與光模組

- **Lumentum**：雷射、光通訊元件，市場焦點在先進光源與 AI optics。
- **Coherent**：材料、雷射、光通訊模組、coherent optics，從上游材料到模組都有布局。
- **MACOM**：高頻 / analog / photonic IC，含 driver、TIA、laser 相關。
- **AAOI**：資料中心光模組與雷射相關，彈性高但競爭也高。

### 4.3 Cisco / Ciena / Nokia：系統與 coherent optics

- **Cisco**：網路設備，Acacia 強化 coherent optics / silicon photonics。
- **Ciena**：光網路與 DCI / coherent 系統核心廠。
- **Nokia**：電信與光網路設備。

### 4.4 Corning / Amphenol / TE：光纖與連接

- **Corning**：光纖、玻璃材料。
- **Amphenol / TE Connectivity**：高速連接器與纜線。

### 4.5 Keysight / Viavi / FormFactor / Aehr / Onto / Camtek：測試與良率

800G / 1.6T / CPO 的測試難度提高，包含 optical test、RF test、wafer probe、burn-in、metrology。若 CPO 量產，測試時間與良率管理會是重要成本項目。

---

## 5. 台股廠商在做什麼？

以下股價與成交量為 FinMind/TWSE 可得資料，日期 2026-05-25；月營收為 2026/05，單位約新台幣百萬元。

### 5.1 核心光源 / InP / 磊晶

| 代號 | 公司 | 角色 | 2026/05 營收 | YoY | MoM | 2026-05-25 收盤 / 量 |
|---|---|---|---:|---:|---:|---|
| 3081 | 聯亞 | InP / 光通磊晶、雷射上游 | 395.3 | +115.4% | +15.2% | 2925 / 2647 張 |
| 4971 | IET-KY | InP / GaAs 磊晶 | 106.3 | +25.2% | -2.9% | 745 / 332 張 |
| 2455 | 全新 | 化合物半導體磊晶，RF + 光電 | 318.6 | +37.7% | +2.4% | 444 / 21814 張 |
| 4991 | 環宇-KY | 化合物半導體 / 光電相關 | 243.9 | +67.9% | -27.8% | 840 / 6425 張 |

判讀：聯亞的營收動能最明顯，但股價也已高度反映。環宇-KY 單月 YoY 強、MoM 弱，要看 3～6 個月趨勢。

### 5.2 光模組 / 光元件

| 代號 | 公司 | 角色 | 2026/05 營收 | YoY | MoM | 2026-05-25 收盤 / 量 |
|---|---|---|---:|---:|---:|---|
| 4979 | 華星光 | 800G / ZR / 光收發模組 | 412.8 | +7.7% | -8.6% | 655 / 1358 張 |
| 6442 | 光聖 | 光通訊元件 / 模組 / 連接 | 886.4 | -16.2% | -12.5% | 2805 / 1600 張 |
| 4977 | 眾達-KY | 光收發模組 | 58.0 | -43.2% | -33.5% | 230.5 / 6235 張 |
| 3163 | 波若威 | 光纖 / 光通模組 / 連接 | 199.1 | +16.5% | -19.5% | 1210 / 7441 張 |
| 4908 | 前鼎 | 光收發模組 | 74.0 | +5.0% | -18.4% | 293.5 / 1211 張 |
| 3450 | 聯鈞 | 光通元件 / 模組 | 877.8 | +45.5% | +20.6% | 501 / 4926 張 |
| 3234 | 光環 | 光主動元件 | 62.5 | +12.2% | -2.7% | 107 / 3158 張 |
| 6530 | 創威 | 小型光通訊股 | 31.5 | +18.1% | -2.3% | 114 / 1606 張 |

判讀：聯鈞與部分上游營收較有跟上；華星光 / 光聖 / 波若威股價題材強，但單月營收要避免只看故事。

### 5.3 CPO / SiPh 封裝與耦光

| 代號 | 公司 | 角色 | 2026/05 營收 | YoY | MoM | 2026-05-25 收盤 / 量 |
|---|---|---|---:|---:|---:|---|
| 3363 | 上詮 | FAU / fiber array / CPO 耦光 | 127.9 | -37.3% | +9.1% | 846 / 4131 張 |
| 6451 | 訊芯-KY | 先進封裝 / SiP / 光電封裝相鄰 | 641.1 | -2.8% | +11.8% | 576 / 3614 張 |
| 2330 | 台積電 | SiPh / 先進封裝潛在平台，低純度 | 410725.1 | +17.5% | -1.1% | 2310 / 28251 張 |
| 2303 | 聯電 | SiPh foundry 地圖中出現，但純度低 | 22663.9 | +10.8% | +8.8% | 125 / 340936 張 |

判讀：上詮是 CPO 耦光題材純度高，但 2026/05 營收 YoY 仍弱，代表市場先交易未來 CPO 可能性；需要等量產客戶與營收證據。

### 5.4 網通交換器 / PCB / 外溢受惠

| 代號 | 公司 | 角色 | 2026/05 營收 | YoY | MoM | 2026-05-25 收盤 / 量 |
|---|---|---|---:|---:|---:|---|
| 2345 | 智邦 | AI switch / 白牌交換器 | 27360.3 | +53.9% | +9.4% | 2540 / 2634 張 |
| 3665 | 貿聯-KY | 高速線束 / interconnect | 7383.0 | +18.5% | +5.3% | 2385 / 2036 張 |
| 2313 | 華通 | mSAP / 高階 PCB 外溢 | 6315.3 | -2.9% | -9.0% | 298.5 / 100470 張 |
| 3037 | 欣興 | ABF / PCB / 高階板 | 13932.8 | +27.6% | +6.5% | 990 / 23595 張 |
| 4958 | 臻鼎-KY | PCB / mSAP 外溢 | 15196.3 | +11.8% | -1.6% | 529 / 47337 張 |

判讀：智邦是台股 AI networking 營收證據最清楚的一類，但不是純光通；PCB 廠要看 mSAP 與高階光模組板是否真正提升毛利率。

---

## 6. 美股 vs 台股：定位差異

### 6.1 美國 / 國際廠商優勢

1. **定義規格與平台**：NVIDIA、Broadcom、Marvell、Cisco、Arista、Ciena。
2. **高速 IC / switch ASIC / DSP**：Broadcom、Marvell、MACOM、Semtech、MaxLinear。
3. **雷射與光源技術**：Lumentum、Coherent、MACOM、AAOI。
4. **coherent optics / DCI 系統**：Ciena、Cisco/Acacia、Nokia、Coherent。
5. **測試設備**：Keysight、Viavi、FormFactor、Aehr、Onto、Camtek。

### 6.2 台灣廠商優勢

1. **上游化合物半導體磊晶**：聯亞、IET-KY、全新、環宇-KY。
2. **光模組 / 光元件製造**：華星光、光聖、聯鈞、眾達-KY、前鼎、光環。
3. **FAU / 耦光零件**：上詮。
4. **封裝與系統組裝**：訊芯-KY、台積電先進封裝平台、相關 EMS / OSAT。
5. **白牌交換器與 PCB**：智邦、華通、欣興、臻鼎-KY。

### 6.3 投資含義

美股多數是「規格制定者 / 核心 IC / 光源 / 系統設備」，估值通常反映全球 AI capex。台股多數是「製造與關鍵零件供應」，彈性高，但要看客戶認證、量產良率、月營收與毛利率是否跟上。

---

## 7. 產業分析：為什麼這波跟過去光通循環不一樣？

### 7.1 需求端：AI cluster 讓 bandwidth 成為剛性需求

過去光通景氣常由電信 capex 或雲端一般流量帶動，週期性較明顯。這波新增 AI training / inference cluster，頻寬與低延遲需求更集中，而且和 GPU / ASIC 部署綁在一起。

### 7.2 產品端：從 400G 升 800G / 1.6T，ASP 與技術門檻提高

產品升級帶來：

- 更高 ASP
- 更高測試與良率要求
- 更高功耗壓力
- 更多高階 IC 與光源需求
- 對 PCB / substrate / connector 的規格升級

但也要注意：光模組一旦標準化，價格競爭會很快出現，尤其中國模組廠競爭力很強。

### 7.3 架構端：CPO 可能改變供應鏈價值分配

若 CPO 量產，價值可能從傳統 pluggable module 的前面板模組，部分轉向：

- SiPh photonic engine
- external laser source
- optical coupling / FAU
- advanced packaging
- optical test
- switch ASIC platform

這對台股的意義是：上詮、聯亞、訊芯-KY、台積電等會被市場重新定位，但每家公司受惠程度差異很大。

---

## 8. 觀察指標與反轉訊號

### 正向指標

- 800G / 1.6T 營收占比提升
- AI / data center 客戶占比提升
- 月營收連續 3 個月以上 YoY / MoM 走強
- 毛利率提升，而不是只有營收增加
- 客戶認證 / 新平台量產
- 產能利用率提升、交期拉長
- 法說明確給出高階產品放量時程

### 反轉訊號

- 月營收跟不上股價
- 毛利率沒有因高階產品改善
- 光模組 ASP 快速下滑
- 中國競爭者降價
- 客戶 pull-in 後修正庫存
- CPO 量產時程延後
- 新產能開出造成供給過剩
- 題材股處置、融資過高、爆量長黑

---

## 9. 目前研究清單分級

### A 級：營收與產業位置較值得優先追蹤

- 智邦：AI networking / switch，營收證據強，但非純光通。
- 聯亞：InP / 雷射上游，營收動能強，估值敏感。
- 聯鈞：光通元件 / 模組，2026/05 營收動能佳。
- 全新 / IET-KY / 環宇-KY：化合物半導體上游，需拆分 RF 與光通貢獻。
- 華星光：光模組純度高，但營收需持續驗證。

### B 級：題材純度高，但要等量產證據

- 上詮：FAU / CPO 耦光純度高，但 2026/05 YoY 仍弱。
- 訊芯-KY：SiP / 封裝相鄰，需確認 SiPh / CPO 實際營收。
- 波若威：資料中心布線 / 光通相鄰，股價彈性高但月營收波動。

### C 級：外溢或低純度

- 台積電 / 聯電：SiPh foundry 可能性，但公司整體太大，光通 EPS 純度低。
- 華通 / 欣興 / 臻鼎-KY：mSAP / PCB 外溢受惠，要看高階產品占比與毛利率。
- 貿聯-KY：高速 interconnect 相鄰，不是純光通。

---

## 10. 來源與追蹤清單

### 已使用資料

- FinMind / TWSE：台股 2026-05-25 收盤、成交量、2026/05 月營收。
- Google News RSS：2026 年 3～5 月光通、800G、1.6T、CPO、矽光子新聞快篩。
- TrendForce / I-Connect007 相關新聞：Google 高速互連架構推升 800G+ optical transceiver 占比。
- MoneyDJ / 鉅亨 / 經濟日報 / Yahoo 股市 / 豐雲學堂等台灣新聞：華星光、光聖、上詮、聯亞、PCB mSAP 與 CPO 題材。
- NVIDIA / Lumentum / Coherent 相關新聞與公司發布：NVIDIA 對先進光學 / photonics 供應鏈的策略合作與投資方向。

### 後續應補資料

1. 各公司 2026 Q1 / Q2 法說：800G、1.6T、AI data center 占比。
2. 毛利率趨勢：高階產品是否真正改善獲利。
3. 客戶別：美系 CSP / NVIDIA / Broadcom / switch ODM 是否有明確連結。
4. 產能：InP、FAU、光模組、mSAP 產能與良率。
5. 中國競爭：中際旭創、新易盛等對全球價格的壓力。

---

## 11. 最後判斷

光通不是單一題材，而是 AI infrastructure 從 compute 走向 networking bottleneck 的結果。短中期最可驗證的是 800G / 1.6T 光模組與 AI switch；中長期想像最大的是 CPO / 矽光子。

投資研究上應該把公司分成三種：

1. **已經有營收證據的受惠者**：比較能用月營收、毛利率、EPS 驗證。
2. **技術位置很好但還沒放量者**：可以追蹤，但不該用已兌現估值看待。
3. **只沾題材的外溢股**：要確認產品占比，避免被主題行情帶著追高。

目前台股若要避免 FOMO，優先看「月營收 + 高階產品占比 + 毛利率」三件事；只講 CPO、矽光子、800G，但沒有財報證據的公司，應先放觀察名單。
