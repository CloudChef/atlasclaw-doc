---
title: Requirements
description: Runtime and operational requirements for AtlasClaw Core.
sidebar_position: 2
---

# Requirements

## Runtime {#runtime}

- Python 3.11 or newer.
- A virtual environment for Python dependencies.
- Network access to the configured model provider.
- A writable workspace directory for sessions, memory, users, runtime state, and
  generated user assets.

## Optional Components {#optional-components}

- A database backend when using database-backed users, roles, model configs,
  provider configs, and channel configs.
- A sibling `atlasclaw-providers` checkout when loading external provider
  packages.
- IM platform credentials when users configure DingTalk, Feishu/Lark, or WeCom
  channel connections.

## Security Requirements {#security-requirements}

Keep secrets outside committed files. Use environment variables for model API
keys, provider tokens, cookies, and service credentials.
