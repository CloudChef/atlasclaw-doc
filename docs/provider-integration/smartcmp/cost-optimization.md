---
title: Cost Optimization
description: Review and execute SmartCMP cost optimization actions.
sidebar_position: 11
---

# Cost Optimization

SmartCMP cost optimization skills support FinOps-style review and remediation.

## Supported Actions {#supported-actions}

- List optimization recommendations.
- Analyze savings opportunities.
- Execute SmartCMP-native remediation actions.
- Track execution progress.

Execution must use SmartCMP credentials authorized for the target environment.

## Workflow {#workflow}

1. List optimization recommendations.
2. Inspect the finding and estimated savings.
3. Decide whether the recommendation is safe for the business context.
4. Execute the SmartCMP-native day-2 fix only after explicit user intent.
5. Track the remediation state.

## Safety Boundary {#safety-boundary}

Cost recommendations are advisory until executed. Execution uses SmartCMP-native
remediation, not direct public-cloud API calls from AtlasClaw. The agent should
not claim savings until SmartCMP reports the remediation state.

## Review Criteria {#review-criteria}

- Is the resource still needed?
- Is the recommendation based on current usage?
- Does the fix affect production workloads?
- Is there a maintenance window or approval requirement?
- Can the action be rolled back in SmartCMP?
