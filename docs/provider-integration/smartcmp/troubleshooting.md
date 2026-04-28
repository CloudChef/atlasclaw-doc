---
title: Troubleshooting
description: Diagnose SmartCMP provider setup and runtime issues.
sidebar_position: 13
---

# Troubleshooting

## Provider Not Listed {#provider-not-listed}

Check `providers_root`, package directory name, `PROVIDER.md`, and
`provider.schema.json`.

Also confirm the AtlasClaw process has filesystem access to the provider root
and was restarted after the provider package was added.

## User Token Missing {#user-token-missing}

Ask the user to configure a SmartCMP token in Account Settings. Confirm the
provider instance uses `auth_type: "user_token"`.

## Shared Token Fails {#shared-token-fails}

Verify `CMP_PROVIDER_TOKEN`, base URL, token expiry, and SmartCMP-side
permissions.

## Cookie or Credential Mode Fails {#cookie-or-credential-mode-fails}

Check `CMP_URL`, `auth_url`, cookie expiry, username/password validity, network
access, and whether the deployment uses a non-standard SmartCMP login endpoint.

## Skill Appears but Cannot Execute {#skill-appears-but-cannot-execute}

Check role provider permissions, provider instance access, user credentials, and
SmartCMP-side RBAC.

## Wrong Auth URL {#wrong-auth-url}

SmartCMP SaaS auth URL inference is exact-match based. For private deployments
or non-standard login endpoints, configure `auth_url` explicitly instead of
relying on host inference.

## Resource Operation Fails {#resource-operation-fails}

Confirm the resource ID, resource type, current state, and SmartCMP-side
permission. Start/stop operations may be invalid for some resource types or
states.

## Approval Operation Fails {#approval-operation-fails}

Confirm the approval item is still pending and that the user's SmartCMP
credentials have approval authority. AtlasClaw role access only exposes the
skill; it does not create SmartCMP approval rights.

## What to Capture {#what-to-capture}

For support, capture:

- provider type and instance name;
- auth mode, without secrets;
- user role and provider access;
- skill name and operation;
- upstream error message;
- whether a read-only SmartCMP query succeeds.
