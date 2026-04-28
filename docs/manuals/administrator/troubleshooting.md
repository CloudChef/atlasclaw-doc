---
title: Troubleshooting
description: Diagnose common administrator problems.
sidebar_position: 7
---

# Troubleshooting

## Login Fails {#login-fails}

Check auth provider configuration, local login enablement, token cookie settings,
and the default admin account.

Use the following order:

1. Confirm the browser reaches the AtlasClaw backend.
2. Confirm the selected auth provider is enabled.
3. For local login, verify the user is active and the password is current.
4. For host-cookie or SSO, inspect the upstream token/cookie and claim mapping.
5. Check whether the user has at least one active role.

## Admin Page Is Hidden {#admin-page-is-hidden}

Admin navigation is permission-driven. Confirm the current user has permissions
for the relevant module, such as `users.view`, `roles.view`,
`model_configs.view`, or `channels.view`.

If a user has several roles, remember that boolean permissions merge with OR
semantics. If the page is still hidden, confirm the frontend session has been
refreshed after the role change.

## Provider Skill Is Not Available {#provider-skill-is-not-available}

Check `providers_root`, provider package layout, provider schema, skill metadata,
role skill permissions, and provider instance runtime permissions.

Troubleshoot in layers:

1. Provider package is discovered.
2. Provider instance exists and is active.
3. Role has access to the provider instance.
4. Role has the skill enabled.
5. User has required user-scoped credentials, if any.

## Channel Connection Does Not Start {#channel-connection-does-not-start}

Validate the channel config, check required fields for the selected mode, verify
network access to the IM platform, and review backend logs for handler errors.

For long-connection channels, also check whether the external app is authorized
for event delivery. For webhook mode, send a test message from the upstream IM
platform and confirm AtlasClaw receives the callback.

## Agent Gives Generic Answers {#agent-gives-generic-answers}

Generic answers usually mean the runtime did not expose the intended tool or
provider skill. Check selected model, skill permission, provider access, and the
agent's allowed skill/provider settings. If the model is working but no tool is
available, the issue is usually an authorization or registry problem.

## User Token Looks Saved but Requests Fail {#user-token-looks-saved-but-requests-fail}

Provider Token settings are stored per user and per provider instance. Confirm
the user saved the token against the same provider type and instance name used
by the skill. If the instance was renamed, users may need to save the token
again for the new instance name.
