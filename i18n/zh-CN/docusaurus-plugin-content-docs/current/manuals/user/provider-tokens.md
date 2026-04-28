---
title: Provider Token
description: 配置个人 Provider Token。
sidebar_position: 4
---

# Provider Token

Provider Token 是用户自有凭证，用于需要按用户认证的 Provider 实例。

## 什么时候配置 Token {#when-to-configure-a-token}

当出现以下情况时需要配置：

- Provider 实例使用 user token 认证；
- Agent 提示你的 user token 缺失、无效、被拒绝或已过期；
- 管理员告知某个 Provider 需要用户自有凭证。

## Provider 专属说明 {#provider-specific-instructions}

每个 Provider 都会定义自己的 Token 类型、校验规则和轮换流程。如果某个 Provider 需要额外字段或设置步骤，请以 Provider Integration 下的专属指南为准。

渠道凭证是另一类设置，应在 Channels 中配置，而不是 Provider Tokens。

## Token 配置流程 {#token-workflow}

1. 向管理员确认哪个 Provider 实例需要用户 Token。
2. 从上游 Provider 系统获取 Token。
3. 打开 Account Settings，找到 Provider Tokens。
4. 选择 Provider 类型和实例名。
5. 粘贴 Token 并保存。
6. 重试之前失败的对话请求。

Provider Token 绑定到 Provider 类型和实例名。如果管理员创建了新的 Provider 实例，即使上游 Token 值相同，也可能需要为新实例重新保存。

## 轮换 {#rotation}

当上游 Provider 过期、组织要求定期轮换、怀疑 Token 泄露，或请求开始返回认证错误时，应轮换 Provider Token。轮换后先测试只读操作，再执行写操作。
