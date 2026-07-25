---
title: 成本优化
description: 分析费用建议或资源级优化可能。
sidebar_position: 11
---

# 成本优化

SmartCMP cost optimization 技能既支持以已有建议为入口的 FinOps 流程，也支持直接分析单个资源。

## 支持操作 {#supported-actions}

- 列出优化建议。
- 分析已有建议及 SmartCMP 报告的节省金额。
- 即使 SmartCMP 尚未产生建议，也可以分析云资源、软件、硬件、虚拟化资源、VM 或数据库资源。
- 执行 SmartCMP 原生整改动作。
- 跟踪执行进展。

执行动作必须使用对目标环境有权限的 SmartCMP 凭证。

## 入口路径 {#workflow}

### 已有费用建议

1. 列出优化建议。
2. 查看发现项、资源上下文和 SmartCMP 提供的节省金额。
3. 判断建议是否符合业务上下文。
4. 只有用户明确要求时，执行 SmartCMP 原生 day-2 修复。
5. 跟踪整改状态。

### 直接分析资源

1. 按可见名称、近期列表选择或可信的当前页面 Context 解析一个精确资源。
2. 读取大小受限的资源、账单和利用率事实。
3. 匹配已经启用、适用于该资源且 scope 覆盖该资源的费用策略。
4. 关联策略最近一次精确资源执行和 active violation。
5. 由 LLM 单独标记 `llm_potential` 机会并说明缺失证据。

直接资源分析全程只读，不会执行策略，也不能从纯模型推断生成整改动作。

## 证据状态 {#evidence-states}

| 状态 | 含义 |
| --- | --- |
| `platform_detected` | SmartCMP 已经为该资源产生 active 费用违规。 |
| `evaluated_clear` | 完整的资源执行明确评估了该资源，且没有违规。 |
| `insufficient_evidence` | 存在执行记录，但监控或判断证据不完整。 |
| `covered_not_evaluated` | 存在已启用且适用的策略，但未找到精确资源执行。 |
| `not_covered` | 没有已启用且适用的策略覆盖该资源。 |
| `execution_failed` | 相关平台执行失败。 |

没有 active violation 不代表资源已经完成优化。只有 SmartCMP 提供金额时才报告精确节省额，否则金额保持未知。

## 安全边界 {#safety-boundary}

成本建议在执行前只是建议。执行使用 SmartCMP 原生整改能力，而不是 AtlasClaw 直接调用公有云 API。SmartCMP 返回整改状态前，不应声称节省已经实现。

模型推断的资源机会只能作为只读建议。可靠性或安全配置不能包装成费用节省，缺少监控数据也不能解释为资源空闲。
