---
title: Administrator Guide
description: Operate AtlasClaw Core as an administrator.
sidebar_position: 1
---

# Administrator Guide

Administrators manage workspace access, runtime configuration, model settings,
provider instances, channel governance, and agent identity.

The built-in `admin` role has full workspace management access. Custom roles can
delegate narrower permissions for users, roles, channels, model configs,
provider configs, tokens, skills, and provider runtime access.

## Common Tasks {#common-tasks}

- Create users and assign roles.
- Configure model providers and model tokens.
- Register provider instances.
- Govern channel permissions.
- Customize the main agent name, style, behavior, and memory.
- Troubleshoot permission and runtime errors.

## Initial Setup Checklist {#initial-setup-checklist}

Use this checklist for a new workspace:

1. Confirm local admin login works and change any bootstrap password according
   to your deployment policy.
2. Configure model access before enabling provider workflows. A provider skill
   can be available but still unusable if no model is active.
3. Review built-in roles. Keep `admin` for platform administrators and use
   `user` for the default Standard User experience.
4. Create custom roles when a team needs narrower access than `admin` but more
   access than Standard User.
5. Configure provider instances and assign provider runtime access separately
   from provider configuration permissions.
6. Enable only the skills users should see. Skill visibility and provider
   instance access are both required for provider-backed operations.
7. Decide which channel types are approved for production and whether users may
   connect their own IM bots.
8. Customize the main agent identity and style after runtime access is correct.

## Daily Administration {#daily-administration}

Most administration work falls into four loops:

| Loop | Questions to answer | Primary pages |
| --- | --- | --- |
| Access | Who can log in, which roles do they have, and which provider instances can they use? | Users, Roles, Provider Instances |
| Runtime | Which models, tokens, providers, and skills are active? | Model Configs, Provider Instances |
| Experience | What name, tone, avatar, and guidance does the agent present? | Agent Customization |
| Operations | Which credentials are failing, which channels are disconnected, and which permissions block a request? | Troubleshooting, Channel Governance |

## Change Safety {#change-safety}

Treat model tokens, provider credentials, channel secrets, and role permissions
as operational controls. Prefer small changes that can be tested with one user
before rolling them out broadly. When changing provider access, test both the
management page and an actual chat request, because the UI permission and the
runtime provider permission are different checks.
