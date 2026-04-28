---
slug: /
title: AtlasClaw Documentation
description: Core-first documentation for installing, operating, and integrating AtlasClaw.
sidebar_position: 1
---

# AtlasClaw Documentation

AtlasClaw is an enterprise agent framework for exposing operational systems,
workflows, and internal tools through a governed conversational interface.

This documentation is core-first. It explains the AtlasClaw runtime, shared
configuration, users, roles, sessions, agents, channels, model settings, skills,
tools, and provider-loading contract. Concrete provider behavior is documented
only under Provider Integration.

## Start Here {#start-here}

- New deployers should start with Installation, then configure the first admin
  user, model access, and provider root.
- Workspace administrators should read Administrator Guide before exposing
  provider skills to users. That guide covers roles, model configs, provider
  instances, channel governance, agent customization, and operational
  troubleshooting.
- Standard users should read User Guide for conversations, account settings,
  provider tokens, personal IM channels, and permission blockers.
- Provider maintainers should read Provider Integration. It explains the
  provider loading contract and keeps concrete provider workflows outside Core.

## What This Site Covers {#what-this-site-covers}

| Area | Audience | Outcome |
| --- | --- | --- |
| Installation | Operators | Install AtlasClaw, configure workspace paths, and verify the service starts. |
| Administrator Guide | Administrators | Configure users, roles, models, provider instances, channels, and agents. |
| User Guide | Standard users | Use chat, update profile settings, manage provider tokens, and connect IM channels. |
| Core | Developers and operators | Understand runtime boundaries, sessions, auth, skills, memory, channels, hooks, and heartbeat. |
| Provider Integration | Provider owners | Install and operate concrete provider packages without polluting Core docs. |
| Reference | Operators and integrators | Look up configuration fields, API route groups, permissions, and feature coverage. |

## Operating Model {#operating-model}

AtlasClaw Core provides the runtime shell: authentication, RBAC, session
isolation, agent execution, tool filtering, model access, user-owned channel
connections, memory, hooks, and provider loading. Providers add concrete
business integrations. A provider can expose skills and scripts, but Core keeps
the common rules about authorization, user scope, configuration shape, and
runtime loading.

The recommended rollout order is:

1. Install Core and confirm the admin account can log in.
2. Configure at least one model provider and verify chat works.
3. Set `providers_root` and confirm provider packages are discovered.
4. Create provider instances and assign provider runtime access to roles.
5. Enable the required skills for Standard User or custom roles.
6. Ask users to configure personal provider tokens or IM channels only after
   the related provider/channel instance is ready.

## Documentation Boundary {#documentation-boundary}

Core documentation must not treat SmartCMP, Jira, or any other provider as a
built-in core feature. Core owns the runtime contract. Provider packages own
auth details, fields, workflows, and provider-specific behavior.

When a provider-specific rule is useful as an example, it belongs under
Provider Integration. Core pages may link to provider pages, but they should not
duplicate provider fields, endpoint details, or workflow semantics.
