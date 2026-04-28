---
title: Resource Operations
description: Browse and operate SmartCMP resources.
sidebar_position: 9
---

# Resource Operations

SmartCMP resource skills support read-only resource browsing and selected day-2
operations.

## Browsing {#browsing}

Users can list resources, filter cloud hosts, inspect a resource by ID, and use
the normalized resource view returned by provider scripts.

Discovery examples include:

- list all resources;
- list all cloud hosts;
- filter hosts by keyword;
- refresh and analyze a single host by resource ID;
- fetch resource details for compliance or troubleshooting.

## Operations {#operations}

The resource operation skill supports explicit actions such as start and stop
after the target resource ID is resolved.

Operations depend on the user's SmartCMP permissions and the target resource's
current state.

## Operation Safety {#operation-safety}

Start and stop actions change upstream resource state. Before operating, the
agent must show the target resource name, resource ID, current state when
available, and intended action. It should ask for explicit confirmation, such as
`确认要执行吗？`, stop, and call the operation only after the user confirms.

## Common Blockers {#common-blockers}

| Blocker | Meaning |
| --- | --- |
| Resource not found | The ID is wrong or not visible to the user's SmartCMP credentials. |
| Unsupported action | The target resource type does not support the requested day-2 action. |
| Permission denied | SmartCMP accepted the token but denied the operation. |
| Current state mismatch | The resource is already stopped, running, or in a transitional state. |
