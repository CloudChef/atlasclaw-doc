---
slug: /
title: AtlasClaw 文档
description: AtlasClaw Core 安装、运维和集成文档。
sidebar_position: 1
---

# AtlasClaw 文档

AtlasClaw 是企业 Agent 框架，用于把运维系统、业务流程和内部工具接入到受治理的对话入口。

本仓库文档以 Core 为主：运行时、配置、用户、角色、会话、Agent、渠道、模型、技能、工具和 Provider 加载契约。具体 Provider 的认证、字段和业务流程只放在 Provider Integration 章节。

## 从这里开始 {#start-here}

- 安装部署请看 Installation Guide。
- 用户、角色、模型、Provider、渠道和 Agent 配置请看 Administrator Guide。
- 对话、账号、Provider Token 和个人 IM 渠道请看 User Guide。
- SmartCMP 等具体集成请看 Provider Integration。

## 本站覆盖范围 {#what-this-site-covers}

| 范围 | 读者 | 结果 |
| --- | --- | --- |
| 安装手册 | 运维人员 | 安装 AtlasClaw，配置 workspace 路径并验证服务启动。 |
| 管理员手册 | 管理员 | 配置用户、角色、模型、Provider 实例、渠道和 Agent。 |
| 用户手册 | Standard User | 使用对话、账号设置、Provider Token 和个人 IM 渠道。 |
| Core | 开发者和运维 | 理解运行时边界、会话、认证、技能、记忆、渠道、Hook 和 Heartbeat。 |
| Provider Integration | Provider 维护者 | 安装和运行具体 Provider 包，并保持 Core 文档边界清晰。 |
| Reference | 运维和集成人员 | 查询配置字段、API 分组、权限和功能矩阵。 |

## 推荐上线顺序 {#operating-model}

1. 安装 Core，并确认管理员账号可以登录。
2. 配置至少一个模型，并验证基础对话可用。
3. 设置 `providers_root`，确认 Provider 包可以被发现。
4. 创建 Provider 实例，并给角色分配 Provider 运行时访问权。
5. 只开启用户需要使用的技能。
6. Provider 或渠道实例准备好之后，再让用户配置个人 Provider Token 或 IM 渠道。

## 文档边界 {#documentation-boundary}

Core 文档不能把 SmartCMP、Jira 或其他 Provider 写成 Core 内置能力。Core 只拥有运行时契约，Provider 包拥有具体认证、字段、流程和业务语义。

Provider 规则需要作为示例说明时，应放在 Provider Integration 中。Core 页面可以链接到 Provider 页面，但不复制 Provider 字段、接口细节或业务流程语义。
