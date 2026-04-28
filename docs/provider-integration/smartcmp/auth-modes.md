---
title: Auth Modes
description: SmartCMP auth modes and required fields.
sidebar_position: 3
---

# Auth Modes

SmartCMP Provider requires `base_url` for every instance. Auth mode determines
which credential fields are required.

| Mode | `auth_type` | Required fields | Scope |
| --- | --- | --- | --- |
| Provider Token | `provider_token` | `provider_token` | Instance |
| User Token | `user_token` | `user_token` | User |
| Cookie | `cookie` | `cookie` or request cookie/token | Instance or request |
| Credential | `credential` | `username`, `password` | Instance |

The provider schema defaults to `user_token`.

## Auth URL {#auth-url}

`auth_url` is optional. Use it for private SmartCMP deployments with a
non-standard login endpoint or hostnames that should not follow default auth URL
inference.

## Choosing a Mode {#choosing-a-mode}

| Requirement | Recommended mode |
| --- | --- |
| Each action should use the user's own SmartCMP identity | User Token |
| A shared service account is acceptable for all users | Provider Token |
| AtlasClaw is embedded behind SmartCMP and receives request cookies | Cookie |
| A robot account should log in and cache a session cookie | Credential |

User Token is the default because it keeps accountability closest to the
SmartCMP user. Provider Token and Credential modes are easier to operate but
should be reviewed against your audit and segregation-of-duties requirements.

## Fallback Behavior {#fallback-behavior}

SmartCMP `auth_type` can be configured as a single mode or an ordered chain in
provider source configuration. The runtime uses the first mode whose required
fields are available:

1. Provider Token requires `provider_token`.
2. User Token requires the user's saved `user_token`.
3. Cookie requires a request-scoped token/cookie or configured `cookie`.
4. Credential requires `username` and `password`.

Keep fallback chains short and explicit. Long chains make failures harder for
users to understand.
