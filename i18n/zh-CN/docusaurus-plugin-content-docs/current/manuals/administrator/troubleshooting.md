---
title: 故障排查
description: 管理员常见问题排查。
sidebar_position: 7
---

# 故障排查

## 登录失败 {#login-fails}

检查认证 Provider、本地登录开关、Token Cookie 设置和默认管理员账号。

建议按顺序检查：浏览器是否能访问后端；认证 Provider 是否启用；本地用户是否启用且密码正确；Host-cookie 或 SSO 的上游 Token/Cookie 和 claim 映射是否正确；用户是否至少拥有一个启用角色。

## 管理页面不可见 {#admin-page-is-hidden}

管理导航由权限控制。确认当前用户拥有相应模块权限，例如 `users.view`、`roles.view`、`model_configs.view` 或 `channels.view`。

## Provider 技能不可用 {#provider-skill-is-not-available}

检查 `providers_root`、Provider 包结构、Provider schema、技能元数据、角色技能权限和 Provider 实例运行时权限。

按层排查：Provider 包已被发现；Provider 实例存在并启用；角色有该 Provider 实例访问权；角色启用了该 Skill；用户已配置必要的用户级凭证。

## 渠道连接无法启动 {#channel-connection-does-not-start}

验证渠道配置、所选模式的必填字段、IM 平台网络访问，以及后端日志中的 handler 错误。

长连接模式还需要检查外部应用是否允许事件投递。Webhook 模式可从上游 IM 平台发送测试消息，确认 AtlasClaw 收到回调。

## Agent 只给出泛泛回答 {#agent-gives-generic-answers}

通常表示运行时没有暴露目标工具或 Provider Skill。检查模型、Skill 权限、Provider 访问权以及 Agent 的 allowed skill/provider 设置。
