# Start here

**[Browse the explorer](https://newnol.github.io/awesome-openwebui-stack/)** | **[Markdown catalog](catalog/README.md)** | **[Hướng dẫn tiếng Việt](START-HERE.vi.md)**

You do not need to clone this repository to discover an add-on. Choose a goal, inspect requirements and evidence, then follow the linked project's instructions. This is a directory, not an installer.

## Choose your goal

| I want to... | Read first |
| --- | --- |
| Analyze a spreadsheet | [SheetProof](catalog/tools.md#sheetproof) and its optional [Router](catalog/functions.md#sheetproof-router) |
| Connect a local model | [Ollama](catalog/integrations.md#ollama) |
| Connect several model providers | [LiteLLM](catalog/integrations.md#litellm) |
| Add web search | [SearXNG](catalog/integrations.md#searxng) |
| Let a model run commands | [Open Terminal](catalog/integrations.md#open-terminal); review its security boundary first |
| See services used together | [Open WebUI reference stack](stacks/openwebui-stack/README.md); an example, not a production distribution |

## Use the explorer

Search in your own words, or choose a goal shortcut. Combine **artifact type**, **use case** and **evidence** filters. Select up to three **Compare** checkboxes to inspect requirements and risks side by side. **Copy view link** preserves filters and the comparison for someone else; browser Back restores filter changes. Press `/` to focus search.

No result? Clear a filter. Historical entries with missing implementations are excluded by default. Enable **Include unavailable implementations** only to inspect those records, not to install them.

## Understand the artifact types

| Type | Meaning |
| --- | --- |
| Tool | A capability the model can call, such as analyzing an uploaded spreadsheet. |
| Function | Server-side behavior, such as a filter or action. |
| Pipe | A custom model-like endpoint or routing pipeline; an Open WebUI function subtype, listed separately for discovery. |
| Integration | An external service connected through settings, an API or a tool. |
| Stack | Several services documented as one setup. |

## Check evidence before installing

**Source documented:** source or setup documentation was inspected. This does not prove compatibility, security or end-to-end functionality.

**Example / not runtime-tested:** a reference setup exists, but this directory has not validated a deployment.

**Implementation unavailable:** the linked source does not currently provide the advertised implementation. Preserved for transparency, not recommended.

A source-review date is not a release date or runtime-test date. See [review criteria](docs/review-criteria.md).

## Try safely, one change at a time

1. Read the upstream license, installation guide and compatibility notes. Note your Open WebUI and extension versions.
2. Use a non-production instance with non-sensitive test data and restricted credentials. Review code and permissions, especially for server-side Python, browsers or shell execution.
3. Install using the upstream instructions, run its sample scenario, and record expected versus actual results. Remove the add-on and revoke test credentials when finished.

The [official plugin documentation](https://docs.openwebui.com/features/extensibility/plugin/) explains extension concepts. Report outdated listings through [contributing](CONTRIBUTING.md); report implementation defects to the upstream project.
