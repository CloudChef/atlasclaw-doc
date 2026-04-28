---
title: 审批流程
description: 查看、同意和拒绝 SmartCMP 审批。
sidebar_position: 8
---

# 审批流程

SmartCMP approval 技能用于管理待审批任务。

## 支持操作 {#supported-actions}

- 查看待审批列表。
- 获取申请详情。
- 带原因同意申请。
- 带原因拒绝申请。

## 治理 {#governance}

审批操作必须使用在 SmartCMP 中具备审批权限的凭证。AtlasClaw workspace 角色不会在 SmartCMP 内部授予审批权。

## 推荐审批流程 {#recommended-approval-flow}

1. 列出待审批任务。
2. 查看选中的审批项。
3. 检查申请目的、资源规格、目标环境和成本影响。
4. 如果用户未提供原因，要求补充同意或拒绝原因。
5. 只有用户意图明确时才执行同意或拒绝。
6. 返回上游结果和相关申请或流程 ID。

## 何时升级处理 {#when-to-escalate}

申请缺少业务理由、所有者不清晰、目标为敏感环境或超出预期审批权限时，不应自动批准，应总结风险并让用户在 SmartCMP 或与责任团队处理。
