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
