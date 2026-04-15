# Stack: Privacy-first

## Goal

Keep **prompts, documents, and logs** under **your control** by design—not as an afterthought.

## Typical use cases

- Regulated or sensitive industries
- Personal use where cloud API routing is unacceptable
- Air-gapped or offline networks

## Recommended components (pattern)

| Concern | Approach |
|---------|----------|
| Model hosting | Local inference or self-hosted inference gateway |
| Data path | Avoid sending raw documents to third parties unless contractually allowed |
| Tooling | Prefer tools that run on your network; audit external API calls |
| Auth | SSO, reverse proxy, network segmentation ([self-hosting](../categories/self-hosting.md)) |

## Trade-offs

- **Capability:** local models may lag cloud APIs for some tasks.
- **Ops burden:** you own patching, backups, and monitoring.

## Where to find code or deploy guidance

- This repo does **not** ship production compose files; link your infra repo from contributions.
- [Open WebUI documentation](https://docs.openwebui.com/) for deployment options.
- [categories/security.md](../categories/security.md) for review mindset.
