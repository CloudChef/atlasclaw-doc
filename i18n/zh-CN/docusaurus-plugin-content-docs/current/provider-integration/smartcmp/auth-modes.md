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
| 每次 Provider 调用时使用机器人账号登录 | Credential |

User Token 是默认模式，便于保持 SmartCMP 用户级审计。Provider Token 和 Credential 更容易运维，但需要按审计和职责分离要求评估。

## AtlasClaw 选择与 Provider 执行 {#fallback-behavior}

SmartCMP `auth_type` 在 AtlasClaw Provider 源配置中可以是单一模式，也可以是有序链。AtlasClaw Core 按配置顺序选择当前请求中必填字段可用的第一个模式：

1. Provider Token 需要 `provider_token`。
2. User Token 需要用户保存的 `user_token`。
3. Cookie 需要请求级 Token/Cookie 或配置的 `cookie`。
4. Credential 需要 `username` 和 `password`。

在正常 AtlasClaw Skill 路径中，Core 会删除未选中模式的凭证字段，只向 SmartCMP callable 传入一个已经选定的 `auth_type`。SmartCMP Provider 执行该清理后的模式，不会收到或解释原始有序列表。独立 MCP binding 也会在每个 Authentication Context 中携带一个显式模式。

直接集成也应使用同一个显式 Authentication Context 契约。AtlasClaw 兼容 Resolver 在收到旧版、未清理的配置时，仍可能推断凭证或执行 Credential 登录；这是兼容行为，不是第二套 MCP 认证链，也不是正常 AtlasClaw 路径使用的契约。

AtlasClaw 源配置中的认证链应保持简短、明确。Credential 模式每次 Provider 调用只执行一次 SmartCMP 登录，返回的会话只在本次请求中使用，不写入 Provider Cookie cache。
