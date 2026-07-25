# atlasclaw-doc

Core-first documentation site for AtlasClaw.

This repository uses Docusaurus and keeps English as the source language. Chinese
translations live under `i18n/zh-CN/`.

## Embedded Mode Documentation

The documentation covers both independent Embedded Mode access points and their
shared integration contract:

- [Embedded Mode](docs/provider-integration/embedded-mode.md) explains
  Enterprise System Cookie identity and the configured HostApp Provider.
- [Embedded Menu and Floating
  UI](docs/provider-integration/embedded-menu-and-floating-ui.md) explains menu
  access, floating page lifecycle messages, dynamic Context matching, Domain
  Skills, and state-aware object actions.

English and Chinese pages use localized architecture diagrams. SmartCMP remains
the concrete Provider reference, while Core behavior stays provider-agnostic.

## Local Development

```bash
npm install
npm run start
```

## Build

```bash
npm run build
```

## Export

Create a customer-facing static documentation package:

```bash
npm run export
```

The export command builds the Docusaurus site, checks English/Chinese document
path alignment, scans source docs for local paths or obvious secret material,
and writes `dist/atlasclaw-doc-YYYYMMDD-HHMMSS.zip`.

After extracting the package, do not open `build/index.html` directly. Run
`start.sh`, `start.command`, or `start.bat`, then open the local HTTP URL shown
by the script.

To include static PDFs in the exported package:

```bash
npm run export:pdf
```

PDF export requires Python 3 and either Python Playwright or a local
Chrome/Chromium/Edge executable.

This adds:

```text
pdf/atlasclaw-doc-en.pdf
pdf/atlasclaw-doc-zh-CN.pdf
```

## Content Boundary

- Core documentation covers AtlasClaw runtime, configuration, users, roles,
  sessions, agents, channels, skills, tools, and shared provider-loading
  contracts.
- Provider Integration documentation may cover concrete provider setup and
  workflows. SmartCMP content is sourced from the sibling
  `atlasclaw-providers/providers/SmartCMP-Provider` package.
