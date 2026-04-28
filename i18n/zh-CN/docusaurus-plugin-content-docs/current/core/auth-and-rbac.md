---
title: 认证和 RBAC
description: 认证、影子用户、角色和权限控制。
sidebar_position: 2
---

# 认证和 RBAC

AtlasClaw 区分认证和 workspace 授权。

## 认证 {#authentication}

认证从本地登录、Host Cookie、OIDC、SSO 或其他 Provider 中解析当前用户。运行时会得到包含用户 ID、显示名、租户、角色、Token、Provider subject 和认证类型的 `UserInfo`。

认证回答“请求是谁发起的”。它不会自动授予管理员权限。认证完成后，AtlasClaw 解析 workspace 角色并计算有效权限。

## 影子用户 {#shadow-users}

外部身份可以映射为内部影子用户，使会话、记忆和用户设置在外部身份系统之外保持稳定。

## Workspace 授权 {#workspace-authorization}

Workspace 角色授予管理权限，例如 `users.view`、`roles.edit`、`channels.create` 或 `model_configs.delete`。

Provider 运行时操作仍然继承认证用户在上游系统中的访问权。AtlasClaw 不能用 workspace 管理员身份绕过 Provider 侧 RBAC。

## 有效权限 {#effective-permissions}

用户拥有多个角色时会合并权限。布尔权限采用 OR 语义。Provider 实例拒绝只有在所有活跃角色都拒绝同一实例时才生效。

Skill 权限使用逐 Skill 条目表示。Provider 运行时权限使用 Provider 类型加实例名表示，因此可以分别控制 Skill 可见性和实例访问权。

## 内置角色规则 {#built-in-role-rules}

内置 `admin` 和 `user` 角色由系统管理。其元数据和大多数模块权限会被恢复到默认形态。Skill 和 Provider 等运行时访问模块仍可配置。

## 执行检查点 {#request-enforcement-points}

| 层级 | 示例 |
| --- | --- |
| API 路由 | `agent_configs.create`、`roles.edit`、`channels.delete` |
| UI 导航 | 根据模块 view 权限显示或隐藏管理页面。 |
| Skill Registry | 只向 Agent 暴露启用且授权的 Skill。 |
| Provider Registry | 只暴露用户可访问的 Provider 实例。 |
| Provider API | 执行上游系统自己的 RBAC。 |
