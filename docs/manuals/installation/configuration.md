---
title: Configuration
description: Configure AtlasClaw Core with atlasclaw.json and environment variables.
sidebar_position: 4
---

# Configuration

AtlasClaw reads runtime settings from `atlasclaw.json`, then expands
environment placeholders such as `${OPENAI_API_KEY}`. Keep stable structure in
the JSON file and keep secrets in environment variables or encrypted
configuration values.

## Minimal Configuration {#minimal-configuration}

```json
{
  "providers_root": "../atlasclaw-providers/providers",
  "model": {
    "primary": "main",
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

## Important Settings {#important-settings}

- `providers_root`: directory containing provider packages.
- `model`: model provider and token settings used by the agent runtime.
- `auth`: authentication provider and local login settings.
- `workspace.path`: storage root for agents, users, sessions, memory, and runtime
  state.
- `service_providers`: provider instance configuration loaded into the provider
  registry.

## Full Configuration Skeleton {#full-configuration-skeleton}

Use this skeleton as a starting point for production configuration. Remove
sections you do not use; omitted sections fall back to schema defaults.

```json
{
  "log_level": "info",
  "base_path": "",
  "workspace": {
    "path": "./.atlasclaw"
  },
  "database": {
    "type": "sqlite",
    "sqlite": {
      "path": "./data/atlasclaw.db"
    },
    "echo": false
  },
  "providers_root": "../atlasclaw-providers/providers",
  "skills_root": "../skills",
  "auth": {
    "enabled": true,
    "provider": "local",
    "local": {
      "enabled": true,
      "default_admin_username": "admin",
      "default_admin_password": "${ATLASCLAW_ADMIN_PASSWORD}"
    },
    "jwt": {
      "secret_key": "${ATLASCLAW_JWT_SECRET}",
      "expires_minutes": 480
    }
  },
  "model": {
    "primary": "main",
    "fallbacks": [],
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
  },
  "service_providers": {
    "example_provider": {
      "default": {
        "base_url": "${PROVIDER_URL}",
        "auth_type": "user_token"
      }
    }
  },
  "agent_defaults": {
    "timeout_seconds": 600,
    "max_concurrent": 10,
    "max_tool_calls": 50,
    "prompt_mode": "full"
  },
  "messages": {
    "queue": {
      "mode": "collect",
      "debounce_ms": 1000,
      "cap": 20,
      "drop": "old"
    },
    "reply_to_mode": "auto",
    "inbound_debounce_ms": 1000,
    "dedup_ttl_seconds": 60
  },
  "memory": {
    "enabled": true,
    "max_results": 6
  },
  "security": {
    "allowed_tools": [],
    "denied_tools": [],
    "workspace_access": "rw"
  }
}
```

## Section Summary {#section-summary}

| Section | Purpose | Common changes |
| --- | --- | --- |
| `log_level` | Backend log level. | Use `info` for normal operation and `debug` while diagnosing. |
| `base_path` | Reverse-proxy mount path. | Set when AtlasClaw is served under a prefix such as `/atlasclaw`. |
| `workspace.path` | Runtime storage root. | Move to persistent storage in production. |
| `database` | SQLite or MySQL storage settings. | Use SQLite for local/small deployments, MySQL for shared production deployments. |
| `providers_root` | Directory containing provider packages. | Point to `atlasclaw-providers/providers`. |
| `skills_root` | Directory containing standalone skill packages. | Use when deploying skills outside provider packages. |
| `auth` | AtlasClaw login and identity configuration. | Choose `local`, `host_cookie`, `oidc`, `dingtalk`, or `none`. |
| `model` | LLM token pool and runtime generation defaults. | Configure primary token, fallbacks, temperature, and max tokens. |
| `service_providers` | Provider instance templates. | Configure provider type, instance name, auth mode, and instance fields. |
| `agent_defaults` | Default runtime limits for agent turns. | Tune timeout, concurrency, and tool-call limits. |
| `messages` | Message queueing and deduplication behavior. | Tune IM debounce and queue behavior. |
| `memory` | User-scoped memory retrieval settings. | Enable or tune memory search result count. |
| `security` | Tool and workspace access policy. | Restrict tools or workspace access for hardened deployments. |

## Provider Packages {#provider-packages}

Core scans `providers_root/<provider>/` for `PROVIDER.md`,
`provider.schema.json`, and provider skills. Provider-specific fields and auth
flows belong in Provider Integration docs.

## Provider Instance Configuration {#provider-instance-configuration}

`service_providers` is shaped as:

```json
{
  "service_providers": {
    "<provider_type>": {
      "<instance_name>": {
        "auth_type": "user_token"
      }
    }
  }
}
```

Provider-specific fields come from that provider's `provider.schema.json`.
Core owns the common `auth_type` vocabulary and the instance/user/request
credential boundary.

Common auth modes:

| `auth_type` | Where credentials live | Typical use |
| --- | --- | --- |
| `provider_token` | `atlasclaw.json` provider instance | Shared service token configured by an administrator. |
| `user_token` | User Provider Tokens settings | Each user supplies a personal provider token. |
| `cookie` | Request context or provider instance | Embedded deployments or static session-cookie testing. |
| `credential` | `atlasclaw.json` provider instance | Robot username/password or login credential. |
| `sso` | Request context | Provider uses a token forwarded by the AtlasClaw auth flow. |
| `app_credentials` | `atlasclaw.json` provider instance | Provider-defined application credentials. |

See Provider Auth Model for generic auth examples and the provider-specific
section for exact fields. For seamless embedded deployments, use
`auth.provider: "host_cookie"` together with provider `auth_type: "cookie"`;
see [Embedded Mode](../../provider-integration/embedded-mode.md).
