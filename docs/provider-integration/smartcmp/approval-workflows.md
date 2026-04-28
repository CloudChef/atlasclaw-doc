---
title: Approval Workflows
description: View, approve, and reject SmartCMP approvals.
sidebar_position: 8
---

# Approval Workflows

The SmartCMP approval skill manages pending approval tasks.

## Supported Actions {#supported-actions}

- List pending approvals.
- Fetch request details.
- Approve a request with a reason.
- Reject a request with a reason.

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
6. Report the upstream result and any returned request or workflow identifier.

## When to Escalate {#when-to-escalate}

Do not auto-approve when the request lacks a business reason, has unclear
ownership, targets a sensitive environment, or exceeds the approver's expected
authority. In those cases the agent should summarize the risk and ask the user
to handle it in SmartCMP or consult the owning team.
