---
title: 安装手册
description: 安装并启动 AtlasClaw Core。
sidebar_position: 1
---

# 安装手册

本手册用于安装 AtlasClaw Core，并准备本地或托管部署环境。

AtlasClaw Core 包含 API 层、认证中间件、Agent 运行时、会话、记忆、渠道、模型配置、角色权限和 Provider 加载。具体 Provider 包单独安装，并通过 `providers_root` 引用。

## 安装流程 {#installation-flow}

1. 确认运行环境。
2. 安装 Python 和前端依赖。
3. 创建 `atlasclaw.json`。
4. 配置模型访问和认证。
5. 启动服务。
6. 如需集成外部系统，再添加 Provider 包。
