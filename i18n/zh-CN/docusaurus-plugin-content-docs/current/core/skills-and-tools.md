---
title: 技能和工具
description: 运行时技能、内置工具和权限过滤。
sidebar_position: 5
---

# 技能和工具

技能描述 Agent 能力，工具执行具体操作。

## 内置工具范围 {#built-in-tool-areas}

AtlasClaw Core 包含会话、记忆、网页搜索和抓取、Provider 实例选择、运行时执行、文件系统访问，以及启用时的浏览器自动化工具。

## Markdown 技能 {#markdown-skills}

Markdown 技能可以从 workspace、用户、外部目录或 Provider 目录加载。Provider 绑定技能会加上 Provider 命名空间，避免名称冲突。

Skill 描述何时使用、需要哪些输入、可以调用哪些脚本或工具，以及有哪些安全规则。Provider 专属术语应保留在 Provider 包中。

## 权限过滤 {#permission-filtering}

角色技能权限和 Provider 实例权限会过滤运行时暴露的技能与工具。Provider 绑定工具由 Provider 权限治理，而不是普通 Core 工具权限。

## 运维规则 {#operational-rule}

技能缺失或被禁用时，Agent 应说明访问阻塞，而不是假装能力可用。

## Skill 生命周期 {#skill-lifecycle}

1. 从配置的 Skill 目录或 Provider 包发现 Skill。
2. Registry 校验 Skill 名称和 metadata。
3. 角色策略决定该 Skill 是否可见和启用。
4. Provider 策略决定 Provider 绑定 Skill 是否有可用实例。
5. Agent 运行时只接收授权后的 Skill/Tool 集合。
6. Tool 输出作为证据供 Agent 继续推理。

## 写操作安全 {#write-action-safety}

提交申请、审批、修改资源状态或操作告警的 Skill 都应视为写操作。Skill 应补齐信息、确认意图，并如实报告上游错误。
