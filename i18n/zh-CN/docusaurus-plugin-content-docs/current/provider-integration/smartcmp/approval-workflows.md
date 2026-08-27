---
title: 审批流程
description: 查看、同意和拒绝 SmartCMP 审批。
sidebar_position: 8
---

# 审批流程

SmartCMP approval 技能用于管理待审批任务。它和已提交申请的状态查询是不同能力。

## 支持操作 {#supported-actions}

- 查看待审批列表。
- 获取申请详情。
- 按精确 Request ID 同意申请，原因可选。
- 按精确 Request ID 拒绝申请，必须提供非空原因。

## 和申请状态查询的边界 {#boundary-with-request-status}

Approval 工具只用于待审批任务和同意/拒绝动作。不要用 approval 工具查询用户自己已提交申请的状态，也不要用它回答“我的申请是否已经审批通过”。这类问题应使用 request 技能的 `smartcmp_get_request_status` 工具，并传入提交后返回的 Request ID。

## Request ID 契约 {#request-id-contract}

审批 Tool 使用待审批列表和 SmartCMP UI 中显示的精确用户可见 Request ID。其格式不透明，可以带前缀、是纯数字或呈 UUID 形态。

待审批列表的每一行都包含可见 `index`、标准化 `request_id` 和 Object Action metadata。用户说“同意 1”或“拒绝第 2 个”时，Agent 必须先把行号解析为对应 `request_id`，再调用 `smartcmp_approve` 或 `smartcmp_reject`。不要把显示行号、占位值或 SmartCMP 单独的内部对象 ID 传给审批 Tool；必须保留 Request ID 的大小写和标点。Provider operation 会把用户可见 Request ID 解析为 SmartCMP 内部审批操作 ID。

`ids` 输入可以是一个 Request ID 字符串，也可以是 Request ID 数组。单个字符串始终表示一个不透明 ID，绝不能按空白或标点拆分。

## 治理 {#governance}

审批操作必须使用在 SmartCMP 中具备审批权限的凭证。AtlasClaw workspace 角色不会在 SmartCMP 内部授予审批权。

## 推荐审批流程 {#recommended-approval-flow}

1. 列出待审批任务。
2. 查看选中的审批项。
3. 检查申请目的、资源规格、目标环境和成本影响。
4. 拒绝时必须要求非空原因；同意原因保持可选，除非本地治理规则另有要求。
5. 只有用户意图明确时才执行同意或拒绝。
6. 逐项返回上游结果和用户可见 Request ID。

批量结果必须逐项判断并报告为 succeeded、failed 或 unknown，保留各自 Request ID，不能把部分成功汇总成全部成功。拒绝调用缺少原因时，Provider 会返回与同一工作流绑定的待补充输入结果，不会执行任何 SmartCMP 写操作。

在工单审批页中，Provider 会跨待审批和已完成视图解析记录。只有精确匹配的待审批任务展示审批变更操作；已完成或状态不一致的记录只提供只读详情。

## 何时升级处理 {#when-to-escalate}

申请缺少业务理由、所有者不清晰、目标为敏感环境或超出预期审批权限时，不应自动批准，应总结风险并让用户在 SmartCMP 或与责任团队处理。
