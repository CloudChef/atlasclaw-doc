---
title: 权限参考
description: 角色权限模块和默认角色行为。
sidebar_position: 3
---

# 权限参考

## 权限模块 {#permission-modules}

| 模块 | 常见权限 |
| --- | --- |
| `users` | `view`、`create`、`edit`、`delete`、`assign_roles`、`manage_permissions` |
| `roles` | `view`、`create`、`edit`、`delete`、`manage_permissions` |
| `channels` | `module_permissions.manage_permissions`、`channel_permissions` |
| `tokens` | `view`、`create`、`edit`、`delete`、`manage_permissions` |
| `agent_configs` | `view`、`create`、`edit`、`delete`、`manage_permissions` |
| `provider_configs` | `view`、`create`、`edit`、`delete`、`manage_permissions` |
| `model_configs` | `view`、`create`、`edit`、`delete`、`manage_permissions` |
| `skills` | `view`、`enable_disable`、`manage_permissions`、`skill_permissions` |
| `providers` | `manage_permissions`、`provider_permissions` |

## 内置默认值 {#built-in-defaults}

- `admin`：所有管理权限。
- `user`：默认拥有所有已注册 Skill、Provider 实例和 Channel 类型的运行时访问权，但没有 Skill 或 Provider 配置查看权限。
- `viewer`：审计场景的只读权限。

管理员可以创建自定义角色实现更细粒度授权。

## 模块权限说明 {#module-permission-details}

| 模块 | 说明 |
| --- | --- |
| `users` | `assign_roles` 独立于编辑用户资料。 |
| `roles` | 内置角色 metadata 只读，自定义角色 identifier 创建后不可改。 |
| `channels` | 逐 Channel 类型条目控制角色可使用哪些 Channel。允许某个 Channel 类型后，用户可以管理自己在该类型下的连接。 |
| `tokens` | 管理员模型 Token 配置，不是用户自有 Provider Token。 |
| `agent_configs` | 数据库型 Agent 配置；文件型 Agent 需编辑文件。 |
| `provider_configs` | Provider 实例和共享实例配置。 |
| `model_configs` | 模型端点和模型 Token 配置。 |
| `skills` | 模块权限控制管理能力，逐 Skill 条目控制运行时可用性。 |
| `providers` | 逐 Provider 实例条目控制运行时访问。 |

## 运行时访问 Checklist {#runtime-access-checklist}

Provider Skill 执行前应确认：用户拥有启用角色；Skill 对至少一个角色启用；Provider 实例对至少一个角色开放；Provider 实例启用；如果请求来自 IM Channel，Channel 类型对至少一个角色开放；需要用户凭证时用户已配置。

## 系统管理的内置角色 {#system-managed-built-in-roles}

`admin` 和 `user` 是系统管理的内置角色。应用会基于已注册目录初始化 Skill、Provider 和 Channel 的运行时访问条目。自定义管理策略应使用自定义角色。
