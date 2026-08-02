---
title: 管理员配置
description: 管理员配置 SmartCMP Provider 实例。
sidebar_position: 4
---

# 管理员配置

管理员在 Provider Instances 中创建 SmartCMP 实例。

## User Token 模式 {#user-token-mode}

当每个 AtlasClaw 用户都需要填写个人 SmartCMP Token 时使用：

```json
{
  "service_providers": {
    "smartcmp": {
      "default": {
        "base_url": "${CMP_URL}",
        "auth_type": "user_token"
      }
    }
  }
}
```

## Provider Token 模式 {#provider-token-mode}

当允许使用共享 SmartCMP Token 时使用：

```json
{
  "service_providers": {
    "smartcmp": {
      "default": {
        "base_url": "${CMP_URL}",
        "auth_type": "provider_token",
        "provider_token": "${CMP_PROVIDER_TOKEN}"
      }
    }
  }
}
```

## Cookie 或 Credential 模式 {#cookie-or-credential-mode}

Cookie 模式使用请求级或显式配置的 SmartCMP 会话 Cookie。Credential 模式在每次 Provider 调用时登录一次，得到的会话只在本次请求中使用；Provider 不维护 Cookie cache。

需要清晰的用户责任边界时，优先使用 User Token 模式。

## 必填实例字段 {#required-instance-fields}

每个 SmartCMP 实例都需要 `base_url`。Schema 默认值是 `https://console.smartcmp.cloud`，生产部署应设置为自己的 SmartCMP 环境地址。

| 字段 | 范围 | 何时必填 |
| --- | --- | --- |
| `base_url` | 实例 | 始终 |
| `auth_type` | 实例 | 始终，默认 `user_token` |
| `user_token` | 用户 | `auth_type` 为 `user_token` |
| `provider_token` | 实例 | `auth_type` 为 `provider_token` |
| `cookie` | 实例或请求 | `auth_type` 为 `cookie` |
| `username`、`password` | 实例 | `auth_type` 为 `credential` |
| `auth_url` | 实例 | 非标准登录端点时可选 |
| `timeout` | 实例 | 可选请求超时 |

## 管理员配置流程 {#admin-setup-flow}

1. 确认 AtlasClaw 后端可以访问 SmartCMP。
2. 选择认证模式。
3. 创建 SmartCMP Provider 实例。
4. 给需要使用的角色分配 Provider 运行时访问权。
5. 为这些角色启用 SmartCMP Skill。
6. User Token 模式下通知用户配置个人 Token。
7. 先测试只读 datasource 或 resource-pool 查询，再开放写流程。
