---
title: 会话
description: 会话 key、用户隔离、转录和历史。
sidebar_position: 3
---

# 会话

会话保存某个用户、渠道和线程的对话状态。

## 会话范围 {#session-scope}

AtlasClaw 使用结构化 session key 标识 Agent、渠道、聊天类型、用户和线程，从而隔离 Web、API、Webhook 和 IM 对话。

会话存储以用户为中心。会话元数据位于该用户的 workspace session 目录中，归档或迁移数据也保持在该用户范围内。

## 用户隔离 {#user-isolation}

会话元数据和转录按认证用户隔离。直接会话操作必须拒绝访问其他用户的会话。

## 会话操作 {#session-operations}

Core 提供列出会话、创建会话、创建线程、获取历史、重置、删除、查看状态、排队消息和压缩长历史等 API。

## 压缩 {#compaction}

压缩用于减少长对话历史，同时保留近期用户意图和后续回合所需上下文。

压缩不是 Provider 上游记录的替代品。Provider 创建的工单、申请、审批或资源操作仍以上游系统为准。

## 排队和并发 {#queueing-and-concurrency}

AtlasClaw 可以对同一会话排队，避免并发 Agent 回合互相冲突。IM 渠道中用户连续发送多条消息时，这一点尤其重要。长时间排队通常意味着模型响应慢、Provider API 延迟或工具调用卡住。
