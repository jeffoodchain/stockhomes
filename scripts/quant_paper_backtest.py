#!/usr/bin/env python3
"""Proxy backtests for quant-paper research blog notes.

Data source: Yahoo Finance chart API adjusted close.
This is a lightweight, reproducible research script, not a production trading system.
"""
from __future__ import annotations

import datetime as dt
import json
import math
import os
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

ASSETS = {
    "SPY": "S&P 500 ETF",
    "QQQ": "Nasdaq 100 ETF",
    "IWM": "Russell 2000 ETF",
    "TLT": "20Y Treasury ETF",
    "GLD": "Gold ETF",
    "HYG": "High-yield bond ETF",
    "UUP": "US Dollar ETF",
}
START = dt.date(2018, 1, 1)
END = dt.date(2026, 5, 22)
INITIAL = 1.0
COST_BPS = 5  # applied to one-way turnover at rebalance
OUT_DIR = Path(__file__).resolve().parents[1] / "assets/quant-research/quant-paper-proxy-backtest"
CACHE_DIR = Path.home() / ".cache/yahoo"


def yahoo_adjclose(ticker: str, start: dt.date, end: dt.date) -> pd.Series:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache = CACHE_DIR / f"{ticker}_{start}_{end}.json"
    if cache.exists():
        raw = json.loads(cache.read_text())
    else:
        p1 = int(dt.datetime.combine(start, dt.time(), tzinfo=dt.timezone.utc).timestamp())
        p2 = int(dt.datetime.combine(end + dt.timedelta(days=1), dt.time(), tzinfo=dt.timezone.utc).timestamp())
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?period1={p1}&period2={p2}&interval=1d&events=history&includeAdjustedClose=true"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=600) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
        cache.write_text(json.dumps(raw))
        time.sleep(0.2)
    result = raw["chart"]["result"][0]
    dates = pd.to_datetime(result["timestamp"], unit="s", utc=True).tz_convert(None).date
    prices = result["indicators"]["adjclose"][0]["adjclose"]
    s = pd.Series(prices, index=pd.to_datetime(dates), name=ticker, dtype="float64")
    return s.dropna()


def load_prices() -> pd.DataFrame:
    series = [yahoo_adjclose(t, START, END) for t in ASSETS]
    prices = pd.concat(series, axis=1).dropna(how="any")
    return prices


def month_end_rebalance_dates(index: pd.DatetimeIndex) -> list[pd.Timestamp]:
    ser = pd.Series(index=index, data=index)
    return list(ser.groupby([index.year, index.month]).tail(1).index)


def normalize_positive(raw: pd.Series) -> pd.Series:
    raw = raw.replace([np.inf, -np.inf], np.nan).fillna(0.0).clip(lower=0.0)
    total = float(raw.sum())
    if total <= 0:
        return raw * 0.0
    return raw / total


def compute_weights(strategy: str, prices: pd.DataFrame, rebal_date: pd.Timestamp) -> pd.Series:
    tickers = list(prices.columns)
    hist = prices.loc[:rebal_date]
    if strategy == "SPY buy-and-hold":
        w = pd.Series(0.0, index=tickers); w["SPY"] = 1.0; return w
    if strategy == "Monthly equal weight":
        return pd.Series(1.0 / len(tickers), index=tickers)

    returns = hist.pct_change().dropna()
    if len(hist) < 253 or len(returns) < 252:
        if strategy == "Sparse tangent proxy":
            w = pd.Series(0.0, index=tickers); w["SPY"] = 1.0; return w
        return pd.Series(1.0 / len(tickers), index=tickers)

    if strategy == "Trend inverse-vol proxy":
        ma200 = hist.rolling(200).mean().iloc[-1]
        trend_ok = hist.iloc[-1] > ma200
        vol63 = returns.tail(63).std() * math.sqrt(252)
        score = (1.0 / vol63).where(trend_ok, 0.0)
        return normalize_positive(score.reindex(tickers))

    if strategy == "Sparse tangent proxy":
        look = returns.tail(252)
        mu = look.mean() * 252
        vol = look.std() * math.sqrt(252)
        trailing_sharpe = (mu / vol).replace([np.inf, -np.inf], np.nan).fillna(-999)
        selected = trailing_sharpe.sort_values(ascending=False).head(3).index
        mu_sel = mu[selected].clip(lower=0.0)
        cov = look[selected].cov() * 252
        if float(mu_sel.sum()) <= 0:
            return pd.Series(0.0, index=tickers)
        # Diagonal shrinkage for stability; solve tangent-like long-only weights.
        lam = 0.35
        diag = pd.DataFrame(np.diag(np.diag(cov.values)), index=cov.index, columns=cov.columns)
        cov_shrunk = (1 - lam) * cov + lam * diag
        try:
            raw = pd.Series(np.linalg.pinv(cov_shrunk.values).dot(mu_sel.values), index=selected)
        except Exception:
            raw = mu_sel / np.diag(cov_shrunk.values)
        w_sel = normalize_positive(raw)
        w = pd.Series(0.0, index=tickers)
        w.loc[selected] = w_sel
        return w

    raise ValueError(strategy)


@dataclass
class BacktestResult:
    name: str
    equity: pd.Series
    weights: pd.DataFrame
    turnover: pd.Series


def run_strategy(prices: pd.DataFrame, strategy: str) -> BacktestResult:
    returns = prices.pct_change().fillna(0.0)
    rebal_dates = month_end_rebalance_dates(prices.index)
    weights = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
    turnover = pd.Series(0.0, index=prices.index)
    current_w = compute_weights(strategy, prices, prices.index[0])
    equity = pd.Series(index=prices.index, dtype="float64")
    eq = INITIAL
    prev_w_for_turnover = pd.Series(0.0, index=prices.columns)
    cost_rate = COST_BPS / 10000

    for i, date in enumerate(prices.index):
        if date in rebal_dates or i == 0:
            target_w = compute_weights(strategy, prices, date).reindex(prices.columns).fillna(0.0)
            to = float((target_w - prev_w_for_turnover).abs().sum())
            eq *= (1 - cost_rate * to)
            current_w = target_w
            turnover.loc[date] = to
            prev_w_for_turnover = target_w
        daily_ret = float((current_w * returns.loc[date]).sum())
        eq *= (1 + daily_ret)
        equity.loc[date] = eq
        # drift weights after market move
        gross = current_w * (1 + returns.loc[date])
        s = float(gross.sum())
        if s > 0:
            current_w = gross / s
            prev_w_for_turnover = current_w
        weights.loc[date] = current_w
    return BacktestResult(strategy, equity, weights, turnover)


def metrics(res: BacktestResult) -> dict[str, float | int | str]:
    eq = res.equity.dropna()
    daily = eq.pct_change().dropna()
    years = (eq.index[-1] - eq.index[0]).days / 365.25
    cagr = eq.iloc[-1] ** (1 / years) - 1
    vol = daily.std() * math.sqrt(252)
    sharpe = cagr / vol if vol else np.nan
    dd = eq / eq.cummax() - 1
    monthly = eq.resample("ME").last().pct_change().dropna()
    return {
        "strategy": res.name,
        "final_growth_x": eq.iloc[-1],
        "total_return_pct": (eq.iloc[-1] - 1) * 100,
        "cagr_pct": cagr * 100,
        "ann_vol_pct": vol * 100,
        "sharpe_0rf": sharpe,
        "max_drawdown_pct": dd.min() * 100,
        "worst_month_pct": monthly.min() * 100,
        "positive_month_pct": (monthly > 0).mean() * 100,
        "avg_annual_turnover_x": res.turnover.sum() / years,
        "rebalance_count": int((res.turnover > 0).sum()),
    }


def yearly_returns(eq: pd.Series) -> pd.Series:
    y = eq.resample("YE").last().pct_change()
    first_year = eq[eq.index.year == eq.index[0].year]
    if not first_year.empty:
        y.iloc[0] = first_year.iloc[-1] / first_year.iloc[0] - 1
    return y * 100


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    prices = load_prices()
    prices.to_csv(OUT_DIR / "yahoo_adjusted_close.csv", float_format="%.6f")
    strategies = [
        "SPY buy-and-hold",
        "Monthly equal weight",
        "Trend inverse-vol proxy",
        "Sparse tangent proxy",
    ]
    results = [run_strategy(prices, s) for s in strategies]
    metric_df = pd.DataFrame([metrics(r) for r in results])
    metric_df.to_csv(OUT_DIR / "proxy_backtest_metrics.csv", index=False, float_format="%.4f")
    equities = pd.concat({r.name: r.equity for r in results}, axis=1)
    equities.to_csv(OUT_DIR / "proxy_backtest_equity.csv", float_format="%.6f")
    years = pd.concat({r.name: yearly_returns(r.equity) for r in results}, axis=1)
    years.index = years.index.year
    years.to_csv(OUT_DIR / "proxy_backtest_yearly_returns.csv", float_format="%.2f")
    latest_w = pd.concat({r.name: r.weights.iloc[-1] for r in results}, axis=1).T
    latest_w.to_csv(OUT_DIR / "proxy_latest_weights.csv", float_format="%.4f")
    print("DATA_RANGE", prices.index[0].date(), prices.index[-1].date(), "ROWS", len(prices))
    print("METRICS_CSV", OUT_DIR / "proxy_backtest_metrics.csv")
    def md_table(df: pd.DataFrame, index: bool = False) -> str:
        x = df.copy()
        if index:
            x.insert(0, "year", x.index)
        x = x.reset_index(drop=True)
        cols = list(x.columns)
        lines = ["| " + " | ".join(map(str, cols)) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
        for _, row in x.iterrows():
            vals = []
            for v in row:
                if isinstance(v, (float, np.floating)):
                    vals.append(f"{v:.2f}")
                else:
                    vals.append(str(v))
            lines.append("| " + " | ".join(vals) + " |")
        return "\n".join(lines)

    print(md_table(metric_df))
    print("\nYEARLY")
    print(md_table(years, index=True))
    print("\nLATEST_WEIGHTS")
    print(md_table((latest_w * 100).round(1), index=True))


if __name__ == "__main__":
    main()
