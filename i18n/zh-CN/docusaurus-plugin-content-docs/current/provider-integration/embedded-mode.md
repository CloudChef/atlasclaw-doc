---
title: 内嵌模式
description: 将 AtlasClaw 嵌入宿主系统，并用请求 Cookie 实现无缝 Provider 访问。
sidebar_position: 4
---

# 内嵌模式

内嵌模式用于把 AtlasClaw 运行在一个已经完成用户认证的宿主系统中。用户从宿主系统打开 AtlasClaw 页面，浏览器请求会携带宿主系统 Cookie，AtlasClaw 再把这些 Cookie 映射为 workspace 用户身份和 Provider 访问凭证。

当目标 Provider 系统就是宿主系统，或宿主系统能够转发目标 Provider 可接受的 Cookie 时，应优先使用该模式。这样用户不需要单独登录 AtlasClaw，也不需要在 Provider Tokens 中保存个人 Token。

## 认证分层 {#authentication-layers}

内嵌模式包含两层相关但独立的认证：

| 层次 | AtlasClaw 配置 | 作用 |
| --- | --- | --- |
| AtlasClaw 用户身份 | `auth.provider: "host_cookie"` | 读取宿主 Cookie，解析当前 AtlasClaw 用户。 |
| Provider 访问 | `service_providers.<provider>.<instance>.auth_type: "cookie"` | 把当前请求 Cookie 传入 Provider runtime。 |

第一层回答“谁在使用 AtlasClaw？”。第二层回答“Provider 调用上游系统时使用什么凭证？”。要实现无缝内嵌，两层都需要配置。

## 推荐流程 {#recommended-flow}

1. 用户先登录宿主系统。
2. 宿主系统以 iframe、内嵌页面或路由子应用方式打开 AtlasClaw。
3. 浏览器向 AtlasClaw 请求时携带宿主认证 Cookie 和身份 Cookie。
4. AtlasClaw 使用 `host_cookie` auth 解析用户，并创建或更新 workspace shadow user。
5. `auth_type: "cookie"` 的 Provider 实例在运行时收到请求级 Cookie。
6. Provider Skill 使用该 Cookie 调用目标系统，因此上游 RBAC 和审计仍然与原始宿主登录用户一致。

该 Cookie 只存在于当前请求运行时。它不会复制到 Provider Tokens，不会保存成用户设置，也不应写入 `atlasclaw.json`。

## AtlasClaw Auth 配置 {#atlasclaw-auth-configuration}

将 `auth.provider` 配置为 `host_cookie`，并映射宿主系统签发的 Cookie 名称。

```json
{
  "auth": {
    "enabled": true,
    "provider": "host_cookie",
    "host_cookie": {
      "cookie_name": "Host-Authenticate",
      "subject_cookie_name": "userLoginId",
      "display_name_cookie_name": "username",
      "user_id_cookie_name": "userId",
      "tenant_id_cookie_name": "tenant_id"
    }
  }
}
```

字段含义：

| 字段 | 说明 |
| --- | --- |
| `cookie_name` | 宿主认证 Cookie，包含 AtlasClaw 在 cookie-mode Provider 访问中转发的原始 token。 |
| `subject_cookie_name` | 必填的稳定登录标识，用作 AtlasClaw subject。 |
| `display_name_cookie_name` | 可选显示名，用于 AtlasClaw 页面展示。 |
| `user_id_cookie_name` | 可选上游用户 ID，会写入认证用户 metadata。 |
| `tenant_id_cookie_name` | 可选租户标识；缺省时 AtlasClaw 使用 `default`。 |

在 `host_cookie` 模式下，AtlasClaw 仍会优先接受有效的 AtlasClaw admin JWT。这保证后台管理入口可用，而普通内嵌用户通过宿主 Cookie 进入。

## Provider Cookie 配置 {#provider-cookie-configuration}

当 Provider 调用应该使用当前请求 Cookie 时，把 Provider 实例配置为 `auth_type: "cookie"`。

```json
{
  "service_providers": {
    "example_provider": {
      "default": {
        "base_url": "${PROVIDER_URL}",
        "auth_type": "cookie"
      }
    }
  }
}
```

正常内嵌路径不要配置静态 `cookie` 字段。静态 Cookie 只适合受控的 server-to-server 测试，因为所有请求都会使用同一个会话。生产内嵌模式应选择运行时请求 Cookie 作为凭证。

## 宿主系统要求 {#host-system-requirements}

宿主系统必须让 AtlasClaw 请求可以携带该 Cookie。通常需要满足：

- AtlasClaw 部署在同站点、父域名或反向代理路径下，宿主 Cookie 对 AtlasClaw 请求可见。
- Cookie 的 `Path`、`Domain`、`SameSite`、`Secure` 属性允许浏览器把宿主 Cookie 发送给 AtlasClaw。
- 宿主系统提供稳定的 subject Cookie，AtlasClaw 才能把请求映射到 workspace 用户。
- Provider 系统接受同一个 Cookie，或 Provider 包知道如何用该 Cookie 换取 Provider 原生会话。

如果 AtlasClaw 被嵌入跨站 iframe，浏览器 Cookie 限制可能会阻止请求 Cookie。应在目标部署中验证最终浏览器行为，而不是只检查服务端配置。

## 安全注意事项 {#security-notes}

- 将宿主 Cookie 视为用户凭证。不要记录到日志、记忆或排障输出中。
- 生产环境应使用 HTTPS 和安全 Cookie 属性。
- 保持目标系统的 Provider RBAC 生效。AtlasClaw 不应授予目标系统本身会拒绝的访问。
- 只有在部署明确需要共享身份或机器人身份时，才使用 `provider_token`、`credential` 或 `app_credentials`。

## 故障排查 {#troubleshooting}

| 现象 | 检查项 |
| --- | --- |
| AtlasClaw 页面加载前用户被重定向或拒绝 | 确认 `auth.provider` 是 `host_cookie`，并且 AtlasClaw 请求中存在配置的 `cookie_name`。 |
| 用户映射到错误的 AtlasClaw 账号 | 检查 `subject_cookie_name`，它必须对用户稳定且唯一。 |
| Provider 调用提示缺少凭证 | 确认 Provider 实例选择 `auth_type: "cookie"`，并且当前请求包含宿主 Cookie。 |
| Provider 调用未授权 | 确认目标系统接受转发的 Cookie，并且上游用户拥有所需权限。 |
| iframe 外可用，iframe 内不可用 | 检查浏览器 `SameSite`、第三方 Cookie、`Secure`、Domain/Path 行为。 |
