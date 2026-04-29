---
title: Webhook Robot Execution
description: Configure webhook-triggered backend skills to run with scoped robot credentials.
sidebar_position: 4
---

# Webhook Robot Execution

Webhook robot execution lets an external system call a provider-qualified
backend skill while the provider action runs as a configured robot account.
Use this when the upstream system sends an event, but the provider call must be
auditable inside the target system as a service or robot identity.

## When to Use It {#when-to-use-it}

Use webhook robot execution for backend automation such as:

- approval pre-review from an upstream workflow event;
- request decomposition or request creation from an external intake system;
- compliance or remediation workflows where the provider requires a privileged
  service identity.

Do not use it to impersonate an end user. If provider audit trails must show
the individual user, use user-token or request-scoped authentication instead.

## Configuration Shape {#configuration-shape}

Configure two independent allowlists:

- `webhook.systems[].allowed_skills` controls which skills the webhook system
  may invoke.
- `service_providers.<provider>.<instance>.robot_auth.<profile>.allowed_skills`
  controls which skills may use that robot credential.

Example:

```json
{
  "service_providers": {
    "example_provider": {
      "default": {
        "base_url": "${PROVIDER_URL}",
        "auth_type": "user_token",
        "robot_auth": {
          "backend_bot": {
            "auth_type": "provider_token",
            "provider_token": "${PROVIDER_ROBOT_TOKEN}",
            "allowed_skills": [
              "example_provider:backend-agent"
            ]
          }
        }
      }
    }
  },
  "webhook": {
    "enabled": true,
    "header_name": "X-AtlasClaw-SK",
    "systems": [
      {
        "system_id": "external-review",
        "enabled": true,
        "sk_env": "ATLASCLAW_WEBHOOK_SK_EXTERNAL_REVIEW",
        "default_agent_id": "main",
        "allowed_skills": [
          "example_provider:backend-agent"
        ]
      }
    ]
  }
}
```

Store `PROVIDER_ROBOT_TOKEN` and `ATLASCLAW_WEBHOOK_SK_EXTERNAL_REVIEW` in the
deployment environment, not in the JSON file.

## Webhook Payload {#webhook-payload}

The webhook request selects the skill, provider instance, and robot profile:

```json
{
  "skill": "example_provider:backend-agent",
  "args": {
    "provider_instance": "default",
    "robot_profile": "backend_bot",
    "request_id": "REQ-10001"
  }
}
```

Use `provider_instance` for robot execution. The older shorthand `instance` is
not a robot profile selector.

## Runtime Flow {#runtime-flow}

For a robot webhook dispatch, AtlasClaw:

1. Authenticates the webhook secret from the configured header.
2. Confirms the requested skill is allowed for the webhook system.
3. Resolves `args.provider_instance` under the target provider type.
4. Resolves `args.robot_profile` under that provider instance.
5. Confirms the robot profile allows the requested skill.
6. Builds a runtime-only provider config containing the selected instance and
   selected robot credential.
7. Starts the provider tool process with `ATLASCLAW_PROVIDER_CONFIG`,
   `ATLASCLAW_PROVIDER_TYPE`, `ATLASCLAW_PROVIDER_INSTANCE`, and
   `ATLASCLAW_ROBOT_PROFILE`.

Robot credentials are not added to the prompt. Token, password, and cookie-like
values are redacted from webhook arguments, traces, and API responses.

## Security Requirements {#security-requirements}

- Keep webhook secrets and robot credentials in environment variables.
- Keep robot profile allowlists narrow; create separate profiles for separate
  authority levels.
- Use a provider-native robot account whose upstream permissions match the
  automated workflow.
- Rotate robot credentials through the provider owner's operational process.
- Review provider-specific documentation before enabling mutating skills.

For SmartCMP-specific setup, see
[SmartCMP Admin Configuration](/provider-integration/smartcmp/admin-configuration).
