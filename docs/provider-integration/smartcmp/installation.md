---
title: Installation
description: Install and load SmartCMP Provider.
sidebar_position: 2
---

# Installation

## Add Provider Package {#add-provider-package}

Place `SmartCMP-Provider` under the configured provider root:

```text
atlasclaw-providers/providers/SmartCMP-Provider/
```

Configure Core:

```json
{
  "providers_root": "../atlasclaw-providers/providers"
}
```

Restart AtlasClaw Core after changing provider packages.

## Verify Loading {#verify-loading}

After startup, check that SmartCMP appears in available provider definitions and
that SmartCMP skills are visible to roles with provider access.

## Expected Package Files {#expected-package-files}

The provider package should include:

| File or directory | Purpose |
| --- | --- |
| `PROVIDER.md` | Provider identity, capability context, and LLM-facing guidance. |
| `provider.schema.json` | Config schema for provider instance and user credential fields. |
| `README.md` | Provider source-of-truth setup and skill operation notes. |
| `pyproject.toml` | Installable `smartcmp-provider` distribution metadata. |
| `src/smartcmp_provider/` | Shared authentication, models, transport, domain operations, and services. |
| `assistant_context/` | Optional embedded-page route manifest and explicit Context resolver callable. |
| `skills/` | Thin AtlasClaw Skill adapters and SmartCMP-specific Object Action presentation helpers. |
| `assets/` | Optional provider icon and catalog assets. |

## Post-Install Checks {#post-install-checks}

1. Restart AtlasClaw Core.
2. Open provider definitions and confirm provider type `smartcmp` is present.
3. Confirm the config form shows `base_url` and the auth-mode-specific fields.
4. Create a provider instance.
5. Grant provider runtime access to a test role.
6. Enable one read-only SmartCMP skill and test discovery before enabling write
   operations.

If a provider package is updated, restart Core and re-check the provider schema
before changing production role access.
