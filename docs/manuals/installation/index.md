---
title: Installation Guide
description: Install and start AtlasClaw Core.
sidebar_position: 1
---

# Installation Guide

This guide installs AtlasClaw Core and prepares the runtime for local or managed
deployment.

AtlasClaw Core contains the API layer, auth middleware, agent runtime, sessions,
memory, channels, model configuration, role permissions, and provider loading.
Concrete provider packages are installed separately and referenced through
`providers_root`.

## Installation Flow {#installation-flow}

1. Confirm runtime requirements.
2. Install Python and frontend dependencies.
3. Create `atlasclaw.json`.
4. Configure model access and authentication.
5. Start the service.
6. Add provider packages when provider integration is required.

For SmartCMP-specific setup, use the SmartCMP section under Provider
Integration.
