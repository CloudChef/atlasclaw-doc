---
title: Provider 认证模型
description: Provider 认证职责和凭证范围。
sidebar_position: 3
---

# Provider 认证模型

AtlasClaw 负责识别用户。Provider 负责把该身份转换为目标系统可接受的凭证。

## 凭证范围 {#credential-scopes}

- 实例级凭证由管理员配置。
- 用户级凭证由每个用户配置。
- 请求级凭证可来自 Cookie 或上游 Header。

实例级凭证适合共享服务账号或部署级集成 Token。用户级凭证适合每个操作都需要归属到真实上游用户的场景。请求级凭证适合 AtlasClaw 嵌入在已认证系统之后，由上游转发有效 Token 或 Cookie。

## 运行时规则 {#runtime-rule}

调用外部 API 的 Provider 技能必须使用 Provider 原生凭证。Workspace 管理员身份不能绕过目标系统自己的权限控制。

## 认证链 {#auth-chains}

部分 Provider 支持有序 `auth_type` 链。Provider 会根据可用字段和请求上下文选择第一个可用模式。

`auth_type` 可以是字符串，也可以是有序列表：

```json
{
  "service_providers": {
    "example_provider": {
      "default": {
        "base_url": "${PROVIDER_URL}",
        "auth_type": ["sso", "user_token", "provider_token"],
        "provider_token": "${PROVIDER_TOKEN}"
      }
    }
  }
}
```

实际选择的认证模式始终来自 Provider 实例模板。用户不能在 Account Settings 中把 Provider 切换到另一种认证模式。

## 支持的 Auth Type {#supported-auth-types}

Core 识别下面的公共认证词汇。每个 Provider 的 `provider.schema.json` 决定它支持哪些模式，以及每个模式需要哪些字段。

| `auth_type` | 凭证所有者 | 配置方式 |
| --- | --- | --- |
| `provider_token` | 管理员 | 共享 Token 保存在 Provider 实例中。 |
| `user_token` | 用户 | Provider 实例选择该模式，用户在 Provider Tokens 中保存 `user_token`。 |
| `cookie` | 请求或管理员 | 请求转发的 cookie/token，或实例中的静态 cookie。 |
| `credential` | 管理员 | 用户名/密码或等价登录凭证保存在 Provider 实例中。 |
| `sso` | 请求 | AtlasClaw auth flow 转发的 SSO Token。 |
| `app_credentials` | 管理员 | Provider 定义的应用凭证保存在 Provider 实例中。 |

## Provider Token 模式 {#provider-token-mode}

当所有 AtlasClaw 用户都通过同一个共享 Provider Token 调用上游系统时使用。

```json
{
  "service_providers": {
    "example_provider": {
      "default": {
        "base_url": "${PROVIDER_URL}",
        "auth_type": "provider_token",
        "provider_token": "${PROVIDER_TOKEN}"
      }
    }
  }
}
```

这种模式运维简单，但上游审计可能只看到共享服务账号，而不是具体 AtlasClaw 用户。

## User Token 模式 {#user-token-mode}

当每个用户都需要提供自己的上游凭证时使用。

```json
{
  "service_providers": {
    "example_provider": {
      "default": {
        "base_url": "${PROVIDER_URL}",
        "auth_type": "user_token"
      }
    }
  }
}
```

用户随后在 Account Settings 的 Provider Tokens 中保存凭证。用户设置会按 Provider 类型和实例名绑定，并且只有 `user_token` 是用户拥有的字段。`base_url`、`provider_token`、`cookie`、`auth_type` 等平台字段仍由 Provider 实例模板控制。

## Cookie 模式 {#cookie-mode}

当 Provider 可以使用宿主系统转发的请求级 token/cookie，或管理员明确配置静态 cookie 做 server-to-server 测试时使用。

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

如果使用静态 cookie，字段名由 Provider schema 定义：

```json
{
  "service_providers": {
    "example_provider": {
      "default": {
        "base_url": "${PROVIDER_URL}",
        "auth_type": "cookie",
        "cookie": "${PROVIDER_COOKIE}"
      }
    }
  }
}
```

请求级 cookie 是运行时信号，不能复制到用户设置，也不能提交到配置文件。

在内嵌部署中，应将该 Provider 模式和 AtlasClaw `host_cookie` 认证配合使用。完整配置方式见 [内嵌模式](./embedded-mode.md)。

## Credential 模式 {#credential-mode}

当 Provider 需要使用管理员拥有的机器人账号或服务凭证登录时使用。

```json
{
  "service_providers": {
    "example_provider": {
      "default": {
        "base_url": "${PROVIDER_URL}",
        "auth_type": "credential",
        "username": "${PROVIDER_USERNAME}",
        "password": "${PROVIDER_PASSWORD}"
      }
    }
  }
}
```

准确的必填字段名以 Provider schema 为准。

## SSO 模式 {#sso-mode}

当 Provider 使用 AtlasClaw 认证流程转发的 token 时使用，常见于嵌入式或单点登录部署。

```json
{
  "service_providers": {
    "example_provider": {
      "default": {
        "base_url": "${PROVIDER_URL}",
        "auth_type": "sso"
      }
    }
  }
}
```

只有当前请求中存在可用 Provider SSO Token 时，该模式才可用。

## App Credentials 模式 {#app-credentials-mode}

当 Provider 使用应用级凭证认证时使用，例如 client ID 和 client secret。字段名由 Provider 定义。

```json
{
  "service_providers": {
    "example_provider": {
      "default": {
        "base_url": "${PROVIDER_URL}",
        "auth_type": "app_credentials",
        "client_id": "${PROVIDER_CLIENT_ID}",
        "client_secret": "${PROVIDER_CLIENT_SECRET}"
      }
    }
  }
}
```

不要假设每个 Provider 都支持该模式，应以对应 Provider schema 为准。

## 管理员与用户职责 {#administrator-vs-user-responsibilities}

| 职责 | 管理员 | 用户 |
| --- | --- | --- |
| 安装 Provider 包 | 是 | 否 |
| 创建 Provider 实例 | 是 | 否 |
| 选择认证模式 | 是 | 否 |
| 配置共享 Token 或凭证 | 取决于模式 | 否 |
| 配置个人 Token | 否 | 取决于模式 |
| 处理上游 RBAC 拒绝 | 协调上游系统 owner | 申请所需上游权限 |
