---
title: Permissions Reference
description: Role permission modules and default role behavior.
sidebar_position: 3
---

# Permissions Reference

## Permission Modules {#permission-modules}

| Module | Common permissions |
| --- | --- |
| `users` | `view`, `create`, `edit`, `delete`, `assign_roles`, `manage_permissions` |
| `roles` | `view`, `create`, `edit`, `delete`, `manage_permissions` |
| `channels` | `view`, `create`, `edit`, `delete`, `manage_permissions` |
| `tokens` | `view`, `create`, `edit`, `delete`, `manage_permissions` |
| `agent_configs` | `view`, `create`, `edit`, `delete`, `manage_permissions` |
| `provider_configs` | `view`, `create`, `edit`, `delete`, `manage_permissions` |
| `model_configs` | `view`, `create`, `edit`, `delete`, `manage_permissions` |
| `skills` | `view`, `enable_disable`, `manage_permissions`, `skill_permissions` |
| `providers` | `manage_permissions`, `provider_permissions` |

## Built-In Defaults {#built-in-defaults}

- `admin`: all management permissions.
- `user`: skill view plus own channel view/create/edit/delete by default.
- `viewer`: read-only audit-oriented permissions.

Administrators may create custom roles for narrower operations.

## Module Permission Details {#module-permission-details}

| Module | Notes |
| --- | --- |
| `users` | `assign_roles` is separate from editing user profile fields. |
| `roles` | Built-in role metadata is read-only. Custom role identifiers cannot be changed after creation. |
| `channels` | Default Standard User can manage own channel connections. |
| `tokens` | Administrative model token configuration, not user-owned provider tokens. |
| `agent_configs` | Database-backed agent config records. File-based agent definitions are edited on disk. |
| `provider_configs` | Provider instance records and shared instance configuration. |
| `model_configs` | Model endpoint and token configuration. |
| `skills` | Module permissions control skill management; per-skill entries control runtime availability. |
| `providers` | Per-provider-instance entries control runtime access. |

## Runtime Access Checklist {#runtime-access-checklist}

For provider-backed skill execution, verify:

1. The user has an active role.
2. The skill is visible and enabled for at least one role.
3. The provider instance is allowed for at least one role.
4. The provider instance is active.
5. User-scoped credentials are configured when required.

## System-Managed Built-In Roles {#system-managed-built-in-roles}

`admin` and `user` are system-managed built-ins. The application preserves the
canonical shape for most modules and only lets runtime access modules such as
skills and providers remain user-managed. Use custom roles for custom
management policies.
