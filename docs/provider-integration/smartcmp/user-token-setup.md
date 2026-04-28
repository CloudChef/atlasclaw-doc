---
title: User Token Setup
description: Configure a personal SmartCMP token.
sidebar_position: 5
---

# User Token Setup

If the SmartCMP instance uses `user_token` auth, each user must configure a
personal token in AtlasClaw.

## Steps {#steps}

1. Obtain a SmartCMP API token from SmartCMP.
2. Open AtlasClaw Account Settings.
3. Find Provider Tokens.
4. Select the SmartCMP provider instance.
5. Paste the token.
6. Save and retry the SmartCMP request.

## Token Errors {#token-errors}

If the agent reports that `user_token` is missing, invalid, rejected, or
expired, update the SmartCMP token in Account Settings. If the error asks you to
contact an administrator, the provider instance itself may be unavailable or not
authorized for your role.

## What the Token Controls {#what-the-token-controls}

The token is used only for the SmartCMP provider instance where you saved it.
It does not configure IM channels and does not grant AtlasClaw administrator
permissions. SmartCMP still decides which requests, approvals, resources, or
alarms your token can access.

## Rotation Checklist {#rotation-checklist}

1. Generate or obtain a new SmartCMP token.
2. Replace the saved token in AtlasClaw Provider Tokens.
3. Test a read-only SmartCMP action.
4. Retry the original workflow.
5. Revoke the old token in SmartCMP if your organization requires manual
   revocation.
