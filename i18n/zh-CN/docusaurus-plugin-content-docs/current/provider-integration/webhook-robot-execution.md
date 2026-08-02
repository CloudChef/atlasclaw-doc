---
title: Webhook Robot 执行
description: 配置由 webhook 触发、使用限定范围 Robot 凭证运行的 backend Skill。
sidebar_position: 4
---

# Webhook Robot 执行

Webhook Robot 执行允许外部系统调用带 Provider 命名空间的 backend Skill，同时让 Provider 操作以配置的 Robot 账号运行。适用于上游系统发送事件，但 Provider 调用必须在目标系统中以服务账号或 Robot 身份接受审计的场景。

## 适用场景 {#when-to-use-it}

Webhook Robot 执行适合以下 backend 自动化：

- 由上游工作流事件触发的审批预审；
- 由外部受理系统触发的需求拆解或申请创建；
- Provider 要求使用特权服务身份的合规或修复流程。

不要使用该能力模拟最终用户。如果 Provider 审计必须显示具体用户，应使用 User Token 或请求级认证。

## 配置结构 {#configuration-shape}

需要配置两组相互独立的 allowlist：

- `webhook.systems[].allowed_skills` 控制 webhook 系统可以调用哪些 Skill；
- `service_providers.<provider>.<instance>.robot_auth.<profile>.allowed_skills` 控制哪些 Skill 可以使用该 Robot 凭证。

示例：

```json
{
  "service_providers": {
    "example_provider": {
      "default": {
        "base_url": "${PROVIDER_URL}",
        "auth_type": "user_token",
        "robot_auth": {
          "backend_bot": {
            "auth_type": "provider_token",
            "provider_token": "${PROVIDER_ROBOT_TOKEN}",
            "allowed_skills": [
              "example_provider:backend-agent"
            ]
          }
        }
      }
    }
  },
  "webhook": {
    "enabled": true,
    "header_name": "X-AtlasClaw-SK",
    "systems": [
      {
        "system_id": "external-review",
        "enabled": true,
        "sk_env": "ATLASCLAW_WEBHOOK_SK_EXTERNAL_REVIEW",
        "default_agent_id": "main",
        "allowed_skills": [
          "example_provider:backend-agent"
        ]
      }
    ]
  }
}
```

`PROVIDER_ROBOT_TOKEN` 和 `ATLASCLAW_WEBHOOK_SK_EXTERNAL_REVIEW` 应保存在部署环境中，不能直接写入 JSON 文件。

## Webhook Payload {#webhook-payload}

Webhook 请求负责选择 Skill、Provider 实例和 Robot Profile：

```json
{
  "skill": "example_provider:backend-agent",
  "args": {
    "provider_instance": "default",
    "robot_profile": "backend_bot",
    "request_id": "REQ-10001"
  }
}
```

Robot 执行必须使用 `provider_instance`。旧版简写 `instance` 不能用于选择 Robot Profile。

## 运行流程 {#runtime-flow}

处理 Robot webhook 调度时，AtlasClaw 会：

1. 使用配置的 Header 验证 webhook secret；
2. 确认 webhook 系统允许调用目标 Skill；
3. 在目标 Provider 类型下解析 `args.provider_instance`；
4. 在该 Provider 实例下解析 `args.robot_profile`；
5. 确认 Robot Profile 允许调用目标 Skill；
6. 构造只在本次运行中使用的 Provider 配置，其中只包含选定实例和 Robot 凭证；
7. 调用已注册的 Provider Tool。显式 `file.py:callable` entrypoint 通过 `RunContext` 接收限定范围的实例、凭证和 Robot 身份；只有不带 `:callable` 的旧 entrypoint 才会启动子进程，并接收对应的 `ATLASCLAW_*` 环境变量。

Robot 凭证不会添加到 Prompt。Token、Password 和 Cookie 类字段会从 webhook 参数、Trace 和 API 响应中脱敏。

## 安全要求 {#security-requirements}

- 将 webhook secret 和 Robot 凭证保存在环境变量中；
- 尽量缩小 Robot Profile allowlist，并为不同权限级别创建独立 Profile；
- 使用上游权限与自动化流程匹配的 Provider 原生 Robot 账号；
- 按 Provider 所有者的运维流程轮换 Robot 凭证；
- 启用写操作 Skill 前先检查对应 Provider 文档。

SmartCMP 特定配置见 [SmartCMP 管理员配置](/provider-integration/smartcmp/admin-configuration)。
