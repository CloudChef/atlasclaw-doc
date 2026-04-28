---
title: 渠道
description: 渠道运行时、支持的 handler 和用户自有连接。
sidebar_position: 7
---

# 渠道

渠道把 AtlasClaw 连接到 Web、API、Webhook 和 IM 入口。

## 渠道类型 {#channel-types}

当前 handler 包括：

- DingTalk
- Feishu/Lark
- WeCom
- REST
- WebSocket
- SSE

只有后端 Channel Registry 暴露的 handler 才应作为可用运行时渠道记录。

## 用户归属 {#user-ownership}

渠道连接按用户存储。渠道 API 会列出并管理认证用户自己的连接。

每个 Channel 连接包含类型、名称、启用标记、配置 payload、运行时状态和时间戳。长连接 handler 会建立持久连接，Webhook 类 handler 会校验 endpoint 并处理对应方向的消息。

## 连接生命周期 {#connection-lifecycle}

拥有渠道权限的用户可以列出渠道类型、获取 schema、创建连接、验证配置、检查已保存连接、启用、禁用、编辑和删除连接。

## 消息模型 {#message-model}

Inbound message 会归一化为 `message_id`、`sender_id`、`sender_name`、`chat_id`、`channel_type`、`content`、`content_type`、`thread_id`、metadata 和 timestamp 等字段。Outbound message 包含目标 chat、内容、线程信息和 metadata。

## 运维检查 {#operational-checks}

- 确认用户正在编辑自己拥有的连接。
- 启用前校验必填字段。
- 生产环境优先使用 HTTPS Webhook。
- 不使用的长连接应禁用。
- Provider Token 和 Channel 凭证分开管理。
