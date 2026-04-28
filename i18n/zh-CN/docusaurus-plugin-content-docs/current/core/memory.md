---
title: 记忆
description: 用户隔离的记忆和上下文持久化。
sidebar_position: 6
---

# 记忆

记忆保存可复用的用户和对话上下文。

## 存储模型 {#storage-model}

记忆按用户隔离，避免一个用户的长期信息进入另一个用户会话。

记忆适合保存可复用上下文、偏好和摘要，不应用作 Provider Token、Cookie、Webhook Secret 或密码的安全存储。

## 记忆类型 {#memory-types}

Core 支持 daily、long-term 和 ephemeral 记忆类型。当角色允许时，Agent 运行时可以搜索记忆并读取指定条目。

| 类型 | 典型内容 |
| --- | --- |
| Daily | 近期任务摘要和短期上下文。 |
| Long-term | 稳定偏好、长期项目和耐久用户上下文。 |
| Ephemeral | 不应变为长期知识的临时运行时备注。 |

## Agent 记忆设置 {#agent-memory-settings}

`MEMORY.md` 控制 Agent 级别的记忆策略和 `max_context_rounds`，用于调节近期对话保留和压缩策略。

## 治理 {#governance}

管理员应决定部署中允许的记忆行为。受监管环境应说明长期记忆是否启用、如何删除，以及哪些数据类型永远不应写入记忆。
