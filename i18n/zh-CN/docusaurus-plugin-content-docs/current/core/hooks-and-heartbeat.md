---
title: Hooks 和 Heartbeat
description: 运行时 Hook 事件、待处理决策和心跳任务。
sidebar_position: 8
---

# Hooks 和 Heartbeat

Hooks 和 Heartbeat 让 AtlasClaw 在不把 Provider 行为写入 Core 的情况下运行后台或事件驱动逻辑。

## Hooks {#hooks}

Hook 路由暴露模块事件、待处理决策、确认和拒绝操作。Hook 状态按用户和模块隔离。

当工作流需要显式决策点时使用 Hook。Hook 可以记录 pending item，暴露给用户 review，然后接收 confirm 或 reject。

## Sinks {#sinks}

Hook handler 可以通过 runtime sink 写入 memory 或 context，使副作用明确且可审计。

## Heartbeat {#heartbeat}

Heartbeat 任务可以面向 Agent 或渠道，并发出运行时事件。它适合周期性检查、提醒或后台流程，同时仍需遵守用户范围和运行时权限。

Heartbeat 事件包括 agent started/completed/failed，以及 channel check/reconnect/degraded 等状态。它们可以桥接到 Hook runtime 事件。

## 适用场景 {#when-to-use-heartbeat}

Heartbeat 适合周期性 Channel 健康检查、计划 Agent 提醒、需要用户范围的后台提醒，以及长连接渠道重连。不要把 Provider 专属轮询语义藏在 Core 中。
