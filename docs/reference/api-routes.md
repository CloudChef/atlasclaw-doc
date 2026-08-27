---
title: API Routes
description: High-level API route map for AtlasClaw Core.
sidebar_position: 2
---

# API Routes

## Runtime APIs {#runtime-apis}

- `/api/health`
- `/api/agent/capabilities`
- `/api/agent/run`
- `/api/agent/runs/{run_id}`
- `/api/agent/runs/{run_id}/stream`
- `/api/agent/runs/{run_id}/abort`
- `/api/sessions`
- `/api/sessions/{session_key}`
- `/api/sessions/{session_key}/history`
- `/api/sessions/{session_key}/status`
- `/api/sessions/{session_key}/queue`
- `/api/sessions/{session_key}/compact`
- `/api/skills`
- `/api/skills/execute`
- `/api/memory/search`
- `/api/memory/write`

`POST /api/agent/runs/{run_id}/abort` first verifies that the authenticated
user owns the run, requests cooperative cancellation, and returns the run's
actual status. If the run was already terminal, the response preserves that
status rather than always returning `aborted`.

The run stream uses terminal phases including `end`, `aborted`, `error`, and
`timeout`. Clients should preserve already received response content and
reconcile the terminal phase with `/api/agent/runs/{run_id}` when an abort
outcome is uncertain.

## Embed APIs {#embed-apis}

- `/api/embed/bootstrap`
- `/api/embed/context/resolve`

Bootstrap validates the `menu` or `floating` surface against the configured
default embedded Provider. Context resolution accepts a floating surface ID,
page generation, and normalized host path, then returns `resolved`,
`unsupported`, or `unavailable`. See [Embedded Menu and Floating
UI](/provider-integration/embedded-menu-and-floating-ui) for the
Provider route and Context lifecycle contract.

## Auth APIs {#auth-apis}

- `/api/auth/local/login`
- `/api/auth/login`
- `/api/auth/callback`
- `/api/auth/me`
- `/api/auth/logout`

## Management APIs {#management-apis}

- `/api/users`
- `/api/users/me/profile`
- `/api/users/me/avatar`
- `/api/users/me/password`
- `/api/users/me/provider-settings`
- `/api/roles`
- `/api/model-configs`
- `/api/provider-configs`
- `/api/agent-configs`
- `/api/token-configs`
- `/api/channels`

## Channel APIs {#channel-apis}

- `/api/channels`
- `/api/channels/{channel_type}/schema`
- `/api/channels/{channel_type}/connections`
- `/api/channels/{channel_type}/connections/{connection_id}`
- `/api/channels/{channel_type}/validate-config`
- `/api/channels/{channel_type}/connections/{connection_id}/verify`
- `/api/channels/{channel_type}/connections/{connection_id}/enable`
- `/api/channels/{channel_type}/connections/{connection_id}/disable`

The normal channel catalog returns only channel types allowed by the current
user's roles. `include_all=true` returns the full registered catalog only for
users who can manage role permissions or channel permissions. Channel lifecycle
routes require access to the requested `channel_type`.

## Provider Discovery APIs {#provider-discovery-apis}

- `/api/providers`
- `/api/providers/fetch-models`
- `/api/service-providers/available-instances`
- `/api/service-providers/definitions`

## Hook APIs {#hook-apis}

- `/api/hooks/{module}/events`
- `/api/hooks/{module}/pending`
- `/api/hooks/{module}/pending/{pending_id}/confirm`
- `/api/hooks/{module}/pending/{pending_id}/reject`

## Route Usage Notes {#route-usage-notes}

This page is a high-level map, not an OpenAPI replacement. Use the running
service's OpenAPI schema for request and response bodies. Management APIs are
permission-gated, and runtime APIs may still filter skills or provider tools by
role and provider instance access.
