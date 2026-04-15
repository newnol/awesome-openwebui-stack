# Stack: Chat → automation + files

## Goal

Let the assistant **trigger workflows** (e.g. n8n) and **read/write files** via WebDAV—glue between Open WebUI and the rest of your stack.

## Components (community examples)

| Role | Item | Source |
|------|------|--------|
| Tool | n8n_tools | [openwebui.com](https://openwebui.com/posts/5aefa68c-d630-4399-a211-d28dcff7df03) |
| Tool | WebDAV Toolset | [openwebui.com](https://openwebui.com/posts/d61f1cbb-8ee8-4c71-b158-2f755a6584ed) |

## How it fits together

1. Run **n8n** (or compatible) with sensible auth; point the tool at your instance.
2. Configure **WebDAV** to a bucket or NAS you are allowed to expose to the model.
3. Prefer **least privilege** credentials scoped to one path or workflow namespace.

## Trade-offs

- **Blast radius**: automation + file access can delete or exfiltrate data if prompts go wrong.
- **Maintenance**: two integrations to patch and monitor.

## Status

Illustrative stack from a [community search sample](../docs/openwebui-import.md).
