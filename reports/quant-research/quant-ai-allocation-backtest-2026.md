---
title: "2026 量化論文筆記：可驗證來源與可回測 proxy"
date: 2026-05-26
category: quant-research
tags: ["量化研究", "asset allocation", "Transformer", "Sharpe Ratio", "backtest"]
hackmd_url: "https://hackmd.io/@no0mTG4DTVi61wHzNybh_Q/BJ5jDAzlGx"
description: "把目前可找到公開來源的量化資產配置論文整理成研究筆記，並用可重現的 ETF proxy 回測比較 direct allocation、risk-control 與 sparse Sharpe 思路。"
---

> 更新時間：2026-05-26 16:05 CST  
> 定位：研究筆記 / proxy backtest，不是買賣建議。這篇只把「目前可找到公開來源」的論文納入；未找到公開來源的標題先不當成已發表事實。

# 一句話結論

【判斷】這批量化 AI 論文真正值得追的是同一個方向：**不要只把 ML 拿來預測價格，而是讓模型直接學 portfolio decision / risk objective**。但用簡化 proxy 回測後，結果也提醒一件事：**降低風險比提高報酬容易；要打敗 SPY 的長期總報酬很難。**

本次 proxy 回測中：

- **SPY buy-and-hold** 總報酬最高：2018-01-02 至 2026-05-22 成長 **3.15x**，CAGR **14.67%**，但最大回撤 **-33.72%**。
- **Trend inverse-vol proxy** 報酬較低：成長 **2.04x**，CAGR **8.91%**，但最大回撤只有 **-9.86%**，Sharpe_0rf **1.19**，是風險控制最強的版本。
- **Sparse tangent proxy** 成長 **2.19x**，CAGR **9.81%**，最大回撤 **-19.35%**；沒有明顯優於簡單等權。

【解讀】如果目標是「長期資本成長」，SPY 仍是強 benchmark；如果目標是「降低 drawdown / CVaR」，risk-aware allocation 才有研究價值。

---

# 1. 來源查證：哪些標題目前有公開來源？

| 原始題目 / 相關論文 | 查證狀態 | 公開來源 | 本文處理方式 |
|---|---:|---|---|
| Joint-Embedding Predictive Learning of Latent Market States in U.S. Equities | 未找到精確公開論文 | — | 不納入正式回測，只保留為「regime encoder」研究方向 |
| Signature-Informed Transformer for Asset Allocation | 找到精確 arXiv | arXiv: [2510.03129](https://arxiv.org/abs/2510.03129) | 納入，做 risk-aware direct allocation proxy |
| Portfolio Transformer for Attention-Based Asset Allocation | 找到相關 arXiv | arXiv: [2206.03246](https://arxiv.org/abs/2206.03246) | 納入，作為 direct Sharpe optimization 的前序參考 |
| Global Merger-Arbitrage Forecasting with Language Models | 未找到精確公開論文 | — | 不納入回測；M&A 需要 deal database，不適合用 ETF proxy 硬測 |
| Decision-focused Sparse Tangent Portfolio Optimization | 未找到精確同名論文 | 相關：arXiv [2410.21100](https://arxiv.org/abs/2410.21100)、DOI [10.1016/j.orl.2016.05.012](https://doi.org/10.1016/j.orl.2016.05.012) | 納入 sparse tangent / sparse Sharpe proxy |

---

# 2. 已有來源論文重點

## 2.1 Signature-Informed Transformer for Asset Allocation

【來源】Yoontae Hwang, Stefan Zohren, *Signature-Informed Transformer for Asset Allocation*, arXiv:2510.03129v3，分類 cs.LG / cs.AI / q-fin.PM，初版 2025-10-03，更新 2026-01-22。來源：<https://arxiv.org/abs/2510.03129>

【事實】arXiv 摘要指出，傳統 deep learning asset allocation 常把 forecasting 與 optimization 分開，作者認為這會造成「prediction error 低，但 portfolio decision 不一定好」的 mismatch。論文提出 Signature-Informed Transformer，把 path signatures、特殊 attention module 與 direct policy learning 結合，並直接最小化 Conditional Value at Risk，讓訓練目標與金融風險目標更一致。

【我的解讀】這篇的重點不是「Transformer 比 MA 更會預測價格」，而是：

1. feature extraction 與 allocation decision 合併；
2. objective 從 MSE / return forecast 換成 CVaR；
3. 模型被設計成看資產之間的幾何關係，而不是單一資產時間序列。

【可疑點】金融資料低訊噪，Transformer 容易過擬合；若 turnover、交易成本、universe selection、survivorship bias 沒嚴格處理，漂亮結果不一定能實盤。

## 2.2 Portfolio Transformer for Attention-Based Asset Allocation

【來源】Damian Kisiel, Denise Gorse, *Portfolio Transformer for Attention-Based Asset Allocation*, arXiv:2206.03246。來源：<https://arxiv.org/abs/2206.03246>

【事實】arXiv 摘要表示，傳統流程是 returns forecasting 後再 optimization；Portfolio Transformer 則試圖繞過報酬預測，直接最佳化 Sharpe ratio，作為 end-to-end portfolio optimization framework。

【我的解讀】這是 #2 的前序精神：**不要先預測報酬再丟 optimizer，而是讓模型直接對 portfolio performance 負責。**

## 2.3 Sparse Sharpe / Sparse Tangent Portfolio

【來源 1】Yizun Lin, Zhao-Rong Lai, Cheng Li, *A Globally Optimal Portfolio for m-Sparse Sharpe Ratio Maximization*, arXiv:2410.21100。來源：<https://arxiv.org/abs/2410.21100>

【來源 2】*Sparse tangent portfolio selection via semi-definite relaxation*, Operations Research Letters, DOI: 10.1016/j.orl.2016.05.012。來源：<https://doi.org/10.1016/j.orl.2016.05.012>

【事實】arXiv:2410.21100 摘要指出，現代投組管理可能需要 m-sparse portfolio，也就是最多只持有 m 個活躍資產，以降低管理與交易成本；但 Sharpe ratio + sparsity constraint 因為非凸與稀疏限制而困難。該文將 m-sparse fractional optimization 轉換成等價的 m-sparse quadratic programming problem，並提出 proximal gradient algorithm。

【我的解讀】這條線比單純 AI 更接近實務：不是要持有 500 個權重很漂亮但沒法執行的資產，而是要在可管理的持倉數內，把風險調整後報酬做出來。

---

# 3. Proxy 回測設計

這次沒有重做原論文模型；原因是：

1. Signature-Informed Transformer 需要完整訓練 pipeline、path signature feature、CVaR loss 與原始 universe 設定。
2. Portfolio Transformer 需要神經網路架構與訓練資料切分。
3. Sparse Sharpe 需要更嚴格 optimizer；本文只做「可解釋、可重現」的近似版本。

因此本文做的是 **proxy backtest**：用簡化規則模擬論文思想，而不是宣稱復現論文。

## 資料與假設

【資料來源】Yahoo Finance chart API adjusted close。下載檔保存在本地：`assets/quant-research/quant-paper-proxy-backtest/yahoo_adjusted_close.csv`。

【回測區間】2018-01-02 至 2026-05-22，共 2109 個交易日。

【資產池】

- SPY：S&P 500 ETF
- QQQ：Nasdaq 100 ETF
- IWM：Russell 2000 ETF
- TLT：20Y Treasury ETF
- GLD：Gold ETF
- HYG：High-yield bond ETF
- UUP：US Dollar ETF

【交易假設】

- 月底再平衡。
- 使用 adjusted close。
- 每次單邊 turnover 成本 5 bps。
- 不含稅，不含借券 / 放空，不含股息稅差異。
- 現金部位報酬假設為 0%。

## 策略定義

| 策略 | 對應研究概念 | 實作 proxy |
|---|---|---|
| SPY buy-and-hold | benchmark | 100% SPY，買入持有 |
| Monthly equal weight | naive diversified baseline | 7 個 ETF 每月等權再平衡 |
| Trend inverse-vol proxy | Signature / CVaR / risk-control 思路 | 僅持有價格高於 200 日均線的資產，權重按 63 日 realized volatility 反比配置 |
| Sparse tangent proxy | sparse Sharpe / tangent portfolio 思路 | 每月用過去 252 日估計 mean / covariance，選 trailing Sharpe 前 3 名，再用 shrinkage covariance 做 long-only tangent-like weighting |

---

# 4. 回測結果

## 4.1 總表

| strategy | final_growth_x | total_return_pct | cagr_pct | ann_vol_pct | sharpe_0rf | max_drawdown_pct | worst_month_pct | positive_month_pct | avg_annual_turnover_x | rebalance_count |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| SPY buy-and-hold | 3.15 | 215.04 | 14.67 | 19.23 | 0.76 | -33.72 | -12.49 | 67.00 | 0.12 | 1 |
| Monthly equal weight | 2.23 | 122.69 | 10.02 | 10.42 | 0.96 | -18.79 | -6.23 | 65.00 | 0.45 | 102 |
| Trend inverse-vol proxy | 2.04 | 104.47 | 8.91 | 7.51 | 1.19 | -9.86 | -3.83 | 68.00 | 4.12 | 97 |
| Sparse tangent proxy | 2.19 | 119.15 | 9.81 | 10.86 | 0.90 | -19.35 | -8.80 | 67.00 | 5.30 | 90 |

【解讀】

- SPY 仍然是最難打敗的總報酬 benchmark。
- Trend inverse-vol proxy 不是報酬最高，但 drawdown 壓得最漂亮；這比較符合「CVaR / risk-aware allocation」的研究價值。
- Sparse tangent proxy 沒有打敗等權太多，且 turnover 較高。這提醒：sparse Sharpe 在小資產池、粗糙估計下，不會自動變魔法。

## 4.2 年度報酬

| year | SPY buy-and-hold | Monthly equal weight | Trend inverse-vol proxy | Sparse tangent proxy |
|---:|---:|---:|---:|---:|
| 2018 | -5.25 | -2.02 | -2.02 | -5.25 |
| 2019 | 31.22 | 21.03 | 15.61 | 15.19 |
| 2020 | 18.33 | 18.96 | 17.11 | 12.97 |
| 2021 | 28.73 | 9.99 | 5.80 | 9.18 |
| 2022 | -18.18 | -15.39 | 1.78 | 1.99 |
| 2023 | 26.18 | 18.13 | 10.63 | 7.27 |
| 2024 | 24.89 | 14.53 | 11.98 | 16.13 |
| 2025 | 17.72 | 16.52 | 11.86 | 16.30 |
| 2026 YTD | 9.64 | 7.67 | 3.34 | 10.21 |

【解讀】

2022 是最有資訊量的一年：SPY -18.18%，等權 -15.39%，但 Trend inverse-vol 與 Sparse tangent proxy 都小幅正報酬。這表示 risk-control / trend filter 的核心價值是在熊市與升息壓力期保命，而不是在 2021 或 2023 這種強多頭衝最快。

## 4.3 期末權重

| strategy | SPY | QQQ | IWM | TLT | GLD | HYG | UUP |
|---|---:|---:|---:|---:|---:|---:|---:|
| SPY buy-and-hold | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Monthly equal weight | 14.3 | 14.3 | 14.4 | 14.3 | 14.1 | 14.3 | 14.3 |
| Trend inverse-vol proxy | 12.6 | 9.6 | 8.6 | 0.0 | 6.6 | 32.5 | 30.1 |
| Sparse tangent proxy | 43.7 | 36.1 | 20.2 | 0.0 | 0.0 | 0.0 | 0.0 |

【解讀】

- Trend inverse-vol proxy 的期末配置偏 HYG / UUP，表示在當下規則中，低波動與趨勢條件讓風險資產權重被壓低。
- Sparse tangent proxy 集中在 SPY / QQQ / IWM，這比較像「風險資產 momentum 延伸」，不是真正防守策略。

---

# 5. 對四個研究方向的實務判斷

## A. JEPA market state：可研究，但先不要急著交易

【狀態】未找到公開精確論文，因此不納入本文實證。

【如果要做】我會先拿它做 regime encoder，不直接拿來下單。驗證重點是：embedding 是否能提前或同步辨識 volatility spike、correlation breakdown、breadth deterioration，而不是只重現 VIX。

## B. Signature / Portfolio Transformer：真正價值在風控 objective

【狀態】有公開來源。

【本文 proxy 結果】Trend inverse-vol proxy 顯示：如果把目標放在 CVaR / drawdown control，確實可以顯著降低最大回撤；但代價是犧牲多頭市場報酬。

【實務意義】這類模型比較適合：

- 多資產配置；
- 風控 overlay；
- 退休 / family office / 低回撤目標；
- 不是純粹追求打敗 QQQ 的 aggressive strategy。

## C. Merger-arbitrage LLM：不要用 ETF proxy 硬測

【狀態】未找到公開精確論文。

【原因】M&A arbitrage 的資料單位是 deal，不是 daily ETF price。需要 deal announcement、deal terms、regulatory status、spread、completion / break outcome。沒有乾淨 deal database，用 ETF 回測沒有意義。

## D. Sparse tangent / sparse Sharpe：數學漂亮，但估計誤差是敵人

【狀態】有相關公開來源。

【本文 proxy 結果】Sparse tangent proxy 沒有明顯打敗等權，且 turnover 更高。

【解讀】這不是否定 sparse Sharpe，而是提醒：mean / covariance estimation 很脆弱。若要在台股或美股個股實作，必須加上：

- shrinkage covariance；
- liquidity filter；
- turnover penalty；
- sector cap；
- walk-forward validation；
- transaction cost sensitivity。

---

# 6. 下一步：如果要做成真正研究系統

我會分三階段：

1. **先做 baseline suite**：SPY、等權、risk parity、trend inverse-vol、sparse Sharpe。
2. **再做台股 / 美股 universe**：加入流動性、產業限制、交易成本、稅制。
3. **最後才上神經網路**：Transformer / JEPA 必須打敗上述 baseline，否則只是把 overfit 包裝得比較高級。

【關鍵判準】不是 in-sample Sharpe，而是：

- walk-forward CAGR；
- max drawdown；
- turnover-adjusted return；
- 2020 / 2022 / 2025-2026 各市場 regime 表現；
- 是否能在不同 universe 上維持方向一致。

---

# 7. 可重現資料

本次輸出檔：

- [proxy_backtest_metrics.csv](../../assets/quant-research/quant-paper-proxy-backtest/proxy_backtest_metrics.csv)
- [proxy_backtest_yearly_returns.csv](../../assets/quant-research/quant-paper-proxy-backtest/proxy_backtest_yearly_returns.csv)
- [proxy_backtest_equity.csv](../../assets/quant-research/quant-paper-proxy-backtest/proxy_backtest_equity.csv)
- [proxy_latest_weights.csv](../../assets/quant-research/quant-paper-proxy-backtest/proxy_latest_weights.csv)
- [yahoo_adjusted_close.csv](../../assets/quant-research/quant-paper-proxy-backtest/yahoo_adjusted_close.csv)

回測腳本：`scripts/quant_paper_backtest.py`

---

# 來源

1. Yoontae Hwang, Stefan Zohren, *Signature-Informed Transformer for Asset Allocation*, arXiv:2510.03129. <https://arxiv.org/abs/2510.03129>
2. Damian Kisiel, Denise Gorse, *Portfolio Transformer for Attention-Based Asset Allocation*, arXiv:2206.03246. <https://arxiv.org/abs/2206.03246>
3. Yizun Lin, Zhao-Rong Lai, Cheng Li, *A Globally Optimal Portfolio for m-Sparse Sharpe Ratio Maximization*, arXiv:2410.21100. <https://arxiv.org/abs/2410.21100>
4. *Sparse tangent portfolio selection via semi-definite relaxation*, Operations Research Letters. DOI: 10.1016/j.orl.2016.05.012. <https://doi.org/10.1016/j.orl.2016.05.012>
5. Yahoo Finance chart API, adjusted close data for SPY / QQQ / IWM / TLT / GLD / HYG / UUP, downloaded 2026-05-26. Example endpoint pattern: <https://query1.finance.yahoo.com/v8/finance/chart/SPY>

---

# Tags

量化研究、asset allocation、Transformer、Sharpe Ratio、backtest
