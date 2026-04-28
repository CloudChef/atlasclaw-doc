---
title: IM 渠道
description: 配置个人 DingTalk、Feishu/Lark 和 WeCom 连接。
sidebar_position: 5
---

# IM 渠道

默认 Standard User 角色可以管理自己的渠道连接。内置 `user` 角色由系统管理，因此这项能力应视为产品默认行为，除非部署定义了自定义角色策略。

## 用户流程 {#user-workflow}

1. 打开 `/channels`。
2. 选择渠道类型。
3. 创建连接。
4. 选择连接模式。
5. 填写必填字段。
6. 验证或检查配置。
7. 根据需要启用、禁用、编辑或删除连接。

连接名称只用于你自己管理。建议使用能识别上游机器人或群组的名称，例如 `team-oncall-dingtalk` 或 `personal-feishu`。

## DingTalk {#dingtalk}

| 模式 | 必填字段 | 说明 |
| --- | --- | --- |
| Stream | `client_id`、`client_secret` | 企业机器人长连接。 |
| Webhook | `webhook_url` | 外发 Webhook 机器人。 |
| Webhook 签名 | `webhook_url`，可选 `secret` | `secret` 是 DingTalk 签名密钥。 |

需要 AtlasClaw 通过 DingTalk 企业机器人收发消息时使用 Stream；只需要向机器人地址发送消息时使用 Webhook。

## Feishu/Lark {#feishu-lark}

| 模式 | 必填字段 | 说明 |
| --- | --- | --- |
| Long Connection | `app_id`、`app_secret` | 企业应用长连接。 |
| Webhook | `webhook_url` | 自定义机器人 Webhook。 |

Long Connection 适合交互式机器人对话；Webhook 更适合简单外发通知。

## WeCom {#wecom}

| 模式 | 必填字段 | 说明 |
| --- | --- | --- |
| WebSocket | `bot_id`、`bot_secret` | 智能机器人长连接。 |
| Webhook | `webhook_url` | 群机器人 Webhook。 |

WebSocket 支持双向智能机器人会话；Webhook 用于向群机器人 endpoint 发送消息。

## 启用、禁用、编辑和删除 {#enable-disable-edit-delete}

禁用连接会保留配置但停止运行时使用。轮换凭证或变更 endpoint 时编辑连接。机器人退役或连接不再需要时删除连接。编辑凭证后，应重新验证配置。

## 凭证边界 {#credential-boundary}

渠道凭证属于用户自有渠道连接设置。Provider Token 在 Provider Tokens 中单独配置。

不要把 Channel secret 粘贴到对话中，只应保存在 Channel 配置表单里。
