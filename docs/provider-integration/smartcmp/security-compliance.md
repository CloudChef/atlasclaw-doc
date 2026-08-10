---
title: Security Compliance
description: Review SmartCMP Security posture and use the confirmed two-phase violation status workflow.
sidebar_position: 12
---

# Security Compliance

SmartCMP separates resource-first Security analysis from CMP policy-violation
workflows. The `security-compliance` Skill owns the CMP-wide Security overview,
the Security violation collection, and actions on one violation object. The
`resource` Skill owns questions about a named, selected, listed, or current
resource, including its Security posture and associated violations.

## Routing Boundary {#routing-boundary}

| User intent or context | Owning Skill |
| --- | --- |
| CMP-wide Security posture, policies, executions, trends, or violation list | `security-compliance` |
| A violation ID, a selected violation row, or “the Nth violation” | `security-compliance` |
| A resource name or ID, a selected resource row, or the current Resource page | `resource` |

List indexes are presentation references, not violation IDs. The Provider keeps
the real violation ID in hidden object metadata and uses that exact ID when an
Analyze action starts.

## Violation Workflow {#violation-workflow}

1. Use `smartcmp_get_security_overview` for the CMP-wide Security policy,
   execution, compliance, severity, violation, and trend state.
2. Use `smartcmp_list_security_violations` to browse Security violations. A list
   row exposes only **Analyze**.
3. **Analyze** calls `smartcmp_analyze_security_violation` and freshly rereads
   the exact violation, its latest status, resource, and policy. It presents
   CMP-confirmed facts, evidence gaps, manual remediation guidance, and
   verification steps, then stops.
4. Only a fresh analysis whose latest status is `ACTIVED` may expose **Mark
   Fixed**. The UI requires a separate explicit confirmation. After confirmation,
   `smartcmp_mark_security_violation_fixed` rereads the exact violation before
   updating and verifying its status.

Analyze and Mark Fixed must never run in the same turn.

## Effect and Safety {#effect-and-safety}

Mark Fixed changes only the CMP violation status. It does not modify, repair,
restart, patch, upgrade, or reconfigure the underlying resource, and a `FIXED`
status alone is not proof that remediation occurred. Apply any resource change
through an independently approved resource or change-management workflow, then
verify the resource and obtain a fresh Security policy result before marking the
violation FIXED.

This workflow exposes no automatic remediation or Security Day-2 execution.

## Resource-First Security Analysis {#resource-first-security-analysis}

For a named or selected resource, use the `resource` Skill. Its Security
analysis combines a bounded, redacted resource profile with associated
CMP-confirmed Security violations. Resource posture inferred by the LLM remains
visibly separate from CMP-confirmed violations and cannot create, clear, or
replace a CMP conclusion.

Associated-violation coverage has three states:

- `complete`: report every match; only an empty result supports “no associated
  CMP Security violation”;
- `partial`: report every match as confirmed and state that the inventory is
  incomplete; an empty result means only that no match was found in scanned
  pages;
- `failed`: report the collection failure and make no absence claim.
