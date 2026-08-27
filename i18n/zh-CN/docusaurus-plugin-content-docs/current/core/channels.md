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

Channel catalog 会按当前用户的有效角色权限过滤。只有至少一个活跃角色在 `channels.channel_permissions` 中允许对应 Channel 类型时，用户才能列出该类型、获取 schema、创建连接、验证配置、检查已保存连接、启用、禁用、编辑和删除连接。

Channel catalog 的 `include_all=true` 是治理视图，仅对可以管理角色权限或 Channel 权限的用户开放。

## HA 节点所有权 {#ha-node-ownership}

HA 模式中，每个 Channel 连接都有 runtime owner node。新连接分配给当前用户粘性会话所在节点；没有 owner 的历史连接会在该用户首次请求 Channel API 时完成分配，之后只在被分配节点启动已启用连接。

HA 只接受注册 Handler 识别为 long-connection 的连接模式。即使同一 Handler 在单机模式支持 Webhook，Webhook 模式在 HA 中仍会被拒绝。Owner node 永久故障后，AtlasClaw 不会自动把 Channel 迁移到其他节点；运维人员必须恢复原节点，或按部署方受控的恢复流程处理。

当前粘性节点和记录的 owner 不一致时，Channel API 会安全拒绝。用户的 Channel 管理流量和持久连接生命周期必须保持在同一节点。

## 消息模型 {#message-model}

Inbound message 会归一化为 `message_id`、`sender_id`、`sender_name`、`chat_id`、`channel_type`、`content`、`content_type`、`thread_id`、metadata 和 timestamp 等字段。Outbound message 包含目标 chat、内容、线程信息和 metadata。

## 运维检查 {#operational-checks}

- 确认用户正在编辑自己拥有的连接。
- 启用前校验必填字段。
- 生产环境优先使用 HTTPS Webhook。
- 不使用的长连接应禁用。
- Provider Token 和 Channel 凭证分开管理。
