---
title: 成本优化
description: 查看并执行 SmartCMP 成本优化动作。
sidebar_position: 11
---

# 成本优化

SmartCMP cost optimization 技能支持 FinOps 类建议查看和整改。

## 支持操作 {#supported-actions}

- 列出优化建议。
- 分析节省机会。
- 执行 SmartCMP 原生整改动作。
- 跟踪执行进展。

执行动作必须使用对目标环境有权限的 SmartCMP 凭证。

## 工作流 {#workflow}

1. 列出优化建议。
2. 查看发现项和预估节省。
3. 判断建议是否符合业务上下文。
4. 只有用户明确要求时，执行 SmartCMP 原生 day-2 修复。
5. 跟踪整改状态。

## 安全边界 {#safety-boundary}

成本建议在执行前只是建议。执行使用 SmartCMP 原生整改能力，而不是 AtlasClaw 直接调用公有云 API。SmartCMP 返回整改状态前，不应声称节省已经实现。
