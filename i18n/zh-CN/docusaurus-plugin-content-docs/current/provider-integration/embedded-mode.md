---
title: 内嵌模式
description: 将 AtlasClaw Agent 嵌入企业系统，并复用系统请求 Cookie 实现无缝 Provider 访问。
sidebar_position: 4
---

# 内嵌模式

内嵌模式把 AtlasClaw Agent 带入一个已经完成用户认证的现有企业系统，让系统获得页面感知分析和受控执行能力，同时无需重构现有 UI、API、身份、权限、业务流程或审计模型。

Embedded 模式支持两支独立 UI：完整菜单 UI 和紧凑悬浮 UI。两者使用相同的企业系统 Cookie 认证上下文，因此会解析为同一个已登录用户，并沿用该用户对现有系统的访问权限。只有悬浮 UI 附加动态页面 Context。详见[内嵌菜单与悬浮 UI](./embedded-menu-and-floating-ui.md)。

## AtlasClaw 理解并操作企业系统 {#hostapp-provider}

正式集成组件是 **HostApp Provider**：它是运行在 AtlasClaw 中、用于把企业系统页面映射为业务对象、Domain Skills 和状态相关对象操作的 Provider 包。`embed_integration` 会把内嵌运行时固定绑定到唯一 Provider 类型和实例。

HostApp Provider 随 AtlasClaw 安装和配置，不是要求企业系统新部署的一项服务。它使用当前用户的请求 Cookie 调用现有系统 API，使 AtlasClaw 能够理解当前 Context 并执行操作，同时继续沿用现有 RBAC、业务流程与审计。

![AtlasClaw 内嵌到现有企业系统的架构](/img/embedded/hostapp-provider-architecture-zh.svg)

这一边界使集成保持轻量：

- 企业系统增加独立菜单入口、悬浮 UI，或同时提供两者；
- 悬浮消息桥只发送规范化 `path` 和 `generation`；
- AtlasClaw 负责 Chat、Context Snapshot、Agent 编排、确认与执行安全；
- HostApp Provider 负责解释页面、解析对象、提供 Domain Skills，并生成统一的 `object_actions`；
- 企业系统继续负责现有数据、API、权限、业务流程与审计。

## 认证分层 {#authentication-layers}

内嵌模式包含两层相关但独立的认证：

| 层次 | AtlasClaw 配置 | 作用 |
| --- | --- | --- |
| AtlasClaw 用户身份 | `auth.provider: "host_cookie"` | 读取企业系统 Cookie，解析当前 AtlasClaw 用户。 |
| Provider 访问 | `service_providers.<provider>.<instance>.auth_type: "cookie"` | 把当前请求 Cookie 传入 Provider runtime。 |

第一层回答“谁在使用 AtlasClaw？”。第二层回答“Provider 调用上游系统时使用什么凭证？”。要实现无缝内嵌，两层都需要配置。

## 推荐流程 {#recommended-flow}

1. 用户先登录企业系统。
2. 企业系统把 AtlasClaw 菜单 UI、悬浮 UI 或两者作为独立内嵌界面打开。
3. 浏览器对两支 UI 的 AtlasClaw 请求携带相同的企业系统认证 Cookie 和身份 Cookie。
4. AtlasClaw 使用 `host_cookie` auth 解析用户，并创建或更新 workspace shadow user。
5. AtlasClaw 使用 `embed_integration` 选定的 HostApp Provider。
6. 该 Provider 实例通过 `auth_type: "cookie"` 获得请求级 Cookie。
7. Domain Skills 使用该 Cookie 调用现有系统 API，因此上游 RBAC、业务流程和审计仍然与原企业系统登录用户一致。

该 Cookie 只存在于当前请求运行时。它不会复制到 Provider Tokens，不会保存成用户设置，也不应写入 `atlasclaw.json`。

## AtlasClaw Auth 配置 {#atlasclaw-auth-configuration}

将 `auth.provider` 配置为 `host_cookie`，并映射企业系统签发的 Cookie 名称。

```json
{
  "auth": {
    "enabled": true,
    "provider": "host_cookie",
    "host_cookie": {
      "cookie_name": "Host-Authenticate",
      "subject_cookie_name": "userLoginId",
      "display_name_cookie_name": "username",
      "user_id_cookie_name": "userId",
      "tenant_id_cookie_name": "tenant_id"
    }
  }
}
```

字段含义：

| 字段 | 说明 |
| --- | --- |
| `cookie_name` | 企业系统认证 Cookie，包含 AtlasClaw 在 cookie-mode Provider 访问中转发的原始 token。 |
| `subject_cookie_name` | 必填的稳定登录标识，用作 AtlasClaw subject。 |
| `display_name_cookie_name` | 可选显示名，用于 AtlasClaw 页面展示。 |
| `user_id_cookie_name` | 可选上游用户 ID，会写入认证用户 metadata。 |
| `tenant_id_cookie_name` | 可选租户标识；缺省时 AtlasClaw 使用 `default`。 |

在 `host_cookie` 模式下，AtlasClaw 仍会优先接受有效的 AtlasClaw admin JWT。这保证后台管理入口可用，而普通内嵌用户通过企业系统 Cookie 进入。

## HostApp Provider Cookie 配置 {#provider-cookie-configuration}

当 HostApp Provider 调用现有系统时需要使用当前请求 Cookie，应把该 Provider 实例配置为 `auth_type: "cookie"`。

```json
{
  "service_providers": {
    "example_provider": {
      "default": {
        "base_url": "${PROVIDER_URL}",
        "auth_type": "cookie"
      }
    }
  }
}
```

正常内嵌路径不要配置静态 `cookie` 字段。静态 Cookie 只适合受控的 server-to-server 测试，因为所有请求都会使用同一个会话。生产内嵌模式应选择运行时请求 Cookie 作为凭证。

## 企业系统要求 {#host-system-requirements}

企业系统必须让 AtlasClaw 请求可以携带该 Cookie。通常需要满足：

- AtlasClaw 部署在同站点、父域名或反向代理路径下，企业系统 Cookie 对 AtlasClaw 请求可见。
- Cookie 的 `Path`、`Domain`、`SameSite`、`Secure` 属性允许浏览器把企业系统 Cookie 发送给 AtlasClaw。
- 企业系统提供稳定的 subject Cookie，AtlasClaw 才能把请求映射到 workspace 用户。
- HostApp Provider 可以使用该 Cookie 调用现有系统 API，或知道如何把它换成这些 API 所需的原生会话。

对于菜单 UI，完成上述 Cookie 配置并嵌套 Agent 入口就是全部企业系统集成：打开 `/atlasclaw/?embedded=1&surface=menu`。菜单 UI 不需要页面变化消息桥。

对于悬浮 UI，企业系统还需要渲染并管理紧凑 iframe，使用精确 Host Origin 和全新 nonce 构造 URL，上报带单调递增 generation 的标准化路由路径，并严格校验双向消息。企业系统只提供页面导航事实；Context 解析以及操作、确认、执行和权限检查由 AtlasClaw 与 HostApp Provider 负责。详见[企业系统能力要求](./embedded-menu-and-floating-ui.md#host-app-capabilities)。

如果 AtlasClaw 被嵌入跨站 iframe，浏览器 Cookie 限制可能会阻止请求 Cookie。应在目标部署中验证最终浏览器行为，而不是只检查服务端配置。

## 安全注意事项 {#security-notes}

- 将企业系统 Cookie 视为用户凭证。不要记录到日志、记忆或排障输出中。
- 生产环境应使用 HTTPS 和安全 Cookie 属性。
- 保持目标系统的 Provider RBAC 生效。AtlasClaw 不应授予目标系统本身会拒绝的访问。
- 只有在部署明确需要共享身份或机器人身份时，才使用 `provider_token`、`credential` 或 `app_credentials`。

## 故障排查 {#troubleshooting}

| 现象 | 检查项 |
| --- | --- |
| AtlasClaw 页面加载前用户被重定向或拒绝 | 确认 `auth.provider` 是 `host_cookie`，并且 AtlasClaw 请求中存在配置的 `cookie_name`。 |
| 用户映射到错误的 AtlasClaw 账号 | 检查 `subject_cookie_name`，它必须对用户稳定且唯一。 |
| Provider 调用提示缺少凭证 | 确认 Provider 实例选择 `auth_type: "cookie"`，并且当前请求包含企业系统 Cookie。 |
| Provider 调用未授权 | 确认目标系统接受转发的 Cookie，并且上游用户拥有所需权限。 |
| iframe 外可用，iframe 内不可用 | 检查浏览器 `SameSite`、第三方 Cookie、`Secure`、Domain/Path 行为。 |
