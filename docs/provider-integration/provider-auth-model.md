---
title: Provider Auth Model
description: Provider authentication responsibility and credential scope.
sidebar_position: 3
---

# Provider Auth Model

AtlasClaw identifies the user. A provider is responsible for turning that
identity into credentials the target system accepts.

## Credential Scopes {#credential-scopes}

- Instance-scoped credentials are configured by administrators.
- User-scoped credentials are configured by each user.
- Request-scoped credentials can come from cookies or upstream headers.

Instance credentials are appropriate for shared service accounts or deployment
integration tokens. User credentials are appropriate when every action must be
attributable to the upstream user. Request-scoped credentials are appropriate
when AtlasClaw is embedded behind a system that already authenticated the user
and forwards a valid upstream token or cookie.

## Runtime Rule {#runtime-rule}

Provider skills that call external APIs must run with provider-native
credentials. Workspace admin status must not bypass the target system's own
authorization.

## Auth Chains {#auth-chains}

Some providers support an ordered `auth_type` chain. The provider selects the
first usable mode based on available fields and request context.

Auth chains should be explicit. If a provider can use several credential
sources, document the selection order and the fields required by each mode.

`auth_type` can be a string or an ordered list:

```json
{
  "service_providers": {
    "example_provider": {
      "default": {
        "base_url": "${PROVIDER_URL}",
        "auth_type": ["sso", "user_token", "provider_token"],
        "provider_token": "${PROVIDER_TOKEN}"
      }
    }
  }
}
```

The selected auth mode always comes from the provider instance template. A user
cannot switch the provider to another auth mode from Account Settings.

## Supported Auth Types {#supported-auth-types}

Core recognizes this public auth vocabulary. Each provider's
`provider.schema.json` defines which modes it supports and which fields are
required.

| `auth_type` | Credential owner | Configuration pattern |
| --- | --- | --- |
| `provider_token` | Administrator | Shared token stored on the provider instance. |
| `user_token` | User | Provider instance selects the mode; user saves `user_token` in Provider Tokens. |
| `cookie` | Request or administrator | Request-scoped forwarded cookie/token, or static cookie on the instance. |
| `credential` | Administrator | Username/password or equivalent login credentials on the provider instance. |
| `sso` | Request | SSO token forwarded by the AtlasClaw auth flow. |
| `app_credentials` | Administrator | Provider-defined app credentials on the provider instance. |

## Provider Token Mode {#provider-token-mode}

Use `provider_token` when all AtlasClaw users should call the upstream system
through one shared provider token.

```json
{
  "service_providers": {
    "example_provider": {
      "default": {
        "base_url": "${PROVIDER_URL}",
        "auth_type": "provider_token",
        "provider_token": "${PROVIDER_TOKEN}"
      }
    }
  }
}
```

This is easy to operate, but upstream audit trails may show the shared service
identity rather than the individual AtlasClaw user.

## User Token Mode {#user-token-mode}

Use `user_token` when each user must bring their own upstream credential.

```json
{
  "service_providers": {
    "example_provider": {
      "default": {
        "base_url": "${PROVIDER_URL}",
        "auth_type": "user_token"
      }
    }
  }
}
```

Users then save their credential in Account Settings under Provider Tokens. The
saved user setting is scoped by provider type and instance name, and only the
`user_token` field is user-owned. Platform fields such as `base_url`,
`provider_token`, `cookie`, and `auth_type` remain controlled by the provider
instance template.

## Cookie Mode {#cookie-mode}

Use `cookie` when the provider can use a request-scoped token/cookie forwarded
by an embedding host, or when an administrator intentionally configures a static
cookie for server-to-server testing.

```json
{
  "service_providers": {
    "example_provider": {
      "default": {
        "base_url": "${PROVIDER_URL}",
        "auth_type": "cookie"
      }
    }
  }
}
```

If using a static cookie, the provider schema will define the field name:

```json
{
  "service_providers": {
    "example_provider": {
      "default": {
        "base_url": "${PROVIDER_URL}",
        "auth_type": "cookie",
        "cookie": "${PROVIDER_COOKIE}"
      }
    }
  }
}
```

Request-scoped cookies are runtime-only and must not be copied into user
settings or committed into configuration files.

For embedded deployments, pair this provider mode with AtlasClaw
`host_cookie` authentication. See [Embedded Mode](./embedded-mode.md) for the
full configuration pattern.

## Credential Mode {#credential-mode}

Use `credential` when the provider should log in with an administrator-owned
robot account or service credential.

```json
{
  "service_providers": {
    "example_provider": {
      "default": {
        "base_url": "${PROVIDER_URL}",
        "auth_type": "credential",
        "username": "${PROVIDER_USERNAME}",
        "password": "${PROVIDER_PASSWORD}"
      }
    }
  }
}
```

The exact required field names come from the provider schema.

## SSO Mode {#sso-mode}

Use `sso` when the provider should use the token forwarded by AtlasClaw's auth
flow. This usually appears in embedded or single-sign-on deployments.

```json
{
  "service_providers": {
    "example_provider": {
      "default": {
        "base_url": "${PROVIDER_URL}",
        "auth_type": "sso"
      }
    }
  }
}
```

The provider can use SSO only when the current request contains a usable
provider SSO token.

## App Credentials Mode {#app-credentials-mode}

Use `app_credentials` when a provider authenticates with application-level
credentials such as a client ID and client secret. Field names are
provider-defined.

```json
{
  "service_providers": {
    "example_provider": {
      "default": {
        "base_url": "${PROVIDER_URL}",
        "auth_type": "app_credentials",
        "client_id": "${PROVIDER_CLIENT_ID}",
        "client_secret": "${PROVIDER_CLIENT_SECRET}"
      }
    }
  }
}
```

Do not assume every provider supports this mode. Check that provider's schema.

## Administrator vs User Responsibilities {#administrator-vs-user-responsibilities}

| Responsibility | Administrator | User |
| --- | --- | --- |
| Install provider package | Yes | No |
| Create provider instance | Yes | No |
| Choose auth mode | Yes | No |
| Configure shared token or credential | Yes, if the mode uses shared credentials | No |
| Configure personal token | No | Yes, if the mode uses user credentials |
| Resolve upstream RBAC denial | Usually coordinate with upstream system owner | Request the required upstream access |
