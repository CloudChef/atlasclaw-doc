---
title: Skills and Tools
description: Runtime skills, built-in tools, and permission filtering.
sidebar_position: 5
---

# Skills and Tools

Skills describe agent capabilities. Tools execute concrete operations.

## Built-In Tool Areas {#built-in-tool-areas}

AtlasClaw Core includes tools for sessions, memory, web search and fetch,
provider instance selection, runtime execution, filesystem access, and browser
automation when enabled.

## Markdown Skills {#markdown-skills}

Markdown skills can be loaded from workspace, user, external, or provider
locations. Provider-bound skills are qualified with the provider namespace to
avoid collisions.

A skill describes when it should be used, what inputs it expects, what scripts
or tools it may call, and what safety rules apply. Provider skills should keep
provider-specific terminology inside the provider package.

### Tool Parameters and Safety Metadata {#tool-parameters-and-safety-metadata}

A Markdown Tool may declare an ordinary JSON object schema with no properties
and an empty `required` list. Zero-argument Tools do not need a synthetic CLI
argument:

```yaml
tool_health_parameters: |
  {
    "type": "object",
    "properties": {},
    "required": [],
    "additionalProperties": false
  }
```

Two per-Tool metadata flags control read-only continuation behavior:

| Metadata | Contract |
| --- | --- |
| `tool_<id>_read_only: true` | The Tool explicitly guarantees that it does not mutate persisted or external state. |
| `tool_<id>_auto_select_single_option: true` | A sole visible candidate from this read-only Tool may continue the active workflow without another user turn. |

Both flags default to `false`. `auto_select_single_option` does not apply to
mutation or confirmation Tools, and it does not permit automatic choice when
several visible candidates remain. Core only continues when it can identify
one candidate collection and one candidate with a stable identity and display
label. Candidate identity comes from `id`, `key`, or `code`; its visible label
comes from `name`, `label`, `title`, `displayName`, or `display_name`.

### Workflow Continuation Metadata {#workflow-continuation-metadata}

A Tool result may include an `_internal` value for hidden workflow state such
as the current request trace, selected Provider instance, or exact IDs needed
by the next step. Core accepts `_internal` as either a structured value or a
serialized JSON value. It removes the field from user-facing history and does
not treat it as final response content.

Continuation metadata is reusable only for the active request trace and the
selected Provider instance. Keep it bounded and include only next-step identity
or validation evidence; do not duplicate a public list result inside
`_internal`. Oversized entries are dropped from the prompt context and logged
as `workflow_context_metadata_budget_exceeded`, with a reason such as
`single_entry_oversized` or `aggregate_limit`.

## Permission Filtering {#permission-filtering}

Role skill permissions and provider instance permissions filter which skills
and tools are exposed to the runtime. Provider-bound tools are governed by
provider permissions instead of being treated as ordinary core tools.

Filtering happens before the agent chooses tools. A missing tool is therefore a
configuration or authorization signal, not a prompt-engineering problem.

After a Skill is selected, Core preserves that Skill's complete authorized Tool
scope. A page Context may supply the default object and owning Skill, but it
does not remove other authorized Skills or Tools from the ordinary Chat turn.

## Operational Rule {#operational-rule}

If a skill is missing or disabled, the agent should explain the access blocker
instead of inventing capabilities.

## Skill Lifecycle {#skill-lifecycle}

1. The skill is discovered from a configured skill directory or provider
   package.
2. The registry validates the skill name and metadata.
3. The role policy decides whether the skill is visible and enabled.
4. The provider policy decides whether provider-bound skills have an allowed
   provider instance.
5. The agent runtime receives only the allowed skill/tool set.
6. Tool execution records output that the agent can use as evidence.

## Write-Action Safety {#write-action-safety}

Skills that submit requests, approve work, change resource state, or operate
alerts must be treated as write actions. A well-authored skill should ask for
missing information, confirm intent when appropriate, and report upstream errors
without fabricating success.
