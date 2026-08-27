---
title: Provider 加载
description: 通过 providers_root 加载 Provider 包。
sidebar_position: 2
---

# Provider 加载

AtlasClaw Core 从 `providers_root` 加载 Provider。

## 包结构 {#package-layout}

Provider 包通常包含：

```text
providers/<provider-name>/
├── PROVIDER.md
├── provider.schema.json
├── README.md
├── pyproject.toml              # Provider 提供可导入 Python 包时使用
├── assets/
├── src/<provider_package>/     # 可复用 API、领域、模型和服务代码
├── assistant_context/          # 可选页面 Context 清单与 callable
└── skills/                     # AtlasClaw Adapter
    └── <skill>/
        ├── SKILL.md
        ├── scripts/
        └── references/
```

`src/` 和 `assistant_context/` 是可选目录。存在可复用领域执行逻辑时，应将实现放入可导入 Provider 包，并保持 Skill handler 为薄层：转换 AtlasClaw `RunContext` 和 Tool 输入、调用 typed Provider operation，再转换结果。协议 Adapter 不应重复实现 Provider 认证、API 路径或业务规则。

## 发现过程 {#discovery}

启动时 Core 扫描 `providers_root`，加载 Provider 定义，注册 Provider 实例，并加载 Provider 技能。技能会带上 Provider 命名空间避免冲突。

Provider 发现依赖可读取的 metadata。Provider 包应包含 `PROVIDER.md` 作为 LLM 上下文，并包含 `provider.schema.json` 作为 UI/API 配置字段定义。

## Callable 运行时 {#callable-runtime}

可执行 Skill metadata 支持两种 entrypoint：

| Entrypoint | 运行方式 |
| --- | --- |
| `scripts/adapter.py:operation` | Core 在进程内加载指定 callable，并通过 AtlasClaw `RunContext` 调用。 |
| `scripts/legacy_command.py` | 兼容路径；以子进程启动文件，通过环境变量传入限定范围的运行时数据。 |

新的 Python Provider Tool 应使用显式 `file.py:callable` entrypoint。同一个 Skill 的多个 Tool 可以指向同一 Adapter 模块中的不同 callable。页面 Context Resolver 也必须使用 `assistant_context/resolve.py:resolve_context` 这样的显式 async callable，不支持旧子进程形式。

## Callable 结果契约 {#callable-result-contract}

Callable 返回作为 Agent 证据的公开 Tool 结果，也可以包含有界 `_internal` 值，保存与请求 trace 绑定的续跑 metadata。Core 接受结构化或 JSON 序列化的 `_internal`，对用户隐藏该值，并且只在同一请求 trace 和所选 Provider 实例中恢复。

Provider Adapter 应保持该 metadata 精简，只保留下一步必需的精确 ID、Provider identity、验证 token 或其他事实。不要把整页公开列表复制进 `_internal`；过大的 metadata 会从工作流上下文中省略，并产生结构化预算诊断。只读唯一候选续跑所用的 Markdown Tool 标记见[技能和工具](/core/skills-and-tools)。

## 配置 {#configuration}

在 `atlasclaw.json` 中设置：

```json
{
  "providers_root": "../atlasclaw-providers/providers"
}
```

## 加载 Checklist {#loading-checklist}

1. `providers_root` 指向包含 Provider 目录的根路径。
2. Provider 目录包含 `PROVIDER.md`。
3. `provider.schema.json` 是合法 JSON。
4. Skill 目录包含 `SKILL.md`，以及 entrypoint 指向的所有 callable 模块或旧脚本。
5. AtlasClaw Core 对 Provider 根目录有文件读取权限。
6. 添加或修改 Provider 包后已重启服务。

## 常见失败 {#failure-modes}

| 现象 | 可能原因 |
| --- | --- |
| Provider catalog 为空 | `providers_root` 错误或不可读。 |
| Provider 出现但没有 Skill | `skills/` 结构或 `SKILL.md` 缺失。 |
| 配置表单缺字段 | `provider.schema.json` 缺失或无效。 |
