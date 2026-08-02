---
title: Embedded Menu and Floating UI
description: Deploy two independent AtlasClaw surfaces with shared enterprise-system Cookie authentication.
sidebar_position: 5
---

# Embedded Menu and Floating UI

AtlasClaw Embedded mode provides two independent UI surfaces that can be
deployed together: a full menu UI and a compact floating UI. They are separate
entry points, not expanded and collapsed states of one component.

Both surfaces receive the same enterprise-system Cookie authentication
context. AtlasClaw `host_cookie` authentication resolves the same signed-in
user, and the HostApp Provider's Cookie auth mode uses the current request
Cookie to access the existing system with that user's upstream permissions.

## Surfaces {#surfaces}

| Surface | UI and lifecycle | Page Context |
| --- | --- | --- |
| Menu | Independent full AtlasClaw conversation opened from the enterprise-system menu with `surface=menu`. | Does not receive `PAGE_CHANGED` or attach page Context. |
| Floating | Independent compact assistant displayed over the enterprise system with `surface=floating`. | Re-resolves Context for every newer page generation. |

Both surfaces use the normal AtlasClaw Chat, Session, Skill, Tool, Provider,
and RBAC runtime. They can coexist and share the active Chat Session selected
through AtlasClaw-origin bootstrap state, while retaining separate layouts and
Context behavior. The embedding page never receives or forwards the AtlasClaw
`session_key`.

## AtlasClaw Understands the Current Page and Available Actions {#architecture}

Configured through `embed_integration`, the HostApp Provider maps enterprise
system pages to business objects, Domain Skills, and state-aware actions. It is
an AtlasClaw Provider package, not a service the enterprise system must add to
its own architecture.

![AtlasClaw menu, floating UI, runtime, Provider, and existing enterprise-system services](/img/embedded/hostapp-provider-architecture-en.svg)

The two UI surfaces reach the same Agent runtime, but they provide different
inputs. Menu access opens the full Agent without page Context. Floating UI adds
the current `path` and `generation`. AtlasClaw then uses the configured HostApp
Provider to match the page, resolve an object through existing APIs, and load
the owning Domain Skill's state-aware actions.

The HostApp Provider returns the same generic `object_actions` contract used by
normal Chat Tool results. Core owns that contract's schema, normalization,
safe builders, extraction, and delivery to the UI. The Provider supplies only
business-specific availability, labels, prompts, inputs, and URLs. It does not
maintain a separate floating-UI action catalog. This keeps page assistance and
ordinary Agent conversations aligned as Domain Skills evolve.

## Enterprise System Capabilities {#host-app-capabilities}

The menu integration is intentionally minimal. The enterprise system only
needs to add an entry in its menu and embed the AtlasClaw Agent:

```text
/atlasclaw/?embedded=1&surface=menu
```

Dynamic floating Context requires an additional embedding integration because
AtlasClaw must know when the visible enterprise-system page changes:

```text
/atlasclaw/?embedded=1&surface=floating&host_origin=<exact-origin>&nonce=<random-nonce>
```

The two surfaces have the following enterprise-system requirements:

| Enterprise system capability | Menu | Floating |
| --- | --- | --- |
| Embed the AtlasClaw surface | Required | Required |
| Make the enterprise-system Cookie available to AtlasClaw requests | Required | Required |
| Provide a launcher and manage the compact iframe lifecycle | Not required | Required |
| Create the floating URL with the exact Host Origin and a fresh, high-entropy nonce | Not required | Required |
| Validate the exact message Origin, source window, nonce, protocol, event type, and payload | Not required | Required |
| Report normalized router paths with monotonically increasing generations through `PAGE_CHANGED` | Not required | Required |
| Handle floating lifecycle events such as ready and close | Not required | Required |
| Resolve the page object, select a Provider or Skill, or render confirmation UI | Not allowed | Not allowed |

The enterprise system should remove the launcher and iframe when the
floating-assistant feature is disabled. It may also hide the launcher while
the full menu Agent is open to avoid presenting two entry controls for the
same assistant.

For `PAGE_CHANGED`, send only the shared protocol fields, nonce, generation,
and normalized absolute path. Do not include query strings, fragments, page
contents, selected text, business DTOs, Provider identifiers, or AtlasClaw
Session identifiers. Enterprise-system code must not call Embed REST, Agent
Run, or Tool APIs on behalf of the iframe.

AtlasClaw owns bootstrap, Context snapshots, Chat submission, the generic
Object Action contract and builders, action rendering, confirmation, Tool
execution, and permission checks. The HostApp Provider owns path semantics,
object reads, Domain Skills, and the business rules and copy that determine
which actions are currently available. This keeps the embedding integration
generic even as the Provider's routes and workflows grow.

## Menu Flow {#menu-flow}

1. The enterprise system opens AtlasClaw with `embedded=1&surface=menu`.
2. Embed bootstrap validates the menu surface and any AtlasClaw-origin
   candidate active Chat Session.
3. AtlasClaw renders the full embedded conversation UI.
4. The menu uses ordinary Chat capability selection and does not attach an
   enterprise-system page object to turns.

## Floating Context Flow {#floating-context-flow}

1. The enterprise system sends `PAGE_CHANGED` with a monotonically increasing
   generation and a normalized absolute path.
2. AtlasClaw selects the single HostApp Provider configured by
   `embed_integration`; the embedding message cannot override it.
3. Core matches the path against that Provider's
   `assistant_context/routes.json`.
4. The Provider resolver reads the current object with the request-scoped user
   credential and returns a bounded object projection plus its current
   `object_actions`.
5. Core binds the snapshot to the user, floating surface, generation, Provider
   instance, matched existing Skill, and a bounded lifetime.
6. The floating UI renders the object and actions. A prompt action enters the
   ordinary Chat path with the immutable Context reference.
7. When that Chat turn is submitted, Core verifies the Context owner,
   generation, latest-page marker, lifetime, and Session scope before copying
   the object and default Skill into the turn.
8. Core separately resolves current authorization for the ordinary Chat Tool
   inventory. The turn is not restricted to the page Skill's Tools, and Core
   does not revalidate the page before every later Provider Tool I/O in the
   same turn.

An older asynchronous response cannot restore stale object details or actions
after the enterprise system has reported a newer page.

Floating page matching is dynamic at runtime but deterministic. AtlasClaw does
not send page contents to an LLM to guess the active workflow. It matches the
path against the configured HostApp Provider's route manifest and asks that
Provider to resolve the object.

## Resolution Status {#resolution-status}

| Status | Meaning | UI and execution behavior |
| --- | --- | --- |
| `resolved` | The route, object, and owning Skill were resolved. | Show the current object and its dynamic actions. |
| `unsupported` | No Provider route matches the current path. | Keep ordinary Chat available without page Context. |
| `unavailable` | A route matched, but its object or Skill binding could not be safely resolved. | Keep the page scope closed and do not fall back to unrelated capabilities. |

Permission failures are returned separately. Resolving an object never grants a
Skill, Tool, or upstream permission that the user did not already have.

## Configuration {#configuration}

Enable one HostApp Provider and instance:

```json
{
  "embed_integration": {
    "provider_type": "example_provider",
    "provider_instance": "default"
  }
}
```

AtlasClaw derives the shared Chat Session scope for both surfaces from that
HostApp Provider and loads `assistant_context/routes.json` for floating page
matching. Enterprise-system code cannot choose another Provider or instance.
Omitting `embed_integration` preserves the legacy embedded behavior without
the configured menu/floating integration.

Authentication is configured separately. For an enterprise system that already
authenticates the user, pair this feature with AtlasClaw `host_cookie`
authentication and the Provider's request-cookie authentication mode. See
[Embedded Mode](./embedded-mode.md).

## HostApp Provider Route Contract {#provider-route-contract}

A HostApp Provider that supports page Context uses this optional layout:

```text
providers/example-provider/
├── assistant_context/
│   ├── routes.json
│   └── resolve.py
└── skills/
    └── item/
        └── SKILL.md
```

Example route manifest:

```json
{
  "schema_version": 1,
  "provider_type": "example_provider",
  "context_resolver": {
    "entrypoint": "assistant_context/resolve.py:resolve_context"
  },
  "routes": [
    {
      "id": "item-detail",
      "priority": 300,
      "match": {
        "path_template": "/main/items/{item_id}"
      },
      "result": {
        "page_type": "item-detail",
        "object_type": "item",
        "skill_ref": "example_provider:item"
      }
    }
  ]
}
```

Templates support static path segments and single-segment placeholders.
Matching order uses explicit priority, template specificity, and manifest
order. Query strings, fragments, Origins, page titles, selected text, and
business DTOs are not match inputs.

The entrypoint must explicitly name an async callable with the
`file.py:callable` form. Core loads and validates it in process when the Embed
Integration is initialized; Context resolution does not start a resolver
subprocess.

The HostApp Provider-level resolver returns:

- a minimal object with the route-declared type and a non-empty ID;
- approved display fields and bounded attributes;
- `object_actions` derived from the current object state with Core's generic
  action builders.

The matching `skill_ref` is declared by the route and cannot be replaced by
resolver output. Object actions may open a safe enterprise-system URL or
submit a Provider-authored prompt. They do not declare an exact Tool
invocation. Core defines and validates the generic action shape; the Provider
decides whether each business action is available and supplies its wording and
arguments.

## SmartCMP Reference Implementation {#smartcmp-reference}

SmartCMP demonstrates the complete HostApp Provider pattern as an existing
enterprise system with AtlasClaw embedded. SmartCMP keeps its APIs, Cookie
session, RBAC, workflows, and audit. The SmartCMP Provider is installed with
AtlasClaw and supplies the page-to-object mapping, unified object resolver,
Domain Skills, and SmartCMP-specific action availability and copy through
Core's generic action builders.

| SmartCMP page | Resolved object and Skill | State-aware actions |
| --- | --- | --- |
| `/main/virtual-machines/{resource_id}/details` | `virtual_machine` → `smartcmp:resource` | Open, Analyze, Operations |
| `/main/alarm-activity-management/alarm-triggered/edit/{alert_id}` | `alarm_alert` → `smartcmp:alarm` | Analyze plus Mute, Resolve, or Reopen according to alarm state |
| `/main/new-application/pendingApproval/{approval_type}/{approval_id}` | `approval_request` → `smartcmp:approval` | Analyze, Approve, Reject with confirmation and required inputs |

![SmartCMP VM page with floating Context and resource actions](/img/embedded/context-vm-floating.png)

On the VM page, SmartCMP publishes only the normalized route. The SmartCMP
Provider resolves the current resource through the existing API and reuses the
resource Domain Skill action builder to expose Open, Analyze, and Operations.

![SmartCMP alert page with analysis and alarm actions](/img/embedded/context-alert-analysis.png)

On an alert page, the same pattern resolves the alert and offers actions valid
for its current status. A mutation action enters the normal Agent run and still
passes through confirmation, Provider permission checks, and SmartCMP's
downstream authorization.

## Dynamic Extension Rules {#dynamic-extension-rules}

- Add a route entry when a new path represents an object type and owning Skill
  the HostApp Provider already supports.
- Extend the HostApp Provider read adapter when a new object type requires
  another existing enterprise-system API.
- Add state-aware business rules and copy to the owning Domain Skill, using
  Core's generic action builders and the same Provider helper used by normal
  Chat Tool results.
- Do not add Provider page paths, field mappings, action labels, or business
  rules to AtlasClaw Core or the generic floating UI.

This boundary lets a Provider add pages and workflows without changing the
shared embedded protocol or Core UI.

## Security and Deployment Boundaries {#security-and-deployment-boundaries}

- Validate the exact message Origin, source window, protocol, nonce, event type,
  and payload schema.
- Never use `targetOrigin="*"`.
- Generate a new high-entropy nonce for each floating iframe instance, and
  accept messages only from that iframe's `contentWindow`.
- Never place Cookies, tokens, credentials, query strings, fragments, or raw
  business payloads in embedding messages, manifests, browser storage, or
  Context snapshots.
- Keep object visibility checks in the Provider and use the current user's
  upstream credential.
- Context snapshots are process-local and do not survive restart. Use one
  AtlasClaw process or sticky routing that keeps bootstrap, Context resolution,
  and the page-scoped Agent turn on the same process.
