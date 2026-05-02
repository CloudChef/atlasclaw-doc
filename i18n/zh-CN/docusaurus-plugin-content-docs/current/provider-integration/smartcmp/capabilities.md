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
- 资源启动、停止等操作。
- 告警列表、分析和状态操作。
- 成本优化建议、执行和跟踪。
- 资源生命周期、补丁、安全和配置合规分析。

Provider 技能从 SmartCMP Provider 包加载，并带有 Provider 命名空间。

## Skill 地图 {#skill-map}

| Skill | 类型 | 主要操作 |
| --- | --- | --- |
| `datasource` | 只读发现 | 服务目录、业务组、模板、镜像、资源详情。 |
| `resource-pool` | 只读目录 | 列出和过滤资源池。 |
| `resource` | 目录和 day-2 | 列资源或云主机、查看详情、启动或停止资源。 |
| `request` | 申请和状态 | 构造并提交 SmartCMP 服务或资源申请；按 Request ID 查询已提交申请状态。 |
| `approval` | 流程 | 列出待审批、同意、拒绝。 |
| `alarm` | 监控 | 列告警、分析告警、操作告警状态。 |
| `cost-optimization` | FinOps | 列建议、分析节省、执行原生修复、跟踪执行。 |
| `resource-compliance` | 分析 | 获取资源并分析生命周期、补丁、安全和配置状态。 |

## 读写边界 {#read-vs-write-capabilities}

只读发现 Skill 适合配置完成后的首次测试。提交申请、审批/拒绝、资源启停、告警状态操作和成本修复执行都属于有副作用流程，需要明确用户意图。
