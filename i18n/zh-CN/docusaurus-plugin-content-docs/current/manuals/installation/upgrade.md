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

## 升级到 v1.0.1

最终的 `v1.0.1` 标签指向 `1838dec1f60edf5d5a9ca96f0262a6071730d57d`，已包含 Docker 发布修复。

```bash
docker pull registry.cn-shanghai.aliyuncs.com/atlasclaw/atlasclaw:v1.0.1
```

- 执行访问令牌迁移 `011` 和聊天附件迁移 `012`。
- 更新依赖，并按 Python 3.14.10 配置重新构建原生包或容器镜像。
- 将回复语言模式值替换为具体语言区域值、`null`，或省略字段；部署时包含共享的回复语言 JSON 提示词资源。
- 使用图片分析前，在兼容模型上明确启用 `capabilities.vision`。
- 五个迁移中的时间戳默认值现使用 `CURRENT_TIMESTAMP`。已完成的迁移不会自动重新执行；失败迁移遗留的表需要在重试前检查，不会自动删除。

升级后，根据启用的功能验证登录、纯文本聊天、图片上传与追问、令牌创建与撤销，以及嵌入式 Context 导航。发布构建已通过 Docker 推送和拉取验证，但这不代表已完成真实 MySQL 8.0.16 环境的升级验证。

参阅 [v1.0.1 完整发布说明](https://github.com/CloudChef/atlasclaw/releases/tag/v1.0.1)。
