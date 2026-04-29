---
title: Admin Configuration
description: Configure SmartCMP provider instances as an administrator.
sidebar_position: 4
---

# Admin Configuration

Administrators create SmartCMP provider instances under Provider Instances.

## User Token Mode {#user-token-mode}

Use this when each AtlasClaw user must provide a personal SmartCMP token:

```json
{
  "service_providers": {
    "smartcmp": {
      "default": {
        "base_url": "${CMP_URL}",
        "auth_type": "user_token"
      }
    }
  }
}
```

## Provider Token Mode {#provider-token-mode}

Use this when a shared SmartCMP token is acceptable:

```json
{
  "service_providers": {
    "smartcmp": {
      "default": {
        "base_url": "${CMP_URL}",
        "auth_type": "provider_token",
        "provider_token": "${CMP_PROVIDER_TOKEN}"
      }
    }
  }
}
```

## Robot Profiles for Webhook Skills {#robot-profiles-for-webhook-skills}

Use a SmartCMP robot profile when an external webhook triggers backend skills
that must execute as a SmartCMP robot or administrator account. The provider
instance can keep its normal interactive auth mode, while `robot_auth` defines
the credential used only for authorized webhook robot execution.

```json
{
  "service_providers": {
    "smartcmp": {
      "cmp": {
        "base_url": "${CMP_URL}",
        "auth_type": "user_token",
        "robot_auth": {
          "preapproval_bot": {
            "auth_type": "provider_token",
            "provider_token": "${CMP_ROBOT_APPROVER_TOKEN}",
            "allowed_skills": [
              "smartcmp:preapproval-agent",
              "smartcmp:request-decomposition-agent"
            ]
          }
        }
      }
    }
  }
}
```

Recommended SmartCMP robot credentials use `cmp_tk_*` tokens. SmartCMP scripts
send those tokens as `Authorization: Bearer <token>`. SmartCMP audit trails
should show the configured robot/admin account for approval actions and for
webhook request submissions that do not forward SmartCMP user cookies.

The webhook payload must include the selected provider instance and robot
profile:

```json
{
  "skill": "smartcmp:preapproval-agent",
  "args": {
    "provider_instance": "cmp",
    "robot_profile": "preapproval_bot",
    "request_id": "REQ-10001"
  }
}
```

See [Webhook Robot Execution](/provider-integration/webhook-robot-execution)
for the generic webhook configuration and security rules.

## Cookie or Credential Mode {#cookie-or-credential-mode}

Cookie mode uses a SmartCMP session cookie. Credential mode logs in with
username and password and may cache a runtime cookie.

Use user token mode when you need clean per-user accountability.

## Required Instance Fields {#required-instance-fields}

Every SmartCMP instance requires `base_url`. The schema default is
`https://console.smartcmp.cloud`, but production deployments should set the URL
that matches their SmartCMP environment.

| Field | Scope | Required when |
| --- | --- | --- |
| `base_url` | Instance | Always |
| `auth_type` | Instance | Always; defaults to `user_token` |
| `user_token` | User | `auth_type` is `user_token` |
| `provider_token` | Instance | `auth_type` is `provider_token` |
| `cookie` | Instance or request | `auth_type` is `cookie` |
| `username`, `password` | Instance | `auth_type` is `credential` |
| `auth_url` | Instance | Optional override for non-standard login endpoints |
| `timeout` | Instance | Optional request timeout |

## Admin Setup Flow {#admin-setup-flow}

1. Confirm SmartCMP network access from the AtlasClaw backend.
2. Choose an auth mode.
3. Create the SmartCMP provider instance.
4. Grant provider runtime access to the roles that should use it.
5. Enable SmartCMP skills for those roles.
6. In user-token mode, instruct users to configure their personal token.
7. Test a read-only datasource or resource-pool query before enabling request,
   approval, resource operation, or remediation workflows.

## Security Notes {#security-notes}

- Do not store user-specific SmartCMP tokens in provider instance fields.
- Prefer user-token mode when SmartCMP audit trails must identify the real user.
- Rotate provider-token, cookie, and credential-mode secrets through the
  administrator workflow.
- Keep `auth_url` explicit for private deployments with unusual login routing.
