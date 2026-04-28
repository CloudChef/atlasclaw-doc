---
title: Model Configs
description: Configure model providers and model tokens.
sidebar_position: 3
---

# Model Configs

Model configuration controls which LLM endpoints AtlasClaw can use at runtime.

## What Administrators Configure {#what-administrators-configure}

- Provider name, model ID, and display name.
- Base URL and API type.
- API key or token.
- Context window, max tokens, temperature, priority, and weight.
- Active or inactive state.

## Operational Notes {#operational-notes}

Store API keys securely. The API response masks stored keys. Rotate keys through
the model configuration workflow instead of editing database records directly.

When multiple model tokens are configured, AtlasClaw can load them into the
runtime token pool and use priority and weight to choose active entries.

## Recommended Rollout {#recommended-rollout}

1. Create one model configuration and mark it active.
2. Run a simple chat request before enabling provider skills.
3. Add fallback or weighted token entries only after the primary model path is
   stable.
4. Document which model is approved for production and which models are for
   testing.

## Fields to Review {#fields-to-review}

| Field | Why it matters |
| --- | --- |
| Provider/API type | Determines which model client and request format the runtime uses. |
| Base URL | Must match the model gateway or vendor endpoint reachable from AtlasClaw. |
| Model ID | Must be a model name accepted by the target provider. |
| Context window | Controls how much session history and tool evidence can fit. |
| Max tokens | Caps the generated response length and cost exposure. |
| Temperature | Controls output variability; use lower values for operational workflows. |
| Priority/weight | Controls selection when more than one token/model entry is active. |

## Failure Modes {#failure-modes}

- `401` or `403`: API key, token, or model entitlement is wrong.
- `404`: model ID or base URL does not match the provider.
- Timeout: AtlasClaw cannot reach the model endpoint or the model is overloaded.
- Repeated truncation: context window or max-token settings are too small for
  the workflow.

When testing provider skills, keep model errors separate from provider errors.
First confirm a plain conversation works, then test tool use.
