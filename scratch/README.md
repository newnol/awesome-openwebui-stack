# Scratch (local only)

This directory holds **machine-generated** imports from [Open WebUI Community](https://openwebui.com) and similar sources.

- **Raw dumps** go under `community-raw/`. That subtree is **gitignored** so large JSON/NDJSON files never enter git.
- Generate dumps with: `node scripts/fetch_openwebui_search.mjs` (see [docs/openwebui-import.md](../docs/openwebui-import.md)).
- After you scrape, **curate** entries manually (or with your own notes) and promote only reviewed items into `catalog/` via pull requests.

See [docs/openwebui-import.md](../docs/openwebui-import.md) for the scraper command and review workflow.
