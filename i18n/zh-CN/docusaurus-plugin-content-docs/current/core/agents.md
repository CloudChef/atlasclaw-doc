---
title: Agent
description: Agent 定义、元数据和运行时配置。
sidebar_position: 4
---

# Agent

AtlasClaw Agent 由身份、系统指令、交互风格、允许能力和记忆行为组成。

## 文件型定义 {#file-based-definitions}

Agent 文件位于 `.atlasclaw/agents/<agent_id>/`：

- `SOUL.md`：系统提示词、能力、允许 Provider、允许技能。
- `IDENTITY.md`：显示名、头像和语气。
- `USER.md`：个性化和交互风格。
- `MEMORY.md`：记忆策略和最大上下文轮数。

## 运行时元数据 {#runtime-metadata}

`/api/agent/info` 读取主 Agent 定义，并为聊天 UI 返回名称、描述、欢迎语和解析后的 soul 数据。

## 数据库 Agent 配置 {#database-agent-configs}

`agent-configs` API 可以创建、查询、更新和删除数据库型 Agent 记录。当前运行时启动路径可以在存在时加载 `main` Agent 的数据库型配置，然后回退到文件型定义；其他 Agent ID 仍通过 `.atlasclaw/agents/<agent_id>/` 文件定义。

请把 `agent-configs` 用于当前支持的数据库型 main-agent 工作流。除非部署明确接入了额外逻辑，不要把它理解为完整的前端 Agent Template 目录。

## 配置来源 {#configuration-sources}

| 来源 | 适用场景 |
| --- | --- |
| 文件型 Agent | 稳定默认 Agent、可纳入版本控制的部署配置。 |
| 数据库 Agent Config | 使用 DB-backed 路径的 main-agent API 管理记录。 |
| 用户设置 | 不应改变全局 Agent 身份的个人化设置。 |

## Agent 设计 Checklist {#agent-design-checklist}

- 名称和显示名对用户清晰。
- 语气和交互风格符合运维环境。
- 系统提示词说明权限边界和凭证处理。
- allowed providers 和 allowed skills 与角色策略一致。
- 写操作需要明确用户意图。
