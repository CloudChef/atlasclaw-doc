---
title: 安装
description: 安装并加载 SmartCMP Provider。
sidebar_position: 2
---

# 安装

## 添加 Provider 包 {#add-provider-package}

把 `SmartCMP-Provider` 放在配置的 Provider 根目录下：

```text
atlasclaw-providers/providers/SmartCMP-Provider/
```

配置 Core：

```json
{
  "providers_root": "../atlasclaw-providers/providers"
}
```

修改 Provider 包后重启 AtlasClaw Core。

## 验证加载 {#verify-loading}

启动后确认 SmartCMP 出现在可用 Provider 定义中，并确认拥有 Provider 访问权的角色能看到 SmartCMP 技能。

## 期望包文件 {#expected-package-files}

| 文件或目录 | 作用 |
| --- | --- |
| `PROVIDER.md` | Provider 身份、能力上下文和 LLM 指导。 |
| `provider.schema.json` | Provider 实例和用户凭证字段 schema。 |
| `README.md` | Provider 安装和 Skill 运行说明。 |
| `pyproject.toml` | 可安装 `smartcmp-provider` distribution metadata。 |
| `src/smartcmp_provider/` | 共享认证、模型、transport、领域 operation 和 service。 |
| `assistant_context/` | 可选内嵌页面路由清单和显式 Context Resolver callable。 |
| `skills/` | 薄 AtlasClaw Skill Adapter 和 SmartCMP 特有的 Object Action 展示 helper。 |
| `assets/` | Provider 图标和 catalog 资源。 |

## 安装后检查 {#post-install-checks}

重启 Core，确认 `smartcmp` 出现在 Provider 定义中，配置表单显示 `base_url` 和认证模式相关字段，然后创建实例、授权测试角色，并先测试只读查询。
