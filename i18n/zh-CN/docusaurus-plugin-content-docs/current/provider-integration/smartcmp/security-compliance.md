---
title: Security 合规
description: 查看 SmartCMP Security 状态，并使用经过确认的两阶段违规状态工作流。
sidebar_position: 12
---

# Security 合规

SmartCMP 将资源优先的安全分析与 CMP 策略违规工作流分开。`security-compliance`
Skill 负责 CMP 全局 Security 总览、安全违规集合和单个违规对象的操作；
`resource` Skill 负责关于指定、已选择、已列出或当前资源的问题，包括该资源的
安全状态和关联违规。

## 路由边界 {#routing-boundary}

| 用户意图或上下文 | 所属 Skill |
| --- | --- |
| CMP 全局 Security 状态、策略、执行、趋势或违规列表 | `security-compliance` |
| 违规 ID、已选择的违规行或“第 N 条违规” | `security-compliance` |
| 资源名称或 ID、已选择的资源行或当前 Resource 页面 | `resource` |

列表序号只是显示引用，不是违规 ID。Provider 会把真实违规 ID 保存在隐藏对象
元数据中，并在启动“分析”操作时使用这个精确 ID。

## 违规工作流 {#violation-workflow}

1. 使用 `smartcmp_get_security_overview` 查看 CMP 全局 Security 策略、执行、
   合规、严重等级、违规和趋势状态。
2. 使用 `smartcmp_list_security_violations` 浏览安全违规。每次调用只读取一个有界页面，每页最多 50 行；使用 `page` 继续。列表行只展示**分析**。
3. **分析**调用 `smartcmp_analyze_security_violation`，重新读取精确违规及其
   最新状态、资源和策略；展示 CMP 已确认事实、证据缺口、人工整改建议和验证
   步骤后停止。
4. 只有最新状态仍为 `ACTIVED` 的新鲜分析结果才能展示**标记已修复**。UI 会
   要求单独明确确认。确认后，`smartcmp_mark_security_violation_fixed` 会在更新
   前重新读取精确违规，并在更新后验证状态。

“分析”和“标记已修复”绝不能在同一轮执行。

当前页为空不能证明完整违规清单为空。作出不存在违规的结论前，必须检查返回的分页和覆盖 metadata。

## 影响与安全边界 {#effect-and-safety}

“标记已修复”只修改 CMP 违规状态，不会修改、修复、重启、打补丁、升级或重新
配置底层资源；仅有 `FIXED` 状态也不能证明资源已经整改。任何资源变更都必须通过
独立审批的资源操作或变更管理工作流完成。完成后，应先验证资源并取得最新 Security
策略结果，再将违规标记为 FIXED。

该工作流不提供自动整改，也不执行 Security Day-2 操作。

## 资源优先的安全分析 {#resource-first-security-analysis}

对于指定或已选择的资源，使用 `resource` Skill。它会把受限、脱敏的资源 Profile
与关联的 CMP 已确认 Security 违规结合分析。LLM 推断的资源安全状态必须与 CMP
已确认违规明显分开，不能创建、清除或替换 CMP 结论。

关联违规清单有三种覆盖状态：

- `complete`：报告所有匹配；只有结果为空时才能说明“没有关联的 CMP Security
  违规”；
- `partial`：将所有匹配作为已确认违规报告，同时说明清单不完整；结果为空时只能
  说明“在已扫描页面中未找到匹配”；
- `failed`：报告采集失败，不得对违规是否存在作出否定结论。
