---
title: "AI 先進封裝的真正分歧：CoWoS、CoPoS、CoWoP 與 CPO"
date: 2026-06-11
category: advanced-packaging
tags: ["advanced packaging", "CoWoS", "CoPoS", "CoWoP", "CPO", "TSMC", "NVIDIA", "AI server"]
hackmd_url: ""
description: "從 AI 系統瓶頸出發，說明 CoWoS、CoPoS、CoWoP 與共同封裝光學 CPO 各自代表的產業分歧：算力與記憶體、晶圓與面板、載板與 PCB、電訊號與光訊號。"
keywords: ["CoWoS", "CoPoS", "CoWoP", "共同封裝光學", "Co-Packaged Optics", "玻璃核心基板", "TGV", "ABF", "AI 伺服器", "先進封裝"]
---

> 版本：2026-06-11  
> 定位：產業研究與供應鏈分析，不是買賣建議。X 貼文視為 market intelligence / 供應鏈線索；公開公司、媒體與技術資料為主要引用依據。

![先進封裝路線對照：CoWoS、CoPoS、CoWoP](../../assets/reports/advanced-packaging/advanced_packaging_comparison_cn_v2.png)

先進封裝這件事，如果只用名詞去看，很容易變成 CoWoS、CoPoS、CoWoP、CPO 的縮寫背誦。但它真正反映的，不是封裝技術突然變得花俏，而是 AI 系統已經大到傳統半導體分工開始失效。

過去的主線很單純：製程越先進，晶片越強，算力越高。但 AI accelerator 走到 HBM、chiplet、rack-scale networking 之後，問題不再只是「單顆 die 夠不夠快」，而是資料能不能被搬到運算單元旁邊、記憶體能不能塞進封裝裡、封裝面積能不能繼續放大、網路功耗會不會吃掉整座 AI factory 的效率。換句話說，封裝從後段製程變成系統架構本身；它決定的不只是晶片能不能做出來，而是整個 AI 基礎設施能不能擴張。

**1. 算力敘事的失效（系統分歧）：** CoWoS 的出現，代表 AI 晶片競爭已經不能只看 GPU die 本身。GPU / ASIC 再強，如果 HBM 頻寬不夠、資料離運算單元太遠，算力就只是理論值。CoWoS（Chip-on-Wafer-on-Substrate，晶片-晶圓-基板）真正解決的是「GPU 與 HBM 如何在同一個封裝內高速溝通」：把 GPU / ASIC 與 HBM 放在矽中介層（Silicon Interposer）或高密度互連結構上，再接到 ABF 封裝載板與 PCB。這讓資料路徑變短、頻寬提高、延遲降低，也讓 NVIDIA H100 / H200 這類 AI accelerator 得以量產；Basler 對 CoWoP 的技術說明也把 CoWoS 視為已成熟並支撐現行 AI accelerator 的主流先進封裝。[^basler-cowop] 因此，CoWoS 不是一個普通封裝名詞，而是 AI 算力從「單晶片性能」轉向「記憶體與運算共封裝」後的第一個答案。

但這個答案本身也製造了新的瓶頸。當 HBM 堆疊數增加、GPU / ASIC 面積擴大、package 變得越來越大，CoWoS 開始面臨矽中介層成本、ABF 載板供給、封裝翹曲與產能限制。也就是說，CoWoS 不是因為落後才被討論替代，而是因為它太成功，成功到所有下一代 AI GPU 都擠在這條產線上，逼迫產業去尋找更大尺寸、更好面積經濟性的封裝方式。

**2. 晶圓經濟性的失效（製造分歧）：** CoPoS 的核心不是「玻璃題材」，而是傳統晶圓式封裝在超大型 AI package 面前開始不夠經濟。當一個 package 要容納更多 HBM、更多 compute tile、更多 I/O chiplet，用圓形 wafer 處理超大型矩形封裝，面積利用率與成本曲線會越來越差。CoPoS（Chip-on-Panel-on-Substrate，晶片-面板-基板）代表的分歧是：先進封裝是否要從 wafer-level 的圓形生產邏輯，轉向 panel-level 的方形生產邏輯。

郭明錤在 X 上提到，CoPoS 目前預期 2H28 量產，目標是改善 9.5x reticle-size 以上超大型封裝的經濟性，並提到 310 × 310 mm temporary glass carrier、250 × 250 pilot / 510 × 515 mass production glass panel 等尺寸線索。[^kuo-copos] TrendForce 引述 Commercial Times 的報導也指出，TSMC CoPoS pilot line 已開始導入設備，市場預期 volume production 可能在 2028–2029 ramp；但同時也提醒，substrate size 放大後，warpage 會成為主要量產挑戰。[^trendforce-copos]

這裡最容易被誤讀的是玻璃。玻璃核心基板（Glass Core Substrate）不是把晶片直接放在玻璃上，也不是用玻璃簡單取代 ABF。比較正確的理解是 ABF / Glass / ABF：玻璃提供平坦度、尺寸穩定性與機械支撐；上下兩側的 ABF build-up layers 仍負責細線路與 chip attach。Intel 在 glass substrate 資料中指出，相比 organic substrate，玻璃具備更好的平坦度、熱機械穩定性與尺寸穩定性，並可能支援更高 interconnect density，適合 data center、AI、graphics 等大型高效能封裝。[^intel-glass]

因此，CoPoS 的投資重點不該停在「玻璃」兩字，而是要看誰能解玻璃通孔（Through Glass Via, TGV）、填銅 / 金屬化、面板級曝光、翹曲控制與檢測。Arvind Srinivas 的 X 貼文指出，CoPoS glass core substrate 是 ABF / Glass / ABF 三層堆疊，而 TGV 是關鍵瓶頸。[^arvind-copos] LPKF 的 LIDE 技術資料則提到，其玻璃加工可透過 ultrafast laser modification + wet etching 製作 through-glass vias，並標示 aspect ratio 可達 up to 1:50、sub-micron accuracy，以及 zero micro-cracks / chipping 等能力。[^lpkf-lide] 這意味著 CoPoS 若要成立，靠的不是玻璃材料敘事，而是整條 glass core substrate 製程能否被量產驗證。

**3. 載板邊界的鬆動（供應鏈分歧）：** CoWoP 則更激進，它挑戰的是「封裝載板一定要存在嗎？」這個問題。CoPoS 還是在改善基板與面板製程；CoWoP（Chip-on-Wafer-on-PCB，晶片-晶圓-PCB）則試圖把傳統 ABF substrate 拿掉，讓高精度類載板 PCB（Substrate-Like PCB, SLP）直接承擔更多封裝任務。

這個方向之所以有吸引力，是因為 ABF 載板已經成為成本、供給與尺寸放大的壓力點。如果能把 chip + interposer module 直接接到高階 SLP / PCB，理論上訊號路徑更短、結構更簡化、熱路徑更直接，也可能降低對 ABF substrate 的依賴。Basler 對 CoWoP 的描述是，它把 package substrate 與 PCB 整合成單一結構，使模組更薄、頻寬更高、熱性能更好；但同時也指出，整個 PCB supply chain 必須達到 semiconductor-grade accuracy。[^basler-cowop]

這句話決定了 CoWoP 不能被簡化成「PCB 股受惠」。普通 PCB 是系統板，不是先進封裝載板；CoWoP 要求 PCB / SLP 具備接近封裝級的線路精度、層間對位、低翹曲、材料穩定性與檢測能力。Basler 文中提到 CoWoP 可能需要 15–20 µm line / space 的能力，並面臨多層結構、翹曲、材料穩定性與半導體級檢測挑戰。[^basler-cowop] 這代表 PCB 產業會出現分化：能往 substrate-like precision 升級的廠商，可能被重新定價；仍停留在普通板材產能的公司，則很難真正吃到核心價值。

**4. 電訊號路徑的失效（網路分歧）：** CPO 與前面三者不同，它解的不是 GPU package 內部問題，而是 AI factory 網路問題。當 GPU cluster 擴大，rack 之間、switch 之間的資料交換變成主要瓶頸，傳統 pluggable transceiver 架構會讓高速電訊號從 switch ASIC 經過 PCB、connector，再到前面板光模組才轉成光訊號。速度越高，這段 electrical path 的 loss、功耗、散熱與故障點就越難接受。

共同封裝光學（Co-Packaged Optics, CPO）的分歧在於：光學引擎是否必須從前面板移到 switch ASIC 旁邊。NVIDIA 的 CPO 技術文章指出，傳統 200 Gbps channel 的 electrical loss 可高達 22 dB；把 electro-optical conversion 放到 switch package 旁後，loss 可降到約 4 dB，每 interface 功耗可從常見 30W 降到 as low as 9W。NVIDIA 也宣稱其 CPO-based systems 可帶來 up to 3.5x power efficiency 與 10x resiliency improvement，Quantum-X / Spectrum-X Photonics 商用時間指向 2026。[^nvidia-cpo]

因此，CPO 不是 CoPoS 或 CoWoP 的同義詞。CoWoS、CoPoS、CoWoP 處理的是 AI accelerator package 如何承載更多 compute / memory；CPO 處理的是 AI data center network 如何用更低功耗搬更多資料。它的供應鏈重點也不同：laser source、silicon photonics / PIC、optical engine、fiber attach、FAU、optical testing、switch system integration 才是核心。這裡的錢不會平均灑到所有光通概念股，而會集中在 laser reliability、optical engine yield、fiber alignment 自動化、optical test throughput 與系統維修性這些瓶頸層。

**5. 估值敘事的分裂（投資分歧）：** 這一輪先進封裝最危險的地方，是市場會把技術分歧簡化成標籤交易：CoWoS 等於 ABF，CoPoS 等於玻璃，CoWoP 等於 PCB，CPO 等於光通。這種分法太粗，買到的常常是名詞，而不是財報。真正的研究應該反過來，先問瓶頸在哪，再問誰有資格解瓶頸。

CoWoS 的瓶頸在 TSMC advanced packaging capacity、ABF substrate、HBM allocation、測試與散熱；CoPoS 的瓶頸在 glass core substrate、TGV / LIDE、Cu filling / metallization、panel-level lithography、warpage control 與 inspection；CoWoP 的瓶頸在高階 SLP / PCB、mSAP / SAP、超薄銅箔、半導體級 AOI、低翹曲與可靠性；CPO 的瓶頸在 laser source、silicon photonics / PIC、optical engine、fiber attach、optical testing 與 switch system integration。

這不再只是封裝技術路線圖，而是一場關於 AI 系統控制權的重新分配。誰能把下一個瓶頸變成客戶 qualification、出貨占比、ASP 或毛利率，誰才有機會把題材轉成估值；誰只是名字沾到概念，最後大概率只會停留在交易熱度。

先進封裝真正的結論不是「哪個技術最強」，而是 AI 系統已經大到必須重新切分半導體供應鏈的價值。CoWoS 讓今天的 GPU + HBM 能量產；CoPoS 嘗試讓下一代超大型 package 具備面積經濟性；CoWoP 逼 PCB 供應鏈向封裝載板升級；CPO 則把光學推進 switch package，避免 AI factory 被網路功耗拖垮。這些技術共同指向同一件事：**AI 時代的封裝，不是晶片做完之後的收尾，而是決定算力能不能被真正釋放的主戰場。**

---

## Sources

[^kuo-copos]: 郭明錤｜Ming-Chi Kuo, “Key takeaways on TSMC's next-generation advanced packaging, CoPoS,” X, 2026-06-11. https://x.com/mingchikuo/status/2064896082203849094?s=20

[^arvind-copos]: Arvind Srinivas, “CoPoS's glass core substrate is a 3-layer stack: ABF / glass / ABF… TGV is the Bottleneck…,” X, 2026-06-11. https://x.com/arv9293/status/2064955872250388728?s=20

[^trendforce-copos]: TrendForce, “[News] TSMC Advances Panel-Level Packaging, CoPoS Pilot Line Reportedly Set for June Completion, 2028–29 Ramp Eyed,” 2026-04-13. https://www.trendforce.com/news/2026/04/13/news-tsmc-advances-panel-level-packaging-copos-pilot-line-reportedly-set-for-june-completion-2028-29-ramp-eyed/

[^intel-glass]: Intel, “Intel Unveils Industry-Leading Glass Substrates to Meet Demand for More Powerful Compute,” 2023. https://www.intc.com/news-events/press-releases/detail/1647/intel-unveils-industry-leading-glass-substrates-to-meet

[^lpkf-lide]: LPKF, “LIDE® Technology: Industry Standard for Advanced Glass Processing.” https://lide.lpkf.com/en/technology/lide

[^basler-cowop]: Basler, “CoWoP Is Coming, and Semiconductor Inspection Is Ready All Along.” https://www.baslerweb.com/en/learning/semicon-chip-on-wafer-on-pcb/

[^nvidia-cpo]: NVIDIA Technical Blog, “Scaling AI Factories with Co-Packaged Optics for Better Power Efficiency,” 2026. https://developer.nvidia.com/blog/scaling-ai-factories-with-co-packaged-optics-for-better-power-efficiency/
