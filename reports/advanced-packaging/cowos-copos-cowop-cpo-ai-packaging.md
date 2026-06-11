---
title: "AI 先進封裝路線解析：CoWoS、CoPoS、CoWoP 與 CPO 到底在解什麼問題"
date: 2026-06-11
category: advanced-packaging
tags: ["advanced packaging", "CoWoS", "CoPoS", "CoWoP", "CPO", "TSMC", "NVIDIA", "AI server"]
hackmd_url: ""
description: "用一條產業主線理解 CoWoS、CoPoS、CoWoP 與共同封裝光學 CPO：AI 晶片為什麼需要這些封裝，它們各自解決什麼瓶頸，以及供應鏈應該看哪裡。"
keywords: ["CoWoS", "CoPoS", "CoWoP", "共同封裝光學", "Co-Packaged Optics", "玻璃核心基板", "TGV", "ABF", "AI 伺服器", "先進封裝"]
---

> 版本：2026-06-11  
> 定位：產業研究與供應鏈分析，不是買賣建議。X 貼文視為 market intelligence / 供應鏈線索；公開公司、媒體與技術資料為主要引用依據。  
> 這篇文章只想回答一個問題：**AI 晶片為什麼突然需要這麼多種先進封裝？**

---

## 一張圖先建立共同語言

![先進封裝路線對照：CoWoS、CoPoS、CoWoP](../../assets/reports/advanced-packaging/advanced_packaging_comparison_cn_v2.png)

[[toc]]

---

## 先講結論：這不是誰取代誰，而是 AI 系統變大之後，瓶頸開始分層

如果只看名詞，CoWoS、CoPoS、CoWoP、CPO 很容易變成一串令人疲乏的縮寫。但從產業角度看，它們其實都在回答同一個問題：**當 AI 晶片不能再只靠單顆 die 變大來提升效能時，怎麼把更多運算、更多 HBM、更多 I/O、更多網路頻寬，用可量產、可散熱、可接受成本的方式放進同一個系統？**

今天的 AI accelerator 已經不是「一顆 GPU」而已。它是一個由 GPU / ASIC、HBM、interposer、ABF substrate、PCB、電源、散熱、網路交換器與光學模組共同組成的系統。當 NVIDIA、AMD 或 hyperscaler 要推下一代平台時，真正的問題不是單顆邏輯晶片能不能再快 20%，而是整個系統能不能支撐更多 HBM、更大 package、更高功耗密度、更低網路延遲，以及更合理的良率與成本。

所以這些技術可以這樣理解：**CoWoS 是現在 AI GPU 能量產的主力封裝；CoPoS 是為了解決下一代超大型 package 面積與成本；CoWoP 是更激進地把封裝載板與 PCB 邊界打掉；CPO 則是把同一場封裝戰爭延伸到 AI data center 的網路交換器。** 它們不是排隊取代的單一路線，而是對應到不同層級的瓶頸。

---

## CoWoS 是現在式：先把 GPU 和 HBM 接起來，AI GPU 才能真的跑起來

CoWoS（Chip-on-Wafer-on-Substrate，晶片-晶圓-基板）之所以重要，是因為 AI GPU 的效能很大一部分被 HBM 頻寬決定。GPU / ASIC 本身再強，如果拿不到足夠快、足夠近的記憶體資料，運算單元就會閒置。因此，AI accelerator 需要把 GPU / ASIC 與 HBM 放得很近，並用高密度 interposer 把它們接起來。

用最簡單的方式講，CoWoS 就是：**GPU / ASIC 與 HBM 先放在矽中介層（Silicon Interposer）或類似高密度互連結構上，再接到 ABF 封裝載板，最後進入 PCB 與系統。** 這種結構讓 HBM 與 GPU 之間的訊號路徑很短、頻寬很高、延遲較低，因此成為現行 AI GPU 的主力量產方案。Basler 的 CoWoP 技術文章也把 CoWoS 描述為已成熟並支撐 NVIDIA H100 / H200 等 AI accelerator 的主流先進封裝。[^basler-cowop]

但 CoWoS 的成功也帶來下一個問題：package 越做越大，成本與產能壓力會快速上升。矽中介層面積越大，成本越高；ABF substrate 尺寸越大，良率與翹曲越難控；CoWoS 產能本身也成為 AI GPU 交付速度的瓶頸。換句話說，CoWoS 不是不行，而是它太重要、用量太大、尺寸越來越誇張，所以產業必須尋找下一個可以支撐更大 package 的方法。

這就是 CoPoS 被討論的背景。

---

## CoPoS 的出現，是因為下一代 AI package 可能大到「晶圓思維」不夠經濟

CoPoS（Chip-on-Panel-on-Substrate，晶片-面板-基板）最容易被誤解成「玻璃封裝」或「玻璃取代 ABF」。這種說法太粗。更準確地說，CoPoS 是在嘗試把先進封裝從圓形 wafer 的生產邏輯，推向更適合大型矩形 package 的 panel-level 生產邏輯。

為什麼要這樣做？因為 AI package 正在變得非常大。當一個封裝裡要放更多 HBM、更多 compute tile、更多 I/O chiplet，package 面積會快速膨脹。圓形 wafer 對超大型矩形封裝的面積利用率並不好，而且 silicon interposer 面積越大，成本上升越快。這時候，方形 panel 的排版與產出效率就開始有吸引力。

郭明錤在 X 上提到，CoPoS 目前預期 2H28 量產，目標是改善 9.5x reticle-size 以上超大型封裝的經濟性，並提到 310 × 310 mm temporary glass carrier、250 × 250 pilot / 510 × 515 mass production glass panel 等尺寸線索。[^kuo-copos] TrendForce 引述 Commercial Times 的報導也指出，TSMC CoPoS pilot line 已開始導入設備，市場預期 volume production 可能在 2028–2029 ramp，同時提醒 substrate size 放大後，warpage 是主要量產挑戰。[^trendforce-copos]

這裡的玻璃核心基板（Glass Core Substrate）很關鍵，但它的角色不是「玻璃 interposer」。比較正確的結構是 **ABF / Glass / ABF**：玻璃在中間提供尺寸穩定性、平坦度與機械支撐；ABF build-up layers 仍在上下兩側負責線路與 chip attach。Intel 在 glass substrate 資料中指出，相比 organic substrate，玻璃具備更好的平坦度、熱機械穩定性與尺寸穩定性，並可能支援更高 interconnect density，適合 data center、AI、graphics 等大型高效能封裝。[^intel-glass]

也就是說，CoPoS 的本質不是「換一種材料所以比較潮」，而是要解決超大型 AI package 的面積、穩定性與成本曲線。玻璃只是其中一個關鍵材料平台，真正困難的是把玻璃、ABF、RDL、TGV、電鍍、檢測與翹曲控制整合成可量產流程。

TGV（Through Glass Via，玻璃通孔）就是這條路線的核心瓶頸。Arvind Srinivas 的 X 貼文指出，CoPoS glass core substrate 是 ABF / Glass / ABF 三層堆疊，而 TGV 的難點是在玻璃中形成大量微孔並填銅。[^arvind-copos] LPKF 的 LIDE 技術頁面則提到，其玻璃加工可透過 ultrafast laser modification + wet etching 製作 through-glass vias，並標示 aspect ratio 可達 up to 1:50、sub-micron accuracy，以及 zero micro-cracks / chipping 等能力。[^lpkf-lide]

這就是投資與供應鏈研究要注意的地方：**CoPoS 不是買所有玻璃概念，也不是買所有 ABF 概念，而是要找誰能解 TGV、玻璃加工、面板級金屬化、翹曲控制與量產檢測。** 如果這些瓶頸解不掉，panel-level 的理論成本優勢就不會轉成財報；如果解掉，TSMC 的先進封裝護城河會從 CoWoS 延伸到更大尺寸的 AI package。

---

## CoWoP 是另一條更激進的路：既然 ABF 載板貴又卡，那能不能直接讓 PCB 承擔封裝責任？

CoWoP（Chip-on-Wafer-on-PCB，晶片-晶圓-PCB）的思路更激進。CoPoS 還是保留「封裝基板」這個角色，只是把它推向 glass core + panel-level；CoWoP 則是問：**能不能把傳統 ABF substrate 拿掉，讓高精度類載板 PCB（Substrate-Like PCB, SLP）直接承擔更多封裝功能？**

這個方向的吸引力很明顯。少一層 substrate，訊號路徑理論上更短，power integrity 可能更好，熱路徑也有機會更直接；如果能用大面積 PCB / SLP 製程取代部分 ABF 功能，成本與產能瓶頸也可能改善。Basler 對 CoWoP 的描述是：它把 package substrate 與 PCB 整合成單一結構，使模組更薄、頻寬更高、熱性能更好；但同時也指出 PCB supply chain 必須達到 semiconductor-grade accuracy。[^basler-cowop]

這句話其實就是 CoWoP 的成敗關鍵。傳統 PCB 是系統板，不是先進封裝載板；但 CoWoP 要求 PCB 做接近封裝級的事情。Basler 文中提到 CoWoP 可能需要 15–20 µm line / space 的能力，並面臨多層結構、翹曲、材料穩定性與半導體級檢測挑戰。[^basler-cowop] 如果未來規格繼續往 <10 µm 靠近，普通 PCB 產能幾乎沒有意義，只有真正能做到 mSAP / SAP、高階 SLP、低翹曲與高良率檢測的廠商才可能進入供應鏈。

所以 CoWoP 不能被簡化成「PCB 股全部受惠」。它更像是 PCB 產業的一場升級淘汰賽。成功的話，高階 PCB / SLP 的價值會被重估；失敗或延後的話，CoWoP 就只會停留在漂亮的架構圖與供應鏈故事裡。對投資人來說，關鍵不是聽到 CoWoP 三個字就興奮，而是要問：這家公司是否真的有 substrate-like precision？是否有可靠性數據？是否能通過 NVIDIA / TSMC / OSAT 的 qualification？良率損失由誰承擔？

---

## CPO 跟 CoPoS / CoWoP 不是同一件事：它解的是 AI factory 網路功耗與頻寬

共同封裝光學（Co-Packaged Optics, CPO）常被放進同一個討論，是因為它也叫「封裝」，而且同樣與 AI infrastructure 有關。但 CPO 解的不是 GPU + HBM package substrate 問題，而是 AI data center network 的問題。

AI cluster 越大，GPU 之間、rack 之間、switch 之間的資料交換就越誇張。傳統 pluggable transceiver 架構下，訊號要從 switch ASIC 經過 PCB、connector，再到前面板的光模組才轉成光訊號。速度越高，這段 electrical path 的 loss、功耗與散熱問題越嚴重。NVIDIA 的 CPO 技術文章指出，傳統 200 Gbps channel 的 electrical loss 可高達 22 dB；把 electro-optical conversion 放到 switch package 旁後，loss 可降到約 4 dB，每 interface 功耗可從常見 30W 降到 as low as 9W。NVIDIA 也宣稱其 CPO-based systems 可帶來 up to 3.5x power efficiency 與 10x resiliency improvement，Quantum-X / Spectrum-X Photonics 商用時間指向 2026。[^nvidia-cpo]

換句話說，CPO 的核心不是「把 GPU 封得更大」，而是「讓 switch ASIC 跟光學引擎靠得更近」。這會改變光通供應鏈的價值分布：laser source、silicon photonics、optical engine、fiber attach、FAU、optical test、switch system integration 都會變重要。但同樣地，錢不會平均流向所有 CPO 概念股。真正值錢的是瓶頸層：laser 是否可靠、optical engine 良率是否夠高、fiber alignment 是否能自動化、optical test throughput 是否能支撐量產、系統維修模式是否可接受。

這也是為什麼 CPO 要跟 CoPoS / CoWoP 分開看。CoPoS 與 CoWoP 主要討論 AI accelerator package 如何承載更多 compute / memory；CPO 則討論 AI factory network 如何用更低功耗搬更多資料。它們都屬於 AI 基礎設施的封裝升級，但在系統位置與供應鏈瓶頸上完全不同。

---

## 供應鏈研究應該從「瓶頸」出發，而不是從名詞出發

這一輪先進封裝題材最危險的地方，是市場會把所有名詞都變成一籃子概念股：CoWoS 就買 ABF，CoPoS 就買玻璃，CoWoP 就買 PCB，CPO 就買光通。這種分法太粗，容易買到敘事，而不是買到真正能轉成營收與毛利率的瓶頸。

比較務實的看法是：CoWoS 的瓶頸在 TSMC advanced packaging capacity、ABF substrate、HBM allocation、測試與散熱；CoPoS 的瓶頸在 glass core substrate、TGV / LIDE、Cu filling / metallization、panel-level lithography、warpage control 與 inspection；CoWoP 的瓶頸在高階 SLP / PCB、mSAP / SAP、超薄銅箔、半導體級 AOI、低翹曲與可靠性；CPO 的瓶頸則在 laser source、silicon photonics / PIC、optical engine、fiber attach、optical testing 與 switch system integration。

如果一家公司只是「產品名稱跟題材有關」，但沒有客戶認證、沒有規格升級、沒有產能限制、沒有良率門檻，那它的受益很可能只是股價敘事。反過來，如果一家公司卡在瓶頸層，且能證明它的能力被客戶 qualification、ASP、出貨量或毛利率驗證，那才比較可能形成產業 alpha。

---

## 最後的判斷：先進封裝正在從後段製程，變成 AI 系統架構本身

CoWoS、CoPoS、CoWoP、CPO 其實共同指向同一件事：AI 競爭已經不是單顆晶片競爭，而是整個系統如何被封裝、互連、供電、散熱與量產的競爭。

CoWoS 會繼續是現在的主力，因為它已經被 AI GPU 量產驗證，不應過早喊被取代。CoPoS 是 TSMC 面對 ultra-large package 的中長期戰略，重點不是玻璃噱頭，而是面板級封裝與玻璃核心基板能否真的改善大尺寸 package 的成本與良率。CoWoP 是更激進的 system-level packaging，如果成功，會把高階 PCB / SLP 推到更高價值的位置；但它的量產難度也最高。CPO 則把封裝戰爭推到 AI data center networking，因為當 cluster scale 繼續放大，網路功耗與可靠性會變成另一個核心瓶頸。

因此，研究這條產業鏈時，最重要的不是記住縮寫，而是抓住主線：**AI 系統越做越大，資料越搬越多，封裝就從成本項目變成效能、功耗、良率與供應鏈控制權的核心。誰掌握下一個瓶頸層，誰才有機會從題材變成財報。**

---

## Sources

[^kuo-copos]: 郭明錤｜Ming-Chi Kuo, “Key takeaways on TSMC's next-generation advanced packaging, CoPoS,” X, 2026-06-11. https://x.com/mingchikuo/status/2064896082203849094?s=20

[^arvind-copos]: Arvind Srinivas, “CoPoS's glass core substrate is a 3-layer stack: ABF / glass / ABF… TGV is the Bottleneck…,” X, 2026-06-11. https://x.com/arv9293/status/2064955872250388728?s=20

[^trendforce-copos]: TrendForce, “[News] TSMC Advances Panel-Level Packaging, CoPoS Pilot Line Reportedly Set for June Completion, 2028–29 Ramp Eyed,” 2026-04-13. https://www.trendforce.com/news/2026/04/13/news-tsmc-advances-panel-level-packaging-copos-pilot-line-reportedly-set-for-june-completion-2028-29-ramp-eyed/

[^intel-glass]: Intel, “Intel Unveils Industry-Leading Glass Substrates to Meet Demand for More Powerful Compute,” 2023. https://www.intc.com/news-events/press-releases/detail/1647/intel-unveils-industry-leading-glass-substrates-to-meet

[^lpkf-lide]: LPKF, “LIDE® Technology: Industry Standard for Advanced Glass Processing.” https://lide.lpkf.com/en/technology/lide

[^basler-cowop]: Basler, “CoWoP Is Coming, and Semiconductor Inspection Is Ready All Along.” https://www.baslerweb.com/en/learning/semicon-chip-on-wafer-on-pcb/

[^nvidia-cpo]: NVIDIA Technical Blog, “Scaling AI Factories with Co-Packaged Optics for Better Power Efficiency,” 2026. https://developer.nvidia.com/blog/scaling-ai-factories-with-co-packaged-optics-for-better-power-efficiency/
