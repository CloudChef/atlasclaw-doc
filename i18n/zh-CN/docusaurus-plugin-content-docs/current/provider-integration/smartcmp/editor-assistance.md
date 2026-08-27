---
title: 编辑辅助
description: 为受支持的 SmartCMP 编辑器生成完整替换内容，不写入上游状态。
sidebar_position: 7
---

# 编辑辅助

SmartCMP Provider 为部分编辑器页面提供上下文绑定的只读 Skill。每个 Skill 都使用当前用户的 SmartCMP 凭证读取精确的已保存对象，根据用户要求调整内容，并返回完整替换稿供人工审查和复制。

这些 Skill 不会在 SmartCMP 中保存、发布、执行、启用或部署任何内容。

## 支持的编辑器 {#supported-editors}

| SmartCMP 页面 | 所属 Skill | 生成的替换内容 |
| --- | --- | --- |
| `/main/service-model/forms/edit/{form_id}` | `smartcmp:form-designer` | 完整、规范化的表单 schema。 |
| `/main/service-model/forms/design/{form_id}` | `smartcmp:form-designer` | 完整、规范化的表单 schema。 |
| `/main/model-design/scripts/edit/{script_id}` | `smartcmp:script-designer` | 脚本 `content` 字段的完整替换内容。 |
| `/main/measurement-billing/cost-optimization/optimization-policy/edit/{policy_id}` | `smartcmp:optimization-policy-designer` | 完整 `ruleContent` 和本次需要变更的字段。 |
| `/main/model-design/blueprint-components/edit/{component_id}` | `smartcmp:component-script-designer` | `scripts/` 下一个精确文件的完整内容。 |

Form Designer 也可以在普通对话中使用精确的 SmartCMP 表单编辑 URL。其他 Skill 依赖已解析的编辑器页面 Context 安全绑定目标。

## 工作流 {#workflow}

1. 在 SmartCMP 悬浮助手界面打开受支持的编辑器页面，或提供受支持的精确表单 URL。
2. AtlasClaw 解析已保存对象并绑定所属 Skill。
3. 描述希望完成的修改。
4. Skill 返回完整替换内容，不返回带省略号的缩写或不完整 patch。
5. 审查结果、复制内容，并在 SmartCMP 中人工应用。

回答可以包含辅助说明，但替换代码块本身会保留复制所需的完整内容。

## 编辑器专属边界 {#editor-specific-boundaries}

- 表单辅助返回完整、规范化的 schema，绝不写入表单定义。
- 脚本辅助只替换 `content`；其他脚本 metadata 只作为兼容性上下文，不会被隐式改写。
- 优化策略辅助只适用于成本优化策略，不会启用策略或执行整改。
- 蓝图组件辅助只处理 `scripts/` 下一个精确文件。可能存在多个文件时，用户必须提供精确路径；该能力不会更新或部署组件。

生成内容仍需人工审查、通过 SmartCMP 校验，并由用户使用正常的 SmartCMP 保存或发布权限应用。
