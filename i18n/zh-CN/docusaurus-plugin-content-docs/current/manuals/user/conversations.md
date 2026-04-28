---
title: 对话
description: 与 AtlasClaw 对话并使用会话。
sidebar_position: 2
---

# 对话

聊天页是 Standard User 使用 AtlasClaw 的主要工作区。

## 开始对话 {#start-a-conversation}

打开 AtlasClaw Web UI，在输入框发送消息。Agent 会基于当前认证用户、已启用技能、Provider 访问权限和可用模型配置生成回复。

## 会话 {#sessions}

AtlasClaw 按认证用户隔离会话。用户可以切换自己的会话并继续之前的工作。

会话会按用户、渠道和线程隔离。Web Chat 和 IM Thread 即使来自同一用户，也可以保留不同历史。

## 请求 Provider 工作 {#asking-for-provider-work}

当你希望 Agent 使用运维系统时，请尽量说明：要做什么、目标环境或项目、请求是只读还是会产生变更、审批理由或业务背景。写操作会在上游系统产生效果，应在确认摘要后再继续。

## 权限提示 {#permission-messages}

如果请求需要未启用技能、不可用 Provider 实例或缺失凭证，Agent 应说明阻塞原因，并提示用户配置自己的 Token 或联系管理员。

## 良好对话模式 {#good-conversation-patterns}

| 表达 | 作用 |
| --- | --- |
| “先列出可选项。” | 让 Agent 先使用只读发现能力。 |
| “使用生产实例。” | 多个 Provider 实例存在时减少歧义。 |
| “先生成草稿，不要提交。” | 保留人工 review 空间。 |
| “解释为什么被阻塞。” | 暴露缺失权限或凭证。 |

不要把密钥粘贴到对话中。凭证应通过 Provider Tokens 或 Channel 配置表单保存。
