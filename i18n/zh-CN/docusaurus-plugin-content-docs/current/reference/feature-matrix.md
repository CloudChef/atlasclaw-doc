---
title: 功能矩阵
description: 文档到角色、UI、API 和源码模块的映射。
sidebar_position: 4
---

# 功能矩阵

| 功能 | 主要角色 | UI 入口 | API 区域 | 源码区域 |
| --- | --- | --- | --- | --- |
| 对话 | Standard User | `/` | `/api/agent`, `/api/sessions` | `app/atlasclaw/agent`, `api/routes_agent.py` |
| 内嵌菜单 UI | Standard User | 内嵌 `surface=menu` | `/api/embed/bootstrap`、Chat API | `core/embed`, `scripts/embed` |
| 上下文感知悬浮 UI | Standard User | 内嵌 `surface=floating` | `/api/embed/*`, `/api/agent/run` | `core/embed`, `scripts/embed` |
| 账号资料 | Standard User | `/account` | `/api/users/me/*` | `api/api_routes.py`, `pages/account-settings.js` |
| Provider Token | Standard User | `/account` | `/api/users/me/provider-settings` | `api/api_routes.py` |
| IM 渠道 | Standard User | `/channels` | `/api/channels/*` | `channels/`, `pages/channels.js` |
| 用户 | Administrator | `/admin/users` | `/api/users` | `db/orm/user.py`, `pages/admin-users.js` |
| 角色 | Administrator | `/admin/roles` | `/api/roles` | `db/orm/role.py`, `pages/role-management.js` |
| 模型 | Administrator | `/models` | `/api/model-configs` | `api/model_config_routes.py`, `pages/models.js` |
| Provider 实例 | Administrator | `/providers` | `/api/provider-configs` | `api/api_routes.py`, `pages/providers.js` |
| Agent 配置 | Administrator | 文件/API | `/api/agent-configs` | `agent/agent_definition.py`, `db/orm/agent_config.py` |
| Provider 集成 | User/Admin | Chat, Account, Providers | Provider 工具/配置 API | `providers_root` 下的 Provider 包 |

更新文档时可把本矩阵作为 review 清单。

## Review Checklist {#review-checklist}

功能变化时，应同步检查：用户流程页、管理员流程页、Core 行为页、Provider Integration 页、Reference 页，以及 `i18n/zh-CN` 下的中文翻译。

## 权威来源规则 {#source-of-truth-rules}

| 内容类型 | 权威来源 |
| --- | --- |
| 权限默认值 | Role service 和 auth guard 代码。 |
| Channel 必填字段 | Channel handler schema 和 validation 代码。 |
| Agent 文件解析 | Agent definition parser 和 Agent config service。 |
| Provider 字段 | Provider `provider.schema.json`。 |
| Provider 工作流 | Provider `README.md`、`PROVIDER.md` 和 Skill 文件。 |
| API 路由 | FastAPI route 模块。 |
