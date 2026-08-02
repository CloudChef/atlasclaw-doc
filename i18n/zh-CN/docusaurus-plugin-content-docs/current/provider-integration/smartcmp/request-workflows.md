---
title: 申请流程
description: 提交 SmartCMP 服务和资源申请，并查询已提交申请状态。
sidebar_position: 7
---

# 申请流程

SmartCMP request 技能帮助用户把基础设施需求转换成结构化 SmartCMP 申请，也支持用提交后返回的 SmartCMP Request ID 查询申请状态。

## 典型流程 {#typical-flow}

1. 用 `smartcmp_list_services` 查询一次已发布服务，并从结果选择一个 catalog UUID。
2. 用 `smartcmp_get_request_catalog` 加载该 catalog 的标准化字段契约。
3. 用 `smartcmp_list_available_bgs` 查询可用业务组。
4. 在服务和业务组范围确定后补齐缺失字段。
5. 构造申请 JSON。
6. 展示完整 JSON 预览并请用户确认。
7. 只有用户确认后，才用 `smartcmp_submit_request` 提交。
8. 在 SmartCMP 中跟踪返回的 Request ID、工单或申请结果；一次提交可能返回多个申请记录。

服务列表、所选 catalog 详情和业务组发现步骤不能省略。如果 `smartcmp_list_available_bgs` 只返回一个业务组，Agent 可以直接使用；如果返回多个，必须让用户选择。

## 相关技能 {#related-skills}

- `request`
- `datasource`
- `resource-pool`
- request decomposition agent
- preapproval agent

当用户不知道合法 SmartCMP 字段值时，应先使用 datasource 和 resource-pool 技能查询。

## 已提交申请状态 {#submitted-request-status}

当用户询问已提交申请的状态或审批结果时，使用 `smartcmp_get_request_status`，例如：

- “查询申请 RES20260501000095 的状态”；
- “申请 RES20260501000095 是否已经审批通过”；
- “我刚才提交的申请是否已经被批准了”。

输入是提交后返回给用户的 SmartCMP Request ID，例如 `RES20260501000095` 或 `TIC20260316000001`。如果用户说“刚才提交的申请”，应复用当前对话里最近一次提交返回的 Request ID；如果找不到，就要求用户提供 Request ID。

不要把 SmartCMP 内部 UUID 当作 Request ID。Typed submit 和 status Provider operation 可以在 API 查询中使用内部 ID，但不能向 Agent 展示这些值，也不能在后续状态查询中使用它们。

状态查询和审批动作是不同任务。用户查询自己已提交申请的状态或审批结果时，使用 request 状态查询工具；只有查看待审批任务或执行同意/拒绝时，才使用 approval 技能。

## Request ID 契约 {#request-id-contract}

`smartcmp_submit_request` 返回包含 `items` 列表的结构化结果。每一项代表一条 SmartCMP 申请记录；SmartCMP 返回用户可见标识时，该标识会出现在标准化的 `request_id` 字段中。因此一次提交可以返回多条申请记录和多个 outcome，例如 `REQ20260501000095`、`RES20260501000095`、`TIC20260316000001` 和 `CHG20260413000011`。

Submit Provider operation 可能收到 SmartCMP 的 `workflowId`、`requestNo` 或 `customizedId` 等上游别名。它会把每个合法别名标准化为 `items[].request_id`，再由薄 Skill Adapter 返回给 Agent。必须检查每一项的 `outcome`；只有 Request ID 并不能把 pending 或 failed outcome 变成已确认成功。内部 UUID 只是 Provider 实现细节，不能作为用户回答或后续 Tool 调用中的 Request ID。

后续状态查询必须使用相关的用户可见 Request ID。用户询问“刚才提交的申请”时，应复用对话中最近且适用的 `items[].request_id`，不能要求或暴露内部 ID。如果一次提交返回多个 ID，且无法判断用户指的是哪一个，应让用户选择。

状态 Provider operation 返回稳定字段，例如 `state`、`status_category`、`approval_passed`、`current_step`、`current_approver`、`provision_state`、`error` 和 `updated_at`。薄 Skill Adapter 将这些 typed 结果转换为 AtlasClaw Tool 输出，Agent 可以用用户当前语言解释这些字段。

常见审批结果语义：

| State | 含义 |
| --- | --- |
| `APPROVAL_PENDING` | 尚未审批通过，仍在审批中。 |
| `APPROVAL_REJECTED`、`APPROVAL_RETREATED` | 审批未通过。 |
| `STARTED`、`TASK_RUNNING`、`WAIT_EXECUTE`、`FINISHED` | 审批已通过，或申请已进入后续执行阶段。 |
| `INITIALING`、`INITIALING_FAILED`、`FAILED`、`CANCELED` | 只报告当前状态，不声称已批准或已拒绝。 |

## 需要收集的信息 {#information-to-collect}

| 信息 | 作用 |
| --- | --- |
| 服务目录项 | 决定申请 schema 和组件类型。 |
| 业务组/租户/项目 | 决定 SmartCMP 中的归属和授权。 |
| 资源池 | 决定资源部署位置。 |
| 模板、镜像或规格 | 提供部署参数。 |
| 数量和容量 | 影响成本和资源规模。 |
| 业务理由 | 支持审批和审计。 |

## 提交前生成草稿 {#draft-before-submit}

自然语言需求不明确时，应先用 request decomposition agent 生成草稿，并标记未解决字段。只有用户 review 完整 JSON 申请体并确认后才提交。

## 安全边界 {#safety-boundary}

提交 SmartCMP 申请会创建上游流程。必填字段缺失、用户只要求查询、服务目录项有歧义，或 JSON 预览尚未得到用户确认时，都不能提交。Agent 展示 JSON 预览后必须停止，等待用户确认。
