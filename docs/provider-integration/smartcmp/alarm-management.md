---
title: Alarm Management
description: List, analyze, and operate SmartCMP alarms.
sidebar_position: 10
---

# Alarm Management

SmartCMP alarm skills help users inspect operational alerts.

## Supported Actions {#supported-actions}

- List current alerts.
- Analyze one alert with context and recommendations.
- Operate on alert status when the user explicitly requests an action such as
  mute, resolve, or reopen.

## Safety Rule {#safety-rule}

The agent should not change alert state unless the user explicitly asks for an
operation.

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
