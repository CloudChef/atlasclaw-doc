---
title: Provider Tokens
description: Configure personal provider tokens.
sidebar_position: 4
---

# Provider Tokens

Provider tokens are user-owned credentials for provider instances that require
per-user authentication.

## When to Configure a Token {#when-to-configure-a-token}

Configure a provider token when:

- the provider instance uses user token authentication;
- you use a provider from an IM channel and that provider must access the
  upstream system as your own user;
- the agent says your user token is missing, invalid, rejected, or expired;
- your administrator tells you a provider requires user-owned credentials.

IM channel conversations go through `IM tool -> IM channel -> Agent ->
Provider`. The IM message does not carry your browser cookie or SSO token for
the target provider system, so per-user provider access from IM requires a
saved Provider Token.

## Provider-Specific Instructions {#provider-specific-instructions}

Each provider defines its own token type, validation rules, and rotation
process. Follow the provider-specific guide under Provider Integration when a
provider requires extra fields or setup steps.

Channel credentials are separate. IM channel settings belong under Channels, not
Provider Tokens.

## Token Workflow {#token-workflow}

1. Ask your administrator which provider instance requires a user token.
2. Obtain the token from the upstream provider system.
3. Open Account Settings and find Provider Tokens.
4. Select the provider type and instance name.
5. Paste the token and save.
6. Retry the chat request that previously failed.

Provider tokens are scoped to the provider type and instance name. If your
administrator creates a new provider instance, you may need to save a token for
that new instance even if the upstream token value is the same.

## Rotation {#rotation}

Rotate a provider token when:

- the upstream provider expires it;
- your organization rotates credentials on a schedule;
- you suspect the token was exposed;
- the provider request starts failing with an authentication error.

After rotation, retry a read-only provider action first. That confirms the new
token is accepted before you run a write workflow.
