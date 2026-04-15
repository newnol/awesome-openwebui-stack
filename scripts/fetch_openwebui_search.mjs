#!/usr/bin/env node
/**
 * Download search results from the Open WebUI Community HTTP API (no browser needed).
 * Endpoint (observed from network traffic): GET https://api.openwebui.com/api/v1/posts/search
 *
 * Usage:
 *   node scripts/fetch_openwebui_search.mjs --query=tools --pages=2
 *
 * Output: JSON + NDJSON under scratch/community-raw/ (see .gitignore).
 */

import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const OUT_DIR = path.join(ROOT, "scratch", "community-raw");
const API = "https://api.openwebui.com/api/v1/posts/search";

function parseArgs(argv) {
  const out = {
    query: "tools",
    pages: 1,
    sort: "top",
    t: "all",
    types: null,
  };
  for (const a of argv) {
    if (a.startsWith("--query=")) out.query = a.slice("--query=".length);
    else if (a.startsWith("--pages=")) out.pages = Math.max(1, parseInt(a.slice("--pages=".length), 10) || 1);
    else if (a.startsWith("--sort=")) out.sort = a.slice("--sort=".length);
    else if (a.startsWith("--t=")) out.t = a.slice("--t=".length);
    else if (a.startsWith("--types=")) {
      const raw = a.slice("--types=".length).trim();
      out.types = raw ? new Set(raw.split(",").map((s) => s.trim().toLowerCase())) : null;
    }
  }
  return out;
}

function communityUrl(item) {
  const u = item.user?.username;
  const s = item.slug;
  if (!u || !s) return null;
  switch (item.type) {
    case "tool":
      return `https://openwebui.com/t/${u}/${s}`;
    case "function":
      return `https://openwebui.com/f/${u}/${s}`;
    case "model":
      return `https://openwebui.com/models/${u}/${item.data?.model?.id ?? s}`;
    default:
      return `https://openwebui.com/posts/${item.id}`;
  }
}

function normalizeItem(raw) {
  return {
    id: raw.id,
    type: raw.type ?? null,
    title: raw.title ?? null,
    slug: raw.slug ?? null,
    username: raw.user?.username ?? null,
    url: communityUrl(raw),
    upvotes: raw.upvotes ?? null,
    downloads: raw.downloads ?? null,
    views: raw.views ?? null,
    createdAt: raw.createdAt ?? null,
  };
}

async function fetchPage(args, page) {
  const q = new URLSearchParams({
    query: args.query,
    sort: args.sort,
    t: args.t,
    page: String(page),
  });
  const url = `${API}?${q.toString()}`;
  const res = await fetch(url, {
    headers: { Accept: "application/json", "User-Agent": "awesome-openwebui-tools-fetch/1.0" },
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`HTTP ${res.status} ${url}\n${text.slice(0, 500)}`);
  }
  return res.json();
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  console.error("Options:", args);

  await fs.mkdir(OUT_DIR, { recursive: true });
  const stamp = new Date().toISOString().replace(/[:.]/g, "-");
  const allItems = [];

  for (let page = 1; page <= args.pages; page++) {
    const data = await fetchPage(args, page);
    const items = (data.items || []).map(normalizeItem);
    const filtered = args.types
      ? items.filter((i) => i.type && args.types.has(String(i.type).toLowerCase()))
      : items;
    allItems.push(...filtered);
    console.error(`Page ${page}: ${items.length} raw → ${filtered.length} after type filter (total API total=${data.total ?? "?"})`);
  }

  const payload = {
    scrapedAt: new Date().toISOString(),
    api: API,
    args,
    count: allItems.length,
    items: allItems,
  };

  const base = `openwebui-api_${args.query}_${stamp}`;
  const jsonPath = path.join(OUT_DIR, `${base}.json`);
  await fs.writeFile(jsonPath, JSON.stringify(payload, null, 2), "utf8");

  const ndPath = path.join(OUT_DIR, `${base}.ndjson`);
  await fs.writeFile(
    ndPath,
    allItems.map((row) => JSON.stringify(row)).join("\n") + "\n",
    "utf8",
  );

  console.log(`Wrote ${allItems.length} items → ${path.relative(ROOT, jsonPath)}`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
