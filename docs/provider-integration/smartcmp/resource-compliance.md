---
title: Resource Compliance
description: Analyze SmartCMP resource lifecycle, patch, security, and configuration posture.
sidebar_position: 12
---

# Resource Compliance

The resource compliance skill fetches resources by ID and analyzes their
posture.

## Analysis Areas {#analysis-areas}

- Lifecycle state.
- Patch posture.
- Security posture.
- Configuration risk.
- Operational recommendations.

The analysis uses the shared normalized resource view exposed by SmartCMP
`datasource/scripts/list_resource.py`.

## Workflow {#workflow}

1. Fetch resource facts by resource ID through `list_resource.py`.
2. Read the normalized `type + properties` view.
3. Route to the relevant analyzer based on resource type and evidence.
4. Perform best-effort validation when version or lifecycle evidence is
   available.
5. Return findings, evidence, and recommendations.

## Evidence Rules {#evidence-rules}

The compliance skill should distinguish between confirmed evidence and missing
data. If a product version, OS version, or configuration field is unavailable,
the result should say so instead of inventing a risk.

## Scope {#scope}

Resource compliance is advisory. It does not remediate resources and does not
change SmartCMP state. Use resource operations or other SmartCMP workflows only
when the user separately requests a concrete action.
