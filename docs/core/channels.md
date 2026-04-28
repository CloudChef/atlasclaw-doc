---
title: Channels
description: Channel runtime, supported handlers, and user-owned connections.
sidebar_position: 7
---

# Channels

Channels connect AtlasClaw to web, API, webhook, and IM entry points.

## Channel Types {#channel-types}

Current handlers include:

- DingTalk
- Feishu/Lark
- WeCom
- REST
- WebSocket
- SSE

Planned or UI-only channel cards must not be documented as available runtime
handlers unless the backend exposes them through the channel registry.

## User Ownership {#user-ownership}

Channel connections are stored per user. The channel API lists and manages
connections for the authenticated user.

Each channel connection has a channel type, display name, enabled flag,
configuration payload, runtime state, and timestamps. Long-connection handlers
establish persistent connections. Webhook-style handlers validate endpoint
configuration and process inbound or outbound messages according to their mode.

## Connection Lifecycle {#connection-lifecycle}

Users with channel permissions can list channel types, fetch a schema, create a
connection, validate config, verify a saved connection, enable or disable it,
edit it, and delete it.

## Message Model {#message-model}

Inbound messages normalize external events into common fields such as
`message_id`, `sender_id`, `sender_name`, `chat_id`, `channel_type`, `content`,
`content_type`, `thread_id`, metadata, and timestamp. Outbound messages carry
the target chat, content, optional thread information, and metadata.

This model lets the agent runtime treat web chat, IM messages, and API-triggered
messages consistently while still allowing channel handlers to manage their own
platform-specific details.

## Operational Checks {#operational-checks}

- Confirm the user owns the channel connection being edited.
- Validate required fields before enabling a connection.
- Prefer HTTPS webhook endpoints.
- Disable unused long-connection channels to reduce background load.
- Keep provider tokens separate from channel credentials.
