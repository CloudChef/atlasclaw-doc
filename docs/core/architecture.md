---
title: Core Architecture
description: AtlasClaw Core runtime architecture and provider boundary.
sidebar_position: 1
---

# Core Architecture

AtlasClaw Core is the provider-agnostic runtime. It owns API routing, auth,
session isolation, agent execution, model access, channels, memory, hooks, and
provider loading.

## Main Components {#main-components}

- API layer: REST, streaming, auth, session, channel, and management routes.
- Agent runtime: prompt construction, tool routing, execution, streaming, and
  compaction.
- Session and memory: per-user conversation state and long-term memory.
- Auth and RBAC: authentication, role permissions, and request authorization.
- Channel runtime: user-owned channel connections and message handlers.
- Provider registry: external provider discovery and instance configuration.

## Runtime Responsibilities {#runtime-responsibilities}

Core is responsible for behavior that must be consistent across all providers:

| Responsibility | What Core guarantees |
| --- | --- |
| Identity | Every request resolves a current user or is rejected. |
| Authorization | Management APIs and runtime capabilities are filtered by effective roles. |
| Session scope | Conversation history is isolated by user, channel, and thread. |
| Tool exposure | Skills and provider tools are exposed only when enabled and authorized. |
| Model access | Agent execution uses configured model providers and active model tokens. |
| Credential boundary | Provider credentials are resolved by provider contracts, not by Core shortcuts. |
| Auditability | Runtime state is stored under workspace paths instead of being hidden in provider code. |

## Provider Boundary {#provider-boundary}

Core loads providers but does not own provider-specific auth fields, workflow
semantics, business objects, or UI copy. Concrete provider behavior belongs
under Provider Integration.

## Runtime Flow {#runtime-flow}

1. A user authenticates.
2. The request resolves an authorization context.
3. The session key scopes state to user, channel, and thread.
4. The agent runtime builds context and available tools.
5. Provider and skill permissions filter runtime capabilities.
6. The response streams back through the selected channel.

## Deployment Shape {#deployment-shape}

A typical deployment has:

- a workspace directory that stores sessions, memory, user settings, channel
  state, and runtime artifacts;
- a database that stores users, roles, model configs, provider instances, agent
  configs, and channel records;
- a provider root containing external provider packages;
- environment variables for deployment-specific secrets and URLs;
- a frontend that consumes the same API permissions enforced by the backend.

## What Core Does Not Do {#what-core-does-not-do}

Core does not define provider-specific request forms, approval semantics,
resource catalogs, token formats, or business workflow states. When a provider
adds those concepts, document them under that provider's integration section and
keep Core pages limited to the shared contract.
