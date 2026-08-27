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

`POST /api/agent/runs/{run_id}/abort` 会先校验认证用户拥有该 run，再请求协作式取消，并返回 run 的实际状态。如果 run 已经结束，响应会保留该终态，不会固定返回 `aborted`。

Run stream 的终止 phase 包括 `end`、`aborted`、`error` 和 `timeout`。客户端应保留已收到的回复内容；abort 结果不确定时，使用 `/api/agent/runs/{run_id}` 对账最终状态。

## Embed API {#embed-apis}

- `/api/embed/bootstrap`
- `/api/embed/context/resolve`

Bootstrap 使用已配置的默认内嵌 Provider 分别校验独立的 `menu` 或 `floating` 界面。两支 UI 使用相同的企业系统 Cookie 认证；Context 解析只服务悬浮 UI，接收界面 ID、页面 generation 和标准化企业系统路径，并返回 `resolved`、`unsupported` 或 `unavailable`。Provider 路由和 Context 生命周期契约详见[内嵌菜单与悬浮 UI](/provider-integration/embedded-menu-and-floating-ui)。

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

普通 Channel catalog 只返回当前用户角色允许的 Channel 类型。只有可以管理角色权限或 Channel 权限的用户，才能通过 `include_all=true` 查看完整已注册 catalog。Channel lifecycle 路由要求用户有对应 `channel_type` 的访问权。

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
