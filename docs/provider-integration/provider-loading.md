---
title: Provider Loading
description: Load provider packages through providers_root.
sidebar_position: 2
---

# Provider Loading

AtlasClaw Core loads providers from `providers_root`.

## Package Layout {#package-layout}

A provider package normally contains:

```text
providers/<provider-name>/
├── PROVIDER.md
├── provider.schema.json
├── README.md
├── pyproject.toml              # when the Provider exposes an importable package
├── assets/
├── src/<provider_package>/     # reusable API, domain, model, and service code
├── assistant_context/          # optional page Context manifest and callable
└── skills/                     # AtlasClaw-facing adapters
    └── <skill>/
        ├── SKILL.md
        ├── scripts/
        └── references/
```

`src/` and `assistant_context/` are optional. A Provider with reusable domain
execution should keep that implementation in its importable package and keep
Skill handlers thin: translate AtlasClaw `RunContext` and Tool input, invoke a
typed Provider operation, then translate the result. Protocol-specific adapters
must not duplicate Provider authentication, API paths, or business rules.

## Discovery {#discovery}

At startup, Core scans `providers_root`, loads provider definitions, registers
provider instances, and loads provider skills. Skills are provider-qualified so
that names do not collide across integrations.

Provider discovery depends on readable provider metadata. A provider package
should include `PROVIDER.md` for LLM-facing provider context and
`provider.schema.json` for UI/API configuration fields.

## Callable Runtime {#callable-runtime}

Executable Skill metadata supports two entrypoint forms:

| Entrypoint | Runtime |
| --- | --- |
| `scripts/adapter.py:operation` | Core loads the named callable and executes it in process with AtlasClaw `RunContext`. |
| `scripts/legacy_command.py` | Compatibility path that starts the file as a subprocess and passes scoped runtime values through its environment. |

New Python Provider Tools should use an explicit `file.py:callable` entrypoint.
Several Tools in one Skill may name different callables from the same adapter
module. A page Context resolver must also use an explicit async callable such
as `assistant_context/resolve.py:resolve_context`; the resolver contract does
not support the legacy subprocess form.

## Callable Result Contract {#callable-result-contract}

A callable returns the public Tool result used as Agent evidence. It may also
include a bounded `_internal` value for trace-bound continuation metadata. Core
accepts a structured `_internal` value or a JSON-serialized one, hides it from
the user-visible result, and restores it only for the same request trace and
selected Provider instance.

Provider adapters should keep this metadata small. Retain only exact IDs,
Provider identity, validation tokens, or other facts required by the immediate
next step. Do not copy an entire public page of rows into `_internal`; oversized
metadata is omitted from workflow context and produces a structured budget
diagnostic. See [Skills and Tools](/core/skills-and-tools) for the Markdown Tool
flags that govern read-only single-candidate continuation.

## Configuration {#configuration}

Set `providers_root` in `atlasclaw.json` to the directory containing provider
folders:

```json
{
  "providers_root": "../atlasclaw-providers/providers"
}
```

## Loading Checklist {#loading-checklist}

1. `providers_root` points to the directory that contains provider folders.
2. The provider folder has a stable name and contains `PROVIDER.md`.
3. `provider.schema.json` is valid JSON.
4. Skill directories contain `SKILL.md` and every callable module or legacy
   script named by their entrypoints.
5. AtlasClaw Core has filesystem access to the provider root.
6. The service is restarted after adding or changing provider packages.

## Failure Modes {#failure-modes}

| Symptom | Likely cause |
| --- | --- |
| Provider catalog is empty | `providers_root` is wrong or unreadable. |
| Provider appears but no skills load | `skills/` layout or `SKILL.md` files are missing. |
| Config form lacks fields | `provider.schema.json` is missing or invalid. |
| Skill names collide | Skills are not properly provider-qualified. |

Provider code should not require Core to know provider-specific defaults. Put
those defaults in the provider manifest and schema.
