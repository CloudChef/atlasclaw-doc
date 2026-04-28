---
title: Install and Run
description: Install dependencies and start AtlasClaw Core.
sidebar_position: 3
---

# Install and Run

## Install Dependencies {#install-dependencies}

From the AtlasClaw Core repository:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

For frontend development:

```bash
cd app/frontend
npm install
npm run build
```

## Start the Service {#start-the-service}

Use the local foreground script when working in the combined repository:

```bash
atlasclaw-share/scripts/restart-atlasclaw-core-foreground.sh
```

Or start the FastAPI app directly:

```bash
uvicorn app.atlasclaw.main:app --reload --host 0.0.0.0 --port 8000
```

The web UI is served from the same backend. Open `http://127.0.0.1:8000/`.

## Default Local Admin {#default-local-admin}

When local authentication is enabled, AtlasClaw creates the configured default
admin account if it does not already exist. In the default local development
setup, the account is `admin` / `admin`.
