# Stack: Chat → automation + files

## Goal

Let the assistant **trigger workflows** (e.g. n8n) and **read/write files** via WebDAV—glue between Open WebUI and the rest of your stack.

## Components (community examples)

| Role | Item | Source |
|------|------|--------|
| Tool | n8n_tools | [openwebui.com](https://openwebui.com/t/willyma/n8n_tools_5aefa68c) |
| Tool | WebDAV Toolset | [openwebui.com](https://openwebui.com/t/cdmsin/webdav_toolset_d61f1cbb) |

## How it fits together

1. Run **n8n** (or compatible) with sensible auth; point the tool at your instance.
2. Configure **WebDAV** to a bucket or NAS you are allowed to expose to the model.
3. Prefer **least privilege** credentials scoped to one path or workflow namespace.

## Trade-offs

- **Blast radius**: automation + file access can delete or exfiltrate data if prompts go wrong.
- **Maintenance**: two integrations to patch and monitor.

## Status

Illustrative stack from a [community search sample](../docs/openwebui-import.md).
