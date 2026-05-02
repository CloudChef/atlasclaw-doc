---
title: SmartCMP Provider
description: SmartCMP Provider 概览和来源边界。
sidebar_position: 1
---

# SmartCMP Provider

SmartCMP Provider 将 AtlasClaw 连接到 SmartCMP 云管理平台工作流，支持资源申请、已提交申请状态查询、审批、目录查询、资源操作、告警、成本优化和资源合规分析。

权威来源是 Provider 包：

```text
atlasclaw-providers/providers/SmartCMP-Provider/
├── README.md
├── PROVIDER.md
├── provider.schema.json
└── skills/
```

本文档总结稳定的安装、配置和使用流程。实现细节仍以 Provider 仓库为准。

## 读者 {#audience}

- 配置 SmartCMP Provider 实例的 AtlasClaw 管理员。
- 需要配置 SmartCMP user token 的 Standard User。
- 校验文档和 Provider Skill 一致性的 Provider 维护者。
- 排查 SmartCMP 认证或 Skill 执行问题的运维人员。

## 能力范围 {#capability-areas}

| 范围 | 典型意图 |
| --- | --- |
| Request | 提交服务目录或资源申请，或按 Request ID 查询已提交申请状态。 |
| Approval | 列出待审批任务，并带原因同意或拒绝。 |
| Datasource | 查询服务、业务组、模板、镜像和资源事实。 |
| Resource pool | 列出和过滤资源池。 |
| Resource | 浏览资源、查看云主机并执行 start/stop。 |
| Alarm | 在明确请求时列出、分析、mute、resolve 或 reopen 告警。 |
| Cost optimization | 查看建议、执行原生修复并跟踪整改。 |
| Resource compliance | 分析资源生命周期、补丁、安全和配置状态。 |
