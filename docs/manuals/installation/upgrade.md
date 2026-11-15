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

## Upgrading to v1.0.1

The final `v1.0.1` tag points to `1838dec1f60edf5d5a9ca96f0262a6071730d57d`, including the Docker publishing fix.

```bash
docker pull registry.cn-shanghai.aliyuncs.com/atlasclaw/atlasclaw:v1.0.1
```

- Apply migration `011` for access tokens and `012` for chat attachments.
- Refresh dependencies and rebuild native packages or container images for the Python 3.14.10 configuration.
- Replace response-language mode values with a concrete locale, `null`, or omission. Include the shared response-language JSON prompt resource.
- Explicitly enable `capabilities.vision` on compatible models before using image analysis.
- Timestamp defaults in five migrations now use `CURRENT_TIMESTAMP`. Completed migrations do not rerun automatically, and tables left by failed migrations require inspection before retrying; they are not automatically removed.

After upgrading, verify login, plain-text chat, image upload and follow-up, token creation and revocation, and embedded context navigation as applicable. The release build passed Docker push and pull verification; this does not establish live MySQL 8.0.16 upgrade validation.

See the [complete v1.0.1 release notes](https://github.com/CloudChef/atlasclaw/releases/tag/v1.0.1).
