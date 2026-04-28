---
title: Configuration Reference
description: Common AtlasClaw configuration fields.
sidebar_position: 1
---

# Configuration Reference

## Core Fields {#core-fields}

| Field | Purpose |
| --- | --- |
| `log_level` | Backend log level: `debug`, `info`, `warning`, or `error`. |
| `base_path` | Optional reverse-proxy mount path such as `/atlasclaw`. |
| `providers_root` | Directory containing provider packages. |
| `skills_root` | Directory containing standalone skill packages outside provider packages. |
| `workspace.path` | Runtime storage root. |
| `database` | Database backend configuration for SQLite or MySQL. |
| `model` | Model provider, model tokens, and primary model settings. |
| `auth` | Authentication provider and token settings. |
| `service_providers` | Provider instance configuration. |
| `agent_defaults` | Runtime limits and prompt mode defaults for agent turns. |
| `messages` | Message queue, debounce, and deduplication behavior. |
| `compaction` | Long-context compaction thresholds. |
| `context_pruning` | Tool-result pruning policy under context pressure. |
| `memory` | User-scoped memory retrieval settings. |
| `sandbox` | Optional sandbox mode and workspace root. |
| `security` | Tool allow/deny lists and workspace access policy. |
| `skills` | Markdown skill loading limits and script-execution policy. |
| `reset` | Session reset policy. |
| `webhook` | Inbound webhook dispatch configuration. |
| `hooks_runtime` | Config-driven hook script handlers. |
| `search_runtime` | Web search provider runtime configuration. |
| `heartbeat` | Agent and channel heartbeat runtime configuration. |

## AtlasClaw JSON Structure {#atlasclaw-json-structure}

`atlasclaw.json` is the main deployment configuration file. The most common
production sections are:

```json
{
  "workspace": {
    "path": "./.atlasclaw"
  },
  "database": {
    "type": "sqlite",
    "sqlite": {
      "path": "./data/atlasclaw.db"
    }
  },
  "providers_root": "../atlasclaw-providers/providers",
  "skills_root": "../skills",
  "auth": {
    "enabled": true,
    "provider": "local"
  },
  "model": {
    "primary": "main",
    "tokens": []
  },
  "service_providers": {}
}
```

### Workspace and Database {#workspace-and-database}

`workspace.path` stores runtime files such as sessions, memory, user settings,
agent files, channel artifacts, and provider runtime artifacts. Use persistent
storage for production.

`database.type` can be `sqlite` or `mysql`:

```json
{
  "database": {
    "type": "mysql",
    "mysql": {
      "host": "${MYSQL_HOST}",
      "port": 3306,
      "database": "atlasclaw",
      "user": "${MYSQL_USER}",
      "password": "${MYSQL_PASSWORD}",
      "charset": "utf8mb4"
    },
    "pool_size": 5,
    "max_overflow": 10,
    "echo": false
  }
}
```

### Auth Section {#auth-section}

`auth.provider` selects AtlasClaw login behavior:

| Provider | Use case | Key fields |
| --- | --- | --- |
| `local` | Local username/password login. | `auth.local.enabled`, `default_admin_username`, `default_admin_password`, `auth.jwt.*` |
| `host_cookie` | Embedded behind a host system that already authenticates users. | `auth.host_cookie.cookie_name`, `subject_cookie_name`, display/user/tenant cookie fields |
| `oidc` | OIDC/OAuth2 SSO. | `issuer`, `client_id`, `client_secret`, endpoints, `redirect_uri` |
| `dingtalk` | DingTalk SSO login. | `app_key`, `app_secret`, `corp_id`, `redirect_uri` |
| `none` | Development/no-auth mode. | `auth.none.default_user_id` |

Authentication identifies the AtlasClaw user. It is separate from provider
authentication under `service_providers`.

### Model Section {#model-section}

`model.primary` references a token `id` from `model.tokens`. `fallbacks` is an
ordered list of backup token IDs. `selection_strategy`, `priority`, and
`weight` control token selection when multiple entries are active.

```json
{
  "model": {
    "primary": "main",
    "fallbacks": ["backup"],
    "temperature": 0.2,
    "max_tokens": 4096,
    "selection_strategy": "health",
    "tokens": [
      {
        "id": "main",
        "provider": "openai",
        "model": "gpt-4.1",
        "base_url": "https://api.openai.com/v1",
        "api_key": "${OPENAI_API_KEY}",
        "api_type": "openai",
        "priority": 0,
        "weight": 100,
        "context_window": 128000
      }
    ]
  }
}
```

### Provider Instance Section {#provider-instance-section}

`service_providers` stores administrator-owned provider templates:

```json
{
  "service_providers": {
    "example_provider": {
      "default": {
        "base_url": "${PROVIDER_URL}",
        "auth_type": "user_token"
      },
      "shared": {
        "base_url": "${PROVIDER_URL}",
        "auth_type": "provider_token",
        "provider_token": "${PROVIDER_TOKEN}"
      }
    }
  }
}
```

The first key is the provider type. The second key is the instance name. The
inner object is the provider instance template. Provider-specific fields are
declared by `provider.schema.json`.

## Environment Expansion {#environment-expansion}

String values in configuration may reference environment variables with
`${VAR_NAME}` syntax. Use this for secrets and deployment-specific URLs.

Configuration is loaded from defaults, config files, environment variables, and
runtime overrides. Values such as `${PROVIDER_URL}` are expanded from the process
environment after file configuration is merged.

## Common Files {#common-files}

| File | Purpose |
| --- | --- |
| `atlasclaw.json` | Project or workspace configuration. |
| `atlasclaw.yaml` | Alternate configuration file format. |
| `~/.atlasclaw/config.json` | User-level fallback configuration. |
| `.env` | Environment variables used by deployment scripts. |
| `users/<user_id>/user_setting.json` | User-scoped preferences and provider settings. |

## Configuration Precedence {#configuration-precedence}

Later sources override earlier sources:

1. Defaults from the configuration schema.
2. Global config file.
3. Workspace config file.
4. `ATLASCLAW_*` environment variables and `${VAR}` expansion.
5. Runtime overrides.

Use environment variables for secrets and deployment-specific URLs. Use files
for stable structure such as workspace path and provider root.

## Provider Fields {#provider-fields}

Provider-specific fields come from `provider.schema.json` and belong under the
Provider Integration section.

Provider schema files define:

- `default_auth_type`;
- `auth_modes` and required fields per mode;
- config `fields`;
- field `scope`, such as `instance` or `user`;
- sensitive/password fields that must be redacted.

## Secret Handling {#secret-handling}

Do not commit API keys, cookies, provider tokens, channel secrets, or model
tokens. Prefer environment variables or encrypted config values when supported
by your deployment. When rotating a secret, update the owning configuration
surface instead of editing runtime artifacts directly.
