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
├── assets/
└── skills/
    └── <skill>/
        ├── SKILL.md
        ├── scripts/
        └── references/
```

## Discovery {#discovery}

At startup, Core scans `providers_root`, loads provider definitions, registers
provider instances, and loads provider skills. Skills are provider-qualified so
that names do not collide across integrations.

Provider discovery depends on readable provider metadata. A provider package
should include `PROVIDER.md` for LLM-facing provider context and
`provider.schema.json` for UI/API configuration fields.

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
4. Skill directories contain `SKILL.md` and any scripts they call.
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
