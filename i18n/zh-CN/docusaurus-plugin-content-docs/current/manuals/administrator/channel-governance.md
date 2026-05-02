---
title: 渠道治理
description: 管理渠道访问和用户自有渠道连接。
sidebar_position: 5
---

# 渠道治理

渠道把 AtlasClaw 连接到外部消息入口。当前包括 DingTalk、Feishu/Lark、WeCom、REST、WebSocket 和 SSE。

## 权限边界 {#permission-boundary}

Channel 访问按 Channel 类型授权。角色只能管理 `channels.channel_permissions` 中显式允许的 Channel 类型。默认 `admin` 和 `user` 角色会初始化为允许所有已注册 Channel 类型。如果角色没有任何允许的 Channel 类型条目，仅拥有该角色的用户不能创建或管理 Channel 连接。

`channels.module_permissions.manage_permissions` 控制谁可以在 Role Management 中配置 Channel 访问模型。它本身不授予所有 Channel 类型的运行时访问权。

渠道记录属于具体用户。除非系统提供显式管理员流程，否则用户不应管理其他人的渠道连接。

## 治理清单 {#governance-checklist}

- 决定哪些角色可以管理 Channel 权限。
- 决定每个角色可以在生产中使用哪些 Channel 类型。
- 要求 Webhook URL 使用 HTTPS。
- 在原 IM 平台轮换凭证。
- 禁用不再使用的连接。

## Channel 所有权模型 {#channel-ownership-model}

Channel 连接是个人运行时绑定。记录中包含名称、类型、启用状态、默认标记、配置 payload、运行时状态和时间戳。配置中的凭证属于创建该连接的用户。

该模型适用于代表个人或由某个用户连接的团队机器人。如果部署需要集中管理 Channel 连接，应记录运维 owner，并避免共享个人密钥。

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

## 生产策略 {#production-policy}

生产 IM 集成应记录：

- 机器人的业务 owner；
- 谁可以轮换上游 app secret 或 webhook secret；
- 哪些 AtlasClaw 角色拥有对应 Channel 类型的访问权；
- 是否允许入站消息，还是仅用于外发；
- 事件期间如何禁用该连接。
