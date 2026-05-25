# Stock Homes

Markdown → HTML renderer for stock / industry reports.

## Workflow

1. Keep a local Markdown copy of every report under `reports/<category>/<slug>.md`.
2. Publish the primary version to HackMD, then paste the HackMD URL into front matter as `hackmd_url`.
3. Run `pnpm build` to render `dist/`.
4. Push to `main`; GitHub Actions deploys the generated site to GitHub Pages.

## Create a new local report

```bash
pnpm new -- "NVIDIA Rubin passive components" passive-components
```

This creates a dated Markdown file with front matter. The renderer supports:

- YAML front matter via `front-matter`
- Markdown tables, footnotes, links, and raw HTML
- syntax-highlighted code blocks
- KaTeX math
- Mermaid diagrams
- table of contents marker: `[[toc]]`

## Front matter

```yaml
---
title: Report title
date: 2026-05-25
category: passive-components
tags: [NVIDIA, Rubin, supply-chain]
hackmd_url: https://hackmd.io/...
description: Short summary for the index page
---
```

`reports/` is the durable local source of truth. `dist/` is generated and intentionally not committed.
