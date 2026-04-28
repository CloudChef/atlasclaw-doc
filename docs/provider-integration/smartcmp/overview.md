---
title: SmartCMP Provider
description: SmartCMP Provider overview and source boundary.
sidebar_position: 1
---

# SmartCMP Provider

SmartCMP Provider connects AtlasClaw to SmartCMP cloud management workflows.
It supports resource requests, approvals, directory queries, resource
operations, alarm handling, cost optimization, and resource compliance analysis.

The source of truth is the provider package:

```text
atlasclaw-providers/providers/SmartCMP-Provider/
├── README.md
├── PROVIDER.md
├── provider.schema.json
└── skills/
```

This documentation summarizes stable setup and user workflows. Implementation
details remain in the provider repository.

## Audience {#audience}

- AtlasClaw administrators configuring SmartCMP provider instances.
- Standard Users who need SmartCMP user-token setup guidance.
- Provider maintainers validating documentation against provider skills.
- Operators troubleshooting SmartCMP authentication or skill execution.

## Capability Areas {#capability-areas}

| Area | Typical user intent |
| --- | --- |
| Request | Submit a service catalog or resource provisioning request. |
| Approval | List pending approvals and approve or reject with a reason. |
| Datasource | Discover services, business groups, templates, images, and resource facts. |
| Resource pool | List and filter available SmartCMP resource pools. |
| Resource | Browse resources, inspect cloud hosts, and perform start/stop operations. |
| Alarm | List, analyze, mute, resolve, or reopen alerts when explicitly requested. |
| Cost optimization | Review recommendations, execute native fixes, and track remediation. |
| Resource compliance | Analyze resource lifecycle, patch, security, and configuration posture. |

SmartCMP permissions still come from SmartCMP. AtlasClaw role access only
decides whether a user can invoke the provider skill from AtlasClaw.
