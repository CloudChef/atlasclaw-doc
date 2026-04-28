---
title: Agent Customization
description: Customize AtlasClaw agent identity, style, behavior, and memory.
sidebar_position: 6
---

# Agent Customization

AtlasClaw supports file-based agent definitions and database-backed agent
configuration records. The current frontend does not expose a complete Agent
Template editor. In the current runtime, database-backed configuration is used
for the supported `main` agent path when available, while additional agent IDs
remain file-based under `.atlasclaw/agents/<agent_id>/`.

Use files for complete multi-agent customization. Use the `agent-configs` API
when your deployment intentionally manages the supported database-backed
main-agent record.

## File-Based Configuration {#file-based-configuration}

The main agent is defined under:

```text
.atlasclaw/agents/main/
├── SOUL.md
├── IDENTITY.md
├── USER.md
└── MEMORY.md
```

Use `.atlasclaw/agents/<agent_id>/` for additional agent definitions.

## Supported Fields {#supported-fields}

| File | Fields |
| --- | --- |
| `SOUL.md` | `name`, `system_prompt`, `capabilities`, `allowed_providers`, `allowed_skills` |
| `IDENTITY.md` | `display_name`, `avatar`, `tone` |
| `USER.md` | `interaction_style` |
| `MEMORY.md` | `memory_strategy`, `max_context_rounds` |

## Name and Branding Surfaces {#name-and-branding-surfaces}

- Product name: AtlasClaw UI copy and documentation branding.
- Agent ID: stable runtime identifier such as `main`.
- Agent name: used by `/api/agent/info` and chat welcome metadata.
- Display name: human-readable agent identity.
- Tone and style: guidance that shapes response style.

Changing product branding is different from changing an agent's display name.
If you need to rename the product surface itself, track it as a UI/configuration
change, not only an agent definition edit.

## Example Agent Definition {#example-agent-definition}

`IDENTITY.md`:

```md
---
name: AtlasClaw Operations Agent
---

# Identity

**Display Name**: AtlasClaw Ops

**Avatar**: AC

**Tone**: concise, operational, and security-aware
```

`SOUL.md`:

```md
---
name: AtlasClaw Ops
description: Enterprise operations agent for governed workflows.
---

## System Prompt

You are an enterprise operations assistant. Follow user permissions and use
provider tools only when they are authorized and relevant.

## Capabilities

- Answer operational questions
- Use approved provider skills
- Explain permission or credential blockers

## Available Providers

- example_provider

## Available Skills

- example_provider:request
- example_provider:approval
```

## API-Based Configuration {#api-based-configuration}

The `agent-configs` APIs create, list, update, and delete database-backed agent
records. Treat them as an API workflow for supported DB-backed agent records,
not as proof that every agent template in the UI or every additional agent ID is
loaded from the database.
