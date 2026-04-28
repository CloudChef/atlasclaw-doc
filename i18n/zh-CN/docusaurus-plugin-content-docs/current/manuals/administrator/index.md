---
title: 管理员手册
description: 以管理员身份运维 AtlasClaw Core。
sidebar_position: 1
---

# 管理员手册

管理员负责 workspace 访问控制、运行时配置、模型设置、Provider 实例、渠道治理和 Agent 身份。

内置 `admin` 角色拥有完整管理权限。也可以创建自定义角色，把用户、角色、渠道、模型、Provider、Token、技能和权限模型的管理能力拆分授权。

## 常见任务 {#common-tasks}

- 创建用户并分配角色。
- 配置模型服务和模型 Token。
- 注册 Provider 实例。
- 管理渠道权限。
- 定制主 Agent 的名称、风格、行为和记忆。
- 排查权限和运行时错误。

## 初始配置 Checklist {#initial-setup-checklist}

1. 确认本地管理员登录可用，并按部署策略修改 bootstrap 密码。
2. 先配置模型，再开放 Provider 工作流。
3. 保留 `admin` 给平台管理员，使用 `user` 作为 Standard User 默认体验。
4. 当团队需要介于 `admin` 和 Standard User 之间的权限时，创建自定义角色。
5. 配置 Provider 实例，并单独分配 Provider 运行时访问权。
6. 只启用用户需要看到和执行的技能。
7. 决定哪些 Channel 类型可以用于生产。
8. 在运行时访问配置正确之后，再定制 Agent 身份和风格。

## 日常管理循环 {#daily-administration}

| 循环 | 需要回答的问题 | 主要页面 |
| --- | --- | --- |
| 访问控制 | 谁能登录、拥有哪些角色、能访问哪些 Provider 实例？ | Users、Roles、Provider Instances |
| 运行时 | 哪些模型、Token、Provider 和 Skill 处于启用状态？ | Model Configs、Provider Instances |
| 体验 | Agent 对用户展示什么名称、语气、头像和指导？ | Agent Customization |
| 运维 | 哪些凭证失败、哪些 Channel 断开、哪些权限阻塞请求？ | Troubleshooting、Channel Governance |
