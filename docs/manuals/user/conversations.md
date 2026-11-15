---
title: Conversations
description: Chat with AtlasClaw and work with sessions.
sidebar_position: 2
---

# Conversations

The chat page is the main AtlasClaw workspace for a Standard User.

## Start a Conversation {#start-a-conversation}

Open the AtlasClaw web UI and send a message in the chat input. The agent uses
the current authenticated user, enabled skills, provider access, and available
model configuration to respond.

## Sessions {#sessions}

AtlasClaw stores conversation sessions under the authenticated user's workspace
scope. Users can switch between their own sessions and continue prior work.

Sessions are separated by user, channel, and thread. A browser chat session and
an IM thread can therefore keep different history even if the same user sends
similar messages from both places.

## Stop an Active Run {#stop-an-active-run}

While a response is running, use **Stop** to request cooperative cancellation.
The current run ends in the stopped state once the backend confirms the abort.
AtlasClaw keeps the input draft and any response content that was already
generated; stopping does not silently replace a partial response with an empty
message.

If the run reached another terminal state before the abort was processed, the
UI reconciles and displays that actual state instead of claiming it was
stopped.

## Complete Generated Content {#complete-generated-content}

When you request complete JSON, source code, configuration, or documentation,
AtlasClaw keeps the generated content instead of replacing the middle with an
ellipsis or summary. Fenced code blocks include a copy control that copies the
original complete block, including formatting that may not be visible in the
rendered HTML.

## Asking for Provider Work {#asking-for-provider-work}

When asking the agent to use an operational system, include enough context for
the provider skill to choose the right action:

- what you want to do;
- which environment, project, tenant, resource, or business group applies;
- whether the request is read-only or should change something;
- any approval reason, ticket reference, or business justification.

For write operations, review the agent's summary before confirming. Provider
skills may create upstream side effects such as requests, approvals, resource
operations, or alert status changes.

## Permission Messages {#permission-messages}

If a request needs a disabled skill, unavailable provider instance, or missing
credential, the agent should explain the blocker and direct the user to configure
their own token or contact an administrator as appropriate.

## Good Conversation Patterns {#good-conversation-patterns}

| Pattern | Why it helps |
| --- | --- |
| "List my available options first." | Lets the agent use read-only discovery before a write action. |
| "Use the production instance." | Avoids ambiguity when several provider instances exist. |
| "Do not submit yet; prepare a draft." | Keeps the workflow reviewable. |
| "Explain why this is blocked." | Surfaces missing permissions or credentials. |

Avoid pasting secrets into chat. Use Provider Tokens or channel configuration
forms for credentials.

## Image Analysis

Upload, paste, or drag static PNG, JPEG, or WebP images into the chat composer. Review the previews before sending. You can send an image alone or ask follow-up questions about images retained in the same conversation. Each upload supports up to four images, with a limit of 5 MiB and 20 million pixels per image.

An administrator must enable image analysis for the effective model and endpoint. Support is not inferred from the model name. Attachments are private to the authenticated user and session; unavailable attachments are reported in history. Retained image context is bounded, so upload an image again if it is no longer available to the model.

## Response Language

Explicitly request a language, for example, "Reply in English." This takes precedence over the configured global response language and interface locale. Writing a question in another language alone does not request a language change. The shared policy also applies to model-backed recovery replies; static error messages are not translated by this policy.
