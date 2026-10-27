# Catalog maintenance

## Design

```text
 data/catalog.json
       |-- assets/catalog.mjs --> assets/app.mjs --> index.html
       |-- scripts/catalog.mjs --> catalog/*.md + categories/*.md
       `-- data/catalog.schema.json + tests --> GitHub Actions
```

`catalog/learning-resources.md` and stack write-ups remain editorial. All artifact/category listing pages are generated. The explorer uses native ES modules, local CSS and a static JSON file, with no runtime package manager, API keys, backend, tracker or remote font requirement. Rendering uses DOM text nodes, not HTML from catalog data.

`assets/catalog.mjs` owns pure filtering, query-state parsing, URL safety and data validation. `assets/app.mjs` owns browser interactions. `scripts/catalog.mjs` owns Markdown generation. Keep these responsibilities separate.

## Local workflow

Use Node 22+ and Python 3.11+.

```bash
node --test tests/catalog.test.mjs
node scripts/catalog.mjs
node scripts/catalog.mjs --check
python3 -m pip install -r requirements-dev.txt
python3 scripts/check_schema.py
python3 -m playwright install chromium
python3 -m unittest discover -s tests -p 'browser_test.py' -v
python3 -m http.server 8000
```

Browser tests use a temporary local HTTP server and save screenshots under `test-results/`. To use an already installed Chromium, set `CHROMIUM_EXECUTABLE` to its executable path. Do not commit test screenshots, caches or virtual environments. Python packages are development-only; users browsing the site do not install them.

## Publishing

The site remains compatible with GitHub Pages **Deploy from a branch**, `main`, `/ (root)`, with the existing `.nojekyll` file. No framework build or Pages-source change is required. If Pages is not enabled, a repository administrator must select that source under Settings > Pages. This change does not alter repository administration settings.

`index.html` is the explorer. `guide.html` is the existing Docsify viewer moved to a separate entry point. Old `/#/...` bookmarks redirect to `guide.html#/...`; existing Markdown files and links remain available. Docsify continues using CDN-hosted dependencies; the explorer does not.

## CI

The checks workflow validates metadata, JSON Schema, generated indexes and JavaScript unit tests, runs browser regressions, checks Markdown and checks external links. Browser screenshots and a static-site preview are uploaded as review artifacts. External link availability is not an installation test.

Browser coverage includes combined filters, unavailable-entry opt-in, empty state, three-item comparison, shared URL state, history navigation, keyboard focus, project-subdirectory hosting, mobile overflow, dark theme, failed-data and JavaScript-disabled fallbacks, blocked local storage, unsafe text rendering and legacy guide redirects.

## Adding an entry

Edit `data/catalog.json`, follow [submission guidelines](submission-guidelines.md), regenerate pages and commit both. Never invent release versions or testing results. Review historical unavailable entries when their upstream authors publish implementations.

## Rollback

Revert the discovery upgrade commit to restore the previous Docsify homepage and hand-maintained catalogs. No database or server migration is involved. Do not delete user-contributed entries while reverting unrelated UI changes.
