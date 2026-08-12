---
title: 资源分析与操作
description: 浏览、综合分析和操作 SmartCMP 资源。
sidebar_position: 9
---

# 资源分析与操作

SmartCMP resource 技能支持资源浏览、单资源综合分析和部分 day-2 操作。

## 浏览 {#browsing}

用户可以列出资源、筛选云主机、按 ID 查看资源，并使用薄 AtlasClaw Skill Adapter 调用 typed Provider operation 后返回的标准化资源视图。

典型发现操作包括：列出全部资源、列出全部云主机、按关键字过滤、按资源 ID 刷新并分析单台主机、获取资源详情用于安全分析或排障。

## 资源综合分析 {#comprehensive-resource-analysis}

解析成功的云资源或虚拟机页面可以展示动态的“综合分析”操作。该操作使用 `resource` Skill 作为协调者，为四个现有只读分析器保留同一个精确的 SmartCMP 内部资源目标：

1. 当前告警，以及触发时间位于配置回溯窗口内且当前状态为已解决的告警；
2. 根据资源组件 Prometheus 监控模型分析运行健康；
3. 根据受限、脱敏的资源 Profile 分析资源优先的安全状态，并将关联的 CMP 已确认安全违规与 LLM 推断分开呈现；
4. 分析平台已确认和 LLM 推断的费用优化机会。

最终回答分别呈现各维度的证据和缺口，再说明跨维度关联。一个维度失败或证据不足不会阻止其他维度完成。综合分析不会修改资源。

安全违规覆盖状态必须明确呈现。即使清单覆盖不完整，也必须报告所有精确匹配。只有完整覆盖且没有匹配时，才能得出“没有关联违规”的结论；部分覆盖或失败覆盖都不能证明违规不存在。

该操作根据当前资源对象动态生成。用户进入另一个受支持的 SmartCMP 页面时，悬浮助手会解析新的 Context；之后携带旧 Context 提交的 Chat turn 会被拒绝，已经通过提交校验的 turn 则继续使用普通 Chat 运行时。

## 操作 {#operations}

资源操作技能支持 start、stop、卸除、删除资源元数据和永久卸除等明确动作。用户可以使用 `resource_id`、`resource_name`、`deployment_id` 或 `deployment_name` 定位目标。名称必须在当前用户可见范围内精确且唯一；找不到或匹配多个对象时，操作必须在写入前停止。

操作是否成功取决于用户在 SmartCMP 中的权限和目标资源当前状态。

成功操作的输出应保持简洁，只包含动作、目标资源 ID、submitted 标记、面向用户的消息和验证提示。不要打印原始 SmartCMP 请求 payload 或原始响应详情。如果 SmartCMP 在 HTTP 200 响应中返回业务失败，工具应输出简短错误，而不是报告提交成功。

### 卸除生命周期 {#removal-lifecycle}

SmartCMP 资源卸除是分阶段的生命周期，三个操作不能互相替代：

| 阶段 | SmartCMP 操作 | 结果 |
| --- | --- | --- |
| 卸除 | `tear_down_in_resource` | 将 active 资源推进到 stopped 或已卸除状态，但不会永久删除 CMP 记录。 |
| 删除资源元数据 | `delete_metadata_in_resource` | 删除 node 资源元数据；node 变为 `status=deleted`，其 deployment 进入 CMP 回收站。 |
| 永久卸除 | `permanently_delete_deployment` | 永久卸除回收站中的 deployment。该操作按 deployment 生效，可能影响其中的全部资源。 |

完整演进为 **active → stopped/已卸除 → node 元数据已删除且 deployment 进入回收站 → deployment 永久卸除**。Node 达到 `status=deleted` 只说明第二阶段已经完成，不能证明永久卸除成功。

用户以资源定位时，Agent 必须先解析并保留该资源所属的回收站 deployment，再执行永久卸除；用户以 deployment 定位时，同样需要精确且唯一的匹配。不得选择第一个名称模糊匹配结果，也不得假设一个 deployment 只包含一个资源。

自动精确定位目前最多扫描 2,000 个回收站 deployment，超过该范围会安全拒绝。无定位字段浏览时，`total`、`page`、`size` 描述 deployment 分页，`items` 是展开后的资源行，因此同一 deployment 可以产生多行。

## 操作安全 {#operation-safety}

所有状态变更操作都需要显式确认。执行前必须展示精确目标、可用时的当前状态和目标动作。永久卸除前还必须展示解析得到的 deployment，提示该操作会影响同一 deployment 中的全部资源且不可恢复，然后停止；只有用户明确确认该影响范围后才可提交。

写请求必须携带刚确认的 deployment ID 和完整资源 ID 集合。Provider 会在提交前重新解析并比较范围；如果 deployment 或资源集合发生变化，必须在写入前停止，重新展示范围并取得确认。

永久卸除是异步操作。提交后必须按 deployment 验证完成状态：回收站 deployment 达到 `deleted=true`、`state=DELETED`，并且其回收态可执行操作列表为空。受 SmartCMP 保留期配置影响，已删除 deployment 仍可能暂时显示在回收站中；保留期后消失也属于有效完成结果。不得仅以 node 的 `status=deleted` 判断永久卸除成功。

## 常见阻塞 {#common-blockers}

| 阻塞 | 含义 |
| --- | --- |
| Resource not found | ID 错误或当前凭证不可见。 |
| Ambiguous name | 当前可见范围内有多个同名资源或 deployment；需要使用精确唯一名称或 ID。 |
| Unsupported action | 资源类型不支持该 day-2 动作。 |
| Permission denied | SmartCMP 接受凭证但拒绝操作。 |
| Current state mismatch | 资源已停止、运行中或处于过渡状态。 |
| Recycled action unavailable | Deployment 不在回收站、仍在处理其他操作、已永久删除，或当前用户没有权限。 |
