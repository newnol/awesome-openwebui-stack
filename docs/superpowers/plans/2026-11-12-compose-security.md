# Compose Security Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Harden the sample Compose and propose tested-by-upstream release versions.
**Architecture:** Keep service topology, named volumes and external Docker network; change configuration, guide and static checks only.
**Tech Stack:** Docker Compose, Node.js built-in tests, GitHub Actions.
**Spec:** docs/superpowers/specs/2026-11-12-compose-security-design.md

## Global Constraints

Never publish secrets, connect to production, or merge to main. Release metadata is not deployment verification.

## Review Focus

- Missing/blank .env secrets must make Compose configuration fail.
- Postgres must not be host-published; app ports must be loopback-only.
- Upgrade guide must require backups before schema migrations.
- External network trust boundary must be documented.
- Rolling image latest tags must be rejected for application services.

---

### Task 1 — Reference stack

**Files:** docker-compose.yml, .env.example, tests/compose.test.mjs

- [x] Add test assertions for ports, secrets and image references.
- [x] Require secrets, restrict ports, select explicit release versions and DB health-gate LiteLLM.
- [ ] Run node --test tests/compose.test.mjs and docker compose config --quiet (in CI).

### Task 2 — Guidance and validation

**Files:** stacks/openwebui-stack/README.md, .github/workflows/checks.yml

- [x] Document versions, backup/migration risks and access controls.
- [x] Validate Compose and static checks in CI.
- [ ] Review CI before merging.
