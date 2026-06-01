# Installation And Release Guide

This guide is the short operational path for installing, verifying, and handing over the TOPdesk Skill Suite plugin.

## What Is Free

The plugin, bundled skills, scripts, templates, demo assets, and local MCP helper are free open-source accelerator assets under the repository license.

The plugin does not include or pay for:

- TOPdesk tenant licenses or API permissions.
- Microsoft Power BI Desktop, Service, capacity, gateway, or workspace licenses.
- Cloud hosting, gateway operation, central database operation, or enterprise monitoring.
- Customer-specific setup, modelling, implementation, training, support, or managed operation.
- Third-party AI model usage or enterprise AI platform costs.

## Local Install

Install from the marketplace submission source or clone the repository root. The marketplace branch layout is the plugin root: `.codex-plugin/plugin.json`, `.mcp.json`, `skills/`, `scripts/`, `docs/`, and `assets/`.

## Verify Before Release

Run the full plugin gate:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\validate_plugin.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\validate_marketplace_readiness.ps1 -CheckExternalUrls
python .\scripts\test_mcp_server.py
```

Expected result:

- The plugin manifest is present at the repository root.
- Text-based SVG marketplace assets are present.
- Marketplace readiness validation succeeds.
- MCP server smoke test passes.
- All bundled skills validate.

## Release Artifact

The release artifact is the `main` branch root:

```text
https://github.com/rweisssieker-xp/TopDeskSkill-Codex
```

## Marketplace Artifact

The public marketplace artifact is the scanner-friendly repository root on `main`:

```text
.codex-plugin/plugin.json
```

The matching checksum file is:

```text
dist/topdesk-skill-suite-marketplace-0.1.3.sha256
```

Use the marketplace package for Codex Marketplace submission. It keeps `.codex-plugin/plugin.json` at the artifact root and stays below the marketplace file-count limit while preserving all 48 skill entry points and the core runtime/analyzer scripts.

## Customer Handover Checklist

- Confirm whether the customer wants demo-data, tenant-read-only, or production-integrated use.
- Confirm available TOPdesk API/OData permissions.
- Confirm Power BI Desktop, Service, gateway, and workspace ownership.
- Confirm whether AI outputs may use customer ticket text.
- Confirm PII handling, retention, and export storage location.
- Run the demo lifecycle pack before connecting real tenant data.
- Run tenant profiling with a read-only credential where possible.
- Document environment variables and never store credentials in source files.

## Minimum Production Gate

Before using customer data in production reporting or automation, also follow `docs/PRODUCTION_READINESS.md`.

- Validate tenant-specific field mappings.
- Validate lifecycle snapshot completeness.
- Reconcile incident counts against TOPdesk source screens or exports.
- Review AI prompts and model outputs with business owners.
- Review PII fields and access boundaries.
- Confirm rollback or disable procedure for every automated workflow.
