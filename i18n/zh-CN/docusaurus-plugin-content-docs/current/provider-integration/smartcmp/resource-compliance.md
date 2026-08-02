---
title: 资源合规
description: 分析 SmartCMP 资源生命周期、补丁、安全和配置状态。
sidebar_position: 12
---

# 资源合规

resource compliance 技能为选定资源收集大小受限的 SmartCMP 证据，再由 LLM 分析其状态。

## 分析范围 {#analysis-areas}

- 生命周期状态。
- 补丁状态。
- 安全状态。
- 配置风险。
- 运维建议。

对于交互请求，薄 Skill Adapter 根据可见资源名或最近列表序号解析一个精确资源。经过授权的 backend 和 webhook 兼容调用也可以直接提供一个或多个内部资源 ID。Adapter 将这个精确目标集合传给 typed `smartcmp_provider` 合规 service；Provider 加载资源证据，再为每个资源构造大小受限、经过脱敏且明确标注覆盖范围和缺失证据的 profile。

## 工作流 {#workflow}

1. 根据精确资源名或可见列表序号解析一个交互资源，或者从经过授权的 backend 兼容请求接收一个或多个内部 ID。
2. 通过 Provider operation 加载精确目标集合的证据。
3. 为每个资源构造大小受限、经过脱敏的 profile，并说明证据覆盖和缺口。
4. 由 LLM 区分确认事实、推断和缺失证据。
5. 返回每个资源的发现和只读建议，不修改 SmartCMP。

## 证据规则 {#evidence-rules}

合规分析应区分确认事实和缺失数据。产品版本、操作系统版本或配置字段不可用时，应明确说明，而不是编造风险。

交互用户应通过可见资源名或最近列表序号选择资源。不要要求用户提供内部资源 ID，也不要在最终回答中暴露这些兼容标识。

## 范围 {#scope}

资源合规是建议性分析，不会修复资源，也不会修改 SmartCMP 状态。
