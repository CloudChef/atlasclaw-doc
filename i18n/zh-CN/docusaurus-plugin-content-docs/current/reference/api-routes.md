---
title: API 路由
description: AtlasClaw Core 高层 API 路由地图。
sidebar_position: 2
---

# API 路由

## 运行时 API {#runtime-apis}

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

## 认证 API {#auth-apis}

- `/api/auth/local/login`
- `/api/auth/login`
- `/api/auth/callback`
- `/api/auth/me`
- `/api/auth/logout`

## 管理 API {#management-apis}

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

## Channel API {#channel-apis}

- `/api/channels`
- `/api/channels/{channel_type}/schema`
- `/api/channels/{channel_type}/connections`
- `/api/channels/{channel_type}/connections/{connection_id}`
- `/api/channels/{channel_type}/validate-config`
- `/api/channels/{channel_type}/connections/{connection_id}/verify`
- `/api/channels/{channel_type}/connections/{connection_id}/enable`
- `/api/channels/{channel_type}/connections/{connection_id}/disable`

## Provider 发现 API {#provider-discovery-apis}

- `/api/providers`
- `/api/providers/fetch-models`
- `/api/service-providers/available-instances`
- `/api/service-providers/definitions`

## Hook API {#hook-apis}

- `/api/hooks/{module}/events`
- `/api/hooks/{module}/pending`
- `/api/hooks/{module}/pending/{pending_id}/confirm`
- `/api/hooks/{module}/pending/{pending_id}/reject`

## 使用说明 {#route-usage-notes}

本页是高层路由地图，不替代 OpenAPI。请求和响应结构以运行服务的 OpenAPI schema 为准。管理 API 受权限控制，运行时 API 还会按角色和 Provider 实例访问过滤 Skill 与工具。
