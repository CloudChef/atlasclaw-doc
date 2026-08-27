---
title: Approval Workflows
description: View, approve, and reject SmartCMP approvals.
sidebar_position: 8
---

# Approval Workflows

The SmartCMP approval skill manages pending approval tasks. It is separate from
submitted request status lookup.

## Supported Actions {#supported-actions}

- List pending approvals.
- Fetch request details.
- Approve a request by SmartCMP Request ID, with an optional reason.
- Reject a request by SmartCMP Request ID, with a required non-empty reason.

## Boundary With Request Status {#boundary-with-request-status}

Use approval tools only for pending approval tasks and approve/reject actions.
Do not use approval tools for a user's submitted request status query or for
questions such as "has my request been approved?" Those questions should use
the request skill's `smartcmp_get_request_status` tool with the submitted
Request ID.

## Request ID Contract {#request-id-contract}

Approval tools use the same exact user-facing SmartCMP Request ID that appears
in the pending approval list and SmartCMP UI. Its format is opaque and may be
prefixed, numeric, or UUID-shaped.

The pending list returns each row with a visible `index`, normalized
`request_id`, and Object Action metadata. When a user says "approve 1",
"同意 1", "reject #2", or another row-based selection, the agent must resolve
that row to its normalized `request_id` before calling `smartcmp_approve` or
`smartcmp_reject`.

Do not pass display row numbers, placeholder values, or SmartCMP's separate
internal object ID to approval action Tools. Preserve a supplied Request ID
exactly, including case and punctuation. The approve and reject Provider
operations resolve that user-facing value to SmartCMP's internal approval
action ID before submitting the decision.

The `ids` input accepts either one Request ID string or an array of Request ID
strings. A single string is one opaque ID and is never split on whitespace or
punctuation.

## Governance {#governance}

Approval operations must run under SmartCMP credentials that have the required
SmartCMP approval authority. AtlasClaw workspace roles do not grant approval
power inside SmartCMP.

## Recommended Approval Flow {#recommended-approval-flow}

1. List pending approvals.
2. Inspect the selected approval item.
3. Review request purpose, resource sizing, target environment, and cost impact.
4. Require a non-empty reason for rejection. An approval reason remains
   optional unless local governance requires one.
5. Execute approve or reject only after the user intent is explicit.
6. Report the upstream result and the user-facing Request ID for every item.

For batch approvals or rejections, resolve every selected row to a Request ID
from the latest pending approval metadata. If that metadata is unavailable or
stale, list pending approvals again before executing the action.

Batch results are evaluated per item. Report every item as succeeded, failed,
or unknown, preserve its Request ID, and never collapse a partial batch into a
single success statement. If a rejection call lacks a reason, the Provider
returns an input-required result bound to the same workflow and performs no
SmartCMP write.

On a work-order approval page, the Provider resolves the record across pending
and completed views. Only an exact pending task exposes approval mutations;
completed or inconsistent records remain available for read-only detail.

## When to Escalate {#when-to-escalate}

Do not auto-approve when the request lacks a business reason, has unclear
ownership, targets a sensitive environment, or exceeds the approver's expected
authority. In those cases the agent should summarize the risk and ask the user
to handle it in SmartCMP or consult the owning team.
