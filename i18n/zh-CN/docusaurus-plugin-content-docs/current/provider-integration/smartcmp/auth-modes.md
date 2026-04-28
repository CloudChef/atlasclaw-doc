---
title: 认证模式
description: SmartCMP 认证模式和必填字段。
sidebar_position: 3
---

# 认证模式

每个 SmartCMP 实例都需要 `base_url`。认证模式决定还需要哪些凭证字段。

| 模式 | `auth_type` | 必填字段 | 范围 |
| --- | --- | --- | --- |
| Provider Token | `provider_token` | `provider_token` | 实例 |
| User Token | `user_token` | `user_token` | 用户 |
| Cookie | `cookie` | `cookie` 或请求 Cookie/Token | 实例或请求 |
| Credential | `credential` | `username`、`password` | 实例 |

Provider schema 默认使用 `user_token`。

## Auth URL {#auth-url}

`auth_url` 是可选字段。私有 SmartCMP 部署使用非标准登录端点时应显式配置。

## 如何选择模式 {#choosing-a-mode}

| 需求 | 推荐模式 |
| --- | --- |
| 每个操作都使用用户自己的 SmartCMP 身份 | User Token |
| 允许所有用户共享一个服务账号 Token | Provider Token |
| AtlasClaw 嵌入在 SmartCMP 后面并接收请求 Cookie | Cookie |
| 使用机器人账号登录并缓存会话 | Credential |

User Token 是默认模式，便于保持 SmartCMP 用户级审计。Provider Token 和 Credential 更容易运维，但需要按审计和职责分离要求评估。
