---
title: 环境要求
description: AtlasClaw Core 的运行和运维要求。
sidebar_position: 2
---

# 环境要求

## 运行时 {#runtime}

- Python 3.11 或更高版本。
- Python 虚拟环境。
- 能访问配置的模型服务。
- 可写 workspace 目录，用于会话、记忆、用户、运行状态和用户资源。

## 可选组件 {#optional-components}

- 数据库后端，用于用户、角色、模型配置、Provider 配置和渠道配置。
- `atlasclaw-providers` 仓库，用于加载外部 Provider 包。
- IM 平台凭证，用于 DingTalk、Feishu/Lark 或 WeCom 渠道连接。

## 安全要求 {#security-requirements}

不要把密钥提交到代码仓库。模型 API Key、Provider Token、Cookie 和服务凭证应通过环境变量或部署系统管理。
