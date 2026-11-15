---
title: 账号设置
description: 管理个人资料、头像和密码。
sidebar_position: 3
---

# 账号设置

使用 Account Settings 管理个人 workspace 资料。

## 资料 {#profile}

在部署允许时，可以更新显示名和邮箱。显示名会用于 AtlasClaw UI 和管理视图。

如果账号来自 SSO 或 Host 系统，部分字段可能只读或由上游身份系统同步。此时应在源身份系统修改，而不是在 AtlasClaw 中覆盖。

## 头像 {#avatar}

可以在账号页上传头像。AtlasClaw 会把用户资源保存在 workspace 的公开用户内容目录下。

请使用适合工作场景的图片，不要把敏感截图或文档作为头像上传。如果头像保存后没有立即刷新，可以重新加载浏览器。

## 密码 {#password}

本地认证用户可以在 Account Settings 修改密码。SSO 或 Host Cookie 用户通常需要在上游身份系统修改凭证。

## 安全说明 {#security-notes}

- 不要把 Provider API Token 写入个人资料字段。
- 不要通过对话分享 IM Channel secret。
- 如果发现异常角色或 Provider 访问权，请联系管理员。
- 在共享设备上使用后请退出登录。

## 管理员访问令牌

管理员可以在账户设置中创建、查看和撤销自己的 AtlasClaw 访问令牌。新令牌的明文只显示一次，请立即复制保存；服务端仅保存摘要。这些令牌用于 API 客户端向 AtlasClaw 认证，与外部 Provider 的凭据相互独立。

使用 `Authorization: Bearer <token>` 发送令牌。请求使用令牌所有者的当前权限。撤销令牌、停用所有者或修改角色会立即影响后续请求。通过 API 令牌认证的请求不能创建、查看或撤销访问令牌。

轮换令牌时，先通过管理员会话创建替代令牌，更新客户端并验证成功后，再撤销旧令牌。不要将访问令牌粘贴到聊天中。
