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
4. 对每个 active 可选字段重新查询 SmartCMP 当前候选，包括带默认值的字段。
5. 在服务、业务组、部署位置、规格和模板范围确定后补齐剩余字段。
6. 构造申请 JSON，并重新校验精确选中的部署位置。
7. 展示完整 JSON 预览，对凭证值进行掩码，并请用户确认。
8. 只有用户确认后，才用 `smartcmp_submit_request` 提交对应的未掩码 JSON。
9. 在 SmartCMP 中跟踪返回的 Request ID、工单或申请结果；一次提交可能返回多个申请记录。

服务列表、所选 catalog 详情和业务组发现步骤不能省略。只有显式允许自动选择的只读查询返回唯一可见候选时，Agent 才能直接继续；多个候选必须由用户已有表述唯一匹配其中一项，否则应提出简洁的单项选择问题。

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

输入是提交后返回给用户的精确 SmartCMP Request ID。它的格式是不透明的，可以使用常见前缀、纯数字，也可以呈 UUID 形态。如果用户说“刚才提交的申请”，应复用当前对话里最近一次提交返回的 Request ID；如果找不到，就要求用户提供 Request ID。

必须原样保留用户提供或 SmartCMP 返回的 Request ID，不要限制前缀、字符集或固定长度。用户可见 Request ID 本身可以呈 UUID 形态；禁止的是用 SmartCMP 单独的内部对象 `id` 替换用户可见 Request ID，而不是禁止某种字符串形态。

状态查询和审批动作是不同任务。用户查询自己已提交申请的状态或审批结果时，使用 request 状态查询工具；只有查看待审批任务或执行同意/拒绝时，才使用 approval 技能。

## Request ID 契约 {#request-id-contract}

`smartcmp_submit_request` 返回包含 `items` 列表的结构化结果。每一项代表一条 SmartCMP 申请记录；SmartCMP 返回用户可见标识时，该标识会出现在标准化的 `request_id` 字段中。因此一次提交可以返回多条申请记录和多个 outcome，例如 `REQ20260501000095`、`RES20260501000095`、`TIC20260316000001` 和 `CHG20260413000011`。

Submit Provider operation 可能收到 SmartCMP 的 `workflowId`、`requestNo` 或 `customizedId` 等上游别名。它会把每个合法别名标准化为 `items[].request_id`，再由薄 Skill Adapter 返回给 Agent。必须检查每一项的 `outcome`；只有 Request ID 并不能把 pending 或 failed outcome 变成已确认成功。单独的内部对象 `id` 只是 Provider 实现细节，不能替换用户回答或后续 Tool 调用中的 `items[].request_id`。

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

## 候选解析与部署位置校验 {#choice-resolution-and-placement-validation}

生成的 catalog metadata 中的默认值只是建议，不能证明该值当前仍可申请。每个 active 可选字段都必须执行实时查询。只有显式允许自动选择的只读查询返回唯一可见候选时，工作流才能自动继续；存在多个候选时，只有用户已有意图能够唯一匹配其中一项才可继续，否则应只询问一个选择并停止。

部署位置相关字段按以下依赖顺序解析：

1. 资源池标签与资源池；
2. 计算规格，以及需要显式选择时的云规格；
3. 逻辑模板；
4. 物理模板或云镜像二选一。

对精确识别为 vSphere 的资源池，SmartCMP 会根据选中的 `computeProfileId` 解析 `flavorId`；此时应省略 `flavorId`，不能发送空值或复制计算规格 ID。其他平台或平台信息不明确时必须安全拒绝，并执行正常的规格查询。

展示预览前，Provider 必须重新读取所选资源池，并确认其仍然有效、所有必要选择都已具备且没有配置错误。选择发生变化或失效时，不得展示可确认预览，也不得提交。

## 模板分支 {#template-branches}

所选 catalog 合同决定序列化哪个互斥模板分支：

| 分支 | 申请体必需字段 | 必须省略的字段 |
| --- | --- | --- |
| 物理模板 | `logicTemplateId` 和 `physicalTemplateId` | `templateId` |
| 云镜像 | `logicTemplateId` 和 `templateId` | `physicalTemplateId` |

不得把镜像 ID 写入 `physicalTemplateId`。显示名称只用于用户选择；申请体使用当前实时查询返回的精确 ID。

镜像和规格查询采用分页，每页最多 50 行。大型清单应使用 `query` 缩小范围，并使用 `page` 继续，不能把第一页当成完整结果。

## 提交前生成草稿 {#draft-before-submit}

自然语言需求不明确时，应先用 request decomposition agent 生成草稿，并标记未解决字段。只有用户 review 完整 JSON 申请体并确认后才提交。凭证值只在展示的预览中掩码，提交体必须使用保留的原始值。

## 安全边界 {#safety-boundary}

提交 SmartCMP 申请会创建上游流程。必填字段缺失、用户只要求查询、服务目录项有歧义，或 JSON 预览尚未得到用户确认时，都不能提交。Agent 展示 JSON 预览后必须停止，等待用户确认。预览后新增或修改任何申请字段或密钥都会使原确认失效，必须重新校验、展示预览并取得确认。
