---
title: SmartCMP Provider
description: SmartCMP Provider 概览和来源边界。
sidebar_position: 1
---

# SmartCMP Provider

SmartCMP Provider 将 AtlasClaw 连接到 SmartCMP 云管理平台工作流，支持资源申请、已提交申请状态查询、审批、目录查询、动态资源分析与操作、告警与资源健康分析、成本优化、资源优先的安全分析和 Security 合规违规工作流。

权威来源是 Provider 包：

```text
atlasclaw-providers/providers/SmartCMP-Provider/
├── README.md
├── PROVIDER.md
├── provider.schema.json
├── pyproject.toml
├── assistant_context/
├── src/
│   └── smartcmp_provider/
└── skills/
```

本文档总结稳定的安装、配置和使用流程。实现细节仍以 Provider 仓库为准。

`src/smartcmp_provider/` 是可复用的 SmartCMP Provider 实现，负责认证解析、typed model、API transport、领域 operation 和共享 service。`skills/` 是薄 AtlasClaw Adapter，只负责在 `RunContext`、Tool 输入输出与 Provider operation 之间转换。独立 SmartCMP MCP Adapter 会导入同一个 Provider 包，但它属于另一种独立入口；AtlasClaw 加载 SmartCMP Skills 时不经过 MCP。

SmartCMP 被配置为 HostApp Provider 时，AtlasClaw 会提供共享同一套 SmartCMP Cookie 认证的独立菜单 UI 和悬浮 UI。菜单 UI 提供完整 Chat，悬浮 UI 则动态跟随受支持的 SmartCMP 页面。SmartCMP Provider 的路由定义把当前页面绑定到审批、申请、告警、费用建议、安全违规集合或资源对象，并展示符合对象当前状态的操作。详见[内嵌菜单与悬浮 UI](../embedded-menu-and-floating-ui.md)。

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
| Resource | 浏览资源、分析单个资源的安全状态及关联 CMP 违规、协调综合分析，并执行允许的 day-2 操作。 |
| Alarm and health | 分析告警，或根据组件监控证据判断资源运行健康。 |
| Cost optimization | 查看建议或直接分析单个资源，只对已有发现执行原生修复并跟踪整改。 |
| Security compliance | 查看 CMP 全局 Security 状态、分析单条违规，并在人工整改和显式确认后仅将其状态标记为 FIXED。 |
