# FAQ

## What is the difference between catalog and categories?

- **Catalog** (`catalog/`) groups by **artifact type**: tools, functions, pipes, etc.
- **Categories** (`categories/`) groups by **goal**: coding, RAG, research, and so on.

Use both: some readers know they need a “tool”; others only know they want “better RAG.”

## What is a “stack” here?

An opinionated **combination** of models, tools, functions, pipes, and sometimes infra patterns to meet a goal (for example “research agent” or “low-cost local”). Stacks live under [stacks/](../stacks/) and are indexed from [catalog/stacks.md](../catalog/stacks.md).

## Does this repo ship production deployments?

No. This repo is for **curation and discovery**. Deployment-heavy content belongs in a dedicated infra or “stack” repository; we link out to it.

## Can I submit my project?

Yes. Read [submission-guidelines.md](submission-guidelines.md) and open an issue or PR. We need a clear purpose, Open WebUI relevance, and a stable link.

## Where is official Open WebUI documentation?

Start with [Open WebUI documentation](https://docs.openwebui.com/). This catalog is independent and may link there frequently.

## What about the Vietnamese notes in some files?

Legacy developer notes may remain bilingual or non-English in deep technical paths. The **curated catalog** (README, `catalog/`, `categories/`, `stacks/`, contributor docs) is English-first.
