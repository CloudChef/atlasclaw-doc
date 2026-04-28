---
title: Upgrade and Backup
description: Upgrade AtlasClaw safely and preserve workspace data.
sidebar_position: 5
---

# Upgrade and Backup

## Before Upgrading {#before-upgrading}

Back up:

- `atlasclaw.json`
- the workspace directory
- database contents
- provider repositories
- environment variable definitions managed by deployment tooling

## Upgrade Steps {#upgrade-steps}

1. Stop the service.
2. Pull the target AtlasClaw Core version.
3. Reinstall dependencies if requirements changed.
4. Run database migrations when using a database backend.
5. Start the service.
6. Verify login, chat, sessions, model configuration, provider instances, and
   channel connections.

## Provider Compatibility {#provider-compatibility}

Upgrade provider packages separately. Recheck provider schemas and skill
metadata after provider updates, especially for provider auth modes and
capability changes.
