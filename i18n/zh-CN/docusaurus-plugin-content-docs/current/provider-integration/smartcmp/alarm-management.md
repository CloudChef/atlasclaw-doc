---
title: 告警管理
description: 列出、分析和操作 SmartCMP 告警。
sidebar_position: 10
---

# 告警管理

SmartCMP alarm 技能用于检查运维告警。

## 支持操作 {#supported-actions}

- 列出当前告警。
- 分析单个告警并给出建议。
- 当用户明确要求时，对告警状态执行 mute、resolve 或 reopen 等操作。

## 安全规则 {#safety-rule}

除非用户明确要求执行操作，否则 Agent 不应改变告警状态。

## 工作流 {#workflow}

1. 列出活跃或相关告警。
2. 按 ID 或明确描述选择一个告警。
3. 分析告警上下文和建议。
4. 如果用户要求状态操作，确认目标告警和动作。
5. 执行动作并返回上游结果。

## 状态操作 {#status-operations}

常见动作包括 `mute`、`resolve` 和 `reopen`。分析告警不等于允许改变告警状态。
