---
title: 能力
description: SmartCMP 能力地图。
sidebar_position: 6
---

# 能力

SmartCMP Provider 提供以下能力：

- 云资源、虚拟机、应用和工单类服务申请，以及按 Request ID 查询已提交申请状态。
- 待审批任务管理。
- 业务组、服务目录、资源池、资源、云主机、模板、镜像等目录查询。
- 跨告警、监控健康、资源优先的安全状态及关联违规和费用优化的单资源综合分析，以及资源启动、停止等操作。
- 告警列表、告警分析、模型驱动的资源健康分析和明确的告警状态操作。
- 成本优化建议、直接资源费用分析、已有发现的执行和跟踪。
- CMP 全局 Security 合规总览、违规浏览、单条违规最新分析，以及经单独确认后仅更新状态的“标记已修复”操作。
- 表单定义、脚本、成本优化策略和蓝图组件脚本的上下文绑定辅助。这些 Skill 会生成完整替换内容，但不会保存、发布、执行或部署。

Provider 技能从 SmartCMP Provider 包加载，并带有 Provider 命名空间。Skill callable Adapter 调用 `smartcmp_provider` 中的 typed operation，不维护第二套 SmartCMP API 或认证实现。

## Skill 地图 {#skill-map}

| Skill | 类型 | 主要操作 |
| --- | --- | --- |
| `datasource` | 只读发现 | 服务目录、业务组、模板、镜像、资源详情。 |
| `resource-pool` | 只读目录 | 列出和过滤资源池。 |
| `resource` | 目录、分析协调和 day-2 | 列资源或云主机、查看详情、分析单个资源的安全状态及关联 CMP 违规、协调只读综合分析，并执行受支持的资源操作。 |
| `request` | 申请和状态 | 构造并提交 SmartCMP 服务或资源申请；按 Request ID 查询已提交申请状态。 |
| `approval` | 流程 | 列出待审批、同意、拒绝。 |
| `alarm` | 监控 | 列出和分析告警，或根据组件监控模型分析资源健康。 |
| `cost-optimization` | FinOps | 列出和分析建议、直接分析资源、对已有发现执行原生修复并跟踪执行。 |
| `security-compliance` | 安全分析与状态处理 | 查看 CMP 全局 Security 状态、列出安全违规、重新分析单条违规，并在不整改资源的前提下显式确认将其状态标记为 FIXED。 |
| `form-designer` | 只读编辑辅助 | 读取已保存的表单定义并生成完整、规范化的替换 schema。 |
| `script-designer` | 只读编辑辅助 | 读取已保存的脚本并为其 `content` 字段生成完整替换内容。 |
| `optimization-policy-designer` | 只读编辑辅助 | 读取成本优化策略并生成替换 `ruleContent` 和需要变更的字段。 |
| `component-script-designer` | 只读编辑辅助 | 读取一个精确的蓝图组件脚本文件并生成完整替换内容。 |

## 上下文感知页面匹配 {#context-aware-page-matching}

SmartCMP Provider 当前会在运行时匹配以下标准化页面：

| SmartCMP 页面 | Context 对象 | 所属 Skill |
| --- | --- | --- |
| 触发告警详情 | 告警 | `smartcmp:alarm` |
| 费用建议详情 | 费用优化建议 | `smartcmp:cost-optimization` |
| Security 合规记录 | 安全违规集合 | `smartcmp:security-compliance` |
| Security 策略编辑 | Security 策略 | `smartcmp:security-compliance` |
| 待审批详情 | 审批申请 | `smartcmp:approval` |
| 工单审批详情 | 审批申请 | `smartcmp:approval` |
| 服务目录申请 | Catalog | `smartcmp:request` |
| 工单申请 | Catalog | `smartcmp:request` |
| My Application 申请详情 | 已提交申请 | `smartcmp:request` |
| 工单“我的申请”详情 | 已提交申请 | `smartcmp:request` |
| 云资源详情 | 资源 | `smartcmp:resource` |
| 虚拟机详情 | 虚拟机 | `smartcmp:resource` |
| 表单编辑或设计 | 表单定义 | `smartcmp:form-designer` |
| 脚本编辑 | 脚本定义 | `smartcmp:script-designer` |
| 成本优化策略编辑 | 优化策略 | `smartcmp:optimization-policy-designer` |
| 蓝图组件编辑 | 蓝图组件 | `smartcmp:component-script-designer` |

SmartCMP 报告更新的页面 generation 时，悬浮助手会重新执行匹配。Provider Resolver 随后加载当前对象并构造状态相关操作。为已经支持的对象和所属 Skill 增加另一条路径时，只需增加 Provider 路由，不需要在 Core 或 UI 添加业务映射。

在工单审批页面中，只有精确匹配的待审批任务会展示分析、同意和拒绝；已完成或状态不一致的记录保持只读。Security 策略编辑路由也只提供只读 Context，不增加策略变更操作。

## 有界列表 {#bounded-lists}

SmartCMP 列表 Tool 返回有界分页，不会把无限制的上游集合复制到一次 Agent turn。大多数 Tool schema 每页最多接受 50 行；回收站浏览每页最多 20 个 deployment，因为一个 deployment 可能展开成多条资源行。大型集合应使用支持的 `query` 或过滤条件缩小范围，并在 `has_more` 或覆盖状态表明仍有数据时推进 `page`。

## 读写边界 {#read-vs-write-capabilities}

只读发现 Skill 适合配置完成后的首次测试。提交申请、审批/拒绝、受支持的资源状态变更、告警状态操作、成本修复执行和将安全违规标记为 FIXED 都属于有副作用流程，需要明确用户意图。“标记已修复”必须单独确认，并且只更新违规状态，不会修改或整改资源。编辑辅助即使返回完整替换文档或脚本，仍然是只读能力。
