---
title: 内嵌菜单与悬浮 UI
description: 部署两支共享企业系统 Cookie 认证的独立 AtlasClaw UI。
sidebar_position: 5
---

# 内嵌菜单与悬浮 UI

AtlasClaw Embedded 模式提供两支可以同时部署的独立 UI：完整菜单 UI 和紧凑悬浮 UI。它们是两个不同入口，不是同一组件的展开和收起状态。

两支 UI 接收相同的企业系统 Cookie 认证上下文。AtlasClaw `host_cookie` 认证会解析出同一个已登录用户，HostApp Provider 的 Cookie 认证模式则使用当前请求 Cookie，以该用户的上游权限访问现有系统。

## 界面形态 {#surfaces}

| 界面 | UI 与生命周期 | 页面 Context |
| --- | --- | --- |
| Menu | 使用 `surface=menu` 从企业系统菜单打开的独立完整 AtlasClaw 会话。 | 不接收 `PAGE_CHANGED`，也不附加页面 Context。 |
| Floating | 使用 `surface=floating` 覆盖在企业系统上的独立紧凑助手。 | 每个更新的页面 generation 都会重新解析 Context。 |

两支 UI 都使用正常的 AtlasClaw Chat、Session、Skill、Tool、Provider 和 RBAC 运行时。它们可以同时存在，并共享通过 AtlasClaw Origin bootstrap 状态选定的当前 Chat Session，但各自保留独立布局和 Context 行为。内嵌页面不会接收或转发 AtlasClaw `session_key`。

## AtlasClaw 理解当前页面与可用操作 {#architecture}

通过 `embed_integration` 配置的 HostApp Provider，将企业系统页面映射为业务对象、Domain Skills 与状态相关操作。它是运行在 AtlasClaw 中的 Provider 包，不是要求企业系统在自身架构中新增的一项服务。

![AtlasClaw 菜单、悬浮 UI、运行时、Provider 与企业系统现有服务的内嵌架构](/img/embedded/hostapp-provider-architecture-zh.svg)

两支 UI 进入同一个 AtlasClaw Agent 运行时，但提供的信息不同。菜单访问打开不带页面 Context 的完整 Agent；悬浮 UI 额外发送当前 `path` 和 `generation`。AtlasClaw 随后使用配置的 HostApp Provider 匹配页面、通过现有 API 解析对象，并加载所属 Domain Skill 根据对象状态生成的操作。

HostApp Provider 返回的通用 `object_actions` 合同也会被普通 Chat Tool 结果复用。Core 负责该合同的 schema、规范化、安全 builder、提取以及向 UI 传递；Provider 只提供业务操作是否可用、标签、Prompt、输入项和 URL。Provider 不为悬浮 UI 维护第二套操作目录，因此页面助手与普通 Agent 对话会随 Domain Skills 的演进保持一致。

## 企业系统能力要求 {#host-app-capabilities}

菜单模式的集成有意保持最小化。企业系统只需要在菜单中增加入口并嵌套 AtlasClaw Agent：

```text
/atlasclaw/?embedded=1&surface=menu
```

动态悬浮 Context 需要额外的内嵌集成，因为 AtlasClaw 必须知道用户当前看到的企业系统页面何时发生变化：

```text
/atlasclaw/?embedded=1&surface=floating&host_origin=<exact-origin>&nonce=<random-nonce>
```

两支 UI 对企业系统的要求如下：

| 企业系统能力 | 菜单 UI | 悬浮 UI |
| --- | --- | --- |
| 嵌套 AtlasClaw 界面 | 必需 | 必需 |
| 让 AtlasClaw 请求可以携带企业系统 Cookie | 必需 | 必需 |
| 提供悬浮入口并管理紧凑 iframe 生命周期 | 不需要 | 必需 |
| 使用精确 Host Origin 和全新高熵 nonce 构造悬浮 URL | 不需要 | 必需 |
| 校验精确的消息 Origin、来源窗口、nonce、协议、事件类型和 payload | 不需要 | 必需 |
| 通过 `PAGE_CHANGED` 上报标准化路由路径和单调递增 generation | 不需要 | 必需 |
| 处理 ready、close 等悬浮生命周期事件 | 不需要 | 必需 |
| 解析页面对象、选择 Provider/Skill 或渲染确认 UI | 禁止 | 禁止 |

关闭悬浮助手功能开关时，企业系统应移除悬浮入口和 iframe。完整菜单 Agent 打开时，企业系统也可以隐藏悬浮入口，避免同时展示同一个助手的两个入口控件。

`PAGE_CHANGED` 只发送共享协议字段、nonce、generation 和标准化绝对路径。不要包含 query、fragment、页面内容、选中文本、业务 DTO、Provider 标识或 AtlasClaw Session 标识。企业系统代码不应代替 iframe 调用 Embed REST、Agent Run 或 Tool API。

AtlasClaw 负责 bootstrap、Context Snapshot、Chat 提交、通用 Object Action 合同与 builder、操作展示、确认、Tool 执行和权限校验。HostApp Provider 负责页面路径语义、对象读取、Domain Skills，以及决定操作当前是否可用的业务规则和文案。这样即使 Provider 路由和工作流持续增加，内嵌集成仍然保持通用。

## 菜单 UI 流程 {#menu-flow}

1. 企业系统使用 `embedded=1&surface=menu` 打开 AtlasClaw。
2. Embed bootstrap 校验菜单 UI，以及来自 AtlasClaw Origin 的候选当前 Chat Session。
3. AtlasClaw 渲染完整的内嵌会话 UI。
4. 菜单 UI 使用普通 Chat 能力选择，不在 turn 中附加企业系统页面对象。

## 悬浮 Context 流程 {#floating-context-flow}

1. 企业系统发送 `PAGE_CHANGED`，其中包含单调递增的 generation 和标准化绝对路径。
2. AtlasClaw 选择 `embed_integration` 配置的唯一 HostApp Provider；内嵌消息不能覆盖该绑定。
3. Core 使用该 Provider 的 `assistant_context/routes.json` 匹配路径。
4. Provider Resolver 使用请求级用户凭证读取当前对象，并返回受限的对象投影和当前 `object_actions`。
5. Core 将 Snapshot 绑定到用户、悬浮界面、generation、Provider 实例、匹配到的现有 Skill 和有限生命周期。
6. 悬浮 UI 展示对象和操作。Prompt 操作携带不可变 Context 引用进入普通 Chat 路径。
7. 提交该 Chat turn 时，Core 会校验 Context 所有者、generation、最新页面标记、有效期和 Session scope，然后把对象和默认 Skill 复制到本次 turn。
8. Core 会另外根据当前授权生成普通 Chat Tool 集合。该 turn 不会被限制为页面 Skill 的 Tool，也不会在同一 turn 的每次 Provider Tool I/O 前再次校验页面。

企业系统报告新页面后，较早的异步响应无法恢复已经过期的对象信息或操作。

悬浮页面匹配在运行时动态发生，但过程是确定性的。AtlasClaw 不会把页面内容交给 LLM 猜测当前工作流，而是使用已配置 HostApp Provider 的路由清单匹配路径，再由该 Provider 解析对象。

## 解析状态 {#resolution-status}

| 状态 | 含义 | UI 和执行行为 |
| --- | --- | --- |
| `resolved` | 路由、对象和所属 Skill 均解析成功。 | 展示当前对象和动态操作。 |
| `unsupported` | 当前路径没有匹配任何 Provider 路由。 | 保留普通 Chat，不附加页面 Context。 |
| `unavailable` | 路由已匹配，但对象或 Skill 绑定无法安全解析。 | 保持页面作用域关闭，不降级到无关能力。 |

权限失败会单独返回。解析对象不会授予用户原本没有的 Skill、Tool 或上游权限。

## 配置 {#configuration}

启用一个 HostApp Provider 和实例：

```json
{
  "embed_integration": {
    "provider_type": "example_provider",
    "provider_instance": "default"
  }
}
```

AtlasClaw 会根据该 HostApp Provider 推导两支 UI 共享的 Chat Session scope，并为悬浮页面匹配加载 `assistant_context/routes.json`。企业系统代码不能选择其他 Provider 或实例。不配置 `embed_integration` 时，继续使用不带已配置 menu/floating 集成的旧内嵌行为。

认证需要单独配置。企业系统已经完成用户认证时，应将该功能和 AtlasClaw `host_cookie` 认证、Provider 请求 Cookie 认证模式配合使用，详见[内嵌模式](./embedded-mode.md)。

## HostApp Provider 路由契约 {#provider-route-contract}

支持页面 Context 的 HostApp Provider 可以使用以下可选结构：

```text
providers/example-provider/
├── assistant_context/
│   ├── routes.json
│   └── resolve.py
└── skills/
    └── item/
        └── SKILL.md
```

路由清单示例：

```json
{
  "schema_version": 1,
  "provider_type": "example_provider",
  "context_resolver": {
    "entrypoint": "assistant_context/resolve.py:resolve_context"
  },
  "routes": [
    {
      "id": "item-detail",
      "priority": 300,
      "match": {
        "path_template": "/main/items/{item_id}"
      },
      "result": {
        "page_type": "item-detail",
        "object_type": "item",
        "skill_ref": "example_provider:item"
      }
    }
  ]
}
```

模板支持静态路径段和单路径段占位符。匹配顺序依次考虑显式 priority、模板具体程度和清单顺序。Query、fragment、Origin、页面标题、选中文本和业务 DTO 都不是匹配输入。

Entrypoint 必须使用 `file.py:callable` 形式显式指定 async callable。Core 在初始化 Embed Integration 时在进程内加载并校验它；Context 解析不会启动 Resolver 子进程。

HostApp Provider 级 Resolver 返回：

- 类型与路由声明一致、ID 非空的最小对象；
- 经过批准的展示字段和大小受限的 attributes；
- 使用 Core 通用 action builder、根据当前对象状态生成的 `object_actions`。

匹配的 `skill_ref` 由路由声明，Resolver 输出不能替换它。对象操作可以打开安全的企业系统 URL，或提交 Provider 编写的 Prompt，但不能声明一次精确 Tool 调用。Core 定义并校验通用 action 结构；Provider 决定每项业务操作是否可用，并提供相应文案与参数。

## SmartCMP 参考实现 {#smartcmp-reference}

SmartCMP 作为内嵌 AtlasClaw 的现有企业系统，展示了完整的 HostApp Provider 模式。SmartCMP 保留现有 API、Cookie 会话、RBAC、业务流程与审计；SmartCMP Provider 随 AtlasClaw 安装，提供页面到对象的匹配、统一对象 Resolver、Domain Skills，并通过 Core 通用 action builder 提供 SmartCMP 特有的操作可用性和文案。

| SmartCMP 页面 | 解析对象与 Skill | 状态相关操作 |
| --- | --- | --- |
| `/main/virtual-machines/{resource_id}/details` | `virtual_machine` → `smartcmp:resource` | 打开、综合分析、操作 |
| `/main/alarm-activity-management/alarm-triggered/edit/{alert_id}` | `alarm_alert` → `smartcmp:alarm` | 分析，并根据告警状态提供静音、解决或重新打开 |
| `/main/new-application/pendingApproval/{approval_type}/{approval_id}` | `approval_request` → `smartcmp:approval` | 分析、同意、拒绝，并保留确认和必填输入 |

![SmartCMP VM 页面中的悬浮 Context 与资源操作](/img/embedded/context-vm-floating.png)

在 VM 页面中，SmartCMP 只发送规范化路由。SmartCMP Provider 通过现有 API 解析当前资源，并复用 resource Domain Skill 的操作构建器提供打开、综合分析和操作入口。

![SmartCMP 告警页面中的分析与告警操作](/img/embedded/context-alert-analysis.png)

在告警页面中，同一模式会解析当前告警，并提供与其状态一致的操作。变更类操作仍然进入普通 Agent run，经过确认、Provider 权限检查和 SmartCMP 下游授权。

## 动态扩展规则 {#dynamic-extension-rules}

- 新路径对应 HostApp Provider 已支持的对象类型和所属 Skill 时，只增加一个路由条目。
- 新对象类型需要其他现有企业系统 API 时，扩展 HostApp Provider 读取适配器。
- 在所属 Domain Skill 中增加状态相关操作，优先复用普通 Chat Tool 结果使用的操作构建器。
- 不要把 Provider 页面路径、字段映射、操作文案或业务规则加入 AtlasClaw Core 或通用悬浮 UI。

按照该边界，Provider 可以增加页面和工作流，而无需修改共享内嵌协议或 Core UI。

## 安全与部署边界 {#security-and-deployment-boundaries}

- 校验精确的消息 Origin、来源窗口、协议、nonce、事件类型和 payload schema。
- 禁止使用 `targetOrigin="*"`。
- 每个悬浮 iframe 实例生成新的高熵 nonce，并且只接受来自该 iframe `contentWindow` 的消息。
- 不要把 Cookie、Token、凭证、query、fragment 或原始业务 payload 放入内嵌消息、路由清单、浏览器存储或 Context Snapshot。
- 对象可见性由 Provider 使用当前用户的上游凭证进行校验。
- Context Snapshot 只保存在进程内，重启后失效。部署必须使用单个 AtlasClaw 进程，或保证 bootstrap、Context 解析和页面范围 Agent turn 落在同一进程的粘性路由。
