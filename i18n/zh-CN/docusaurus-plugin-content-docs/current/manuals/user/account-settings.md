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
