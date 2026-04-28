---
title: Agents
description: Agent definitions, metadata, and runtime configuration.
sidebar_position: 4
---

# Agents

An AtlasClaw agent combines identity, system instructions, interaction style,
allowed capabilities, and memory behavior.

## File-Based Definitions {#file-based-definitions}

Agent files live under `.atlasclaw/agents/<agent_id>/`:

- `SOUL.md`: system prompt, capabilities, allowed providers, allowed skills.
- `IDENTITY.md`: display name, avatar, and tone.
- `USER.md`: personalization and interaction style.
- `MEMORY.md`: memory strategy and max context rounds.

## Runtime Metadata {#runtime-metadata}

`/api/agent/info` reads the main agent definition and returns display metadata
for the chat UI, including name, description, welcome message, and parsed soul
data.

The UI-facing identity should be stable enough for users to recognize the
agent. Runtime instructions should be precise enough for tool use, permission
handling, and refusal behavior. Avoid mixing provider-specific playbooks into a
general Core agent file unless the deployment intentionally ships a provider
specialized agent.

## Database Agent Configs {#database-agent-configs}

The `agent-configs` APIs create, list, update, and delete database-backed agent
records. In the current runtime, the startup path can load a database-backed
configuration for the `main` agent and then falls back to file-based
definitions. Additional agent IDs are still defined through
`.atlasclaw/agents/<agent_id>/` files.

Use `agent-configs` for the supported database-backed main-agent workflow. Do
not assume it is a complete frontend Agent Template catalog unless your
deployment has explicitly wired that behavior.

## Configuration Sources {#configuration-sources}

| Source | Best use |
| --- | --- |
| File-based agent files | Stable default agents, source-controlled deployment configuration. |
| Database agent configs | API-managed main-agent records in deployments that use the DB-backed path. |
| User settings | Personalization that should not change the global agent identity. |

When both file and database definitions exist, document which one your
deployment uses as the authoritative path. Do not let operators edit one source
while the runtime reads another.

## Agent Design Checklist {#agent-design-checklist}

- Name and display name are clear to end users.
- Tone and interaction style match the operational environment.
- System prompt explains permission boundaries and credential handling.
- Allowed providers and skills match role policy.
- Memory strategy is appropriate for the amount of context users expect.
- Write operations require explicit user intent.
