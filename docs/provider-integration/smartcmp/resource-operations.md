---
title: Resource Analysis and Operations
description: Browse, comprehensively analyze, and operate SmartCMP resources.
sidebar_position: 9
---

# Resource Analysis and Operations

SmartCMP resource skills support read-only resource browsing, comprehensive
single-resource analysis, and selected day-2 operations.

## Browsing {#browsing}

Users can list resources, filter cloud hosts, inspect a resource by ID, and use
the normalized resource view returned by typed Provider operations through the
thin AtlasClaw Skill adapter.

Discovery examples include:

- list all resources;
- list all cloud hosts;
- filter hosts by keyword;
- refresh and analyze a single host by resource ID;
- fetch resource details for compliance or troubleshooting.

## Comprehensive Resource Analysis {#comprehensive-resource-analysis}

A resolved cloud-resource or virtual-machine page can expose a dynamic
**Analyze** action. It uses the `resource` Skill as a coordinator and keeps one
exact internal SmartCMP resource target across four existing read-only
analyzers:

1. current alerts and currently resolved alerts whose trigger time is inside
   the configured lookback;
2. runtime health from the resource component's Prometheus monitoring model;
3. generic compliance risk from a bounded and redacted resource profile;
4. platform-confirmed and LLM-inferred cost optimization opportunities.

The final response separates evidence and gaps for each dimension, then
highlights cross-dimensional relationships. Failure or missing evidence in one
dimension does not suppress the other dimensions. Comprehensive analysis does
not change the resource.

The action is generated from the current resource object. When the user
navigates to another supported SmartCMP page, the floating assistant resolves
a new Context. A later Chat submission carrying the older Context is rejected;
a turn that was already accepted continues through the ordinary Chat runtime.

## Operations {#operations}

The resource operation skill supports explicit actions such as start and stop
after the target resource ID is resolved.

Operations depend on the user's SmartCMP permissions and the target resource's
current state.

Successful operation output is intentionally concise. It should include the
action, target resource IDs, submitted flag, user-facing message, and
verification hint. It should not print raw SmartCMP request payloads or raw
response details. If SmartCMP returns a business failure in an HTTP 200
response, the tool should surface a concise error instead of reporting
submission success.

## Operation Safety {#operation-safety}

Start and stop actions change upstream resource state. Before operating, the
agent must show the target resource name, current state when available, and
intended action. The stable SmartCMP resource ID is resolved and retained
internally rather than requested from or exposed to the user. The agent should
ask for explicit confirmation, such as `确认要执行吗？`, stop, and call the
operation only after the user confirms.

## Common Blockers {#common-blockers}

| Blocker | Meaning |
| --- | --- |
| Resource not found | The ID is wrong or not visible to the user's SmartCMP credentials. |
| Unsupported action | The target resource type does not support the requested day-2 action. |
| Permission denied | SmartCMP accepted the token but denied the operation. |
| Current state mismatch | The resource is already stopped, running, or in a transitional state. |
