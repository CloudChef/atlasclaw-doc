---
title: Provider Integration
description: Integrate external systems through AtlasClaw providers.
sidebar_position: 1
---

# Provider Integration

Provider Integration documents concrete provider packages. This section is the
right place for provider-specific auth modes, fields, workflows, and examples.

Core documentation explains how AtlasClaw loads providers and enforces shared
runtime rules. Provider documentation explains what a concrete integration does.

## Included Providers {#included-providers}

This documentation currently includes detailed guidance for SmartCMP Provider.
Other providers can be added here when their package contracts and workflows are
stable enough for end-user documentation.

## What Belongs Here {#what-belongs-here}

Provider Integration is the home for:

- provider-specific auth modes and required fields;
- provider instance examples;
- upstream workflow semantics;
- provider skill behavior and safety rules;
- provider troubleshooting steps;
- provider-owned UI labels, placeholders, and operational terminology.

Do not move those details into Core pages. Core pages should describe loading,
permission filtering, and credential scope without becoming responsible for one
provider's business model.

## Adding a Provider Page Set {#adding-a-provider-page-set}

When documenting a new provider, include at minimum:

1. Overview and source-of-truth package path.
2. Installation and loading instructions.
3. Auth modes and credential scopes.
4. Administrator setup.
5. User credential setup, when applicable.
6. Capability map.
7. Major workflow pages.
8. Troubleshooting.
