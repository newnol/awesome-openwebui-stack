# Agent Ecosystem Catalog Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a verified-source, carefully scoped coding agent discovery entry and guide.
**Architecture:** Canonical JSON entry drives generated Markdown; editorial guide and navigation remain hand-maintained.
**Tech Stack:** JSON catalog, Node generator, static Markdown, GitHub Actions.
**Spec:** docs/superpowers/specs/2026-11-12-agent-ecosystem-design.md

## Global Constraints

One catalog entry per integration, not one per supported CLI; no runtime-test claims, permission bypass or automatic deployment.

## Review Focus

- Accurate status: source-documented only, never runtime-tested.
- Safe URLs: source, guide, evidence must be HTTPS and attributable to upstream.
- Generated pages: catalog.mjs --check should report zero stale files.
- Agent image variants: stock terminal image may not include installed CLIs.
- Trust boundary: terminal credentials, command execution and multi-user limits must be explicit.

---

### Task 1 — Catalog entry and generated pages

**Files:** data/catalog.json, catalog/integrations.md, catalog/README.md, categories/*.md

- [x] Add one canonical metadata entry with source, compatibility and risk evidence.
- [x] Regenerate only affected category, integration and directory indexes.
- [ ] Run node --test tests/catalog.test.mjs and node scripts/catalog.mjs --check in CI.

### Task 2 — Documentation and navigation

**Files:** docs/open-terminal-agents.md, README.md, README.vi.md, START-HERE.md, _sidebar.md, docs/README.md

- [x] Explain version requirements, CLI login, terminal connection, Tether and agent automations.
- [x] Add appropriate reader navigation.
- [ ] Review link/Markdown/browser CI before merge.
