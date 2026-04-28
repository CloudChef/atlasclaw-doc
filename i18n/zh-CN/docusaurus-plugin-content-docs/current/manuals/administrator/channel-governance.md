---
title: 渠道治理
description: 管理渠道访问和用户自有渠道连接。
sidebar_position: 5
---

# 渠道治理

渠道把 AtlasClaw 连接到外部消息入口。当前包括 DingTalk、Feishu/Lark、WeCom、REST、WebSocket 和 SSE。

## 权限边界 {#permission-boundary}

默认 Standard User 角色可以查看、创建、编辑和删除自己的渠道连接。内置 `user` 角色由系统管理；如果部署需要不同策略，应使用自定义角色或明确的运行时变更，而不是把内置角色当作可自由编辑的角色。

渠道记录属于具体用户。除非系统提供显式管理员流程，否则用户不应管理其他人的渠道连接。

## 治理清单 {#governance-checklist}

- 决定哪些角色可以创建和编辑渠道。
- 决定哪些 IM 平台允许用于生产。
- 要求 Webhook URL 使用 HTTPS。
- 在原 IM 平台轮换凭证。
- 禁用不再使用的连接。

## Channel 所有权模型 {#channel-ownership-model}

Channel 连接是个人运行时绑定。记录中包含名称、类型、启用状态、默认标记、配置 payload、运行时状态和时间戳。配置中的凭证属于创建该连接的用户。

## 连接校验 {#validating-connections}

`/channels` 工作流提供 schema 表单校验和已保存连接验证。校验会检查必填字段和明显 URL 问题，验证会通过后端 handler 检查已保存连接。

| Channel | 模式 | 必填字段 |
| --- | --- | --- |
| DingTalk | Stream | `client_id`、`client_secret` |
| DingTalk | Webhook | `webhook_url` |
| Feishu/Lark | Long Connection | `app_id`、`app_secret` |
| Feishu/Lark | Webhook | `webhook_url` |
| WeCom | WebSocket | `bot_id`、`bot_secret` |
| WeCom | Webhook | `webhook_url` |

生产环境 Webhook URL 应使用 HTTPS。
