---
title: Provider 实例
description: 配置运行时 Provider 实例。
sidebar_position: 4
---

# Provider 实例

Provider 实例把 AtlasClaw Core 连接到 `providers_root` 中的具体 Provider 包。

## 职责 {#responsibilities}

管理员配置 Provider 实例字段，如 base URL、共享 Provider Token、认证模式、启用状态和实例名。具体字段来自 Provider 的 `provider.schema.json`。

## 运行时访问 {#runtime-access}

Provider 实例配置权限和运行时访问权限是两件事。角色可以被允许管理配置记录，也可以被单独授予某个 Provider 实例的运行时访问权。

这三层需要同时正确：Provider 配置权限允许管理员创建或编辑实例记录；Provider 运行时权限允许用户通过 Agent 调用某个 Provider 实例；Provider 原生凭证决定上游系统最终允许哪些操作。

## 面向 IM 渠道的认证模式 {#auth-mode-for-im-channels}

Provider 被 IM 渠道使用时，需要记住运行时路径：

```text
IM 工具 -> IM 渠道 -> Agent -> Provider
```

IM 渠道不会携带用户在浏览器中的 Cookie，也不会携带目标 Provider 系统的 SSO Token。如果 Provider 必须以单个用户身份调用上游系统，应把 Provider 实例配置为 `auth_type: "user_token"`，并要求用户为对应 Provider 类型和实例名保存 Provider Token。

如果 Provider 使用管理员统一管理的共享凭证，则不需要用户配置个人 Token。这适用于使用 `provider_token`、username/password `credential` 或 `app_credentials` 的 Provider 实例。

## 实例命名 {#instance-naming}

建议使用稳定的环境名称，如 `default`、`prod`、`staging` 或业务单元名。不要把密钥、个人姓名或临时事件写进实例名。Provider 权限和用户凭证会绑定到 Provider 类型加实例名，因此重命名实例应视为访问迁移。

## 配置流程 {#configuration-flow}

1. 确认 Provider 包存在于 `providers_root`。
2. 确认 Provider definition 和 schema 可以被发现。
3. 按 schema 创建 Provider 实例。
4. 给需要使用的角色分配 Provider 运行时访问权。
5. 为这些角色启用对应 Skill。
6. 如果使用用户凭证模式，通知用户配置 Provider Token。
7. 先测试只读 Skill，再开放写操作、审批或修复类流程。

## Provider 专属设置 {#provider-specific-setup}

Provider 专属设置记录在 Provider Integration 章节。具体认证模式、用户 Token 设置、Provider schema 和能力流程应以对应 Provider 章节为准。
