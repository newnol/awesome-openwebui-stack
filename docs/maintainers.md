# Maintainer checklist: GitHub repository settings

These are one-time GitHub settings (not files in the repo) that make the project
easier to discover and nicer to share on Discord, Slack, or X. Do these once in
the repository's **Settings** and **About** panel.

## About panel (top-right of the repo home)

- **Description** — keep it short. Suggested:
  > A curated showcase of finished Open WebUI stacks, tools, functions, and pipes.
- **Website** — leave blank for now (GitHub Pages is planned later).
- **Topics** — add these so the repo shows up in GitHub topic searches:
  - `open-webui`
  - `awesome`
  - `awesome-list`
  - `llm`
  - `self-hosted`
  - `rag`
  - `docker-compose`

## Social preview image (link previews on chat apps)

Settings → **General** → **Social preview** → **Edit** → upload an image.

- Recommended size: **1280×640** px (2:1). PNG or JPG, under 1 MB.
- Keep the repo name and one-line description readable at small sizes.
- Without this, shared links fall back to a plain GitHub avatar card.

## Website (GitHub Pages + Docsify)

The site is [Docsify](https://docsify.js.org/): it renders the existing markdown at
runtime, so there is **no build step**. The files live at the repo root
(`index.html`, `.nojekyll`, `_sidebar.md`).

To publish:

- Settings → **Pages** → **Build and deployment** → Source: **Deploy from a branch**.
- Branch: **`main`**, folder: **`/ (root)`** → **Save**.
- Wait a minute, then open `https://newnol.github.io/awesome-openwebui-stack/`.

Notes:

- `.nojekyll` is required so GitHub Pages serves files as-is (no Jekyll processing).
- Editing any `.md` file updates the site on the next push. No extra workflow needed.
- To preview locally: `npx docsify-cli serve .` (optional; needs Node).

## Quick verification

- Open the repo home in a private window: the description and topics render.
- Paste the repo URL into a chat app: the social preview card shows your image.
- Open the Pages URL: the sidebar loads and catalog/category links resolve.
