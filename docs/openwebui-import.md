# Importing listings from openwebui.com

Community search is backed by a public JSON API (no browser required):

`https://api.openwebui.com/api/v1/posts/search`

This repository includes a small script that calls it and writes **local-only** files under `scratch/community-raw/` (gitignored).

## Prerequisites

- **Node.js 18+** (uses built-in `fetch`).

## Run

```bash
node scripts/fetch_openwebui_search.mjs --query=tools --pages=3
```

Options:

| Flag | Default | Meaning |
|------|---------|---------|
| `--query=` | `tools` | Search query |
| `--pages=` | `1` | How many API pages to fetch (`page=1`, `page=2`, …) |
| `--sort=` | `top` | Sort parameter (`top`, etc.) |
| `--t=` | `all` | Time filter (`all`, …) |
| `--types=` | *(none)* | Optional comma list to keep only those `type` values, e.g. `tool,function` |

Outputs in `scratch/community-raw/`:

- `openwebui-api_<query>_<timestamp>.json` — full payload + normalized items (`url`, `type`, `title`, …)
- `openwebui-api_<query>_<timestamp>.ndjson` — one JSON object per line for filtering / spreadsheets

## Security and terms

- **Do not** commit credentials. The API used here is the same one the website uses for public search; if access rules change, update the script.
- Respect [openwebui.com](https://openwebui.com) terms of service and avoid aggressive looping / high `pages` values.

## Review → catalog

1. Open the generated `.json` / `.ndjson` in `scratch/community-raw/`.
2. For each item you want to list publicly, add **Purpose**, **Best for**, **Status**, and notes to [catalog/tools.md](../catalog/tools.md), [catalog/functions.md](../catalog/functions.md), or [catalog/pipes.md](../catalog/pipes.md) per [submission-guidelines.md](submission-guidelines.md).
3. You can also group related items into **simple stacks** under [stacks/](../stacks/) (see `community-*.md` examples and [catalog/stacks.md](../catalog/stacks.md)).
4. Commit **only** catalog changes; keep raw dumps local.

## Optional rating fields

You can copy the NDJSON and add columns such as `rating` (1–5) or `verdict` (`include` / `skip` / `needs-check`) in a **separate** file still under `scratch/` before promoting entries to the catalog.
