# Submission guidelines

Submit finished tools, functions, pipes, integrations or reference stacks that readers can inspect and adopt. Tutorials on authoring new extensions belong in upstream repositories or the official Open WebUI documentation.

## Entry format

The canonical listing is an object in [`data/catalog.json`](../data/catalog.json), validated against [`data/catalog.schema.json`](../data/catalog.schema.json). Copy an existing object rather than copying a generated Markdown section.

| Field | What to provide |
| --- | --- |
| `id`, `name` | Stable kebab-case identifier and unique human-readable name. |
| `type` | `tool`, `function`, `pipe`, `stack` or `integration`. |
| `categories` | One or more categories from the schema. |
| `summary` | A brief, factual description of the user-facing outcome. |
| `source`, `guide` | HTTPS URLs to the original source and usable setup instructions. |
| `status` | `documented`, `example` or `unavailable`; see review criteria. |
| `reviewed`, `evidence`, `review_note` | Actual source-inspection date, evidence URL and scope of the inspection. |
| `compatibility` | Known versions and their evidence, or an explicit statement that no runtime test was performed. |
| `requirements` | Non-empty list of prerequisites: services, permissions, model features or dependencies. |
| `risk` | Permissions, code execution, egress, data handling or credential caveats. |
| `license` | Verified upstream license/terms, or clearly state that the reader must check upstream. |

Dates use `YYYY-MM-DD` and cannot be in the future. URLs must use HTTPS and contain no credentials. IDs and names must be unique; multiple components can legitimately share a source repository.

## Evidence levels

`documented` means an implementation or setup documentation was inspected. It is not a certification, runtime-test badge or maintenance guarantee. `example` is for reference infrastructure without deployment validation. `unavailable` is reserved for existing historical listings whose implementation cannot be found; it is not a way to submit new placeholders.

## Generate and check

```bash
node scripts/catalog.mjs
node --test tests/catalog.test.mjs
node scripts/catalog.mjs --check
```

Commit metadata and generated pages together. For stack write-ups, also follow [stack format](stack-format.md). See the [maintenance guide](catalog-maintenance.md) for full schema and browser tests.

## No-code submissions

The [catalog issue form](https://github.com/newnol/awesome-openwebui-stack/issues/new?template=catalog-entry.yml) collects the same information without requiring a Git checkout. Maintainers review and convert submissions; opening an issue does not automatically publish an entry.
