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
  description: "Jeff / FoodChain stock and industry research archive",
  baseUrl: process.env.SITE_BASE_URL || "",
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
  if (Array.isArray(tags)) return tags.map(String);
  return String(tags).split(",").map((x) => x.trim()).filter(Boolean);
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

ensureDir(DIST_DIR);
ensureDir(REPORTS_DIR);

const baseTemplate = readTemplate("base");
const reportTemplate = readTemplate("report");
const indexTemplate = readTemplate("index");
const reports = [];

for (const file of walkMarkdown(REPORTS_DIR)) {
  const raw = fs.readFileSync(file, "utf8");
  const { attributes, body } = fm(raw);
  const rel = path.relative(REPORTS_DIR, file);
  const category = attributes.category || path.dirname(rel).split(path.sep)[0] || "uncategorized";
  const slug = attributes.slug || slugifyFile(file);
  const outDir = path.join(DIST_DIR, "reports", category);
  const outPath = path.join(outDir, `${slug}.html`);
  ensureDir(outDir);

  const title = attributes.title || slug;
  const tags = normalizeTags(attributes.tags);
  const content = md.render(body);
  const url = `reports/${encodeURIComponent(category)}/${encodeURIComponent(slug)}.html`;
  const meta = {
    title,
    category,
    date: attributes.date || "",
    dateText: formatDate(attributes.date),
    tags,
    hackmd_url: attributes.hackmd_url || "",
    sourcePath: toPosix(path.relative(ROOT, file)),
    url,
    excerpt: attributes.description || excerpt(body),
  };
  reports.push(meta);

  const reportHtml = renderTemplate(reportTemplate, {
    title: escapeHtml(title),
    date: escapeHtml(meta.dateText),
    category: escapeHtml(category),
    tags: tags.map((t) => `<span class="tag">${escapeHtml(t)}</span>`).join(""),
    hackmd: meta.hackmd_url ? `<a href="${escapeHtml(meta.hackmd_url)}" target="_blank" rel="noopener">HackMD</a>` : "",
    sourcePath: escapeHtml(meta.sourcePath),
    content,
  });

  const finalHtml = renderTemplate(baseTemplate, {
    title: `${escapeHtml(title)} | ${site.title}`,
    description: escapeHtml(meta.excerpt),
    base: "../..",
    content: reportHtml,
  });
  fs.writeFileSync(outPath, finalHtml);
  console.log(`Built ${toPosix(path.relative(ROOT, outPath))}`);
}

reports.sort((a, b) => new Date(b.date || 0) - new Date(a.date || 0));
const grouped = Map.groupBy ? Map.groupBy(reports, (r) => r.category) : reports.reduce((m, r) => (m.get(r.category)?.push(r) || m.set(r.category, [r]), m), new Map());

let listHtml = "";
for (const [category, items] of [...grouped.entries()].sort(([a], [b]) => a.localeCompare(b))) {
  listHtml += `<section class="category"><h2>${escapeHtml(category)}</h2><div class="cards">`;
  for (const report of items) {
    listHtml += `<article class="card">
      <a class="card-title" href="${report.url}">${escapeHtml(report.title)}</a>
      <div class="card-meta">${escapeHtml(report.dateText)} · ${escapeHtml(report.sourcePath)}</div>
      <p>${escapeHtml(report.excerpt)}</p>
      <div class="tags">${report.tags.map((t) => `<span class="tag">${escapeHtml(t)}</span>`).join("")}</div>
    </article>`;
  }
  listHtml += `</div></section>`;
}

const indexHtml = renderTemplate(baseTemplate, {
  title: site.title,
  description: site.description,
  base: ".",
  content: renderTemplate(indexTemplate, {
    reports: listHtml || `<p class="empty">No reports yet. Add Markdown files under <code>reports/</code>.</p>`,
    count: String(reports.length),
  }),
});
fs.writeFileSync(path.join(DIST_DIR, "index.html"), indexHtml);
fs.writeFileSync(path.join(DIST_DIR, "reports.json"), JSON.stringify(reports, null, 2));
fs.copyFileSync(path.join(ROOT, "styles.css"), path.join(DIST_DIR, "styles.css"));
copyDir(ASSETS_DIR, path.join(DIST_DIR, "assets"));
console.log(`Build complete: ${reports.length} report(s).`);
