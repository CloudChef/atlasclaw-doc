---
title: Account Settings
description: Manage profile, avatar, and password settings.
sidebar_position: 3
---

# Account Settings

Use Account Settings to manage your workspace profile.

## Profile {#profile}

You can update display name and email when the deployment allows profile edits.
Your display name is used in the AtlasClaw UI and administrative views.

If your account comes from SSO or a host system, some fields may be read-only or
synced from the upstream identity provider. In that case, update the source
identity system instead of trying to override it in AtlasClaw.

## Avatar {#avatar}

Upload an avatar image through the account page. AtlasClaw stores user assets
under the workspace public user-content area.

Use a workplace-appropriate image and avoid uploading sensitive screenshots or
documents as an avatar. If the avatar does not refresh immediately, reload the
browser after saving.

## Password {#password}

Local-auth users can change their password from Account Settings. SSO or
host-cookie users may need to change credentials in the upstream identity
system.

## Security Notes {#security-notes}

- Do not enter provider API tokens in profile fields.
- Do not share IM channel secrets through chat.
- Report unexpected role or provider access to an administrator.
- Log out from shared machines after using AtlasClaw.

## Administrator Access Tokens

Administrators can create, list, and revoke their AtlasClaw access tokens from Account Settings. Copy a newly created token immediately: its plaintext is displayed only once, and the server stores only a digest. These tokens authenticate API clients to AtlasClaw; they are separate from credentials for external providers.

Send the token as `Authorization: Bearer <token>`. Requests use the owner's current permissions. Revocation, owner deactivation, and role changes affect subsequent requests immediately. Token-authenticated requests cannot create, list, or revoke access tokens.

To rotate a token, create a replacement through an administrator session, update and verify the client, then revoke the old token. Never paste access tokens into chat.
