---
title: SmartCMP Provider
description: SmartCMP Provider overview and source boundary.
sidebar_position: 1
---

# SmartCMP Provider

SmartCMP Provider connects AtlasClaw to SmartCMP cloud management workflows.
It supports resource requests, submitted request status lookup, approvals,
directory queries, dynamic resource analysis and operations, alarm and resource
health analysis, cost optimization, resource-first Security analysis, and
Security compliance violation workflows. Context-bound editor assistants can
also read selected SmartCMP definitions and generate complete replacement
content for manual review and copy.

The source of truth is the provider package:

```text
atlasclaw-providers/providers/SmartCMP-Provider/
├── README.md
├── PROVIDER.md
├── provider.schema.json
├── pyproject.toml
├── assistant_context/
├── src/
│   └── smartcmp_provider/
└── skills/
```

This documentation summarizes stable setup and user workflows. Implementation
details remain in the provider repository.

`src/smartcmp_provider/` is the reusable SmartCMP Provider implementation. It
owns authentication resolution, typed models, API transport, domain operations,
and shared services. `skills/` contains thin AtlasClaw adapters that translate
`RunContext` and Tool results around those Provider operations. The standalone
SmartCMP MCP adapter imports the same Provider package, but it is a separate
entry scenario and is not involved when AtlasClaw loads SmartCMP Skills.

When SmartCMP is configured as the HostApp Provider, AtlasClaw exposes
independent menu and floating UIs that share the same SmartCMP Cookie
authentication. The menu provides full Chat, while the floating UI dynamically
follows supported SmartCMP pages. SmartCMP Provider route definitions bind the
current page to an approval, request, alarm, cost recommendation, Security
violation collection, resource object, work order, or supported editor object
and expose actions appropriate to that object's current state. See
[Embedded Menu and Floating UI](../embedded-menu-and-floating-ui.md).

## Audience {#audience}

- AtlasClaw administrators configuring SmartCMP provider instances.
- Standard Users who need SmartCMP user-token setup guidance.
- Provider maintainers validating documentation against provider skills.
- Operators troubleshooting SmartCMP authentication or skill execution.

## Capability Areas {#capability-areas}

| Area | Typical user intent |
| --- | --- |
| Request | Submit a service catalog or resource provisioning request, or check a submitted request by Request ID. |
| Approval | List pending approval tasks and approve or reject with a reason. |
| Datasource | Discover services, business groups, templates, images, and resource facts. |
| Resource pool | List and filter available SmartCMP resource pools. |
| Resource | Browse resources, analyze one resource's Security posture and associated CMP violations, coordinate comprehensive analysis, and perform permitted day-2 operations. |
| Alarm and health | Analyze alerts or determine a resource's runtime health from its component monitoring evidence. |
| Cost optimization | Review recommendations or directly analyze one resource, execute native fixes for existing findings, and track remediation. |
| Security compliance | View CMP-wide Security posture, analyze one violation, and explicitly mark only its status FIXED after manual remediation and confirmation. |
| Editor assistance | Read supported form, script, optimization-policy, and blueprint-component definitions and generate complete replacement content for manual copy. |

SmartCMP permissions still come from SmartCMP. AtlasClaw role access only
decides whether a user can invoke the provider skill from AtlasClaw.
