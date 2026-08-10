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
- Comprehensive single-resource analysis across alerts, monitoring health,
  resource-first Security posture and associated violations, and cost
  optimization, plus operations such as start and stop.
- Alarm listing, alert analysis, model-driven resource health analysis, and
  explicit alert status operations.
- Cost optimization recommendation review, direct resource-cost analysis,
  execution for existing findings, and tracking.
- CMP-wide Security compliance overview, violation browsing, fresh
  single-violation analysis, and an explicitly confirmed status-only Mark Fixed
  operation.

Provider skills are loaded from the SmartCMP provider package and qualified by
provider namespace. Their callable adapters invoke typed operations from
`smartcmp_provider`; they do not maintain a second SmartCMP API or
authentication implementation.

## Skill Map {#skill-map}

| Skill | Type | Main operations |
| --- | --- | --- |
| `datasource` | Read-only discovery | Service catalogs, business groups, templates, images, resource details. |
| `resource-pool` | Read-only directory | List and filter SmartCMP resource pools. |
| `resource` | Directory, analysis coordination, and day-2 | List resources or cloud hosts, inspect details, analyze one resource's Security posture and associated CMP violations, coordinate comprehensive read-only analysis, start or stop resources. |
| `request` | Provisioning and status | Build and submit SmartCMP service/resource requests; check submitted request status by Request ID. |
| `approval` | Workflow | List pending approval tasks, approve, reject. |
| `alarm` | Monitoring | List and analyze alerts, or analyze resource health from its component monitoring model. |
| `cost-optimization` | FinOps | List and analyze recommendations, directly analyze a resource, execute native fixes for existing findings, and track execution. |
| `security-compliance` | Security analysis and status handling | View CMP-wide Security posture, list Security violations, freshly analyze one violation, and explicitly mark its status FIXED without remediating the resource. |
| `preapproval-agent` | Agent workflow | Apply policy-based pre-review to approval workflows. |
| `request-decomposition-agent` | Agent workflow | Convert natural language needs into request drafts. |

## Context-Aware Page Matching {#context-aware-page-matching}

The SmartCMP Provider currently maps these normalized page patterns at runtime:

| SmartCMP page | Context object | Owning Skill |
| --- | --- | --- |
| Triggered alarm detail | Alarm alert | `smartcmp:alarm` |
| Cost recommendation detail | Cost optimization recommendation | `smartcmp:cost-optimization` |
| Security compliance records | Security violation collection | `smartcmp:security-compliance` |
| Pending approval detail | Approval request | `smartcmp:approval` |
| Service catalog request | Catalog | `smartcmp:request` |
| My Application request detail | Submitted request | `smartcmp:request` |
| Cloud resource detail | Resource | `smartcmp:resource` |
| Virtual-machine detail | Virtual machine | `smartcmp:resource` |

The floating assistant re-runs this match when SmartCMP reports a newer page
generation. The Provider resolver then loads the current object and builds
state-aware actions. Adding another path for an already supported object and
owning Skill requires a Provider route entry, not a Core or UI business
mapping.

## Read vs Write Capabilities {#read-vs-write-capabilities}

Read-only discovery skills are suitable for first tests after setup. Write or
side-effecting skills include request submission, approval/rejection, resource
start/stop, alert status operations, cost remediation execution, and marking a
Security violation FIXED. Mark Fixed is a separately confirmed status-only
operation: it does not modify or remediate the resource. Require clear user
intent before running write workflows.
