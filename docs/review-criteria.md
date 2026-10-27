# Review criteria

An entry helps a reader decide whether to investigate a project. It does not certify the project as secure, maintained or compatible with every version of Open WebUI.

## Evidence before enthusiasm

| Status | Minimum evidence | What it does not mean |
| --- | --- | --- |
| `documented` | The source or usable setup documentation exists and was inspected. | Runtime-tested, security-audited, officially endorsed or actively maintained. |
| `example` | Reference infrastructure and configuration are available. | Production-ready or deployment-tested. |
| `unavailable` | An existing listing's linked implementation cannot currently be found. | An installation recommendation. |

The `reviewed` date records source inspection only. `review_note` explains what was checked and `evidence` links to it. Prefer immutable references when recording a missing implementation. Do not silently turn an upstream claim into a verified fact.

## Review checklist

- Verify that the source and setup guide actually contain the advertised artifact, not just a repository name or placeholder README.
- Confirm the artifact type and its Open WebUI connection point. Pipes are listed separately for discovery even though they are a function subtype.
- Record requirements, known version limits, license evidence and data-handling risks. State when runtime testing has not been performed.
- Review duplicates by name and purpose. Separate components of the same project may share a repository URL.
- Run data/schema validation, generated-page checks and tests. A working hyperlink alone is not evidence that an integration works.

## Missing or stale implementations

Do not delete history merely to make the list look healthy. Mark an existing entry `unavailable`, explain the source inspection and retain its stable ID. The explorer hides these entries by default; Markdown pages show the warning explicitly. Restore `documented` only after inspecting a real implementation and setup instructions.

There is currently no runtime-tested badge. A future testing program should record exact Open WebUI and extension versions, the test scenario, observed results and a reproducible evidence link before introducing one.

## Safety

Tools and functions may execute code on the server; command-execution integrations can act on files and networks. See the [official filter security warning](https://docs.openwebui.com/features/extensibility/plugin/functions/filter/) and [Open Terminal security guide](https://docs.openwebui.com/features/open-terminal/advanced/security/). Listing an item does not replace code review, isolation, credential scoping or an organization's approval process.
