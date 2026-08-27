---
title: 模型配置
description: 配置模型服务和模型 Token。
sidebar_position: 3
---

# 模型配置

模型配置决定 AtlasClaw 运行时可使用哪些 LLM 端点。

## 管理员配置内容 {#what-administrators-configure}

- Provider 名称、模型 ID 和显示名。
- Base URL 和 API 类型。
- API Key 或 Token。
- 上下文窗口、最大 token、temperature、优先级和权重。
- 启用或禁用状态。

## 运维说明 {#operational-notes}

安全保存 API Key。API 响应会脱敏显示密钥。轮换密钥时应通过模型配置流程完成，不要直接修改数据库记录。

启动时，AtlasClaw 会先校验并合并 `atlasclaw.json`、数据库 Model Token 和 active Model Config，再判断运行时 Token 池是否为空。不可用的凭证条目会被排除；显式配置为无需 API Key 的 Provider 仍可保留。ID 重复时，数据库条目继续使用既有的覆盖优先级。

存在多个可用条目时，AtlasClaw 使用优先级和权重进行选择。配置的 primary ID 已不可用时，启动日志会告警并回退到第一个可用条目。

## 推荐上线步骤 {#recommended-rollout}

1. 创建一个模型配置并设为启用。
2. 在开启 Provider Skill 前，先验证普通对话可用。
3. 主模型路径稳定后，再增加 fallback 或加权 Token。
4. 记录生产模型和测试模型的用途边界。

## 需要重点检查的字段 {#fields-to-review}

| 字段 | 作用 |
| --- | --- |
| Provider/API 类型 | 决定运行时使用哪个模型客户端和请求格式。 |
| Base URL | 必须是 AtlasClaw 后端可访问的模型网关或厂商地址。 |
| Model ID | 必须是目标 Provider 接受的模型名称。 |
| Context window | 决定会话历史和工具证据可容纳的规模。 |
| Max tokens | 控制回复长度和成本暴露。 |
| Temperature | 控制输出随机性；运维流程建议较低。 |
| Priority/weight | 多个配置启用时影响选择策略。 |

DeepSeek 使用 OpenAI-compatible client，并显式规范化 thinking mode 请求。运行时模型参数启用或禁用 thinking 时，AtlasClaw 会发送相应的 DeepSeek 请求体，并在端点返回时读取 `reasoning_content`。
