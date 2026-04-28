---
title: User Guide
description: Use AtlasClaw as a Standard User.
sidebar_position: 1
---

# User Guide

This guide describes the default Standard User experience. The built-in
Standard User role has identifier `user`.

With the default role settings, a Standard User can use chat, manage account
settings, configure personal provider tokens, and manage their own channel
connections. The built-in `user` role is system-managed; deployments that need a
different default should introduce custom role policy deliberately.

## Main Workflows {#main-workflows}

- Start or continue conversations.
- Review conversation history.
- Update account profile, avatar, and password.
- Configure personal provider tokens.
- Configure personal IM channel connections.
- Ask an administrator for missing permissions or provider access.

## First Login Checklist {#first-login-checklist}

1. Confirm your display name and email under Account Settings.
2. Send a simple message in chat to confirm the agent can respond.
3. If you plan to use provider workflows, open Provider Tokens and check whether
   any provider instance requires your personal token.
4. If you plan to chat from an IM platform, open `/channels` and create your
   personal channel connection.
5. When a request is blocked, read the blocker message before retrying. It
   usually names the missing credential, disabled skill, or provider access.

## What Standard User Means {#what-standard-user-means}

Standard User is a workspace role, not an upstream system role. AtlasClaw may
allow you to ask the agent to use a provider skill, but the provider still uses
the credentials available for you. If the upstream system denies an action,
AtlasClaw should report the denial instead of bypassing it.

## Where Settings Live {#where-settings-live}

| Setting | Where to manage it | Owner |
| --- | --- | --- |
| Profile name, email, avatar | Account Settings | You |
| Local password | Account Settings | You, when local login is enabled |
| Provider tokens | Provider Tokens | You |
| IM channel credentials | `/channels` | You |
| Role and provider access | Administrator pages | Administrator |
| Model and provider instance setup | Administrator pages | Administrator |
