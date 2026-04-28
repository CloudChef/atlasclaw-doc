---
title: 升级和备份
description: 安全升级 AtlasClaw 并保留 workspace 数据。
sidebar_position: 5
---

# 升级和备份

## 升级前 {#before-upgrading}

备份：

- `atlasclaw.json`
- workspace 目录
- 数据库
- Provider 仓库
- 部署系统中的环境变量定义

## 升级步骤 {#upgrade-steps}

1. 停止服务。
2. 更新 AtlasClaw Core 到目标版本。
3. 如依赖变更，重新安装依赖。
4. 如使用数据库，执行迁移。
5. 启动服务。
6. 验证登录、对话、会话、模型配置、Provider 实例和渠道连接。

## Provider 兼容性 {#provider-compatibility}

Provider 包单独升级。升级后重新检查 Provider schema、技能元数据和认证模式。
