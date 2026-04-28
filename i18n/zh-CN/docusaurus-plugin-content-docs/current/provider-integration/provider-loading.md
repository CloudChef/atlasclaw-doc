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
├── assets/
└── skills/
    └── <skill>/
        ├── SKILL.md
        ├── scripts/
        └── references/
```

## 发现过程 {#discovery}

启动时 Core 扫描 `providers_root`，加载 Provider 定义，注册 Provider 实例，并加载 Provider 技能。技能会带上 Provider 命名空间避免冲突。

Provider 发现依赖可读取的 metadata。Provider 包应包含 `PROVIDER.md` 作为 LLM 上下文，并包含 `provider.schema.json` 作为 UI/API 配置字段定义。

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
4. Skill 目录包含 `SKILL.md` 和所需脚本。
5. AtlasClaw Core 对 Provider 根目录有文件读取权限。
6. 添加或修改 Provider 包后已重启服务。

## 常见失败 {#failure-modes}

| 现象 | 可能原因 |
| --- | --- |
| Provider catalog 为空 | `providers_root` 错误或不可读。 |
| Provider 出现但没有 Skill | `skills/` 结构或 `SKILL.md` 缺失。 |
| 配置表单缺字段 | `provider.schema.json` 缺失或无效。 |
