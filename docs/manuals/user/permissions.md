---
title: Permissions
description: Understand Standard User permissions and access blockers.
sidebar_position: 6
---

# Permissions

The default Standard User role is designed for regular workspace collaboration.

## Default Access {#default-access}

By default, a Standard User can:

- use skills and provider capabilities allowed by role and provider access;
- manage their own channel connections for channel types allowed by role;
- manage their own profile and provider tokens.

## Not Included by Default {#not-included-by-default}

By default, a Standard User cannot manage:

- users;
- roles;
- model configs;
- provider instance configs;
- skill management or permission pages;
- permission models.

If you need access to an administrative page or provider instance, contact an
administrator.

## How Runtime Access Works {#how-runtime-access-works}

A successful provider-backed request usually needs these conditions:

1. The skill is enabled for your role.
2. Your role has access to the target provider instance.
3. The provider instance is active and correctly configured.
4. The IM channel type is allowed for your role, when the request comes from an
   IM channel.
5. Your provider-native credentials are accepted by the upstream system, when
   the provider uses user-scoped credentials.

If any layer is missing, the agent should report a blocker instead of guessing.

## What to Send an Administrator {#what-to-send-an-administrator}

When asking for help, include:

- the action you attempted;
- the provider or channel you expected to use;
- the exact blocker message;
- whether the issue happens in web chat, IM chat, or both;
- whether you have already saved the required Provider Token.

Do not include secrets, API tokens, cookies, or webhook URLs in the help
request.
