---
title: 申请流程
description: 提交 SmartCMP 服务和资源申请。
sidebar_position: 7
---

# 申请流程

SmartCMP request 技能帮助用户把基础设施需求转换成结构化 SmartCMP 申请。

## 典型流程 {#typical-flow}

1. 先用 `smartcmp_list_services` 查询已发布服务。
2. 再用 `smartcmp_list_available_bgs` 查询可用业务组。
3. 在服务和业务组范围确定后补齐缺失字段。
4. 构造申请 JSON。
5. 展示完整 JSON 预览并请用户确认。
6. 只有用户确认后，才用 `smartcmp_submit_request` 提交。
7. 在 SmartCMP 中跟踪工单或申请结果。

服务列表和业务组发现步骤不能省略。如果 `smartcmp_list_available_bgs` 只返回一个业务组，Agent 可以直接使用；如果返回多个，必须让用户选择。

## 相关技能 {#related-skills}

- `request`
- `datasource`
- `resource-pool`
- request decomposition agent
- preapproval agent

当用户不知道合法 SmartCMP 字段值时，应先使用 datasource 和 resource-pool 技能查询。

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
