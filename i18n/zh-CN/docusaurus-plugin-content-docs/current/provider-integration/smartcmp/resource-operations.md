---
title: 资源分析与操作
description: 浏览、综合分析和操作 SmartCMP 资源。
sidebar_position: 9
---

# 资源分析与操作

SmartCMP resource 技能支持资源浏览、单资源综合分析和部分 day-2 操作。

## 浏览 {#browsing}

用户可以列出资源、筛选云主机、按 ID 查看资源，并使用薄 AtlasClaw Skill Adapter 调用 typed Provider operation 后返回的标准化资源视图。

典型发现操作包括：列出全部资源、列出全部云主机、按关键字过滤、按资源 ID 刷新并分析单台主机、获取资源详情用于合规或排障。

## 资源综合分析 {#comprehensive-resource-analysis}

解析成功的云资源或虚拟机页面可以展示动态的“综合分析”操作。该操作使用 `resource` Skill 作为协调者，为四个现有只读分析器保留同一个精确的 SmartCMP 内部资源目标：

1. 当前告警，以及触发时间位于配置回溯窗口内且当前状态为已解决的告警；
2. 根据资源组件 Prometheus 监控模型分析运行健康；
3. 根据受限、脱敏的资源 Profile 分析通用合规风险；
4. 分析平台已确认和 LLM 推断的费用优化机会。

最终回答分别呈现各维度的证据和缺口，再说明跨维度关联。一个维度失败或证据不足不会阻止其他维度完成。综合分析不会修改资源。

该操作根据当前资源对象动态生成。用户进入另一个受支持的 SmartCMP 页面时，悬浮助手会解析新的 Context；之后携带旧 Context 提交的 Chat turn 会被拒绝，已经通过提交校验的 turn 则继续使用普通 Chat 运行时。

## 操作 {#operations}

资源操作技能在解析目标资源 ID 后支持明确动作，例如 start 和 stop。

操作是否成功取决于用户在 SmartCMP 中的权限和目标资源当前状态。

成功操作的输出应保持简洁，只包含动作、目标资源 ID、submitted 标记、面向用户的消息和验证提示。不要打印原始 SmartCMP 请求 payload 或原始响应详情。如果 SmartCMP 在 HTTP 200 响应中返回业务失败，工具应输出简短错误，而不是报告提交成功。

## 操作安全 {#operation-safety}

Start 和 stop 会改变上游资源状态。执行前必须展示目标资源名称、可用时的当前状态和目标动作。稳定的 SmartCMP 资源 ID 应在内部解析并保留，不要求用户提供，也不向用户展示。Agent 应询问明确确认，例如 `确认要执行吗？`，然后停止；只有用户确认后才调用操作。

## 常见阻塞 {#common-blockers}

| 阻塞 | 含义 |
| --- | --- |
| Resource not found | ID 错误或当前凭证不可见。 |
| Unsupported action | 资源类型不支持该 day-2 动作。 |
| Permission denied | SmartCMP 接受凭证但拒绝操作。 |
| Current state mismatch | 资源已停止、运行中或处于过渡状态。 |
