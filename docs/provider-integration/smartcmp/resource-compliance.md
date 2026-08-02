---
title: Resource Compliance
description: Analyze SmartCMP resource lifecycle, patch, security, and configuration posture.
sidebar_position: 12
---

# Resource Compliance

The resource compliance skill collects bounded SmartCMP evidence for selected
resources and lets the LLM analyze their posture.

## Analysis Areas {#analysis-areas}

- Lifecycle state.
- Patch posture.
- Security posture.
- Configuration risk.
- Operational recommendations.

For an interactive request, the thin Skill adapter resolves one exact resource
from its visible name or recent list index. Authorized backend and webhook
compatibility calls may instead supply one or more internal resource IDs. The
adapter passes that exact target set to the typed `smartcmp_provider`
compliance service. The Provider loads resource evidence, then builds a
bounded and redacted profile for each resource with explicit coverage and
missing evidence.

## Workflow {#workflow}

1. Resolve one interactive resource from its exact name or visible list index,
   or accept one or more authorized internal IDs from a backend compatibility
   request.
2. Load evidence for the exact target set through the Provider operation.
3. Build a bounded, redacted profile for each resource and describe evidence
   coverage and gaps.
4. Let the LLM distinguish confirmed facts, inference, and missing evidence.
5. Return per-resource findings and read-only recommendations without changing
   SmartCMP.

## Evidence Rules {#evidence-rules}

The compliance skill should distinguish between confirmed evidence and missing
data. If a product version, OS version, or configuration field is unavailable,
the result should say so instead of inventing a risk.

Interactive users select resources by visible name or recent list index. Do not
ask them for internal resource IDs or expose those compatibility identifiers in
the final answer.

## Scope {#scope}

Resource compliance is advisory. It does not remediate resources and does not
change SmartCMP state. Use resource operations or other SmartCMP workflows only
when the user separately requests a concrete action.
