---
title: 用户手册
description: 以 Standard User 身份使用 AtlasClaw。
sidebar_position: 1
---

# 用户手册

本手册描述默认 Standard User 体验。内置 Standard User 角色标识符是 `user`。

在默认权限下，Standard User 可以使用对话、管理账号设置、配置个人 Provider Token，并管理自己的渠道连接。内置 `user` 角色由系统管理；如果部署需要不同默认策略，应有意识地引入自定义角色策略。

## 主要流程 {#main-workflows}

- 开始或继续对话。
- 查看自己的会话历史。
- 更新个人资料、头像和密码。
- 配置个人 Provider Token。
- 配置个人 IM 渠道连接。
- 权限或 Provider 访问不足时联系管理员。

## 首次登录 Checklist {#first-login-checklist}

1. 在 Account Settings 中确认显示名和邮箱。
2. 发送一条简单消息，确认 Agent 可以回复。
3. 如果要使用 Provider 工作流，检查是否需要配置个人 Provider Token。
4. 如果要从 IM 平台对话，打开 `/channels` 创建个人渠道连接。
5. 请求被阻塞时，先阅读阻塞提示，通常会指出缺失凭证、未启用 Skill 或 Provider 访问不足。

## Standard User 的含义 {#what-standard-user-means}

Standard User 是 AtlasClaw workspace 角色，不是上游系统角色。AtlasClaw 可以允许你调用某个 Provider Skill，但 Provider 仍会使用你的上游凭证执行操作。如果上游系统拒绝，AtlasClaw 应报告拒绝原因，而不是绕过权限。

## 设置位置 {#where-settings-live}

| 设置 | 管理位置 | 所有者 |
| --- | --- | --- |
| 显示名、邮箱、头像 | Account Settings | 用户 |
| 本地密码 | Account Settings | 本地登录用户 |
| Provider Token | Provider Tokens | 用户 |
| IM Channel 凭证 | `/channels` | 用户 |
| 角色和 Provider 访问 | 管理页面 | 管理员 |
| 模型和 Provider 实例 | 管理页面 | 管理员 |
