# Maintainer checklist: repository settings

These are optional, one-time settings managed by a repository administrator. Changing catalog files does not change GitHub administration settings.

## About panel

Suggested description: A community directory of Open WebUI tools, functions, pipes, integrations and reference stacks.

After verifying that Pages is published, set Website to `https://newnol.github.io/awesome-openwebui-stack/`. Useful topics include `open-webui`, `awesome`, `awesome-list`, `llm`, `self-hosted`, `rag` and `docker-compose`.

## Website

`index.html` is the static catalog explorer. `guide.html` provides the Docsify guide viewer; old `/#/...` routes redirect there. Both work from the repository root without a framework build. Keep `.nojekyll` committed.

For branch-based publishing, select Settings > Pages > Deploy from a branch, branch `main`, folder `/ (root)`. Do not switch an already working deployment source unnecessarily. Check the deployment result before advertising the public URL.

Listing changes belong in `data/catalog.json`. Run `node scripts/catalog.mjs` and commit the generated Markdown pages. Do not edit generated artifact/category indexes by hand. Preview using `python3 -m http.server 8000`.

See [catalog maintenance](catalog-maintenance.md) for the architecture, tests, deployment artifacts and rollback procedure.

## Quick verification

- Open the homepage, search, filter and compare entries on desktop and mobile.
- Open the Start here guide, Vietnamese guide and an old catalog bookmark.
- Confirm the About website URL matches the deployed site and the GitHub Actions checks passed.
- Verify any social-preview image in a real link preview before promoting it.
