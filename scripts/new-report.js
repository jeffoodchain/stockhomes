import fs from "fs";
import path from "path";

const [, , rawTitle, rawCategory = "uncategorized"] = process.argv;
if (!rawTitle) {
  console.error('Usage: bun run new -- "Report title" category');
  process.exit(1);
}

const today = new Date().toISOString().slice(0, 10);
const slug = rawTitle
  .toLowerCase()
  .normalize("NFKD")
  .replace(/[^\p{Letter}\p{Number}]+/gu, "-")
  .replace(/^-+|-+$/g, "")
  .slice(0, 80) || "report";
const category = rawCategory.toLowerCase().replace(/[^a-z0-9-_]+/g, "-").replace(/^-+|-+$/g, "") || "uncategorized";
const dir = path.join(process.cwd(), "reports", category);
fs.mkdirSync(dir, { recursive: true });
const file = path.join(dir, `${today}-${slug}.md`);
if (fs.existsSync(file)) {
  console.error(`Already exists: ${file}`);
  process.exit(1);
}
const content = `---
title: ${JSON.stringify(rawTitle)}
date: ${today}
category: ${category}
tags: []
hackmd_url: ""
description: ""
---

[[toc]]

## 摘要

## 事實與來源

## 推論 / 不確定性

## 反方觀點

## 結論
`;
fs.writeFileSync(file, content);
console.log(file);
