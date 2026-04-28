---
title: 故障排查
description: 排查 SmartCMP Provider 配置和运行问题。
sidebar_position: 13
---

# 故障排查

## Provider 未列出 {#provider-not-listed}

检查 `providers_root`、包目录名、`PROVIDER.md` 和 `provider.schema.json`。

还要确认 AtlasClaw 进程可以读取 Provider 根目录，并且添加 Provider 包后已重启。

## 用户 Token 缺失 {#user-token-missing}

请用户在 Account Settings 中配置 SmartCMP Token，并确认 Provider 实例使用 `auth_type: "user_token"`。

## 共享 Token 失败 {#shared-token-fails}

检查 `CMP_PROVIDER_TOKEN`、base URL、Token 是否过期，以及 SmartCMP 侧权限。

## Cookie 或 Credential 模式失败 {#cookie-or-credential-mode-fails}

检查 `CMP_URL`、`auth_url`、Cookie 是否过期、用户名密码是否正确、网络访问，以及是否使用非标准 SmartCMP 登录端点。

## 技能可见但无法执行 {#skill-appears-but-cannot-execute}

检查角色 Provider 权限、Provider 实例访问权、用户凭证和 SmartCMP 侧 RBAC。

## Auth URL 错误 {#wrong-auth-url}

SmartCMP SaaS auth URL 推断依赖精确匹配。私有部署或非标准登录端点应显式配置 `auth_url`。

## 资源操作失败 {#resource-operation-fails}

确认资源 ID、资源类型、当前状态和 SmartCMP 侧权限。某些资源类型或状态不支持 start/stop。

## 审批操作失败 {#approval-operation-fails}

确认审批项仍处于 pending 状态，并且用户 SmartCMP 凭证拥有审批权限。AtlasClaw 角色只暴露 Skill，不会创建 SmartCMP 审批权。
