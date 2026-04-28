---
title: Memory
description: User-scoped memory and context persistence.
sidebar_position: 6
---

# Memory

Memory stores reusable user and conversation context.

## Storage Model {#storage-model}

Memory is scoped by user. This prevents one user's long-term notes or derived
context from leaking into another user's session.

Memory should contain reusable context, preferences, and summaries that help
future conversations. It should not be used as a secure store for provider
tokens, cookies, webhook secrets, or passwords.

## Memory Types {#memory-types}

Core supports daily, long-term, and ephemeral memory categories. The agent
runtime can search memory and read selected entries when the tools are enabled
for the current role.

| Type | Typical content |
| --- | --- |
| Daily | Recent task summaries and short-lived context. |
| Long-term | Stable preferences, recurring projects, and durable user context. |
| Ephemeral | Temporary runtime notes that should not become durable knowledge. |

## Agent Memory Settings {#agent-memory-settings}

`MEMORY.md` controls the agent-level memory strategy and `max_context_rounds`.
Use this to tune how much recent dialogue remains in context before compaction
and retrieval behavior become more important.

## Governance {#governance}

Administrators should decide what memory behavior is acceptable for their
deployment. For regulated environments, document whether long-term memory is
enabled, how users can request removal, and which data types must never be
stored.

## Good Memory Candidates {#good-memory-candidates}

- A user's preferred business unit or environment naming convention.
- A recurring project name that appears in many requests.
- A high-level summary of a long planning conversation.

## Bad Memory Candidates {#bad-memory-candidates}

- API tokens, passwords, cookies, or webhook secrets.
- One-time approval codes.
- Sensitive incident details that should remain in the source system.
