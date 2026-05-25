---
title: 範例報告：Markdown 渲染檢查
date: 2026-05-25
category: examples
tags: [demo, renderer]
hackmd_url: ""
description: 用來驗證 Stock Homes Markdown to HTML renderer 的範例報告。
---

[[toc]]

## 摘要

這是一份範例報告。每篇正式報告都應保留 Markdown 原文在 `reports/`，並可用 `hackmd_url` 連到 HackMD 主發布版。

## 表格

| 項目 | 說明 |
| --- | --- |
| Local copy | `reports/<category>/<slug>.md` |
| HTML output | `dist/reports/<category>/<slug>.html` |
| Deployment | GitHub Pages Actions |

## Mermaid

```mermaid
flowchart LR
  A[Markdown reports/] --> B[build.js]
  B --> C[dist/ HTML]
  C --> D[GitHub Pages]
  A --> E[HackMD URL in front matter]
```

## Footnote

研究報告需要來源連結與清楚區分事實 / 推論。[^discipline]

[^discipline]: 這裡只是 renderer sample；正式研究內容仍需要逐條引用來源。
