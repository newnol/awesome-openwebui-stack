# Coding agents through Open Terminal

> Source review: **2026-11-12**. This is a guide to documented upstream capabilities, **not** an installation test, support guarantee, or security certification.

Open WebUI can connect to an [Open Terminal](https://github.com/open-webui/open-terminal) instance and show agent CLIs installed in that terminal. This is distinct from calling a normal LLM provider through LiteLLM or installing a third-party Open WebUI function.

## Versions and evidence

- [Open WebUI v0.13.3](https://github.com/open-webui/open-webui/releases/tag/v0.13.3) supports agent selection and scheduled agent automations. Open WebUI 0.13.0 introduced tabbed file/terminal/browser workspaces and multi-model sub-agents.
- [Open Terminal v0.17.0](https://github.com/open-webui/open-terminal/releases/tag/v0.17.0) documented agent adapters for Codex, Claude Code, Cursor, Grok, OpenCode, Cline, Gemini CLI and Pi. See the current [upstream README](https://github.com/open-webui/open-terminal) for exact CLI protocols.
- [Open Terminal v0.17.7](https://github.com/open-webui/open-terminal/releases/tag/v0.17.7) adds an optional startup directory and setup script.

These are upstream release observations, **not** proof that all three components work together in this repository's Compose example.

## 1. Choose a trusted terminal

The existing [reference Compose stack](../stacks/openwebui-stack/README.md) supplies a standard Open Terminal container; it does **not** necessarily include agent CLIs. For an agent-capable Docker image, upstream documents an `agents` flavor that bundles Codex and Claude Code. Its build workflow also publishes versioned `-agents` tags (for example `0.17.7-agents`); confirm the image tag exists before selecting it. Other CLIs must be installed and authenticated separately.

Do not enable host Docker socket mounts just to make coding agents work. Use a throwaway workspace and the narrowest mounts, credentials and network privileges needed.

## 2. Connect Open WebUI

1. Start Open Terminal and give it a strong `OPEN_TERMINAL_API_KEY`.
2. In Open WebUI, open **Settings → Admin → Integrations → Open Terminal** (labels may vary by version).
3. Add the terminal URL reachable from Open WebUI's server and its API key. For the reference Compose network, use `http://open-terminal:8000` rather than `localhost` inside the WebUI container.
4. Enable the connection and select the terminal inside the chat interface.

Follow the [official connection guide](https://docs.openwebui.com/features/open-terminal/setup/connecting/) if your UI version differs.

## 3. Install, authenticate, and discover an agent

Install an appropriate agent CLI inside the terminal's own user environment, then run its normal interactive sign-in there. Open WebUI does not log in to the CLI on your behalf. Provider CLI credentials remain in the terminal environment.

With an agent-capable connection, Open Terminal advertises installed agents via an authenticated `/agents` catalog. Supported adapters described upstream include **Codex, Claude Code, Cursor, Grok, OpenCode, Cline, Gemini CLI and Pi**. Each adapter depends on the native CLI protocol installed in that environment; check the upstream readme for current commands.

Start with a read-only prompt in a disposable repository, confirm tool approvals and observe the terminal/file changes before allowing writes. Test Stop, reconnect and follow-up behavior before using the agent for real work.

## 4. Automations and multi-model agents

Open WebUI 0.13.3 can attach coding agents to saved automations with a terminal and working folder; failed availability checks stop the scheduled run. This is a built-in Open WebUI feature and is **not** an extra third-party pipe. Open WebUI 0.13.0 also documents multi-model sub-agent selection; that feature is separate from Open Terminal's CLI agents.

For a hosted WebUI and a local machine, upstream documents using **Tether** to reach saved Open Terminal connections without exposing a public terminal address. Check the matching Open WebUI / Tether / Open Terminal versions and keep the terminal key private.

## Security and operational limits

- Agent CLIs can read files and execute commands as the terminal user. Existing provider approvals are not a substitute for container isolation or an independent per-tool policy.
- Keep the terminal and LiteLLM APIs off the public internet, use per-service credentials and do not pass admin keys to untrusted agents.
- Multi-user mode within one Open Terminal container is **not** a strong security boundary between untrusted users; consider per-user isolated terminals if needed.
- Back up Open WebUI's data before upgrading across database migrations. Never treat upgrading a Docker tag as a tested rollback mechanism.
- Record exact app/image/CLI versions, a test prompt, logs and expected versus observed behavior before claiming an integration is **runtime tested**.

Sources: [Open Terminal deployment and agents documentation](https://github.com/open-webui/open-terminal/blob/main/docs/deployment.md), [Open WebUI v0.13.0](https://github.com/open-webui/open-webui/releases/tag/v0.13.0), [Open WebUI v0.13.3](https://github.com/open-webui/open-webui/releases/tag/v0.13.3).
