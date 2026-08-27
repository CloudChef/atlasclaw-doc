---
title: Editor Assistance
description: Generate complete replacement content for supported SmartCMP editors without writing upstream state.
sidebar_position: 7
---

# Editor Assistance

SmartCMP Provider includes context-bound, read-only Skills for selected editor
pages. Each Skill reads the exact saved object with the current user's SmartCMP
credential, applies the user's requested change, and returns complete
replacement content for manual review and copy.

These Skills do not save, publish, execute, enable, or deploy anything in
SmartCMP.

## Supported Editors {#supported-editors}

| SmartCMP page | Owning Skill | Generated replacement |
| --- | --- | --- |
| `/main/service-model/forms/edit/{form_id}` | `smartcmp:form-designer` | Complete normalized form schema. |
| `/main/service-model/forms/design/{form_id}` | `smartcmp:form-designer` | Complete normalized form schema. |
| `/main/model-design/scripts/edit/{script_id}` | `smartcmp:script-designer` | Complete replacement for the script `content` field. |
| `/main/measurement-billing/cost-optimization/optimization-policy/edit/{policy_id}` | `smartcmp:optimization-policy-designer` | Complete `ruleContent` and the fields changed by the request. |
| `/main/model-design/blueprint-components/edit/{component_id}` | `smartcmp:component-script-designer` | Complete content for one exact file under `scripts/`. |

The form designer can also work from an exact SmartCMP form editor URL in an
ordinary conversation. The other Skills rely on a resolved editor-page Context
to bind the target safely.

## Workflow {#workflow}

1. Open a supported editor page in the SmartCMP floating-assistant surface, or
   provide a supported exact form URL.
2. AtlasClaw resolves the saved object and binds it to the owning Skill.
3. Describe the desired change.
4. The Skill returns a complete replacement rather than an abbreviated patch
   or an ellipsis.
5. Review the result, copy it, and apply it manually in SmartCMP.

The generated response may include supporting explanation, but the replacement
block itself preserves the complete content needed for copying.

## Editor-Specific Boundaries {#editor-specific-boundaries}

- Form assistance returns a normalized complete schema and never writes the
  form definition.
- Script assistance replaces only `content`; other script metadata is context
  for compatibility and is not rewritten implicitly.
- Optimization-policy assistance applies only to cost-optimization policies.
  It does not enable the policy or execute remediation.
- Blueprint-component assistance targets exactly one file below `scripts/`.
  If several files are possible, the user must identify the exact path. It does
  not update or deploy the component.

Generated content remains subject to human review, SmartCMP validation, and the
user's normal SmartCMP save or publish permissions.
