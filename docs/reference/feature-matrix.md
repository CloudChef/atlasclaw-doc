---
title: Feature Matrix
description: Documentation mapping to roles, UI, APIs, and source modules.
sidebar_position: 4
---

# Feature Matrix

| Feature | Primary role | UI entry | API area | Source area |
| --- | --- | --- | --- | --- |
| Chat | Standard User | `/` | `/api/agent`, `/api/sessions` | `app/atlasclaw/agent`, `api/routes_agent.py` |
| Account profile | Standard User | `/account` | `/api/users/me/*` | `api/api_routes.py`, `pages/account-settings.js` |
| Provider tokens | Standard User | `/account` | `/api/users/me/provider-settings` | `api/api_routes.py` |
| IM channels | Standard User | `/channels` | `/api/channels/*` | `channels/`, `pages/channels.js` |
| Users | Administrator | `/admin/users` | `/api/users` | `db/orm/user.py`, `pages/admin-users.js` |
| Roles | Administrator | `/admin/roles` | `/api/roles` | `db/orm/role.py`, `pages/role-management.js` |
| Models | Administrator | `/models` | `/api/model-configs` | `api/model_config_routes.py`, `pages/models.js` |
| Provider instances | Administrator | `/providers` | `/api/provider-configs` | `api/api_routes.py`, `pages/providers.js` |
| Agent config | Administrator | File/API | `/api/agent-configs` | `agent/agent_definition.py`, `db/orm/agent_config.py` |
| Provider integrations | User/Admin | Chat, Account, Providers | Provider tools/config APIs | Provider packages under `providers_root` |

Use this matrix as the review checklist when updating documentation.

## Review Checklist {#review-checklist}

When a feature changes, update the docs that match all affected surfaces:

1. User-facing workflow page.
2. Administrator workflow page.
3. Core behavior page, if the shared runtime contract changed.
4. Provider Integration page, if the change is provider-specific.
5. Reference page for route, permission, or configuration changes.
6. Chinese translation under `i18n/zh-CN`.

## Source-of-Truth Rules {#source-of-truth-rules}

| Content type | Source of truth |
| --- | --- |
| Permission defaults | Role service and auth guard code. |
| Channel required fields | Channel handler schemas and validation code. |
| Agent file parsing | Agent definition parser and agent config service. |
| Provider fields | Provider `provider.schema.json`. |
| Provider workflows | Provider `README.md`, `PROVIDER.md`, and skill files. |
| API route list | FastAPI route modules. |
