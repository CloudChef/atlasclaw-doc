---
title: 术语表
description: AtlasClaw 常用术语。
sidebar_position: 5
---

# 术语表

## Agent {#agent}

回答用户请求并使用授权技能与工具的运行时人格和执行单元。

Agent 主要由 `.atlasclaw/agents/<agent_id>/` 下的文件定义。当前支持的 `main` Agent 路径也可以在部署启用时使用数据库型 Agent Config 记录。

## Channel {#channel}

AtlasClaw 与用户或系统消息入口之间的连接。

示例包括 Web Chat、REST、WebSocket、SSE 和受支持的 IM 渠道。Channel 连接默认归具体用户所有。

## Provider {#provider}

Core 通过 `providers_root` 加载的外部集成包。

Provider 拥有具体认证字段、Skill 工作流、业务术语和上游 API 行为。

## Provider Instance {#provider-instance}

某个 Provider 环境的配置连接，例如生产或测试实例。

Provider 实例运行时访问权与创建或编辑实例记录的权限不是一回事。

## Skill {#skill}

定义 Agent 何时以及如何使用工具或 Provider 工作流的能力描述。

Provider Skill 应使用 Provider 命名空间，避免名称冲突。

## Standard User {#standard-user}

标识符为 `user` 的内置角色，是默认协作用户角色。

默认 Standard User 可以使用对话、查看已启用技能，并管理自己的 Channel 连接。

## Workspace {#workspace}

Agent、用户、会话、记忆和运行状态的存储根目录。

## Provider Token {#provider-token}

用户自有 Provider 凭证，绑定到 Provider 类型和实例名。它与 IM Channel 凭证不同。

## Model Config {#model-config}

管理员配置模型 Provider、模型 ID、端点和模型 Token 的记录。

## Runtime Access {#runtime-access}

从 Agent 对话中调用 Skill 或 Provider 实例的能力。它不同于编辑相关配置的管理权限。
