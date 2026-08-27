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
- fetch resource details for Security analysis or troubleshooting.

## Comprehensive Resource Analysis {#comprehensive-resource-analysis}

A resolved cloud-resource or virtual-machine page can expose a dynamic
**Analyze** action. It uses the `resource` Skill as a coordinator and keeps one
exact internal SmartCMP resource target across four existing read-only
analyzers:

1. current alerts and currently resolved alerts whose trigger time is inside
   the configured lookback;
2. runtime health from the resource component's Prometheus monitoring model;
3. resource-first Security posture from a bounded and redacted resource profile,
   with associated CMP-confirmed Security violations kept separate from LLM
   inference;
4. platform-confirmed and LLM-inferred cost optimization opportunities.

The final response separates evidence and gaps for each dimension, then
highlights cross-dimensional relationships. Failure or missing evidence in one
dimension does not suppress the other dimensions. Comprehensive analysis does
not change the resource.

Security violation coverage remains explicit. Every exact match is reported even
when the inventory is partial. Only complete coverage with no matches supports a
no-associated-violation conclusion; partial or failed coverage cannot establish
absence.

The action is generated from the current resource object. When the user
navigates to another supported SmartCMP page, the floating assistant resolves
a new Context. A later Chat submission carrying the older Context is rejected;
a turn that was already accepted continues through the ordinary Chat runtime.

## Operations {#operations}

The Agent's explicit generic resource-action set is `refresh`, `start`, `stop`,
`restart`, `suspend`, and `tear_down_in_resource`. The action must also be
enabled by SmartCMP for the exact target's current type, state, and user
permission. A user may identify the
target with `resource_id`, `resource_name`, `deployment_id`, or
`deployment_name`. Names must resolve to exactly one visible SmartCMP object;
the operation stops before making any change when a name is missing or
ambiguous.

Operations depend on the user's SmartCMP permissions and the target resource's
current state.

Listing available actions does not execute one. After the target and available
actions have been shown, a later exact command that names the resolved target
and operation is explicit confirmation; the Agent does not ask for a redundant
second confirmation. An action-only command from a validated current resource
page inherits that page target but still follows the owning resource Skill's
state and permission checks.

Successful operation output is intentionally concise. It should include the
action, target resource IDs, submitted flag, user-facing message, and
verification hint. It should not print raw SmartCMP request payloads or raw
response details. If SmartCMP returns a business failure in an HTTP 200
response, the tool should surface a concise error instead of reporting
submission success.

### Removal Lifecycle {#removal-lifecycle}

Recycle-bin cleanup follows this lifecycle. These stages are not
interchangeable:

| Stage | SmartCMP operation | Result |
| --- | --- | --- |
| Tear down | `tear_down_in_resource` | Moves the active resource into its stopped or torn-down state. It does not permanently remove the CMP record. |
| Refresh scope | Fresh exact recycle-bin read | Resolves the target deployment and its complete resource-ID set immediately before permanent removal. |
| Permanently remove | `permanently_delete_deployment` | Permanently removes the recycled deployment. This is a deployment-level action and can affect every resource that belongs to that deployment. |

In other words, the cleanup progression is **tear down → fresh exact
recycle-bin read with complete deployment and resource scope → submit
permanent removal exactly once**. `delete_metadata_in_resource` is not an
Agent-supported resource action and must never be used as a cleanup step or as
a substitute for the dedicated recycle-bin workflow. A node whose `status` is already
`deleted` is not evidence that permanent removal succeeded.

When the target is supplied as a resource, the agent resolves and retains its
owning recycle-bin deployment before permanent removal. When the target is
supplied as a deployment, the same exact and unique matching rule applies. The
agent must not choose the first partial name match or assume that a deployment
contains only one resource.

Automatic exact-locator resolution currently scans at most 2,000 recycled
deployments and fails closed beyond that limit. For unfiltered recycle-bin
browsing, `total`, `page`, and `size` describe the deployment page; `items`
contains expanded resource rows, so one deployment can produce several items.
The page size is at most 20 deployments.

## Operation Safety {#operation-safety}

State-changing actions require explicit confirmation. Before operating, the
agent must show the exact target, its current state when available, and the
intended action. For permanent removal, it must also show the resolved
deployment and warn that the operation affects all resources in that deployment
and cannot be undone. The agent then stops and submits the operation only after
the user explicitly confirms that scope. The fresh recycle-bin row must expose
`permanently_delete_deployment`; otherwise the workflow stops without a write.
The write carries the confirmed
deployment ID and complete resource-ID set; if the freshly resolved scope has
changed, the Provider stops before submission and requires a new confirmation.

Permanent removal is asynchronous. The agent submits
`permanently_delete_deployment` exactly once and polls without resubmitting.
After a successful purge submission, completion is verified against the
deployment rather than the node: either the deployment disappears, or the
recycle-bin read returns a tombstone with `deleted=true`, `state=DELETED`, a
positive `recycle_delete_time`, and no available operations. A tombstone may
remain visible during SmartCMP's configured retention period. Node
`status=deleted` alone must never be used as proof of permanent removal.

## Common Blockers {#common-blockers}

| Blocker | Meaning |
| --- | --- |
| Resource not found | The ID is wrong or not visible to the user's SmartCMP credentials. |
| Ambiguous name | More than one visible resource or deployment has the requested name; use an exact unique name or an ID. |
| Unsupported action | The target resource type does not support the requested day-2 action. |
| Permission denied | SmartCMP accepted the token but denied the operation. |
| Current state mismatch | The resource is already stopped, running, or in a transitional state. |
| Recycled action unavailable | The deployment is not in the recycle bin, is still processing another action, is already permanently deleted, or the user lacks permission. |
