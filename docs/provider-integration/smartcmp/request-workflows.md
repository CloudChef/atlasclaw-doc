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
4. Resolve every active selectable field against current SmartCMP choices,
   including fields that declare a default.
5. Clarify remaining fields after the service, business-group, placement,
   flavor, and template scope are known.
6. Build the request JSON and revalidate the exact selected placement.
7. Show the full JSON preview with credential values masked and ask the user to
   confirm.
8. Submit the corresponding unmasked JSON with `smartcmp_submit_request` only
   after confirmation.
9. Track the resulting SmartCMP user-facing Request IDs, tickets, or work
   orders in SmartCMP.

The service-list, selected-catalog detail, and business-group discovery steps
are mandatory. A sole candidate returned by an explicitly eligible read-only
lookup can be selected without another user turn. Multiple candidates require
an existing user statement that uniquely identifies one result or a concise
selection question.

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

The input is the exact user-visible SmartCMP Request ID returned by submission.
Its format is opaque: it can use a familiar prefix, be numeric, or be
UUID-shaped. If the user refers to the request they just submitted,
reuse the most recent Request ID from the current conversation. If no
user-facing Request ID is available, ask the user for it.

Preserve a supplied or returned Request ID exactly. Do not impose a prefix,
character set, or fixed-length pattern. A user-facing Request ID can itself be
UUID-shaped; the forbidden substitution is SmartCMP's separate internal object
`id`, not the shape of the user-facing value.

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
success. The separate internal object `id` remains a Provider implementation
detail and must not replace `items[].request_id` in replies or follow-up Tool
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

## Choice Resolution and Placement Validation {#choice-resolution-and-placement-validation}

Defaults in generated catalog metadata are suggestions, not proof that a value
is still requestable. For every active selectable field, the request workflow
performs a current lookup. It may continue automatically only when an eligible
read-only lookup has one visible candidate. When several candidates remain, it
uses already stated intent only if that intent uniquely matches one result;
otherwise it asks one selection question and stops.

Resolve placement fields in dependency order:

1. resource-pool tags and resource pool;
2. compute profile and, when explicitly selectable, cloud flavor;
3. logical template;
4. either a physical template or a cloud image.

For an exact vSphere resource pool, SmartCMP resolves `flavorId` from the
selected `computeProfileId`; omit `flavorId` instead of sending an empty value
or copying the compute-profile ID. Other or unknown platforms remain
fail-closed and require the normal flavor lookup.

Immediately before preview, the Provider must re-read the selected resource
pool and verify that it remains valid, that all required placement selections
are present, and that no configuration error remains. A changed or invalid
selection blocks preview and submission.

## Template Branches {#template-branches}

The selected catalog contract decides which mutually exclusive template branch
is serialized:

| Branch | Required request fields | Field that must be omitted |
| --- | --- | --- |
| Physical template | `logicTemplateId` and `physicalTemplateId` | `templateId` |
| Cloud image | `logicTemplateId` and `templateId` | `physicalTemplateId` |

Never place an image ID in `physicalTemplateId`. Display names are for user
selection; the request body uses the exact IDs returned by the current lookup.

Image and flavor discovery is paginated and bounded to at most 50 rows per
page. Use `query` to narrow large inventories and `page` to continue instead of
assuming that the first page is complete.

## Draft Before Submit {#draft-before-submit}

For ambiguous natural-language requests, use the request decomposition agent to
create a draft. The draft should mark unresolved fields instead of inventing
values. Submit only after the user reviews the completed JSON request body and
confirms it. Credential values are masked only in the displayed preview; the
submit body must use the retained original values.

## Safety Boundary {#safety-boundary}

Submitting a SmartCMP request creates an upstream workflow. The agent should not
submit if required fields are missing, if the user asks only for discovery, or
if the selected catalog item is ambiguous. The agent must stop after showing the
JSON preview until the user confirms submission. Any request field or secret
added or changed after preview invalidates the earlier confirmation and
requires a new validated preview and confirmation.
