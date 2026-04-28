---
title: 资源合规
description: 分析 SmartCMP 资源生命周期、补丁、安全和配置状态。
sidebar_position: 12
---

# 资源合规

resource compliance 技能按资源 ID 获取资源并分析状态。

## 分析范围 {#analysis-areas}

- 生命周期状态。
- 补丁状态。
- 安全状态。
- 配置风险。
- 运维建议。

分析使用 SmartCMP `datasource/scripts/list_resource.py` 暴露的标准化资源视图。

## 工作流 {#workflow}

1. 通过 `list_resource.py` 按资源 ID 获取事实。
2. 读取标准化 `type + properties` 视图。
3. 按资源类型和证据路由到对应 analyzer。
4. 在版本或生命周期证据足够时做 best-effort 校验。
5. 返回发现、证据和建议。

## 证据规则 {#evidence-rules}

合规分析应区分确认事实和缺失数据。产品版本、操作系统版本或配置字段不可用时，应明确说明，而不是编造风险。

## 范围 {#scope}

资源合规是建议性分析，不会修复资源，也不会修改 SmartCMP 状态。
