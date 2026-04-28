---
title: 用户 Token 设置
description: 配置个人 SmartCMP Token。
sidebar_position: 5
---

# 用户 Token 设置

如果 SmartCMP 实例使用 `user_token` 认证，每个用户都需要在 AtlasClaw 中配置个人 Token。

## 步骤 {#steps}

1. 从 SmartCMP 获取 API Token。
2. 打开 AtlasClaw Account Settings。
3. 找到 Provider Tokens。
4. 选择 SmartCMP Provider 实例。
5. 填入 Token。
6. 保存后重试 SmartCMP 请求。

## Token 错误 {#token-errors}

如果 Agent 提示 `user_token` 缺失、无效、被拒绝或过期，请更新 Account Settings 中的 SmartCMP Token。如果提示联系管理员，可能是 Provider 实例不可用或角色没有访问权。

## Token 控制什么 {#what-the-token-controls}

该 Token 只用于你保存它的 SmartCMP Provider 实例。它不会配置 IM Channel，也不会授予 AtlasClaw 管理员权限。SmartCMP 仍决定你的 Token 能访问哪些申请、审批、资源或告警。

## 轮换 Checklist {#rotation-checklist}

生成或获取新 SmartCMP Token，在 AtlasClaw Provider Tokens 中替换，先测试只读 SmartCMP 操作，再重试原工作流。组织要求时，在 SmartCMP 中撤销旧 Token。
