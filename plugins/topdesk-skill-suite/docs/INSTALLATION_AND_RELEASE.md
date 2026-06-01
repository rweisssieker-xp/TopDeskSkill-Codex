# Installation And Release Guide

This guide is the short operational path for installing, verifying, and handing over the TOPdesk Skill Suite plugin.

## What Is Free

The plugin, bundled skills, scripts, templates, demo assets, and local MCP helper are free open-source accelerator assets under the repository license.

The plugin does not include or pay for:

- TOPdesk tenant licenses or API permissions.
- Microsoft Power BI Desktop, Service, capacity, gateway, or workspace licenses.
- Cloud, database, gateway, or scheduler hosting.
- Customer-specific setup, modelling, implementation, training, support, or managed operation.
- Third-party AI model usage or enterprise AI platform costs.

## Local Install

Run from the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\plugins\topdesk-skill-suite\scripts\install_local_plugin.ps1
```

The script copies the plugin to the local Codex plugin location and updates the local marketplace entry.

## Verify Before Release

Run the full plugin gate:

```powershell
powershell -ExecutionPolicy Bypass -File .\plugins\topdesk-skill-suite\scripts\verify_plugin.ps1
```

Expected result:

- Skills are synchronized into the plugin bundle.
- PNG assets are generated.
- Plugin manifest, inventory, and health report are regenerated.
- Plugin config validation succeeds.
- Marketplace readiness validation succeeds.
- MCP server smoke test passes.
- All bundled skills validate.
- Python scripts compile.
- Plugin zip is created in `dist/`.
- Package extraction test passes.
- SHA256 checksum is written.

## Release Artifact

The release artifact is:

```text
dist/topdesk-skill-suite-plugin-0.1.3.zip
```

The matching checksum file is:

```text
dist/topdesk-skill-suite-plugin-0.1.3.sha256
```

## Customer Handover Checklist

- Confirm whether the customer wants demo-data, tenant-read-only, or production-integrated use.
- Confirm available TOPdesk API/OData permissions.
- Confirm Power BI Desktop, Service, gateway, and workspace ownership.
- Confirm whether AI/KI outputs may use customer ticket text.
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
