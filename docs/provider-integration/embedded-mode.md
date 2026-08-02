---
title: Embedded Mode
description: Embed an AtlasClaw Agent into an enterprise system and reuse its request Cookie for seamless Provider access.
sidebar_position: 4
---

# Embedded Mode

Embedded mode brings an AtlasClaw Agent into an existing enterprise system
that already authenticates the user. It adds page-aware analysis and governed
action without rebuilding the system's UI, APIs, identity, permissions,
workflows, or audit model.

Embedded mode supports two independent UI surfaces: a full menu UI and a
compact floating UI. Both use the same enterprise-system Cookie authentication
context, so they resolve the same signed-in user and preserve that user's
existing system access. Only the floating UI attaches dynamic page Context.
See [Embedded Menu and Floating UI](./embedded-menu-and-floating-ui.md).

## AtlasClaw Understands and Acts Within the Enterprise System {#hostapp-provider}

The formal integration component is the **HostApp Provider**: the AtlasClaw
Provider package that maps the enterprise system's pages to business objects,
Domain Skills, and state-aware object actions. `embed_integration` binds the
embedded runtime to exactly one Provider type and instance.

The HostApp Provider is installed and configured with AtlasClaw. It is not a
new service that the enterprise system must deploy. It calls existing system
APIs with the current user's request Cookie, so AtlasClaw can understand the
current Context and act while preserving existing RBAC, workflows, and audit.

![AtlasClaw Embedded Mode architecture for an existing enterprise system](/img/embedded/hostapp-provider-architecture-en.svg)

This boundary keeps the integration narrow:

- the enterprise system adds an independent menu entry, a floating UI, or both;
- the floating bridge publishes only normalized `path` and `generation`;
- AtlasClaw owns Chat, Context snapshots, orchestration, confirmation,
  execution safety, and the generic `object_actions` schema and builders;
- the HostApp Provider owns page meaning, object resolution, Domain Skills,
  and the business availability, copy, URLs, and inputs for each action;
- the enterprise system continues to own its existing data, APIs, permissions,
  workflows, and audit.

## Authentication Layers {#authentication-layers}

Embedded mode has two related but separate authentication layers:

| Layer | AtlasClaw config | Purpose |
| --- | --- | --- |
| AtlasClaw user identity | `auth.provider: "host_cookie"` | Reads enterprise-system Cookies and resolves the current AtlasClaw user. |
| Provider access | `service_providers.<provider>.<instance>.auth_type: "cookie"` | Passes the current request cookie into the provider runtime. |

The first layer answers "who is using AtlasClaw?". The second layer answers
"which upstream credential should this provider call use?". For a seamless
embedded deployment, configure both layers.

## Recommended Flow {#recommended-flow}

1. The user signs in to the enterprise system.
2. The enterprise system opens the AtlasClaw menu UI, floating UI, or both as
   independent embedded surfaces.
3. The browser sends the same enterprise-system authentication and identity
   Cookies to AtlasClaw requests from both surfaces.
4. AtlasClaw resolves the user with `host_cookie` auth and creates or updates
   the workspace shadow user.
5. AtlasClaw uses the HostApp Provider selected by `embed_integration`.
6. That Provider instance receives the request-scoped Cookie through
   `auth_type: "cookie"`.
7. Its Domain Skills call the existing system APIs with that Cookie, so
   upstream RBAC, workflows, and audit stay aligned with the original
   enterprise-system login.

The cookie is runtime-only. It is not copied into Provider Tokens, not saved as
a user setting, and should not be committed into `atlasclaw.json`.

## AtlasClaw Auth Configuration {#atlasclaw-auth-configuration}

Configure `auth.provider` as `host_cookie` and map the cookie names issued by
the enterprise system.

```json
{
  "auth": {
    "enabled": true,
    "provider": "host_cookie",
    "host_cookie": {
      "cookie_name": "Host-Authenticate",
      "subject_cookie_name": "userLoginId",
      "display_name_cookie_name": "username",
      "user_id_cookie_name": "userId",
      "tenant_id_cookie_name": "tenant_id"
    }
  }
}
```

Field behavior:

| Field | Meaning |
| --- | --- |
| `cookie_name` | Enterprise-system authentication Cookie containing the raw token AtlasClaw forwards for cookie-mode Provider access. |
| `subject_cookie_name` | Required stable login identifier used as the AtlasClaw subject. |
| `display_name_cookie_name` | Optional display name shown in AtlasClaw. |
| `user_id_cookie_name` | Optional upstream user ID copied into the authenticated user metadata. |
| `tenant_id_cookie_name` | Optional tenant identifier; AtlasClaw uses `default` when it is absent. |

In `host_cookie` mode, AtlasClaw can still accept a valid AtlasClaw admin JWT
first. This keeps backend management access available while normal embedded
users enter through enterprise-system Cookies.

## HostApp Provider Cookie Configuration {#provider-cookie-configuration}

Configure the HostApp Provider instance with `auth_type: "cookie"` when calls
to the existing system should use the current request Cookie.

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

Do not add a static `cookie` field for the normal embedded path. A static cookie
is suitable only for controlled server-to-server testing because every request
would use the same session. In production embedded mode, the runtime request
cookie should be the selected credential.

## Enterprise System Requirements {#host-system-requirements}

The embedding enterprise system must make the Cookie visible to AtlasClaw
requests. In practice, that usually means:

- AtlasClaw is served under the same site, parent domain, or reverse-proxy path
  where the enterprise-system Cookie is in scope.
- Cookie `Path`, `Domain`, `SameSite`, and `Secure` attributes allow the
  browser to send the enterprise-system Cookie to AtlasClaw.
- The enterprise system provides a stable subject Cookie so AtlasClaw can map
  the request to a workspace user.
- The HostApp Provider can use that Cookie with the existing system APIs, or
  knows how to exchange it for the native session those APIs require.

For the menu surface, this Cookie setup and a nested Agent entry are the full
enterprise-system integration: open
`/atlasclaw/?embedded=1&surface=menu`. The menu does not require a page-change
bridge.

For the floating surface, the enterprise system must additionally render and
manage the compact iframe, create its URL with the exact Host Origin and a fresh
nonce, send normalized router paths with monotonically increasing generations,
and strictly validate messages in both directions. The enterprise system
supplies navigation facts only; AtlasClaw and the HostApp Provider resolve
Context and own actions, confirmation, execution, and permission checks. See
[Enterprise System
Capabilities](./embedded-menu-and-floating-ui.md#host-app-capabilities).

If AtlasClaw is embedded in a cross-site iframe, browser cookie restrictions
can block the request cookie. Validate the final browser behavior in the target
deployment rather than relying only on server-side configuration.

## Security Notes {#security-notes}

- Treat enterprise-system Cookies as user credentials. Do not log them, store
  them in memory, or expose them in troubleshooting output.
- Prefer HTTPS and secure cookie attributes in production.
- Keep provider RBAC enabled in the target system. AtlasClaw should not grant
  access that the target system would deny.
- Use `provider_token`, `credential`, or `app_credentials` only when the
  deployment intentionally uses a shared or robot identity.

## Troubleshooting {#troubleshooting}

| Symptom | Check |
| --- | --- |
| User is redirected or rejected before AtlasClaw loads | Confirm `auth.provider` is `host_cookie` and the configured `cookie_name` is present on the AtlasClaw request. |
| User appears as the wrong AtlasClaw account | Check `subject_cookie_name`; it must be stable and unique for the user. |
| Provider call says missing credentials | Confirm the Provider instance selects `auth_type: "cookie"` and that the request contains the enterprise-system Cookie. |
| Provider call is unauthorized | Confirm the target system accepts the forwarded cookie and the upstream user has the required permissions. |
| Works outside iframe but not inside iframe | Check browser `SameSite`, third-party cookie, `Secure`, and domain/path behavior. |
