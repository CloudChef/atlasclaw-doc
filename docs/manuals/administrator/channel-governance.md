---
title: Channel Governance
description: Govern channel access and user-owned channel connections.
sidebar_position: 5
---

# Channel Governance

Channels let users connect AtlasClaw to external message surfaces. Current
channel handlers include DingTalk, Feishu/Lark, WeCom, REST, WebSocket, and SSE.

## Permission Boundary {#permission-boundary}

The default Standard User role can view, create, edit, and delete its own
channel connections. The built-in `user` role is system-managed, so deployments
that need a different policy should use custom roles or a deliberate runtime
change instead of treating the built-in role as freely editable.

Channel records are user-owned. A user should not manage another user's channel
connections unless the system exposes an explicit administrative workflow for
that purpose.

## Governance Checklist {#governance-checklist}

- Decide which roles may create and edit channels.
- Decide which IM platforms are approved for production use.
- Require HTTPS webhook URLs.
- Rotate IM credentials through the platform that issued them.
- Disable unused connections.

## Channel Ownership Model {#channel-ownership-model}

Channel connections are personal runtime bindings. A channel record stores a
name, channel type, enabled state, default flag, configuration payload, runtime
state, and timestamps. Credentials in the configuration payload belong to the
user who created the connection.

Use this model for IM bots that represent a user or a team-owned bot connected
by a specific user. If a deployment needs centrally managed channel
connections, document the operational owner and avoid sharing personal secrets.

## Validating Connections {#validating-connections}

The `/channels` workflow exposes both schema-driven form validation and saved
connection verification. Validation checks required fields and obvious URL
problems. Verification exercises the saved connection through the backend
handler.

Common validation rules:

| Channel | Mode | Required fields |
| --- | --- | --- |
| DingTalk | Stream | `client_id`, `client_secret` |
| DingTalk | Webhook | `webhook_url` |
| Feishu/Lark | Long Connection | `app_id`, `app_secret` |
| Feishu/Lark | Webhook | `webhook_url` |
| WeCom | WebSocket | `bot_id`, `bot_secret` |
| WeCom | Webhook | `webhook_url` |

Webhook URLs must be HTTP or HTTPS URLs and should use HTTPS in production.

## Production Policy {#production-policy}

For production IM integrations, record:

- the business owner of the bot;
- who can rotate the upstream app secret or webhook secret;
- which AtlasClaw role can create or edit the connection;
- whether inbound messages are allowed or the channel is outbound-only;
- how to disable the connection during an incident.
