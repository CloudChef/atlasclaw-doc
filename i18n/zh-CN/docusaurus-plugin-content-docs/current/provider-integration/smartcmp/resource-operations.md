---
title: 资源操作
description: 浏览和操作 SmartCMP 资源。
sidebar_position: 9
---

# 资源操作

SmartCMP resource 技能支持资源浏览和部分 day-2 操作。

## 浏览 {#browsing}

用户可以列出资源、筛选云主机、按 ID 查看资源，并使用 Provider 脚本返回的标准化资源视图。

典型发现操作包括：列出全部资源、列出全部云主机、按关键字过滤、按资源 ID 刷新并分析单台主机、获取资源详情用于合规或排障。

## 操作 {#operations}

资源操作技能在解析目标资源 ID 后支持明确动作，例如 start 和 stop。

操作是否成功取决于用户在 SmartCMP 中的权限和目标资源当前状态。

## 操作安全 {#operation-safety}

Start 和 stop 会改变上游资源状态。执行前必须展示目标资源名称、资源 ID、可用时的当前状态和目标动作。Agent 应询问明确确认，例如 `确认要执行吗？`，然后停止；只有用户确认后才调用操作。

## 常见阻塞 {#common-blockers}

| 阻塞 | 含义 |
| --- | --- |
| Resource not found | ID 错误或当前凭证不可见。 |
| Unsupported action | 资源类型不支持该 day-2 动作。 |
| Permission denied | SmartCMP 接受凭证但拒绝操作。 |
| Current state mismatch | 资源已停止、运行中或处于过渡状态。 |
