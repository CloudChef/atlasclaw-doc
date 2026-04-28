---
title: Hooks and Heartbeat
description: Runtime hook events, pending decisions, and heartbeat jobs.
sidebar_position: 8
---

# Hooks and Heartbeat

Hooks and heartbeat jobs let AtlasClaw run background or event-driven runtime
logic without hardcoding provider behavior into Core.

## Hooks {#hooks}

Hook routes expose module events, pending decisions, confirm, and reject actions.
Hook state is scoped by user and module.

Hooks are useful when a workflow needs an explicit decision point. A hook can
record a pending item, expose it for review, and later receive a confirm or
reject action. Provider-specific event payloads should stay in provider docs;
Core documents only the generic pending-decision pattern.

## Sinks {#sinks}

Hook handlers can write to memory or context through runtime sink abstractions.
This keeps hook side effects explicit and auditable.

Use sinks deliberately. A memory sink should store reusable context, while a
context sink should influence the current workflow without turning every event
into durable memory.

## Heartbeat {#heartbeat}

Heartbeat jobs can target agents or channels and emit runtime events. Use them
for periodic checks, reminders, or background workflows that still respect user
scope and runtime permissions.

Heartbeat events include agent started/completed/failed and channel
check/reconnect/degraded states. These events can be bridged into hook runtime
events so downstream workflows handle background activity through the same
event model.

## When to Use Heartbeat {#when-to-use-heartbeat}

Use heartbeat for:

- periodic channel health checks;
- scheduled agent prompts;
- background reminders that still need user scope;
- reconnect attempts for long-running channel connections.

Do not use heartbeat to hide provider-specific polling logic in Core. Provider
polling rules and external workflow semantics belong in the provider package.
