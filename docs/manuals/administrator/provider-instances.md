---
title: Provider Instances
description: Configure provider instances for runtime access.
sidebar_position: 4
---

# Provider Instances

Provider instances connect AtlasClaw Core to concrete provider packages loaded
from `providers_root`.

## Responsibilities {#responsibilities}

Administrators configure provider instance fields such as base URL, shared
provider token, credential mode, active state, and instance name. Concrete
fields come from the provider's `provider.schema.json`.

## Runtime Access {#runtime-access}

Provider runtime access is controlled separately from provider instance
configuration. A role may manage provider config records, manage provider
permissions, or be granted runtime access to specific provider instances.

This separation is intentional:

- Provider config permissions let an administrator create or edit instance
  records.
- Provider runtime permissions let a user or role execute skills against a
  specific provider instance.
- Provider-native credentials decide what the upstream system allows after the
  request leaves AtlasClaw.

All three layers must be correct for provider-backed chat operations.

## Instance Naming {#instance-naming}

Use stable, environment-oriented instance names such as `default`, `prod`,
`staging`, or a business-unit name. Avoid names that encode a secret, a user
name, or a temporary incident. Provider permissions and user credentials are
bound to provider type plus instance name, so renaming an instance should be
treated as an access migration.

## Configuration Flow {#configuration-flow}

1. Confirm the provider package is present under `providers_root`.
2. Check the provider definition and schema are visible in the provider catalog.
3. Create a provider instance with the fields required by that schema.
4. Assign provider runtime access to the roles that should use it.
5. Enable the corresponding skills for those roles.
6. If the provider uses user-scoped credentials, ask users to configure their
   Provider Tokens.
7. Test a read-only provider skill before enabling write or approval workflows.

## Provider-Specific Setup {#provider-specific-setup}

Provider-specific setup is documented under Provider Integration. Use that
section for concrete auth modes, user token setup, provider schemas, and
capability workflows.
