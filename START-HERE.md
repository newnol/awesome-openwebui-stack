# Start here: find the right Open WebUI add-on

New to Open WebUI? This page helps you choose a **working project** before reading implementation details. This repository is a curated directory, **not** an app store or a bundled installation.

## Choose by what you want to do

| I want to... | Start with | Type | Before you try it |
|---|---|---|---|
| Summarize YouTube videos | [YouTube Transcript](catalog/tools.md#youtube-transcript) | Tool | Check upstream dependencies and transcript availability. |
| Extract YouTube metadata | [YouTube Info](catalog/tools.md#youtube-info) | Tool | May require a browser and Selenium. |
| Draw architecture diagrams | [Diagram Generator](catalog/tools.md#diagram-generator) | Tool | Graphviz may be required on the server. |
| Reduce manual tool selection | [Auto Tool Filter](catalog/tools.md#auto-tool-filter) | Tool/filter | Review model calls, permissions, and cost. |
| Analyze CSV / Excel without invented numbers | [SheetProof](catalog/tools.md#community-and-upstream-additions-welcome) + [SheetProof Router](catalog/functions.md#sheetproof-router) | Tool + function | Read the upstream setup and data-handling notes. |
| Route requests between models | [Auto Router Model](catalog/pipes.md#auto-router-model) | Pipe | Check supported providers and current configuration upstream. |
| Deploy an example environment | [Open WebUI stack](stacks/openwebui-stack/README.md) | Stack | Review secrets, exposed ports, and resource requirements first. |

These links lead to descriptions or project documentation. An entry being listed **does not** mean it is audited, officially endorsed, or compatible with every Open WebUI version.

## Understand the difference

| Type | What it changes | Read more |
|---|---|---|
| **Tool** | Adds a callable capability, such as fetching a transcript. | [Tools](catalog/tools.md) |
| **Function** | Adds server-side logic, such as an action or filter. | [Functions](catalog/functions.md) |
| **Pipe** | Exposes a custom model-like endpoint or routing pipeline. | [Pipes](catalog/pipes.md) |
| **Integration** | Connects an external service to an Open WebUI workflow. | [Integrations](catalog/integrations.md) |
| **Stack** | Describes multiple services used together. | [Stacks](catalog/stacks.md) |

## Four steps to try an entry

1. **Choose a use case** above or browse [categories](#browse-more).
2. **Open the source link** in its catalog entry. Verify the project's license, maintenance status, compatibility and installation instructions. The code generally lives **outside** this repository.
3. **Test safely:** start in a non-production Open WebUI instance; use restricted API keys and review permissions, network access and data sent to third parties. Be especially careful with code-execution and browser-automation add-ons.
4. **Record the result:** note the Open WebUI version, extension version, required configuration and any limitations. Share corrections through an [issue](https://github.com/newnol/awesome-openwebui-stack/issues) or [pull request](https://github.com/newnol/awesome-openwebui-stack/pulls).

## Browse more

**By goal:** [Coding](categories/coding.md) · [Research](categories/research.md) · [RAG](categories/rag.md) · [Automation](categories/automation.md) · [Productivity](categories/productivity.md) · [Multi-agent](categories/multi-agent.md) · [Self-hosting](categories/self-hosting.md) · [Security](categories/security.md)

**By artifact:** [Tools](catalog/tools.md) · [Functions](catalog/functions.md) · [Pipes](catalog/pipes.md) · [Stacks](catalog/stacks.md) · [Integrations](catalog/integrations.md)

## Want to contribute?

Found a working add-on that is missing? Check [submission guidelines](docs/submission-guidelines.md) and [review criteria](docs/review-criteria.md). Include a stable source URL, purpose, category, compatibility details when known, and honest maintenance status. You do **not** need to submit the tool's entire source tree here.

**Need installation help?** Follow the linked project's instructions and the [official Open WebUI documentation](https://docs.openwebui.com/). This directory cannot guarantee installation steps for third-party projects.
