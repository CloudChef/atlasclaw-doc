---
title: Cost Optimization
description: Analyze recommendations or resource-level optimization potential.
sidebar_position: 11
---

# Cost Optimization

SmartCMP cost optimization skills support both recommendation-first FinOps
workflows and direct analysis of one resource.

## Supported Actions {#supported-actions}

- List optimization recommendations.
- Analyze an existing recommendation and its reported savings.
- Analyze a cloud, software, hardware, virtualized, VM, or database resource
  even when SmartCMP has not produced a recommendation.
- Execute SmartCMP-native remediation actions.
- Track execution progress.

Execution must use SmartCMP credentials authorized for the target environment.

## Entry Paths {#workflow}

### Existing Recommendation

1. List optimization recommendations.
2. Inspect the finding, resource context, and SmartCMP-provided savings.
3. Decide whether the recommendation is safe for the business context.
4. Execute the SmartCMP-native day-2 fix only after explicit user intent.
5. Track the remediation state.

### Direct Resource Analysis

1. Resolve one exact resource by visible name, recent list selection, or trusted
   current-page Context.
2. Read bounded resource, billing, and utilization facts.
3. Match enabled applicable cost policies and their scope.
4. Correlate the policy's latest exact resource execution and active
   violations.
5. Let the LLM identify separately labeled `llm_potential` opportunities and
   missing evidence.

Direct resource analysis is read-only. It does not run a policy and cannot
create a remediation action from model-only evidence.

## Evidence States {#evidence-states}

| State | Meaning |
| --- | --- |
| `platform_detected` | SmartCMP produced an active cost violation for the resource. |
| `evaluated_clear` | A complete resource execution explicitly evaluated the resource without a violation. |
| `insufficient_evidence` | An execution exists, but its monitoring or decision evidence is incomplete. |
| `covered_not_evaluated` | An enabled applicable policy exists, but no exact resource execution was found. |
| `not_covered` | No enabled applicable policy covers the resource. |
| `execution_failed` | The relevant platform execution failed. |

No active violation does not prove that the resource is optimized. Exact saving
amounts are reported only when SmartCMP supplies them; otherwise the amount
remains unknown.

## Safety Boundary {#safety-boundary}

Cost recommendations are advisory until executed. Execution uses SmartCMP-native
remediation, not direct public-cloud API calls from AtlasClaw. The agent should
not claim savings until SmartCMP reports the remediation state.

Model-only resource opportunities remain advisory and read-only. Reliability or
security settings must not be repackaged as cost savings, and missing monitoring
data must not be interpreted as an idle resource.

## Review Criteria {#review-criteria}

- Is the resource still needed?
- Is the recommendation based on current usage?
- Does the fix affect production workloads?
- Is there a maintenance window or approval requirement?
- Can the action be rolled back in SmartCMP?
