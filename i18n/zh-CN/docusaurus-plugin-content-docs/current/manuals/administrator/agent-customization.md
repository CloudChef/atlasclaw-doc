---
title: Agent 定制
description: 定制 AtlasClaw Agent 的身份、风格、行为和记忆。
sidebar_position: 6
---

# Agent 定制

AtlasClaw 支持文件型 Agent 定义和数据库型 Agent 配置。当前前端没有完整的 Agent Template 编辑器。当前运行时在存在数据库型配置时可用于支持的 `main` Agent 路径，其他 Agent ID 仍应放在 `.atlasclaw/agents/<agent_id>/` 文件目录中。

完整多 Agent 定制应使用文件。`agent-configs` API 适合部署有意管理当前支持的数据库型 main-agent 记录时使用。

## 文件型配置 {#file-based-configuration}

主 Agent 定义位于：

```text
.atlasclaw/agents/main/
├── SOUL.md
├── IDENTITY.md
├── USER.md
└── MEMORY.md
```

其他 Agent 可放在 `.atlasclaw/agents/<agent_id>/`。

## 支持字段 {#supported-fields}

| 文件 | 字段 |
| --- | --- |
| `SOUL.md` | `name`、`system_prompt`、`capabilities`、`allowed_providers`、`allowed_skills` |
| `IDENTITY.md` | `display_name`、`avatar`、`tone` |
| `USER.md` | `interaction_style` |
| `MEMORY.md` | `memory_strategy`、`max_context_rounds` |

## 名称和品牌展示面 {#name-and-branding-surfaces}

- 产品名称：AtlasClaw UI 文案和文档品牌。
- Agent ID：如 `main` 的稳定运行时标识。
- Agent name：用于 `/api/agent/info` 和欢迎信息。
- Display name：人类可读的 Agent 名称。
- Tone 和 style：影响回复风格的指导。

修改产品品牌和修改 Agent 显示名不是同一件事。如果需要更改产品层面的 AtlasClaw 名称，应作为 UI 或配置改动单独处理。

## API 型配置 {#api-based-configuration}

`agent-configs` API 可以创建、查询、更新和删除数据库型 Agent 记录。应把它视为当前支持的 DB-backed Agent 记录 API 工作流，而不是所有前端 Agent Template 或额外 Agent ID 都会从数据库加载的证明。
