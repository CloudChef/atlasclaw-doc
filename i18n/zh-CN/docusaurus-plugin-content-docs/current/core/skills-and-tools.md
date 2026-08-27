---
title: 技能和工具
description: 运行时技能、内置工具和权限过滤。
sidebar_position: 5
---

# 技能和工具

技能描述 Agent 能力，工具执行具体操作。

## 内置工具范围 {#built-in-tool-areas}

AtlasClaw Core 包含会话、记忆、网页搜索和抓取、Provider 实例选择、运行时执行、文件系统访问，以及启用时的浏览器自动化工具。

## Markdown 技能 {#markdown-skills}

Markdown 技能可以从 workspace、用户、外部目录或 Provider 目录加载。Provider 绑定技能会加上 Provider 命名空间，避免名称冲突。

Skill 描述何时使用、需要哪些输入、可以调用哪些脚本或工具，以及有哪些安全规则。Provider 专属术语应保留在 Provider 包中。

### Tool 参数与安全 metadata {#tool-parameters-and-safety-metadata}

Markdown Tool 可以声明没有 properties、`required` 为空的普通 JSON object schema。零参数 Tool 不需要虚构 CLI 参数：

```yaml
tool_health_parameters: |
  {
    "type": "object",
    "properties": {},
    "required": [],
    "additionalProperties": false
  }
```

两个逐 Tool metadata 控制只读续跑行为：

| Metadata | 契约 |
| --- | --- |
| `tool_<id>_read_only: true` | Tool 显式保证不会修改持久化状态或外部状态。 |
| `tool_<id>_auto_select_single_option: true` | 该只读 Tool 只有一个可见候选时，active 工作流可以不等待下一轮用户输入而继续。 |

两个标记默认都为 `false`。`auto_select_single_option` 不适用于写入或确认 Tool，也不允许在存在多个可见候选时自动选择。Core 只有在能够识别一个候选集合，以及其中一个带稳定 identity 和显示 label 的候选时才继续。候选 identity 来自 `id`、`key` 或 `code`，可见 label 来自 `name`、`label`、`title`、`displayName` 或 `display_name`。

### 工作流续跑 metadata {#workflow-continuation-metadata}

Tool 结果可以包含 `_internal`，用于保存当前请求 trace、所选 Provider 实例或下一步需要的精确 ID 等隐藏工作流状态。Core 接受结构化值或 JSON 序列化值，并会从用户可见历史中移除该字段，不把它当作最终回答内容。

续跑 metadata 只能在 active 请求 trace 和所选 Provider 实例内复用。它必须保持有界，只包含下一步 identity 或验证证据；不要在 `_internal` 中复制公开列表。超过上下文预算的条目会被丢弃，并记录 `workflow_context_metadata_budget_exceeded`，reason 可能为 `single_entry_oversized` 或 `aggregate_limit`。

## 权限过滤 {#permission-filtering}

角色技能权限和 Provider 实例权限会过滤运行时暴露的技能与工具。Provider 绑定工具由 Provider 权限治理，而不是普通 Core 工具权限。

选定 Skill 后，Core 会保留该 Skill 完整的已授权 Tool 范围。页面 Context 可以提供默认对象和所属 Skill，但不会从普通 Chat turn 中移除其他已授权 Skill 或 Tool。

## 运维规则 {#operational-rule}

技能缺失或被禁用时，Agent 应说明访问阻塞，而不是假装能力可用。

## Skill 生命周期 {#skill-lifecycle}

1. 从配置的 Skill 目录或 Provider 包发现 Skill。
2. Registry 校验 Skill 名称和 metadata。
3. 角色策略决定该 Skill 是否可见和启用。
4. Provider 策略决定 Provider 绑定 Skill 是否有可用实例。
5. Agent 运行时只接收授权后的 Skill/Tool 集合。
6. Tool 输出作为证据供 Agent 继续推理。

## 写操作安全 {#write-action-safety}

提交申请、审批、修改资源状态或操作告警的 Skill 都应视为写操作。Skill 应补齐信息、确认意图，并如实报告上游错误。
