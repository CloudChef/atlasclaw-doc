---
title: Auth and RBAC
description: Authentication, shadow users, roles, and permission enforcement.
sidebar_position: 2
---

# Auth and RBAC

AtlasClaw separates authentication from workspace authorization.

## Authentication {#authentication}

Authentication resolves the current user from local login, host cookie, OIDC,
SSO, or other configured providers. The runtime receives a `UserInfo` object
with user ID, display name, tenant, roles, token, provider subject, and auth
type.

Authentication answers "who is making this request". It does not automatically
grant administrative access. After authentication, AtlasClaw resolves workspace
roles and calculates effective permissions.

## Shadow Users {#shadow-users}

External identities can be mapped to internal shadow users. This lets AtlasClaw
keep sessions, memory, and workspace settings stable even when the upstream
identity provider is external.

## Workspace Authorization {#workspace-authorization}

Workspace roles grant management permissions such as `users.view`,
`roles.edit`, `channels.create`, or `model_configs.delete`.

Runtime provider actions still inherit the authenticated user's upstream access.
AtlasClaw must not use workspace admin status to bypass provider-side RBAC.

Management permissions protect AtlasClaw configuration. Provider runtime
permissions protect which provider instances and skills a user may invoke from
AtlasClaw. Provider-native permissions protect the final upstream operation.

## Effective Permissions {#effective-permissions}

When a user has multiple active roles, permissions are merged. Boolean module
permissions use OR semantics. Provider instance denials are effective only when
every active role denies the same instance.

Skill permissions are represented as per-skill entries. Provider runtime
permissions are represented as provider type plus instance name entries. This
allows one role to grant access to a read-only skill while another role grants
access to a specific provider instance.

## Built-In Role Rules {#built-in-role-rules}

The built-in `admin` and `user` roles are system-managed. Their metadata and
most module permissions are repaired to defaults by the role service. Runtime
access modules for skills and providers remain configurable so administrators
can expose or hide operational capabilities without changing the built-in role
shape.

## Request Enforcement Points {#request-enforcement-points}

| Layer | Example check |
| --- | --- |
| API route | `agent_configs.create`, `roles.edit`, `channels.delete` |
| UI navigation | Hide or show admin pages based on module view permissions. |
| Skill registry | Expose only enabled skills to the agent runtime. |
| Provider registry | Expose only provider instances allowed for the user. |
| Provider script/API | Enforce the upstream system's native RBAC. |
