---
title: Request Workflows
description: Submit SmartCMP service and resource requests and check submitted request status.
sidebar_position: 7
---

# Request Workflows

The SmartCMP request skill helps users translate infrastructure needs into
structured SmartCMP requests. It also supports status lookup for submitted
requests by the SmartCMP Request ID returned after submission.

## Typical Flow {#typical-flow}

1. List published services once with `smartcmp_list_services` and select one
   catalog UUID from that result.
2. Load its normalized field contract with `smartcmp_get_request_catalog`.
3. List available business groups with `smartcmp_list_available_bgs`.
4. Clarify missing request fields after the service and business-group scope
   are known.
5. Build the request JSON.
6. Show the full JSON preview and ask the user to confirm.
7. Submit with `smartcmp_submit_request` only after confirmation.
8. Track the resulting SmartCMP user-facing Request IDs, tickets, or work
   orders in SmartCMP.

The service-list, selected-catalog detail, and business-group discovery steps
are mandatory. If
`smartcmp_list_available_bgs` returns exactly one business group, the agent can
use it silently. If multiple business groups are returned, the agent must ask
the user to choose.

## Related Skills {#related-skills}

- `request`
- `datasource`
- `resource-pool`
- request decomposition agent
- preapproval agent

Use datasource and resource-pool skills before submission when the user does not
know the valid SmartCMP values.

## Submitted Request Status {#submitted-request-status}

Use `smartcmp_get_request_status` when the user asks about a submitted request,
for example:

- "check my request RES20260501000095 status";
- "has request RES20260501000095 been approved?";
- "is the request I just submitted approved?"

The input is the user-visible SmartCMP Request ID returned by submission, such
as `REQ20260501000095`, `RES20260501000095`, `TIC20260316000001`, or
`CHG20260413000011`. If the user refers to the request they just submitted,
reuse the most recent Request ID from the current conversation. If no
user-facing Request ID is available, ask the user for it.

Do not use SmartCMP internal UUID fields as Request IDs. The typed submit and
status Provider operations may use internal IDs for API lookup, but those
values must not be shown to the agent or used in follow-up status queries.

The status lookup is separate from approval actions. Use the request status tool
for a user's submitted request status or approval result. Use the approval skill
only for pending approval tasks and approve/reject actions.

## Request ID Contract {#request-id-contract}

`smartcmp_submit_request` returns a structured result with an `items` list.
Each item represents one SmartCMP request record and includes its normalized
user-facing `request_id` when SmartCMP returned one. A single submission can
therefore return several request records and outcomes. Examples include
`REQ20260501000095`, `RES20260501000095`, `TIC20260316000001`, and
`CHG20260413000011`.

The submit Provider operation may receive several upstream aliases from
SmartCMP, including `workflowId`, `requestNo`, or `customizedId`. It normalizes
each accepted alias to `items[].request_id` before the thin Skill adapter
returns the result to the agent. Check each item's `outcome`; the presence of a
Request ID alone does not turn a pending or failed outcome into a confirmed
success. Internal UUID-shaped lookup IDs are Provider implementation details
and must not be used as Request IDs in user-facing replies or follow-up Tool
calls.

Follow-up status queries must use the relevant user-facing Request ID. If a
user asks about "the request I just submitted", reuse the latest applicable
`items[].request_id` from the conversation instead of asking for or exposing an
internal ID. If the submission returned multiple IDs and the intended request
is ambiguous, ask the user to choose one.

The status Provider operation returns stable fields such as `state`,
`status_category`, `approval_passed`, `current_step`, `current_approver`,
`provision_state`, `error`, and `updated_at`. The agent can explain those
fields in the user's language.

Common approval-result semantics:

| State | Meaning |
| --- | --- |
| `APPROVAL_PENDING` | Approval has not passed yet; the request is still pending. |
| `APPROVAL_REJECTED`, `APPROVAL_RETREATED` | Approval did not pass. |
| `STARTED`, `TASK_RUNNING`, `WAIT_EXECUTE`, `FINISHED` | Approval passed or the request entered a later execution stage. |
| `INITIALING`, `INITIALING_FAILED`, `FAILED`, `CANCELED` | Report the current state without claiming approval or rejection. |

## Information to Collect {#information-to-collect}

| Item | Why it is needed |
| --- | --- |
| Service catalog item | Determines which request schema and component type apply. |
| Business group/tenant/project | Scopes ownership and entitlement in SmartCMP. |
| Resource pool | Determines where the resource will be provisioned. |
| Template, image, or flavor | Supplies platform-specific deployment parameters. |
| Quantity and sizing | Controls capacity and cost. |
| Business reason | Supports approval and audit workflows. |

## Draft Before Submit {#draft-before-submit}

For ambiguous natural-language requests, use the request decomposition agent to
create a draft. The draft should mark unresolved fields instead of inventing
values. Submit only after the user reviews the completed JSON request body and
confirms it.

## Safety Boundary {#safety-boundary}

Submitting a SmartCMP request creates an upstream workflow. The agent should not
submit if required fields are missing, if the user asks only for discovery, or
if the selected catalog item is ambiguous. The agent must stop after showing the
JSON preview until the user confirms submission.
