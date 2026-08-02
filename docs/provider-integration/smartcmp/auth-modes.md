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
| A robot account should log in for each Provider invocation | Credential |

User Token is the default because it keeps accountability closest to the
SmartCMP user. Provider Token and Credential modes are easier to operate but
should be reviewed against your audit and segregation-of-duties requirements.

## AtlasClaw Selection and Provider Execution {#fallback-behavior}

SmartCMP `auth_type` can be configured as a single mode or an ordered chain in
AtlasClaw provider source configuration. AtlasClaw Core uses the first mode in
that configured order whose required fields are available for the current
request:

1. Provider Token requires `provider_token`.
2. User Token requires the user's saved `user_token`.
3. Cookie requires a request-scoped token/cookie or configured `cookie`.
4. Credential requires `username` and `password`.

For the normal AtlasClaw Skill path, Core removes credential fields for
inactive modes and sends exactly one selected `auth_type` to the SmartCMP
callable. SmartCMP Provider executes that sanitized mode; it does not receive
or interpret the original ordered list. Standalone MCP bindings also carry one
explicit mode in each Authentication Context.

Direct integrations should use the same explicit Authentication Context
contract. The AtlasClaw compatibility resolver can still infer a credential or
perform credential login when it receives legacy, unfiltered configuration;
that compatibility behavior is not a second MCP authentication chain and is
not the contract used by the normal AtlasClaw path.

Keep AtlasClaw source chains short and explicit. Long chains make failures
harder for users to understand.

Credential mode performs one SmartCMP login for each Provider invocation. The
resulting session is request-scoped and is not stored in a Provider Cookie
cache.
