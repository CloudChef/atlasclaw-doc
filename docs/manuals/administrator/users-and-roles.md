---
title: Users and Roles
description: Manage workspace users, built-in roles, and permissions.
sidebar_position: 2
---

# Users and Roles

AtlasClaw uses workspace roles for management permissions. Runtime provider
actions still execute under the authenticated user's real upstream identity.

## Built-In Roles {#built-in-roles}

| Role | Identifier | Purpose |
| --- | --- | --- |
| Administrator | `admin` | Full administrative access to workspace configuration and access control. |
| Standard User | `user` | Default collaborator role with access to enabled workspace skills and own channel connections. |
| Viewer | `viewer` | Read-only role for audit and oversight workflows. |

## User Management {#user-management}

Administrators can create users, edit profiles, change authentication type,
activate or deactivate accounts, assign roles, and delete users other than
themselves.

For local-auth users, profile and password lifecycle is managed in AtlasClaw.
For federated or host-cookie users, AtlasClaw stores the workspace profile and
role mapping, while the upstream identity system remains responsible for login
credentials and identity assurance.

Before deleting or deactivating a user, check whether the account owns active
channel connections, provider tokens, or sessions that other teams expect to
audit. User-owned runtime data should be handled according to your retention
policy.

## Permission Model {#permission-model}

Permissions are grouped by module:

- `users`
- `roles`
- `channels`
- `tokens`
- `agent_configs`
- `provider_configs`
- `model_configs`
- `skills`
- `providers`

Use custom roles when an operator needs access to one module without full admin
privileges.

## Built-In Role Behavior {#built-in-role-behavior}

The built-in `admin` and `user` roles are system-managed. Their metadata is
read-only, and most permission modules are restored to canonical defaults when
the application ensures built-in roles. Runtime access modules for skills and
providers can still be managed so administrators can decide which skills and
provider instances users can actually run.

Do not model a custom access policy by trying to turn the built-in Standard
User role into an administrator or a locked-down viewer. Create a custom role
instead.

## Creating a Custom Role {#creating-a-custom-role}

Use a custom role when a group needs a clear operational responsibility, for
example model-configuration operators, provider administrators, or user
managers.

1. Choose a stable `identifier`. Identifiers cannot be changed after creation.
2. Grant only the module permissions needed for the role.
3. Add provider runtime access if the role should execute provider skills.
4. Add skill permissions for the skills the role should see and use.
5. Assign the role to a test user and verify the UI and chat runtime behavior.

## Permission Examples {#permission-examples}

| Need | Permissions to consider |
| --- | --- |
| Manage users but not models | `users.view`, `users.create`, `users.edit`, `users.assign_roles` |
| Operate provider instances | `provider_configs.view`, `provider_configs.create`, `provider_configs.edit` |
| Grant provider runtime access | `providers.manage_permissions` plus provider permission entries |
| Manage model endpoints | `model_configs.view`, `model_configs.create`, `model_configs.edit`, `model_configs.delete` |
| Allow personal channel setup | `channels.view`, `channels.create`, `channels.edit`, `channels.delete` |

## Troubleshooting Access {#troubleshooting-access}

When a user can see a skill but cannot complete a provider-backed request,
check three layers:

1. The role has the skill enabled.
2. The role has access to the target provider instance.
3. The user has valid provider-native credentials when the provider requires
   per-user authentication.
