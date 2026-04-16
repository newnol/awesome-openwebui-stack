# Self-hosting

Running Open WebUI **on your own machines** or **your own cloud account**: updates, backups, GPU vs CPU, and networking.

## Principles (not prescriptions)

- Pin versions and track Open WebUI release notes.
- Separate **secrets** from catalog docs (optional **`.env.example`** next to a stack `README.md` is fine—never commit real secrets).
- Large production compose can live in your own infra repo; link it from the stack README.

## Related stack

- [Open WebUI stack](../stacks/openwebui-stack/) — host sizing, Docker Compose outline

## See also

- [Open WebUI documentation](https://docs.openwebui.com/)
- [catalog/learning-resources.md](../catalog/learning-resources.md)
