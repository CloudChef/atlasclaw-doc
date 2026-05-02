---
title: 权限
description: 理解 Standard User 权限和访问阻塞。
sidebar_position: 6
---

# 权限

默认 Standard User 角色用于普通协作用户。

## 默认能力 {#default-access}

默认情况下，Standard User 可以：

- 使用角色和 Provider 访问允许的技能与 Provider 能力；
- 管理角色允许的 Channel 类型下自己的连接；
- 管理自己的账号资料和 Provider Token。

## 默认不包含 {#not-included-by-default}

默认情况下，Standard User 不能管理：

- 用户；
- 角色；
- 模型配置；
- Provider 实例配置；
- Skill 管理或权限页面；
- 权限模型。

如果需要管理页面或 Provider 实例访问权，请联系管理员。

## 运行时访问如何生效 {#how-runtime-access-works}

一次成功的 Provider 请求通常需要这些条件：

1. 该 Skill 对你的角色启用。
2. 你的角色可以访问目标 Provider 实例。
3. Provider 实例启用且配置正确。
4. 如果请求来自 IM Channel，该 Channel 类型对你的角色开放。
5. 如果 Provider 使用用户凭证，你的上游凭证有效。

任何一层缺失，Agent 都应报告阻塞原因，而不是猜测执行。

## 向管理员求助时提供什么 {#what-to-send-an-administrator}

请提供尝试的操作、期望使用的 Provider 或 Channel、完整阻塞提示、问题发生在 Web Chat 还是 IM Chat，以及是否已保存所需 Provider Token。不要提供密钥、API Token、Cookie 或 Webhook URL。
