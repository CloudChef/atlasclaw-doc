---
title: Capabilities
description: SmartCMP capability map.
sidebar_position: 6
---

# Capabilities

SmartCMP Provider exposes these major capability areas:

- Resource requests for cloud resources, virtual machines, applications, and
  ticket-style services, including submitted request status lookup by Request
  ID.
- Approval management for pending approval tasks.
- Directory queries for business groups, service catalogs, resource pools,
  resources, hosts, templates, images, and reference data.
- Resource operations such as start and stop.
- Alarm listing, analysis, and status operations.
- Cost optimization recommendation review, execution, and tracking.
- Resource compliance analysis for lifecycle, patch, security, and configuration
  posture.

Provider skills are loaded from the SmartCMP provider package and qualified by
provider namespace.

## Skill Map {#skill-map}

| Skill | Type | Main operations |
| --- | --- | --- |
| `datasource` | Read-only discovery | Service catalogs, business groups, templates, images, resource details. |
| `resource-pool` | Read-only directory | List and filter SmartCMP resource pools. |
| `resource` | Directory and day-2 | List resources or cloud hosts, inspect details, start or stop resources. |
| `request` | Provisioning and status | Build and submit SmartCMP service/resource requests; check submitted request status by Request ID. |
| `approval` | Workflow | List pending approval tasks, approve, reject. |
| `alarm` | Monitoring | List alerts, analyze alerts, operate alert status. |
| `cost-optimization` | FinOps | List recommendations, analyze savings, execute native fixes, track execution. |
| `resource-compliance` | Analysis | Fetch resources and analyze lifecycle, patch, security, and configuration posture. |
| `preapproval-agent` | Agent workflow | Apply policy-based pre-review to approval workflows. |
| `request-decomposition-agent` | Agent workflow | Convert natural language needs into request drafts. |

## Read vs Write Capabilities {#read-vs-write-capabilities}

Read-only discovery skills are suitable for first tests after setup. Write or
side-effecting skills include request submission, approval/rejection, resource
start/stop, alert status operations, and cost remediation execution. Require
clear user intent before running write workflows.
