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

## 运行时调用路径 {#runtime-path}

IM 对话通过下面的路径触达 Provider 能力：

```text
IM 工具 -> IM 渠道 -> Agent -> Provider
```

DingTalk、Feishu/Lark 或 WeCom 机器人等 IM 工具先把消息送到 AtlasClaw IM 渠道。渠道解析用户和会话后，把这一轮对话交给 Agent。当 Agent 需要查询或操作外部系统时，再调用 Provider Skill。

这和用户在浏览器或宿主系统内嵌页面中打开 AtlasClaw 不同。IM 消息不会携带用户在目标 Provider 系统中的浏览器 Cookie 或 SSO Token。因此，如果 Provider 必须以真实用户身份调用上游系统，管理员应把 Provider 实例配置为 `auth_type: "user_token"`，并要求每个用户保存自己的 Provider Token。

如果 Provider 实例使用管理员统一配置的共享凭证，则用户不需要配置个人 Provider Token。例如 `provider_token`、带 username/password 的 `credential`，或 `app_credentials`。这些模式下，Provider 调用会使用配置好的共享身份或机器人身份，并继续受目标系统自身权限控制。

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
