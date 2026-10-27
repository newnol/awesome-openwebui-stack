# Contributing

Help someone find a working Open WebUI add-on, not just another link.

## Suggest without editing code

Use the [catalog submission form](https://github.com/newnol/awesome-openwebui-stack/issues/new?template=catalog-entry.yml). Include the source, setup instructions, use case, prerequisites, license and what you actually verified. Maintainers will normalize the metadata. Existing artifact-specific issue forms are still accepted.

For broken or misleading entries, use the [report form](https://github.com/newnol/awesome-openwebui-stack/issues/new?template=broken-link.yml). Never post API keys, private files or personal data.

## Submit a pull request

1. Read the [submission guidelines](docs/submission-guidelines.md) and [review criteria](docs/review-criteria.md).
2. Edit **`data/catalog.json`**, not generated files in `catalog/` or `categories/`. Copy an existing entry and follow [`data/catalog.schema.json`](data/catalog.schema.json).
3. Run `node scripts/catalog.mjs`, `node --test tests/catalog.test.mjs`, and `node scripts/catalog.mjs --check` with Node 22+.
4. Commit both metadata and generated pages. Explain the source evidence and any testing limits in your PR.

New stack write-ups additionally belong in `stacks/<name>/README.md`, including an author link, based on the [stack template](stacks/template-full-stack/README.md). Do not commit secrets or large implementation codebases. Learning-resource links remain editorial in `catalog/learning-resources.md`.

## Principles

Use English for catalog-facing metadata; translations of user guides are welcome. Link to the original implementation and installation instructions. Distinguish upstream claims from independent runtime tests. Do not label a project safe, tested or stable without supporting evidence. New entries must offer an actual implementation or documented integration, not a placeholder.

The website and Markdown indexes share one metadata source. Design and test instructions are in the [maintenance guide](docs/catalog-maintenance.md). By contributing you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).
