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
