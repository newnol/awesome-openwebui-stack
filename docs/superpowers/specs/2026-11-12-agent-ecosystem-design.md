# Agent Ecosystem Catalog Refresh — Design (2026-11-12)

**Goal:** Help users discover and safely evaluate Open WebUI integrations with coding agent CLIs.

**Chosen approach:** Add one source-documented Open Terminal Coding Agents integration in canonical catalog.json, regenerate only the affected Markdown indexes, and link to a security-aware guide from the English/Vietnamese landing pages, start guide and sidebar.

**Alternatives considered:** List every supported CLI as a separate independently tested integration (not justified by available evidence), or change the reference stack to install agent CLIs by default (expands attack surface). Neither is selected.

**Constraints:** Keep catalog generation deterministic, do not claim deployment testing or security guarantees, preserve unavailable historical listings, do not modify Compose or production state, do not merge to main.
