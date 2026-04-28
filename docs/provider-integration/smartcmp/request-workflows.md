---
title: Request Workflows
description: Submit SmartCMP service and resource requests.
sidebar_position: 7
---

# Request Workflows

The SmartCMP request skill helps users translate infrastructure needs into
structured SmartCMP requests.

## Typical Flow {#typical-flow}

1. List published services first with `smartcmp_list_services`.
2. List available business groups with `smartcmp_list_available_bgs`.
3. Clarify missing request fields after the service and business-group scope
   are known.
4. Build the request JSON.
5. Show the full JSON preview and ask the user to confirm.
6. Submit with `smartcmp_submit_request` only after confirmation.
7. Track the resulting SmartCMP ticket or work order in SmartCMP.

The service-list and business-group discovery steps are mandatory. If
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
