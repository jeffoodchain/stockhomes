import fs from "fs";
import path from "path";
import fm from "front-matter";
import MarkdownIt from "markdown-it";
import anchor from "markdown-it-anchor";
import footnote from "markdown-it-footnote";
import toc from "markdown-it-table-of-contents";
import hljs from "highlight.js";
import katex from "@traptitech/markdown-it-katex";

const ROOT = process.cwd();
const REPORTS_DIR = path.join(ROOT, "reports");
const DIST_DIR = path.join(ROOT, "dist");
const TEMPLATE_DIR = path.join(ROOT, "templates");
const ASSETS_DIR = path.join(ROOT, "assets");

const site = {
  title: "Stock Homes",
  description: "Jeff / FoodChain 股票與產業研究報告庫",
};

const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
  highlight: (str, lang) => {
    if (lang === "mermaid") return `<pre class="mermaid">${escapeHtml(str)}</pre>`;
    if (lang && hljs.getLanguage(lang)) {
      try {
        return `<pre class="hljs"><code>${hljs.highlight(str, { language: lang }).value}</code></pre>`;
      } catch (_) {}
    }
    return `<pre class="hljs"><code>${escapeHtml(str)}</code></pre>`;
  },
})
  .use(anchor, { permalink: anchor.permalink.headerLink() })
  .use(footnote)
  .use(toc, { includeLevel: [2, 3], markerPattern: /^\[\[toc\]\]/im })
  .use(katex);

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function escapeHtml(value = "") {
  return String(value).replace(/[&<>"']/g, (ch) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  }[ch]));
}

function formatDate(value) {
  if (!value) return "Undated";
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return String(value);
  return new Intl.DateTimeFormat("zh-TW", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(d);
}

function slugify(value) {
  return String(value)
    .toLowerCase()
    .normalize("NFKD")
    .replace(/[^\p{Letter}\p{Number}]+/gu, "-")
    .replace(/^-+|-+$/g, "") || "untitled";
}

function slugifyFile(file) {
  return path.basename(file, path.extname(file));
}

function toPosix(p) {
  return p.split(path.sep).join("/");
}

function walkMarkdown(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) return walkMarkdown(full);
    return entry.isFile() && entry.name.endsWith(".md") ? [full] : [];
  });
}

function readTemplate(name) {
  return fs.readFileSync(path.join(TEMPLATE_DIR, `${name}.html`), "utf8");
}

function renderTemplate(template, values) {
  return template.replace(/\{\{\s*([\w.]+)\s*\}\}/g, (_, key) => values[key] ?? "");
}

function copyDir(src, dest) {
  if (!fs.existsSync(src)) return;
  ensureDir(dest);
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const from = path.join(src, entry.name);
    const to = path.join(dest, entry.name);
    if (entry.isDirectory()) copyDir(from, to);
    else fs.copyFileSync(from, to);
  }
}

function normalizeTags(tags) {
  if (!tags) return [];
  const values = Array.isArray(tags) ? tags : String(tags).split(",");
  return [...new Set(values.map((x) => String(x).trim()).filter(Boolean))];
}

function normalizeList(value) {
  if (!value) return [];
  const values = Array.isArray(value) ? value : String(value).split(",");
  return [...new Set(values.map((x) => String(x).trim()).filter(Boolean))];
}

function plainText(body) {
  return body
    .replace(/^---[\s\S]*?---/, "")
    .replace(/```[\s\S]*?```/g, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/[#>*_`\[\]()+|:=~!{}.-]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function excerpt(body) {
  return body
    .replace(/^---[\s\S]*?---/, "")
    .replace(/```[\s\S]*?```/g, "")
    .replace(/[#>*_`\[\]()]/g, "")
    .split("\n")
    .map((x) => x.trim())
    .filter(Boolean)
    .join(" ")
    .slice(0, 180);
}

function relFrom(fromDir, url) {
  return toPosix(path.relative(fromDir, path.join(DIST_DIR, url)));
}

function tagLinks(tags, fromDir) {
  return tags
    .map((tag) => `<a class="tag" href="${relFrom(fromDir, `tags/${slugify(tag)}.html`)}">${escapeHtml(tag)}</a>`)
    .join("");
}

const categoryLabels = new Map([
  ["mk", "股癌逐字稿"],
  ["yutinghao", "游庭皓逐字稿"],
  ["nvidia-architecture", "NVIDIA 架構"],
  ["advanced-packaging", "先進封裝"],
  ["passive-components", "被動元件"],
  ["optical-cpo", "光通 / CPO"],
  ["quant-research", "量化研究"],
  ["stock-analysis", "個股分析"],
  ["hermes-agent", "Hermes 教學"],
]);

const indexCollapsedCategories = new Set(["mk", "yutinghao"]);

function categoryTitle(category) {
  return categoryLabels.get(category) || category;
}

function categoryRank(category) {
  if (category === "mk") return 0;
  if (category === "yutinghao") return 1;
  return 10;
}

function compareCategories(a, b) {
  const rank = categoryRank(a) - categoryRank(b);
  if (rank !== 0) return rank;
  return categoryTitle(a).localeCompare(categoryTitle(b));
}

function categoryLink(category, fromDir) {
  return `<a href="${relFrom(fromDir, `categories/${encodeURIComponent(category)}.html`)}">${escapeHtml(categoryTitle(category))}</a>`;
}

function reportList(items, fromDir, options = {}) {
  const className = ["cards", options.className].filter(Boolean).join(" ");
  return `<div class="${className}">${items.map((report) => {
    const metaText = [report.title, report.excerpt, report.category, categoryTitle(report.category), ...report.tags, ...(report.keywords || []), ...(report.aliases || [])].join(" ");
    const href = relFrom(fromDir, report.url);
    return `<article class="card" data-search="${escapeHtml(metaText)}" data-body="${escapeHtml(report.bodyText || "")}" data-url="${escapeHtml(href)}" data-title="${escapeHtml(report.title)}">
      <a class="card-title" href="${href}">${escapeHtml(report.title)}</a>
      <p>${escapeHtml(report.excerpt)}</p>
    </article>`;
  }).join("\n")}</div>`;
}

function categoryIndexCard(category, items, fromDir) {
  const title = categoryTitle(category);
  const searchText = [title, category, ...items.flatMap((report) => [report.searchText || report.title, report.excerpt, ...report.tags])].join(" ");
  const latest = items[0]?.dateText ? `最新：${items[0].dateText}` : "";
  return `<div class="cards"><article class="card" data-search="${escapeHtml(searchText)}">
      <a class="card-title" href="${relFrom(fromDir, `categories/${encodeURIComponent(category)}.html`)}">${escapeHtml(title)}</a>
      <p>${items.length} 篇文章。點進去後以分類頁瀏覽完整清單。${latest ? ` ${escapeHtml(latest)}` : ""}</p>
    </article></div>`;
}

function collapsedCategorySection(category, items, fromDir) {
  const title = categoryTitle(category);
  return `<section class="category category-collapsed"><h2><a href="categories/${encodeURIComponent(category)}.html">${escapeHtml(title)}</a></h2>
    <div data-category-overview>${categoryIndexCard(category, items, fromDir)}</div>
    <div class="search-expanded" data-search-expanded hidden>
      <p class="search-expanded-label">搜尋結果</p>
      ${reportList(items, fromDir, { className: "search-result-cards" })}
    </div>
  </section>`;
}

function baseFrom(fromDir) {
  const rel = relFrom(fromDir, "index.html");
  if (rel === "index.html") return ".";
  return rel.replace(/\/index\.html$/, "") || ".";
}

function page(outFile, title, description, content) {
  ensureDir(path.dirname(outFile));
  const fromDir = path.dirname(outFile);
  const base = baseFrom(fromDir);
  fs.writeFileSync(outFile, renderTemplate(baseTemplate, {
    title: `${escapeHtml(title)} | ${site.title}`,
    description: escapeHtml(description),
    base,
    content,
  }));
}

fs.rmSync(DIST_DIR, { recursive: true, force: true });
ensureDir(DIST_DIR);
ensureDir(REPORTS_DIR);

const baseTemplate = readTemplate("base");
const reportTemplate = readTemplate("report");
const indexTemplate = readTemplate("index");
const reports = [];
const errors = [];

for (const file of walkMarkdown(REPORTS_DIR)) {
  const raw = fs.readFileSync(file, "utf8");
  const { attributes, body } = fm(raw);
  const rel = path.relative(REPORTS_DIR, file);
  const category = attributes.category || path.dirname(rel).split(path.sep)[0] || "uncategorized";
  const slug = attributes.slug || slugifyFile(file);
  const tags = normalizeTags(attributes.tags);
  if (tags.length === 0) errors.push(`${toPosix(path.relative(ROOT, file))}: front matter must include at least one tag`);
  const outDir = path.join(DIST_DIR, "reports", category);
  const outPath = path.join(outDir, `${slug}.html`);
  ensureDir(outDir);

  const title = attributes.title || slug;
  const content = md.render(body);
  const bodyText = plainText(body);
  const keywords = normalizeList(attributes.keywords);
  const aliases = normalizeList(attributes.aliases);
  const url = `reports/${encodeURIComponent(category)}/${encodeURIComponent(slug)}.html`;
  const meta = {
    title,
    category,
    date: attributes.date || "",
    dateText: formatDate(attributes.date),
    tags,
    keywords,
    aliases,
    hackmd_url: attributes.hackmd_url || "",
    sourcePath: toPosix(path.relative(ROOT, file)),
    url,
    excerpt: attributes.description || excerpt(body),
    bodyText,
  };
  meta.searchText = [
    title,
    meta.excerpt,
    category,
    categoryTitle(category),
    ...tags,
    ...keywords,
    ...aliases,
    bodyText,
  ].join(" ");
  reports.push(meta);

  const reportHtml = renderTemplate(reportTemplate, {
    title: escapeHtml(title),
    date: escapeHtml(meta.dateText),
    category: categoryLink(category, outDir),
    tags: tagLinks(tags, outDir),
    hackmd: meta.hackmd_url ? `<a href="${escapeHtml(meta.hackmd_url)}" target="_blank" rel="noopener">HackMD</a>` : "",
    sourcePath: escapeHtml(meta.sourcePath),
    content,
  });

  page(outPath, title, meta.excerpt, reportHtml);
  console.log(`Built ${toPosix(path.relative(ROOT, outPath))}`);
}

if (errors.length > 0) {
  console.error("\nBuild failed:\n" + errors.map((e) => `- ${e}`).join("\n"));
  process.exit(1);
}

reports.sort((a, b) => new Date(b.date || 0) - new Date(a.date || 0));
const categories = reports.reduce((m, r) => (m.get(r.category)?.push(r) || m.set(r.category, [r]), m), new Map());
const tags = reports.reduce((m, r) => {
  for (const tag of r.tags) m.get(tag)?.push(r) || m.set(tag, [r]);
  return m;
}, new Map());

const indexDir = DIST_DIR;
const categoryNav = [...categories.entries()]
  .sort(([a], [b]) => compareCategories(a, b))
  .map(([category, items]) => `<a href="categories/${encodeURIComponent(category)}.html">${escapeHtml(categoryTitle(category))} <span>${items.length} 篇</span></a>`)
  .join("");
const hiddenTopicTags = new Set(["mk", "transcript", "股癌", "substack", "游庭皓", "早晨財經速解讀", "市場觀察"]);
const topicCloud = [...tags.entries()]
  .filter(([tag]) => !hiddenTopicTags.has(tag.toLowerCase()))
  .sort(([, aItems], [, bItems]) => bItems.length - aItems.length)
  .slice(0, 24)
  .sort(([a], [b]) => a.localeCompare(b, "zh-Hant"))
  .map(([tag, items]) => {
    const weight = items.length >= 10 ? 4 : items.length >= 5 ? 3 : items.length >= 2 ? 2 : 1;
    return `<a class="topic-chip topic-chip-w${weight}" href="tags/${slugify(tag)}.html" data-topic="${escapeHtml(tag)}">${escapeHtml(tag)} <span>${items.length}</span></a>`;
  })
  .join("");

let listHtml = "";
for (const [category, items] of [...categories.entries()].sort(([a], [b]) => compareCategories(a, b))) {
  if (indexCollapsedCategories.has(category)) {
    listHtml += collapsedCategorySection(category, items, indexDir);
  } else {
    const title = categoryTitle(category);
    listHtml += `<section class="category"><h2>${escapeHtml(title)}</h2>${reportList(items, indexDir)}</section>`;
  }
}

const indexHtml = renderTemplate(indexTemplate, {
  reports: listHtml || `<p class="empty">目前沒有報告。請將 Markdown 檔案放到 <code>reports/</code>。</p>`,
  categories: categoryNav,
  topics: topicCloud,
  count: String(reports.length),
});
page(path.join(DIST_DIR, "index.html"), site.title, site.description, indexHtml);

for (const [category, items] of categories) {
  page(
    path.join(DIST_DIR, "categories", `${category}.html`),
    `分類：${categoryTitle(category)}`,
    `${items.length} 篇報告，分類為 ${categoryTitle(category)}`,
    `<section class="hero"><p class="eyebrow">分類</p><h1>${escapeHtml(categoryTitle(category))}</h1><p class="stat">${items.length} 篇報告</p></section>
    <section class="search-panel" aria-label="搜尋${escapeHtml(categoryTitle(category))}">
      <label for="report-search">搜尋${escapeHtml(categoryTitle(category))}</label>
      <input id="report-search" data-report-search type="search" placeholder="輸入關鍵字，點結果會跳到文章第一個命中位置" />
      <p>搜尋會比對這個分類內的標題、摘要與文章內文。</p>
      <label class="hit-list-toggle"><input type="checkbox" data-list-toggle /> 逐條列出每個命中（同一篇多次提到會分列）</label>
    </section>
    <p class="empty" data-no-results hidden>找不到符合的報告，試試較短的公司名、股票代號、中文或英文關鍵字。</p>
    <div class="hit-list" data-hit-list hidden></div>
    ${reportList(items, path.join(DIST_DIR, "categories"))}`,
  );
}

for (const [tag, items] of tags) {
  page(
    path.join(DIST_DIR, "tags", `${slugify(tag)}.html`),
    `標籤：${tag}`,
    `${items.length} 篇報告，標籤為 ${tag}`,
    `<section class="hero"><p class="eyebrow">標籤</p><h1>#${escapeHtml(tag)}</h1><p class="stat">${items.length} 篇報告</p></section>${reportList(items, path.join(DIST_DIR, "tags"))}`,
  );
}

fs.writeFileSync(path.join(DIST_DIR, "reports.json"), JSON.stringify(reports, null, 2));
fs.copyFileSync(path.join(ROOT, "styles.css"), path.join(DIST_DIR, "styles.css"));
copyDir(ASSETS_DIR, path.join(DIST_DIR, "assets"));
if (fs.existsSync(path.join(ROOT, "CNAME"))) fs.copyFileSync(path.join(ROOT, "CNAME"), path.join(DIST_DIR, "CNAME"));
console.log(`Build complete: ${reports.length} report(s), ${categories.size} categor${categories.size === 1 ? "y" : "ies"}, ${tags.size} tag(s).`);
