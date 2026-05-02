---
title: 用户和角色
description: 管理用户、内置角色和权限。
sidebar_position: 2
---

# 用户和角色

AtlasClaw 使用 workspace 角色控制管理权限。Provider 运行时操作仍然继承认证用户在上游系统中的真实权限。

## 内置角色 {#built-in-roles}

| 角色 | 标识符 | 用途 |
| --- | --- | --- |
| Administrator | `admin` | 管理 workspace 配置和访问控制。 |
| Standard User | `user` | 默认协作角色，拥有已注册 Skill、Provider 实例和 Channel 类型的运行时访问权。 |
| Viewer | `viewer` | 审计和监督场景的只读角色。 |

## 用户管理 {#user-management}

管理员可以创建用户、编辑资料、修改认证类型、启用或禁用账号、分配角色，以及删除非自己的账号。

本地认证用户的资料和密码生命周期由 AtlasClaw 管理。SSO 或 host-cookie 用户的登录凭证仍由上游身份系统管理，AtlasClaw 只保存 workspace 侧资料和角色映射。

删除或停用用户前，应检查该用户是否拥有仍在使用的 Channel 连接、Provider Token 或需要审计的会话数据。

## 权限模型 {#permission-model}

权限按模块分组，包括 `users`、`roles`、`channels`、`tokens`、`agent_configs`、`provider_configs`、`model_configs`、`skills` 和 `providers`。

## 内置角色行为 {#built-in-role-behavior}

内置 `admin` 和 `user` 角色由系统管理。它们的元数据只读。Skill、Provider 和 Channel 的运行时访问模块会从已注册目录初始化，以便管理员控制用户实际能执行哪些能力。

不要通过修改内置 Standard User 来表达复杂策略。需要自定义管理策略时，应创建新的自定义角色。

## 创建自定义角色 {#creating-a-custom-role}

1. 选择稳定的 `identifier`，创建后不要再修改。
2. 只授予该角色职责所需的模块权限。
3. 添加该角色可用的 Skill 权限。
4. 如果该角色需要执行 Provider Skill，添加 Provider 运行时访问权。
5. 添加该角色可以管理的 IM Channel 类型。
6. 给测试用户分配角色，验证 UI 和 Chat 运行时表现。

## 权限示例 {#permission-examples}

| 需求 | 可考虑的权限 |
| --- | --- |
| 管理用户但不管理模型 | `users.view`、`users.create`、`users.edit`、`users.assign_roles` |
| 运维 Provider 实例 | `provider_configs.view`、`provider_configs.create`、`provider_configs.edit` |
| 授予 Provider 运行时访问权 | `providers.manage_permissions` 加 Provider permission 条目 |
| 管理模型端点 | `model_configs.view`、`model_configs.create`、`model_configs.edit`、`model_configs.delete` |
| 允许个人 Channel 设置 | 对允许的 Channel 类型添加 `channels.channel_permissions` 条目 |

## 访问问题排查 {#troubleshooting-access}

用户能看到 Skill 但无法完成 Provider 请求时，检查四层：角色启用了该 Skill、角色能访问目标 Provider 实例、IM 请求使用的 Channel 类型对角色开放、用户已配置 Provider 需要的有效凭证。
