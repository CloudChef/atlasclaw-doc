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
- Reject a request by SmartCMP Request ID, with an optional reason.

## Boundary With Request Status {#boundary-with-request-status}

Use approval tools only for pending approval tasks and approve/reject actions.
Do not use approval tools for a user's submitted request status query or for
questions such as "has my request been approved?" Those questions should use
the request skill's `smartcmp_get_request_status` tool with the submitted
Request ID.

## Request ID Contract {#request-id-contract}

Approval tools use the same user-facing SmartCMP Request ID that appears in the
pending approval list and SmartCMP UI, for example `RES20260505000010`,
`TIC20260502000003`, or `CHG20260413000011`.

The pending list returns each row with a visible `index`, normalized
`request_id`, and Object Action metadata. When a user says "approve 1",
"同意 1", "reject #2", or another row-based selection, the agent must resolve
that row to its normalized `request_id` before calling `smartcmp_approve` or
`smartcmp_reject`.

Do not pass display row numbers, placeholder values, or UUID-shaped internal
SmartCMP IDs to approval action Tools. The approve and reject Provider
operations resolve the user-facing Request ID to SmartCMP's internal approval
action ID before submitting the decision.

## Governance {#governance}

Approval operations must run under SmartCMP credentials that have the required
SmartCMP approval authority. AtlasClaw workspace roles do not grant approval
power inside SmartCMP.

## Recommended Approval Flow {#recommended-approval-flow}

1. List pending approvals.
2. Inspect the selected approval item.
3. Review request purpose, resource sizing, target environment, and cost impact.
4. Ask the user for an approval or rejection reason if it was not provided.
5. Execute approve or reject only after the user intent is explicit.
6. Report the upstream result and the user-facing Request ID.

For batch approvals or rejections, resolve every selected row to a Request ID
from the latest pending approval metadata. If that metadata is unavailable or
stale, list pending approvals again before executing the action.

## When to Escalate {#when-to-escalate}

Do not auto-approve when the request lacks a business reason, has unclear
ownership, targets a sensitive environment, or exceeds the approver's expected
authority. In those cases the agent should summarize the risk and ask the user
to handle it in SmartCMP or consult the owning team.
