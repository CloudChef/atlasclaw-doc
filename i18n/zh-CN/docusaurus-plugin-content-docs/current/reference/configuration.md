---
title: 配置参考
description: AtlasClaw 常见配置项。
sidebar_position: 1
---

# 配置参考

## Core 字段 {#core-fields}

| 字段 | 用途 |
| --- | --- |
| `log_level` | 后端日志等级：`debug`、`info`、`warning` 或 `error`。 |
| `base_path` | 反向代理挂载路径，例如 `/atlasclaw`。 |
| `providers_root` | Provider 包目录。 |
| `skills_root` | Provider 包之外的独立 Skill 目录。 |
| `workspace.path` | 运行时存储根目录。 |
| `database` | SQLite 或 MySQL 数据库配置。 |
| `model` | 模型服务、模型 Token 和主模型设置。 |
| `auth` | 认证 Provider 和 Token 设置。 |
| `service_providers` | Provider 实例配置。 |
| `agent_defaults` | Agent turn 的运行限制和 prompt mode 默认值。 |
| `messages` | 消息队列、debounce 和去重行为。 |
| `compaction` | 长上下文压缩阈值。 |
| `context_pruning` | 上下文压力下的工具结果裁剪策略。 |
| `memory` | 用户级记忆检索设置。 |
| `sandbox` | 可选 sandbox 模式和 workspace root。 |
| `security` | 工具 allow/deny 和 workspace 访问策略。 |
| `skills` | Markdown Skill 加载限制和脚本执行策略。 |
| `reset` | 会话重置策略。 |
| `webhook` | 入站 webhook dispatch 配置。 |
| `hooks_runtime` | 配置驱动的 hook script handler。 |
| `search_runtime` | Web search provider 运行时配置。 |
| `heartbeat` | Agent 和 Channel heartbeat 配置。 |

## atlasclaw.json 结构 {#atlasclaw-json-structure}

`atlasclaw.json` 是主要部署配置文件。生产环境最常见的 section 如下：

```json
{
  "workspace": {
    "path": "./.atlasclaw"
  },
  "database": {
    "type": "sqlite",
    "sqlite": {
      "path": "./data/atlasclaw.db"
    }
  },
  "providers_root": "../atlasclaw-providers/providers",
  "skills_root": "../skills",
  "auth": {
    "enabled": true,
    "provider": "local"
  },
  "model": {
    "primary": "main",
    "tokens": []
  },
  "service_providers": {}
}
```

### Workspace 和 Database {#workspace-and-database}

`workspace.path` 保存会话、记忆、用户设置、Agent 文件、Channel 产物和 Provider 运行时产物。生产环境应使用持久化存储。

`database.type` 可以是 `sqlite` 或 `mysql`：

```json
{
  "database": {
    "type": "mysql",
    "mysql": {
      "host": "${MYSQL_HOST}",
      "port": 3306,
      "database": "atlasclaw",
      "user": "${MYSQL_USER}",
      "password": "${MYSQL_PASSWORD}",
      "charset": "utf8mb4"
    },
    "pool_size": 5,
    "max_overflow": 10,
    "echo": false
  }
}
```

### Auth Section {#auth-section}

`auth.provider` 选择 AtlasClaw 登录方式：

| Provider | 场景 | 关键字段 |
| --- | --- | --- |
| `local` | 本地用户名/密码登录。 | `auth.local.enabled`、`default_admin_username`、`default_admin_password`、`auth.jwt.*` |
| `host_cookie` | 嵌入在已认证的宿主系统后面。 | `auth.host_cookie.cookie_name`、`subject_cookie_name`、display/user/tenant cookie 字段 |
| `oidc` | OIDC/OAuth2 SSO。 | `issuer`、`client_id`、`client_secret`、endpoints、`redirect_uri` |
| `dingtalk` | DingTalk SSO 登录。 | `app_key`、`app_secret`、`corp_id`、`redirect_uri` |
| `none` | 开发/no-auth 模式。 | `auth.none.default_user_id` |

认证用于识别 AtlasClaw 用户，和 `service_providers` 下的 Provider 认证是两件事。

### Model Section {#model-section}

`model.primary` 引用 `model.tokens` 中的 token `id`。`fallbacks` 是备用 token ID 列表。`selection_strategy`、`priority` 和 `weight` 会影响多个 token 启用时的选择。

```json
{
  "model": {
    "primary": "main",
    "fallbacks": ["backup"],
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
  }
}
```

### Provider Instance Section {#provider-instance-section}

`service_providers` 保存管理员拥有的 Provider 模板：

```json
{
  "service_providers": {
    "example_provider": {
      "default": {
        "base_url": "${PROVIDER_URL}",
        "auth_type": "user_token"
      },
      "shared": {
        "base_url": "${PROVIDER_URL}",
        "auth_type": "provider_token",
        "provider_token": "${PROVIDER_TOKEN}"
      }
    }
  }
}
```

第一层 key 是 Provider 类型，第二层 key 是实例名，内部对象是 Provider 实例模板。Provider 专属字段由 `provider.schema.json` 定义。

## 环境变量展开 {#environment-expansion}

配置字符串可以使用 `${VAR_NAME}` 引用环境变量。密钥和部署相关 URL 应使用这种方式管理。

配置会从默认值、配置文件、环境变量和运行时覆盖合并。文件配置合并后，`${VAR}` 会从进程环境中展开。

## 常见文件 {#common-files}

| 文件 | 用途 |
| --- | --- |
| `atlasclaw.json` | 项目或 workspace 配置。 |
| `atlasclaw.yaml` | 另一种配置文件格式。 |
| `~/.atlasclaw/config.json` | 用户级 fallback 配置。 |
| `.env` | 部署脚本使用的环境变量。 |
| `users/<user_id>/user_setting.json` | 用户级偏好和 Provider 设置。 |

## 配置优先级 {#configuration-precedence}

优先级从低到高：配置 schema 默认值、全局配置文件、workspace 配置文件、`ATLASCLAW_*` 环境变量和 `${VAR}` 展开、运行时覆盖。

## Provider 字段 {#provider-fields}

Provider 特定字段来自 `provider.schema.json`，应记录在 Provider Integration 章节。

Provider schema 会定义 `default_auth_type`、各 `auth_modes` 的必填字段、配置 `fields`、字段 `scope` 以及需要脱敏的 sensitive/password 字段。

## Secret 管理 {#secret-handling}

不要提交 API Key、Cookie、Provider Token、Channel Secret 或模型 Token。优先使用环境变量或部署支持的加密配置。轮换 Secret 时，应通过对应配置入口更新，不要直接修改运行时产物。
