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
| Standard User | `user` | 默认协作角色，可使用已启用技能并管理自己的渠道连接。 |
| Viewer | `viewer` | 审计和监督场景的只读角色。 |

## 用户管理 {#user-management}

管理员可以创建用户、编辑资料、修改认证类型、启用或禁用账号、分配角色，以及删除非自己的账号。

本地认证用户的资料和密码生命周期由 AtlasClaw 管理。SSO 或 host-cookie 用户的登录凭证仍由上游身份系统管理，AtlasClaw 只保存 workspace 侧资料和角色映射。

删除或停用用户前，应检查该用户是否拥有仍在使用的 Channel 连接、Provider Token 或需要审计的会话数据。

## 权限模型 {#permission-model}

权限按模块分组，包括 `users`、`roles`、`channels`、`tokens`、`agent_configs`、`provider_configs`、`model_configs`、`skills` 和 `providers`。

## 内置角色行为 {#built-in-role-behavior}

内置 `admin` 和 `user` 角色由系统管理。它们的元数据只读，大多数权限模块会被系统恢复到规范默认值。Skill 和 Provider 的运行时访问模块仍可管理，以便管理员控制用户实际能执行哪些能力。

不要通过修改内置 Standard User 来表达复杂策略。需要自定义管理策略时，应创建新的自定义角色。

## 创建自定义角色 {#creating-a-custom-role}

1. 选择稳定的 `identifier`，创建后不要再修改。
2. 只授予该角色职责所需的模块权限。
3. 如果该角色需要执行 Provider Skill，添加 Provider 运行时访问权。
4. 添加该角色可见和可用的 Skill 权限。
5. 给测试用户分配角色，验证 UI 和 Chat 运行时表现。

## 访问问题排查 {#troubleshooting-access}

用户能看到 Skill 但无法完成 Provider 请求时，检查三层：角色启用了该 Skill、角色能访问目标 Provider 实例、用户已配置 Provider 需要的有效凭证。
