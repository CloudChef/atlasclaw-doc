---
title: Sessions
description: Session keys, user isolation, transcripts, and history.
sidebar_position: 3
---

# Sessions

Sessions store conversation state for a user, channel, and thread.

## Session Scope {#session-scope}

AtlasClaw uses structured session keys to identify agent, channel, chat type,
user, and thread. This keeps web, API, webhook, and IM conversations isolated.

The storage layout is user-oriented. Session metadata is written under the
workspace user's session directory, and archived or migrated session data stays
inside that user's workspace scope.

## User Isolation {#user-isolation}

Session metadata and transcripts are scoped to the authenticated user. Direct
session operations must reject access to sessions owned by another user.

This matters for IM channels because a channel may carry messages from multiple
threads. The session key must include enough channel and thread information to
avoid mixing histories.

## Session Operations {#session-operations}

Core exposes APIs to list sessions, create sessions, create threads, fetch
history, reset a session, delete a session, inspect status, queue messages, and
compact long histories.

Typical user operations include:

- opening the most recent session;
- creating a new thread for a new task;
- switching back to a prior conversation;
- resetting a session when the current context is no longer useful;
- deleting sessions according to workspace retention policy.

## Compaction {#compaction}

Compaction reduces long conversation history while preserving recent user intent
and useful context for future turns.

Compaction is not a substitute for durable provider records. If a provider
creates an upstream ticket, request, approval, or resource operation, the
provider system remains the record of truth. Session history is conversational
context.

## Queueing and Concurrency {#queueing-and-concurrency}

AtlasClaw can queue messages so a session does not run conflicting agent turns
at the same time. This is especially important for IM channels, where users may
send several messages quickly. Operators should investigate long queues as a
sign of slow model responses, provider API latency, or a stuck tool call.
