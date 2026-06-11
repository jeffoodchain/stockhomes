---
title: "AI 先進封裝路線解析：CoWoS、CoPoS、CoWoP 與 CPO 的差異、效益與供應鏈影響"
date: 2026-06-11
category: advanced-packaging
tags: ["advanced packaging", "CoWoS", "CoPoS", "CoWoP", "CPO", "TSMC", "NVIDIA", "AI server"]
hackmd_url: ""
description: "從產業分析與業內視角拆解 CoWoS、CoPoS、CoWoP 與共同封裝光學 CPO：技術結構、效益、瓶頸、量產時程與供應鏈受益層。"
keywords: ["CoWoS", "CoPoS", "CoWoP", "共同封裝光學", "Co-Packaged Optics", "玻璃核心基板", "TGV", "ABF", "AI 伺服器", "先進封裝"]
---

> 版本：2026-06-11  
> 定位：產業研究與供應鏈分析，不是買賣建議。X 貼文視為 market intelligence / 供應鏈線索；公開公司、媒體與技術資料為主要引用依據。  
> 核心問題：AI 晶片封裝正在從「GPU + HBM 能不能接起來」進化成「能不能用更低成本、更高良率、更低功耗，把更大的 compute / memory / I/O / optics 系統整合起來」。

---

## 一張圖理解三種先進封裝路線

![先進封裝路線對照：CoWoS、CoPoS、CoWoP](../../assets/reports/advanced-packaging/advanced_packaging_comparison_cn_v2.png)

[[toc]]

---

## 0. Executive summary

AI 半導體競爭已經從「單顆晶片製程節點」進入「封裝、記憶體、光學、散熱、測試與系統整合」共同決定效能與成本的階段。CoWoS、CoPoS、CoWoP、共同封裝光學（Co-Packaged Optics, CPO）不是單純世代替代關係，而是分別解決不同瓶頸：

1. **CoWoS（Chip-on-Wafer-on-Substrate，晶片-晶圓-基板）**：現行 AI GPU / ASIC + HBM 的主力量產封裝。優點是成熟、可驗證；瓶頸是 CoWoS 產能、ABF 載板、矽中介層面積與成本。
2. **CoPoS（Chip-on-Panel-on-Substrate，晶片-面板-基板）**：把封裝從圓形晶圓推向方形面板，並結合 ABF / 玻璃核心 / ABF 的玻璃核心基板。目標是改善超大型封裝面積經濟性，市場訊號多指向 2028–2029 量產爬坡。
3. **CoWoP（Chip-on-Wafer-on-PCB，晶片-晶圓-PCB）**：嘗試移除傳統 ABF 封裝載板，讓高精度類載板 PCB（Substrate-Like PCB, SLP）承擔更多封裝功能。理論上成本與訊號路徑更好，但對 PCB 製程、翹曲、可靠性與檢測要求極高。
4. **CPO（Co-Packaged Optics，共同封裝光學）**：不是 GPU package substrate 的同義詞，而是 AI data center networking 的光互連封裝。核心是把光學引擎（Optical Engine）靠近交換器 ASIC（Switch ASIC），降低高速電訊號路徑造成的功耗與損耗。

我的產業判斷：**CoWoS 是現在式，CoPoS 是 TSMC 面向 ultra-large AI package 的中長期戰略，CoWoP 是高風險高潛力的系統級封裝實驗，CPO 則是 AI factory 網路層的封裝革命。真正的投資重點不在題材名稱，而在誰掌握下一個 bottleneck layer。**

---

## 1. 為什麼先進封裝突然變成主戰場？

AI accelerator 的效能已經不只取決於 logic die 本身，而是取決於整個 package 與 system 能否把幾個關鍵資源拉在一起：

- **運算（Compute）**：GPU / ASIC / chiplet。
- **記憶體（Memory）**：HBM 堆疊數、頻寬、容量。
- **I/O 與互連（I/O & Interconnect）**：die-to-die、GPU-to-GPU、rack-to-rack。
- **供電與散熱（Power & Thermal）**：封裝內 power integrity、機櫃液冷與熱路徑。
- **良率與成本（Yield & Cost）**：package 面積越大，任何小缺陷都會被放大成成本問題。

所以封裝的角色從「後段組裝」變成「系統架構的一部分」。對 NVIDIA / AMD / hyperscaler 來說，下一代平台不是只問單顆 GPU 多快，而是問：**能不能在可量產、可維修、可承受成本的前提下，把更多 HBM、更多 compute tile、更多 I/O 甚至 optics 塞進系統。**

---

## 2. CoWoS：AI GPU 現行主流，但大尺寸經濟性開始吃緊

### 2.1 技術結構

CoWoS 是 **Chip-on-Wafer-on-Substrate（晶片-晶圓-基板）**。典型結構為：

> GPU / ASIC + HBM → 矽中介層（Silicon Interposer）或 RDL / local interconnect → ABF 封裝載板（ABF Package Substrate）→ PCB

CoWoS 的價值在於讓 GPU / ASIC 與 HBM 以極短距離、高密度線路互連。對 AI training / inference 而言，HBM 頻寬往往是 compute 能否被充分餵飽的前提。

### 2.2 主要效益

- **高頻寬、低延遲**：HBM 與 GPU / ASIC 放在同一封裝內，以高密度 interposer 連接。
- **成熟度最高**：供應鏈、量產經驗、可靠性驗證最完整。
- **客戶驗證明確**：Basler 的 CoWoP 技術文章指出，CoWoS 已支撐 NVIDIA H100 / H200 等 AI accelerator 類產品量產應用。[^basler-cowop]

### 2.3 主要瓶頸

- **矽中介層面積越大，成本越高**。
- **ABF 載板供給與大尺寸良率是瓶頸**。
- **package size 放大後翹曲（Warpage）與熱機械可靠性更難控**。
- **CoWoS 產能本身是 AI GPU 交付的關鍵限制之一**。

因此，CoPoS / CoWoP 的討論不是因為 CoWoS 失效，而是因為 AI package 正在變得太大、太貴、太難做。

---

## 3. CoPoS：面板級封裝 + 玻璃核心基板，解 ultra-large package 經濟性

### 3.1 正確定義

CoPoS 是 **Chip-on-Panel-on-Substrate（晶片-面板-基板）**。它的重點不是簡單把材料換成玻璃，而是：

- 封裝製程從圓形晶圓邏輯走向方形 / 面板級（Panel-Level）邏輯。
- 使用玻璃核心基板（Glass Core Substrate）支撐大尺寸 package 的尺寸穩定性。
- 典型概念是 **ABF / Glass / ABF**，也就是玻璃不是直接承載 chip 的「玻璃中介層」，而是基板核心。

郭明錤在 X 上提到，CoPoS 目前預期 2H28 量產，目標是改善 9.5x reticle-size 以上超大型封裝的經濟性；其資訊也提到 310 × 310 mm temporary glass carrier，以及 pilot / mass production glass panel 尺寸線索。[^kuo-copos]

TrendForce 引述 Commercial Times 報導，TSMC CoPoS pilot line 已開始導入設備，市場 broadly expects volume production to ramp between 2028 and 2029；同時也指出 substrate size 放大後，warpage 是量產主要挑戰之一。[^trendforce-copos]

### 3.2 為什麼玻璃核心基板重要？

Intel 在 glass substrate 公開資料中指出，相比 organic substrate，玻璃具備更好的平坦度、熱機械穩定性、尺寸穩定性，並可能帶來更高 interconnect density，適合 data center、AI、graphics 等大型高效能封裝。[^intel-glass]

但要特別強調三個常見誤解：

1. **玻璃不是 glass interposer**：CoPoS 的互連仍由 chip-side RDL、TGV / Cu interconnect 與 ABF build-up layers 共同完成。
2. **玻璃沒有取代 ABF**：ABF 仍存在於 glass core 上下兩側，是細線路與 chip attach 的關鍵層。
3. **晶片不是直接坐在玻璃上**：晶片接在 ABF build-up surface 上。

### 3.3 主要效益

- **面積效率更好**：方形 panel 對大型矩形 package 排版更有利。
- **成本曲線可能更平緩**：silicon interposer 面積放大後成本快速上升，panel-level + glass core 的目標是讓 ultra-large package 更有經濟性。
- **支援更多 HBM / chiplet / I/O**：下一代 AI accelerator 需要更大封裝空間。
- **強化 TSMC system-level lock-in**：當客戶架構同時依賴 leading-edge wafer、SoIC、CoWoS / CoPoS、HBM 整合，TSMC 從 foundry 變成高效能系統平台供應商。

### 3.4 關鍵瓶頸：TGV 與玻璃加工

Arvind Srinivas 的 X 貼文指出，CoPoS glass core substrate 是 ABF / Glass / ABF 三層堆疊，TGV（Through Glass Via，玻璃通孔）是關鍵瓶頸，需要在玻璃中鑽大量微孔並填銅。[^arvind-copos]

LPKF 的 LIDE 技術頁面提到，其玻璃加工可用 ultrafast laser modification + wet etching 形成 defect-free glass structures，並標示 TGV aspect ratio 可達 up to 1:50、sub-micron accuracy、zero micro-cracks / chipping 等能力。[^lpkf-lide]

這表示 CoPoS 的瓶頸會外溢到：玻璃加工、雷射設備、蝕刻、電鍍 / 金屬化、面板級 lithography、AOI / inspection、warpage control、reliability test。

---

## 4. CoWoP：讓高階 PCB / SLP 承擔封裝級任務

### 4.1 技術結構

CoWoP 是 **Chip-on-Wafer-on-PCB（晶片-晶圓-PCB）**。它嘗試移除傳統 ABF substrate，讓 chip + interposer module 直接連接到高精度 SLP / PCB。

Basler 對 CoWoP 的描述是：CoWoP integrates the package substrate and PCB into a single structure，讓模組更薄、頻寬更高、熱性能更好；同時也指出整個 PCB supply chain 必須達到 semiconductor-grade accuracy。[^basler-cowop]

### 4.2 主要效益

- **訊號路徑最短**：移除中間 substrate 後，理論上可降低 parasitic loss、改善 latency 與 power integrity。
- **降低 ABF 依賴**：如果高階 PCB / SLP 能承擔部分封裝功能，可減少 ABF 供應瓶頸。
- **熱路徑與結構更簡化**：有機會讓 heat spreader / cold plate 更有效接近熱源。

Basler 文章提到，移除 ABF / BT substrates 並使用大面積 PCB process，理論上可能降低 packaging cost 40–50%。但這類數字應視為供應鏈觀點 / 推估，尚不等於已驗證量產成本。[^basler-cowop]

### 4.3 主要挑戰

CoWoP 的難點在於：PCB 要做封裝級的事情。

- SLP / PCB 需要 15–20 µm line / space，未來甚至可能要求 <10 µm。
- 多層板的翹曲、CTE mismatch、熱循環可靠性更難控。
- 大面積 PCB 製程要達到封裝級 overlay、AOI 與 defect control。
- 若良率不穩，損失的不只是板材，而是高價 chip module 的承載平台。

所以 CoWoP 是高風險高潛力路線：若成功，高階 PCB 價值鏈會被重估；但它不應被簡化成「PCB 股全部受惠」。

---

## 5. CPO：共同封裝光學，解 AI factory 網路功耗，不是 CoPoS

CPO 是 **Co-Packaged Optics（共同封裝光學）**。它不是 CoPoS / CoWoP 的同義詞，而是 AI data center network 的封裝革命。

NVIDIA 技術文章指出，傳統 pluggable transceiver 架構下，資料訊號要從 switch ASIC 走過 PCB、connector、外部 transceiver 才轉成光訊號，200 Gbps channel 的 electrical loss 可高達 22 dB；CPO 把 electro-optical conversion 放到 switch package 旁，可把 electrical loss 降到約 4 dB，並將每 interface 功耗從常見 30W 降到 as low as 9W。NVIDIA 稱其 CPO-based systems 可帶來 up to 3.5x power efficiency 與 10x resiliency improvement，Quantum-X / Spectrum-X Photonics 商用時間指向 2026。[^nvidia-cpo]

CPO 供應鏈應分層看：

1. **造光層**：InP substrate、epitaxy、高功率 laser / external laser source。
2. **載資料層**：SOI wafer、silicon photonics、photonic integrated circuit（PIC）、optical engine、modulator。
3. **連接 / 組裝 / 測試層**：advanced packaging、fiber array unit（FAU）、connector、optical test、system assembly。

CPO 的投資重點不是「誰名字沾到 CPO」，而是誰在 laser reliability、optical engine yield、fiber attach / alignment、optical test throughput 這些瓶頸層有不可替代性。

---

## 6. 供應鏈影響：錢會流向瓶頸層，不會平均流向題材層

### 6.1 CoWoS 受益層

- TSMC advanced packaging capacity。
- ABF substrate。
- HBM。
- OSAT / test。
- 散熱與模組組裝。

這是市場最熟悉、也最容易擁擠的主線。判斷重點是：CoWoS capacity、ABF substrate lead time、HBM allocation、客戶 GPU ramp。

### 6.2 CoPoS 受益層

- glass core substrate。
- ABF build-up material。
- TGV drilling / LIDE / laser processing。
- Cu filling / metallization。
- panel-level lithography / plating / inspection。
- warpage control equipment。

重點不是「玻璃概念」四個字，而是能否進入 TSMC / NVIDIA 類客戶的 qualification flow。

### 6.3 CoWoP 受益層

- 高階 PCB / SLP。
- mSAP / SAP 製程。
- ultra-thin copper foil。
- semiconductor-grade AOI。
- warpage / reliability test。
- thermal-mechanical simulation。

普通 PCB 產能不是重點，重點是 substrate-like precision 與封裝級可靠性。

### 6.4 CPO 受益層

- InP / laser source。
- silicon photonics / PIC foundry。
- optical engine。
- fiber attach / FAU / connector。
- optical testing。
- switch system integration。

CPO 供應鏈最容易被市場用「光通概念」一筆帶過，但實際 alpha 會集中在 bottleneck layer。

---

## 7. 產業判斷與追蹤指標

### 7.1 基本判斷

- **CoWoS**：現在式；不應過早喊被取代。
- **CoPoS**：中長期；若 2028–2029 量產節奏確認，玻璃核心基板與 TGV 設備鏈會更重要。
- **CoWoP**：高風險高潛力；對高階 PCB / SLP 是升級機會，也是淘汰賽。
- **CPO**：網路層封裝革命；與 AI GPU package 本體不同，但會決定 AI factory scale-out 的功耗與頻寬上限。

### 7.2 需要追蹤的 leading indicators

1. TSMC 對 CoPoS / panel-level packaging 的 capex、廠區、設備進度。
2. NVIDIA / AMD 下一代 AI accelerator package size、HBM stack 數、CoWoS / CoPoS / CoWoP 採用訊號。
3. 玻璃核心基板 TGV 良率、Cu filling、warpage control 是否通過客戶驗證。
4. 高階 SLP / PCB 線寬線距、良率與可靠性是否接近封裝級要求。
5. NVIDIA / Broadcom / hyperscaler CPO switch 出貨節奏、optical engine 良率與維修模式。
6. 供應鏈財報是否出現可驗證的營收占比、ASP、毛利率改善，而不是只有題材敘事。

---

## 8. 結論

先進封裝的下一階段，不是單一技術把另一個技術淘汰，而是不同封裝路線在不同系統瓶頸上分工：

- **CoWoS** 解決今天 AI GPU + HBM 的量產需求。
- **CoPoS** 解決下一代 ultra-large package 的面積與成本問題。
- **CoWoP** 挑戰 substrate / PCB 的邊界，若成功將重估高階 PCB 價值鏈。
- **CPO** 把封裝競爭延伸到 AI data center networking，降低 switch 端功耗並提高頻寬密度。

真正的研究重點應該是：**哪一個環節變成新瓶頸、誰有量產資格、誰能把技術優勢轉成營收與毛利率。** 只看題材名稱，很容易買到的是敘事；找到 bottleneck layer，才比較可能找到產業 alpha。

---

## Sources

[^kuo-copos]: 郭明錤｜Ming-Chi Kuo, “Key takeaways on TSMC's next-generation advanced packaging, CoPoS,” X, 2026-06-11. https://x.com/mingchikuo/status/2064896082203849094?s=20

[^arvind-copos]: Arvind Srinivas, “CoPoS's glass core substrate is a 3-layer stack: ABF / glass / ABF… TGV is the Bottleneck…,” X, 2026-06-11. https://x.com/arv9293/status/2064955872250388728?s=20

[^trendforce-copos]: TrendForce, “[News] TSMC Advances Panel-Level Packaging, CoPoS Pilot Line Reportedly Set for June Completion, 2028–29 Ramp Eyed,” 2026-04-13. https://www.trendforce.com/news/2026/04/13/news-tsmc-advances-panel-level-packaging-copos-pilot-line-reportedly-set-for-june-completion-2028-29-ramp-eyed/

[^intel-glass]: Intel, “Intel Unveils Industry-Leading Glass Substrates to Meet Demand for More Powerful Compute,” 2023. https://www.intc.com/news-events/press-releases/detail/1647/intel-unveils-industry-leading-glass-substrates-to-meet

[^lpkf-lide]: LPKF, “LIDE® Technology: Industry Standard for Advanced Glass Processing.” https://lide.lpkf.com/en/technology/lide

[^basler-cowop]: Basler, “CoWoP Is Coming, and Semiconductor Inspection Is Ready All Along.” https://www.baslerweb.com/en/learning/semicon-chip-on-wafer-on-pcb/

[^nvidia-cpo]: NVIDIA Technical Blog, “Scaling AI Factories with Co-Packaged Optics for Better Power Efficiency,” 2026. https://developer.nvidia.com/blog/scaling-ai-factories-with-co-packaged-optics-for-better-power-efficiency/
