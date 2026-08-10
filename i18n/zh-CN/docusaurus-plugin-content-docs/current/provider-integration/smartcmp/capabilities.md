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

Provider 技能从 SmartCMP Provider 包加载，并带有 Provider 命名空间。Skill callable Adapter 调用 `smartcmp_provider` 中的 typed operation，不维护第二套 SmartCMP API 或认证实现。

## Skill 地图 {#skill-map}

| Skill | 类型 | 主要操作 |
| --- | --- | --- |
| `datasource` | 只读发现 | 服务目录、业务组、模板、镜像、资源详情。 |
| `resource-pool` | 只读目录 | 列出和过滤资源池。 |
| `resource` | 目录、分析协调和 day-2 | 列资源或云主机、查看详情、分析单个资源的安全状态及关联 CMP 违规、协调只读综合分析、启动或停止资源。 |
| `request` | 申请和状态 | 构造并提交 SmartCMP 服务或资源申请；按 Request ID 查询已提交申请状态。 |
| `approval` | 流程 | 列出待审批、同意、拒绝。 |
| `alarm` | 监控 | 列出和分析告警，或根据组件监控模型分析资源健康。 |
| `cost-optimization` | FinOps | 列出和分析建议、直接分析资源、对已有发现执行原生修复并跟踪执行。 |
| `security-compliance` | 安全分析与状态处理 | 查看 CMP 全局 Security 状态、列出安全违规、重新分析单条违规，并在不整改资源的前提下显式确认将其状态标记为 FIXED。 |

## 上下文感知页面匹配 {#context-aware-page-matching}

SmartCMP Provider 当前会在运行时匹配以下标准化页面：

| SmartCMP 页面 | Context 对象 | 所属 Skill |
| --- | --- | --- |
| 触发告警详情 | 告警 | `smartcmp:alarm` |
| 费用建议详情 | 费用优化建议 | `smartcmp:cost-optimization` |
| Security 合规记录 | 安全违规集合 | `smartcmp:security-compliance` |
| 待审批详情 | 审批申请 | `smartcmp:approval` |
| 服务目录申请 | Catalog | `smartcmp:request` |
| My Application 申请详情 | 已提交申请 | `smartcmp:request` |
| 云资源详情 | 资源 | `smartcmp:resource` |
| 虚拟机详情 | 虚拟机 | `smartcmp:resource` |

SmartCMP 报告更新的页面 generation 时，悬浮助手会重新执行匹配。Provider Resolver 随后加载当前对象并构造状态相关操作。为已经支持的对象和所属 Skill 增加另一条路径时，只需增加 Provider 路由，不需要在 Core 或 UI 添加业务映射。

## 读写边界 {#read-vs-write-capabilities}

只读发现 Skill 适合配置完成后的首次测试。提交申请、审批/拒绝、资源启停、告警状态操作、成本修复执行和将安全违规标记为 FIXED 都属于有副作用流程，需要明确用户意图。“标记已修复”必须单独确认，并且只更新违规状态，不会修改或整改资源。
