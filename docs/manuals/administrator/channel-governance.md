---
title: Channel Governance
description: Govern channel access and user-owned channel connections.
sidebar_position: 5
---

# Channel Governance

Channels let users connect AtlasClaw to external message surfaces. Current
channel handlers include DingTalk, Feishu/Lark, WeCom, REST, WebSocket, and SSE.

## Permission Boundary {#permission-boundary}

Channel access is granted by channel type. A role can manage only the channel
types that are explicitly allowed in its `channels.channel_permissions` entries.
The default `admin` and `user` roles are initialized with all registered channel
types allowed. If a role has no allowed channel type entries, users with only
that role cannot create or manage channel connections.

`channels.module_permissions.manage_permissions` controls who may configure
the channel access model in Role Management. It does not grant runtime access
to every channel type by itself.

Channel records are user-owned. A user should not manage another user's channel
connections unless the system exposes an explicit administrative workflow for
that purpose.

## Governance Checklist {#governance-checklist}

- Decide which roles may manage channel permissions.
- Decide which channel types each role may use in production.
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

## HA Ownership Policy {#ha-ownership-policy}

In an HA deployment, also record the AtlasClaw runtime node that owns each
Channel. New connections follow the authenticated user's sticky node, and
historical ownerless records are claimed on that user's first Channel API
request. Only the owner node restores and runs an enabled long connection.

HA does not support webhook-mode Channel configurations and does not
automatically transfer ownership after permanent node failure. The production
runbook must therefore cover sticky-session configuration, stable node IDs,
owner-node recovery, and a manually controlled procedure for any stranded
Channel. Do not treat repeated requests against another node as a
failover mechanism; the API rejects an owner mismatch.

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
- which AtlasClaw roles have channel access for the relevant channel type;
- whether inbound messages are allowed or the channel is outbound-only;
- how to disable the connection during an incident.
- the stable HA owner node and recovery procedure, when HA is enabled.
