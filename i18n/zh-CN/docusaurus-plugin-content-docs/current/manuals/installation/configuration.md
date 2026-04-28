---
title: 配置
description: 使用 atlasclaw.json 和环境变量配置 AtlasClaw Core。
sidebar_position: 4
---

# 配置

AtlasClaw 从 `atlasclaw.json` 读取运行时配置，并展开 `${VAR_NAME}` 形式的环境变量。建议把稳定结构放在 JSON 文件中，把密钥放在环境变量或加密配置值中。

## 最小配置 {#minimal-configuration}

```json
{
  "providers_root": "../atlasclaw-providers/providers",
  "model": {
    "primary": "main",
    "tokens": [
      {
        "id": "main",
        "provider": "openai",
        "model": "gpt-4.1",
        "base_url": "https://api.openai.com/v1",
        "api_key": "${OPENAI_API_KEY}",
        "api_type": "openai",
        "priority": 0,
        "weight": 100,
        "context_window": 128000
      }
    ]
  }
}
```

## 重要配置项 {#important-settings}

- `providers_root`：Provider 包目录。
- `model`：模型服务和 Token 配置。
- `auth`：认证方式和本地登录配置。
- `workspace.path`：Agent、用户、会话、记忆和运行状态目录。
- `service_providers`：Provider 实例配置。

## 完整配置骨架 {#full-configuration-skeleton}

可以用下面的骨架作为生产配置起点。未使用的 section 可以删除，缺省值会来自配置 schema。

```json
{
  "log_level": "info",
  "base_path": "",
  "workspace": {
    "path": "./.atlasclaw"
  },
  "database": {
    "type": "sqlite",
    "sqlite": {
      "path": "./data/atlasclaw.db"
    },
    "echo": false
  },
  "providers_root": "../atlasclaw-providers/providers",
  "skills_root": "../skills",
  "auth": {
    "enabled": true,
    "provider": "local",
    "local": {
      "enabled": true,
      "default_admin_username": "admin",
      "default_admin_password": "${ATLASCLAW_ADMIN_PASSWORD}"
    },
    "jwt": {
      "secret_key": "${ATLASCLAW_JWT_SECRET}",
      "expires_minutes": 480
    }
  },
  "model": {
    "primary": "main",
    "fallbacks": [],
    "temperature": 0.2,
    "max_tokens": 4096,
    "selection_strategy": "health",
    "tokens": [
      {
        "id": "main",
        "provider": "openai",
        "model": "gpt-4.1",
        "base_url": "https://api.openai.com/v1",
        "api_key": "${OPENAI_API_KEY}",
        "api_type": "openai",
        "priority": 0,
        "weight": 100,
        "context_window": 128000
      }
    ]
  },
  "service_providers": {
    "example_provider": {
      "default": {
        "base_url": "${PROVIDER_URL}",
        "auth_type": "user_token"
      }
    }
  },
  "agent_defaults": {
    "timeout_seconds": 600,
    "max_concurrent": 10,
    "max_tool_calls": 50,
    "prompt_mode": "full"
  },
  "messages": {
    "queue": {
      "mode": "collect",
      "debounce_ms": 1000,
      "cap": 20,
      "drop": "old"
    },
    "reply_to_mode": "auto",
    "inbound_debounce_ms": 1000,
    "dedup_ttl_seconds": 60
  },
  "memory": {
    "enabled": true,
    "max_results": 6
  },
  "security": {
    "allowed_tools": [],
    "denied_tools": [],
    "workspace_access": "rw"
  }
}
```

## Section 说明 {#section-summary}

| Section | 作用 | 常见调整 |
| --- | --- | --- |
| `log_level` | 后端日志等级。 | 排障时改成 `debug`。 |
| `base_path` | 反向代理挂载路径。 | 部署在 `/atlasclaw` 等前缀下时设置。 |
| `workspace.path` | 运行时存储根目录。 | 生产环境应指向持久化存储。 |
| `database` | SQLite 或 MySQL 配置。 | 本地可用 SQLite，生产共享部署建议 MySQL。 |
| `providers_root` | Provider 包目录。 | 指向 `atlasclaw-providers/providers`。 |
| `skills_root` | 独立 Skill 包目录。 | Provider 外部 Skill 使用。 |
| `auth` | AtlasClaw 登录和身份配置。 | 选择 `local`、`host_cookie`、`oidc`、`dingtalk` 或 `none`。 |
| `model` | LLM token pool 和生成参数。 | 配置 primary、fallback、temperature 和 max tokens。 |
| `service_providers` | Provider 实例模板。 | 配置 Provider 类型、实例名、认证模式和实例字段。 |
| `agent_defaults` | Agent turn 的默认运行限制。 | 调整超时、并发和工具调用上限。 |
| `messages` | 消息队列、debounce 和去重。 | 调整 IM 消息合并和队列行为。 |
| `memory` | 用户级记忆检索设置。 | 开关记忆或调整结果数。 |
| `security` | 工具 allow/deny 和 workspace 权限策略。 | 加固部署时限制工具或文件访问。 |

## Provider 实例配置 {#provider-instance-configuration}

`service_providers` 的结构是：

```json
{
  "service_providers": {
    "<provider_type>": {
      "<instance_name>": {
        "auth_type": "user_token"
      }
    }
  }
}
```

Provider 专属字段来自该 Provider 的 `provider.schema.json`。Core 只定义通用 `auth_type` 词汇和实例级、用户级、请求级凭证边界。

| `auth_type` | 凭证位置 | 典型用途 |
| --- | --- | --- |
| `provider_token` | `atlasclaw.json` Provider 实例 | 管理员配置的共享服务 Token。 |
| `user_token` | 用户 Provider Tokens 设置 | 每个用户提供个人 Provider Token。 |
| `cookie` | 请求上下文或 Provider 实例 | 嵌入式部署或静态 Cookie 测试。 |
| `credential` | `atlasclaw.json` Provider 实例 | 机器人用户名/密码或登录凭证。 |
| `sso` | 请求上下文 | Provider 使用 AtlasClaw auth flow 转发的 Token。 |
| `app_credentials` | `atlasclaw.json` Provider 实例 | Provider 定义的应用凭证。 |

通用认证示例见 Provider Auth Model；具体字段以对应 Provider 章节为准。无缝内嵌部署应同时使用 `auth.provider: "host_cookie"` 和 Provider `auth_type: "cookie"`；详见 [内嵌模式](../../provider-integration/embedded-mode.md)。
