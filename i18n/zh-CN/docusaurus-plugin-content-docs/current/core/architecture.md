---
title: Core 架构
description: AtlasClaw Core 运行时架构和 Provider 边界。
sidebar_position: 1
---

# Core 架构

AtlasClaw Core 是与 Provider 无关的运行时，负责 API、认证、会话隔离、Agent 执行、模型访问、渠道、记忆、Hook 和 Provider 加载。

## 主要组件 {#main-components}

- API 层：REST、流式响应、认证、会话、渠道和管理路由。
- Agent 运行时：Prompt 构造、工具路由、执行、流式输出和压缩。
- 会话与记忆：按用户隔离的对话状态和长期记忆。
- 认证与 RBAC：认证、角色权限和请求授权。
- 渠道运行时：用户自有渠道连接和消息 handler。
- Provider Registry：外部 Provider 发现和实例配置。

## 运行时职责 {#runtime-responsibilities}

Core 负责所有 Provider 都必须遵守的共性行为：身份解析、授权检查、按用户和渠道隔离会话、按权限暴露工具、使用已配置模型、维护凭证边界，并把运行时状态保存在 workspace 中。

## Provider 边界 {#provider-boundary}

Core 加载 Provider，但不拥有 Provider 特定的认证字段、工作流语义、业务对象或 UI 文案。具体 Provider 行为应放在 Provider Integration 中。

## 运行流程 {#runtime-flow}

1. 用户完成认证。
2. 请求解析授权上下文。
3. 会话 key 按用户、渠道和线程隔离状态。
4. Agent 运行时构造上下文和可用工具。
5. Provider 和技能权限过滤运行时能力。
6. 回复通过所选渠道返回。

## Core 不负责什么 {#what-core-does-not-do}

Core 不定义 Provider 专属申请表、审批语义、资源目录、Token 格式或业务状态。这些概念由 Provider 包和 Provider Integration 文档负责。
