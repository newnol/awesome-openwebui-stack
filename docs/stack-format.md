# What is a stack in this repo?

A **stack** is a short showcase write-up under `stacks/<name>/README.md` for services used together. Include an **Author** section with a **GitHub** profile or organization link. Example: [openwebui-stack](../stacks/openwebui-stack/README.md).

Copy [template-full-stack/README.md](../stacks/template-full-stack/README.md), then trim sections that do not apply. Explain prerequisites, intended use, configuration, security caveats and what was actually tested. Reference infrastructure without deployment validation must be labeled as an example, not production-ready.

Optional `docker-compose.yml` and `.env.example` can live beside the README, or link to an external infrastructure repository. Never include real credentials.

Register the stack in [`data/catalog.json`](../data/catalog.json) with type `stack`, then run `node scripts/catalog.mjs`. This generates its entry in [catalog/stacks.md](../catalog/stacks.md) and the relevant categories. Do not hand-edit those indexes. See [submission guidelines](submission-guidelines.md).
