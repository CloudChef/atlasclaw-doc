---
title: Alarm and Resource Health
description: Analyze SmartCMP alerts or resource runtime health.
sidebar_position: 10
---

# Alarm and Resource Health

SmartCMP alarm skills help users inspect operational alerts or analyze one
resource's runtime health independently from alerts.

## Supported Actions {#supported-actions}

- List current alerts.
- Analyze one alert with context and recommendations.
- Analyze whether a resource is healthy, abnormal, or indeterminate from its
  component-specific monitoring evidence.
- Operate on alert status when the user explicitly requests an action such as
  mute, resolve, or reopen.

## Safety Rule {#safety-rule}

The agent should not change alert state unless the user explicitly asks for an
operation.

## Resource Health Analysis {#resource-health-analysis}

Resource health analysis does not require an active alert and does not use the
absence of alerts as proof that a resource is healthy. The Provider:

1. resolves the exact resource and its `componentType`;
2. loads the effective monitoring model for that component;
3. executes the model's resource-scoped Prometheus definitions;
4. returns bounded current-window and baseline statistics;
5. lets the AtlasClaw LLM conclude `healthy`, `abnormal`, or `indeterminate`.

There is no generic hardcoded VM metric list. AWS virtual machines, AWS RDS,
vSphere virtual machines, software, hardware, and other resource types use
their own component monitoring definitions. When monitoring is disabled,
unsupported, inaccessible, or incomplete, the response must describe the
evidence gap instead of reporting a healthy state.

## Workflow {#workflow}

1. List active or relevant alerts.
2. Select one alert by ID or clear description.
3. Analyze the alert context and recommended response.
4. If the user asks for a status operation, confirm the target alert and action.
5. Execute the operation and report the upstream result.

## Status Operations {#status-operations}

Typical actions include `mute`, `resolve`, and `reopen`. Use the exact action
names supported by the provider skill. Do not treat analysis as permission to
change status.

## Troubleshooting Alerts {#troubleshooting-alerts}

If alerts cannot be listed, check SmartCMP token validity and whether the user's
SmartCMP role can access alarm data. If an operation fails, check whether the
alert is still active and whether the requested action is valid for its state.
For resource health, also check whether the component has an effective
monitoring model and whether the resource has usable Prometheus series.
