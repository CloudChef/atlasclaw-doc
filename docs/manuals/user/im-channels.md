---
title: IM Channels
description: Configure personal DingTalk, Feishu/Lark, and WeCom connections.
sidebar_position: 5
---

# IM Channels

With the default Standard User role, you can manage your own channel
connections. The built-in `user` role is system-managed, so this default should
be treated as a product default unless the deployment defines custom role policy.

## User Workflow {#user-workflow}

1. Open `/channels`.
2. Select a channel type.
3. Create a connection.
4. Choose a connection mode.
5. Fill in the required fields.
6. Validate or verify the configuration.
7. Enable, disable, edit, or delete the connection as needed.

The connection name is for your own administration. Use a name that identifies
the upstream bot or group, such as `team-oncall-dingtalk` or `personal-feishu`.

## DingTalk {#dingtalk}

| Mode | Required fields | Notes |
| --- | --- | --- |
| Stream | `client_id`, `client_secret` | Enterprise bot long connection. |
| Webhook | `webhook_url` | Outbound webhook robot. |
| Webhook with signing | `webhook_url`, optional `secret` | `secret` is the DingTalk signing secret. |

Use Stream mode when AtlasClaw should receive and respond to messages through a
DingTalk enterprise bot. Use Webhook mode when AtlasClaw only needs to send
messages to a DingTalk robot endpoint.

## Feishu/Lark {#feishu-lark}

| Mode | Required fields | Notes |
| --- | --- | --- |
| Long Connection | `app_id`, `app_secret` | Enterprise app long connection. |
| Webhook | `webhook_url` | Custom bot webhook. |

Long Connection mode is appropriate for interactive bot conversations. Webhook
mode is simpler and useful for outbound notification flows.

## WeCom {#wecom}

| Mode | Required fields | Notes |
| --- | --- | --- |
| WebSocket | `bot_id`, `bot_secret` | Intelligent robot long connection. |
| Webhook | `webhook_url` | Group bot webhook. |

WebSocket mode supports bidirectional intelligent robot conversations. Webhook
mode sends messages to a group bot endpoint.

## Enable, Disable, Edit, Delete {#enable-disable-edit-delete}

Disable a channel when you want to keep the configuration but stop runtime use.
Edit a channel when rotating credentials or changing the endpoint. Delete a
channel when the bot is retired or the connection should no longer exist.

After editing credentials, run validation again before relying on the channel.

## Credential Boundary {#credential-boundary}

Channel credentials are user-owned channel connection settings. Provider tokens
are configured separately under Provider Tokens.

Do not paste channel secrets into chat. Store them only in the channel
configuration form.
