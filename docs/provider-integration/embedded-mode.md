---
title: Embedded Mode
description: Run AtlasClaw inside a host system and use request cookies for seamless provider access.
sidebar_position: 4
---

# Embedded Mode

Embedded mode runs AtlasClaw inside a system that already authenticates the
user. The browser opens AtlasClaw from that host system, carries the host
cookies with the request, and AtlasClaw maps those cookies into both workspace
identity and provider credentials.

Use this mode when the target provider system is also the embedding host, or
when the embedding host can forward a cookie accepted by the target provider.
In that deployment, users do not need to log in to AtlasClaw separately and do
not need to save a personal provider token.

## Authentication Layers {#authentication-layers}

Embedded mode has two related but separate authentication layers:

| Layer | AtlasClaw config | Purpose |
| --- | --- | --- |
| AtlasClaw user identity | `auth.provider: "host_cookie"` | Reads host cookies and resolves the current AtlasClaw user. |
| Provider access | `service_providers.<provider>.<instance>.auth_type: "cookie"` | Passes the current request cookie into the provider runtime. |

The first layer answers "who is using AtlasClaw?". The second layer answers
"which upstream credential should this provider call use?". For a seamless
embedded deployment, configure both layers.

## Recommended Flow {#recommended-flow}

1. The user signs in to the host system.
2. The host system opens AtlasClaw in an iframe, embedded page, or routed
   sub-application.
3. The browser sends the host authentication cookie and identity cookies to
   AtlasClaw.
4. AtlasClaw resolves the user with `host_cookie` auth and creates or updates
   the workspace shadow user.
5. A provider instance configured with `auth_type: "cookie"` receives the
   request-scoped cookie at runtime.
6. Provider skills call the target system with that cookie, so upstream RBAC
   and audit behavior stay aligned with the original host login.

The cookie is runtime-only. It is not copied into Provider Tokens, not saved as
a user setting, and should not be committed into `atlasclaw.json`.

## AtlasClaw Auth Configuration {#atlasclaw-auth-configuration}

Configure `auth.provider` as `host_cookie` and map the cookie names issued by
the host system.

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
| `cookie_name` | Host authentication cookie containing the raw token AtlasClaw forwards for cookie-mode provider access. |
| `subject_cookie_name` | Required stable login identifier used as the AtlasClaw subject. |
| `display_name_cookie_name` | Optional display name shown in AtlasClaw. |
| `user_id_cookie_name` | Optional upstream user ID copied into the authenticated user metadata. |
| `tenant_id_cookie_name` | Optional tenant identifier; AtlasClaw uses `default` when it is absent. |

In `host_cookie` mode, AtlasClaw can still accept a valid AtlasClaw admin JWT
first. This keeps backend management access available while normal embedded
users enter through host cookies.

## Provider Cookie Configuration {#provider-cookie-configuration}

Configure the provider instance with `auth_type: "cookie"` when provider calls
should use the current request cookie.

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

## Host System Requirements {#host-system-requirements}

The embedding host must make the cookie visible to AtlasClaw requests. In
practice, that usually means:

- AtlasClaw is served under the same site, parent domain, or reverse-proxy path
  where the host cookie is in scope.
- Cookie `Path`, `Domain`, `SameSite`, and `Secure` attributes allow the
  browser to send the host cookie to AtlasClaw.
- The host provides a stable subject cookie so AtlasClaw can map the request to
  a workspace user.
- The provider system accepts the same cookie, or the provider package knows
  how to exchange that cookie for the provider-native session it needs.

If AtlasClaw is embedded in a cross-site iframe, browser cookie restrictions
can block the request cookie. Validate the final browser behavior in the target
deployment rather than relying only on server-side configuration.

## Security Notes {#security-notes}

- Treat host cookies as user credentials. Do not log them, store them in memory,
  or expose them in troubleshooting output.
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
| Provider call says missing credentials | Confirm the provider instance selects `auth_type: "cookie"` and that the request contains the host cookie. |
| Provider call is unauthorized | Confirm the target system accepts the forwarded cookie and the upstream user has the required permissions. |
| Works outside iframe but not inside iframe | Check browser `SameSite`, third-party cookie, `Secure`, and domain/path behavior. |
