---
title: 告警与资源健康
description: 分析 SmartCMP 告警或资源运行健康。
sidebar_position: 10
---

# 告警与资源健康

SmartCMP alarm 技能既可以检查运维告警，也可以脱离告警独立分析单个资源的运行健康。

## 支持操作 {#supported-actions}

- 列出当前告警。
- 分析单个告警并给出建议。
- 根据资源组件专属监控证据判断资源是正常、异常还是证据不足。
- 当用户明确要求时，对告警状态执行 mute、resolve 或 reopen 等操作。

## 安全规则 {#safety-rule}

除非用户明确要求执行操作，否则 Agent 不应改变告警状态。

## 资源健康分析 {#resource-health-analysis}

资源健康分析不要求存在 active 告警，也不会把“没有告警”当作资源健康的证明。Provider 会：

1. 解析精确资源及其 `componentType`；
2. 加载该组件的有效监控模型；
3. 执行模型中限定到该资源的 Prometheus 定义；
4. 返回大小受限的当前窗口和基线统计；
5. 由 AtlasClaw LLM 得出 `healthy`、`abnormal` 或 `indeterminate`。

实现中不存在硬编码的通用 VM 指标列表。AWS VM、AWS RDS、vSphere VM、软件、硬件和其他资源类型分别使用自身的组件监控定义。监控未启用、不支持、不可访问或不完整时，回答必须说明证据缺口，不能报告资源健康。

## 工作流 {#workflow}

1. 列出活跃或相关告警。
2. 按 ID 或明确描述选择一个告警。
3. 分析告警上下文和建议。
4. 如果用户要求状态操作，确认目标告警和动作。
5. 执行动作并返回上游结果。

## 状态操作 {#status-operations}

常见动作包括 `mute`、`resolve` 和 `reopen`。分析告警不等于允许改变告警状态。

资源健康分析失败时，还应检查组件是否存在有效监控模型，以及资源是否有可用的 Prometheus 时序。
