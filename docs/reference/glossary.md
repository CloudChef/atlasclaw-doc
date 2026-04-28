---
title: Glossary
description: Common AtlasClaw terminology.
sidebar_position: 5
---

# Glossary

## Agent {#agent}

Runtime persona and execution unit that answers user requests and uses approved
skills and tools.

Agents are primarily defined by files under `.atlasclaw/agents/<agent_id>/`.
The supported `main` agent path can also use a database-backed agent config
record when the deployment enables that workflow.

## Channel {#channel}

Connection between AtlasClaw and a user-facing or system-facing message surface.

Examples include web chat, REST, WebSocket, SSE, and supported IM channels.
Channel connections are user-owned unless a deployment implements a separate
administrative workflow.

## Provider {#provider}

External integration package loaded by Core through `providers_root`.

Providers own concrete auth fields, skill workflows, business terminology, and
upstream API behavior.

## Provider Instance {#provider-instance}

Configured connection to one provider environment, such as a production or
staging instance.

Provider instance access is separate from the permission to create or edit the
instance record.

## Skill {#skill}

Capability definition that tells the agent when and how to use tools or
provider workflows.

Provider skills should be qualified by provider namespace to avoid collisions.

## Standard User {#standard-user}

Built-in role with identifier `user`. It is the default collaborator role.

The default Standard User can use chat, view enabled skills, and manage their
own channel connections.

## Workspace {#workspace}

Runtime storage root for agents, users, sessions, memory, and state.

## Provider Token {#provider-token}

User-owned provider credential stored for a provider type and instance name. It
is separate from IM channel credentials.

## Model Config {#model-config}

Administrative configuration for model provider access, model IDs, endpoint
settings, and model tokens.

## Runtime Access {#runtime-access}

The ability to invoke a skill or provider instance from an agent conversation.
Runtime access is not the same as permission to edit the related configuration.

## User-Scoped Credential {#user-scoped-credential}

A credential saved by an individual user and used only for that user's provider
operations.
