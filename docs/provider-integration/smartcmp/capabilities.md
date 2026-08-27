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
- Context-bound assistance for form definitions, scripts, cost-optimization
  policies, and blueprint-component scripts. These Skills generate complete
  replacement content but do not save, publish, execute, or deploy it.

Provider skills are loaded from the SmartCMP provider package and qualified by
provider namespace. Their callable adapters invoke typed operations from
`smartcmp_provider`; they do not maintain a second SmartCMP API or
authentication implementation.

## Skill Map {#skill-map}

| Skill | Type | Main operations |
| --- | --- | --- |
| `datasource` | Read-only discovery | Service catalogs, business groups, templates, images, resource details. |
| `resource-pool` | Read-only directory | List and filter SmartCMP resource pools. |
| `resource` | Directory, analysis coordination, and day-2 | List resources or cloud hosts, inspect details, analyze one resource's Security posture and associated CMP violations, coordinate comprehensive read-only analysis, and run supported resource actions. |
| `request` | Provisioning and status | Build and submit SmartCMP service/resource requests; check submitted request status by Request ID. |
| `approval` | Workflow | List pending approval tasks, approve, reject. |
| `alarm` | Monitoring | List and analyze alerts, or analyze resource health from its component monitoring model. |
| `cost-optimization` | FinOps | List and analyze recommendations, directly analyze a resource, execute native fixes for existing findings, and track execution. |
| `security-compliance` | Security analysis and status handling | View CMP-wide Security posture, list Security violations, freshly analyze one violation, and explicitly mark its status FIXED without remediating the resource. |
| `preapproval-agent` | Agent workflow | Apply policy-based pre-review to approval workflows. |
| `request-decomposition-agent` | Agent workflow | Convert natural language needs into request drafts. |
| `form-designer` | Read-only editor assistance | Read a saved form definition and generate a complete normalized replacement schema. |
| `script-designer` | Read-only editor assistance | Read a saved script and generate complete replacement content for its `content` field. |
| `optimization-policy-designer` | Read-only editor assistance | Read a cost-optimization policy and generate replacement `ruleContent` and changed fields. |
| `component-script-designer` | Read-only editor assistance | Read one exact blueprint-component script file and generate complete replacement content. |

## Context-Aware Page Matching {#context-aware-page-matching}

The SmartCMP Provider currently maps these normalized page patterns at runtime:

| SmartCMP page | Context object | Owning Skill |
| --- | --- | --- |
| Triggered alarm detail | Alarm alert | `smartcmp:alarm` |
| Cost recommendation detail | Cost optimization recommendation | `smartcmp:cost-optimization` |
| Security compliance records | Security violation collection | `smartcmp:security-compliance` |
| Security policy editor | Security policy | `smartcmp:security-compliance` |
| Pending approval detail | Approval request | `smartcmp:approval` |
| Work-order approval detail | Approval request | `smartcmp:approval` |
| Service catalog request | Catalog | `smartcmp:request` |
| Work-order request | Catalog | `smartcmp:request` |
| My Application request detail | Submitted request | `smartcmp:request` |
| Work-order application detail | Submitted request | `smartcmp:request` |
| Cloud resource detail | Resource | `smartcmp:resource` |
| Virtual-machine detail | Virtual machine | `smartcmp:resource` |
| Form edit or design | Form definition | `smartcmp:form-designer` |
| Script edit | Script definition | `smartcmp:script-designer` |
| Cost-optimization policy edit | Optimization policy | `smartcmp:optimization-policy-designer` |
| Blueprint-component edit | Blueprint component | `smartcmp:component-script-designer` |

The floating assistant re-runs this match when SmartCMP reports a newer page
generation. The Provider resolver then loads the current object and builds
state-aware actions. Adding another path for an already supported object and
owning Skill requires a Provider route entry, not a Core or UI business
mapping.

On a work-order approval page, only an exact pending task exposes Analyze,
Approve, and Reject. Completed or inconsistent records remain read-only. A
Security policy editor route also supplies read-only Context; it does not add a
policy mutation action.

## Bounded Lists {#bounded-lists}

SmartCMP list Tools return bounded pages instead of copying an unlimited
upstream collection into one Agent turn. Most Tool schemas accept at most 50
rows per page. Recycle-bin browsing accepts at most 20 deployments because one
deployment can expand into several resource rows. Use a supported `query` or
filter to narrow a large collection, and advance `page` when `has_more` or the
coverage metadata shows that more data remains.

## Read vs Write Capabilities {#read-vs-write-capabilities}

Read-only discovery skills are suitable for first tests after setup. Write or
side-effecting skills include request submission, approval/rejection, supported
resource state changes, alert status operations, cost remediation execution, and marking a
Security violation FIXED. Mark Fixed is a separately confirmed status-only
operation: it does not modify or remediate the resource. Require clear user
intent before running write workflows. Editor assistance is read-only even
though its response may contain a complete replacement document or script.
