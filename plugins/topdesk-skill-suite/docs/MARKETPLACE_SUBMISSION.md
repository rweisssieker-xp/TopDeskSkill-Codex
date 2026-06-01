# Marketplace Submission Guide

Use this guide before publishing the TOPdesk Skill Suite outside a local/demo workflow.

## Required Checks

- Run `scripts/verify_plugin.ps1` from the repository root.
- Run `scripts/validate_marketplace_readiness.ps1 -CheckExternalUrls` before external publication.
- Confirm `.codex-plugin/plugin.json` version, display name, category, descriptions, license, repository, homepage, privacy policy, and terms URLs.
- Confirm `docs/PRIVACY_POLICY.md` and `docs/TERMS_OF_SERVICE.md` match the intended distribution model.
- Confirm `docs/PRODUCTION_READINESS.md` is included in release handover material.
- Confirm `docs/SERVICE_INTELLIGENCE_RUNTIME.md` is included when positioning the suite as an operating model accelerator.
- Confirm all screenshots under `assets/` are intentional for the target marketplace.
- Confirm demo visuals are labelled as demo/product-shape visuals when not captured from a live tenant.

## Marketplace Copy

Short description:

```text
Free open-source TOPdesk implementation, reporting, operations, and enablement skills.
```

Long description:

```text
A free open-source TOPdesk skill suite for service-management workflows, OData/API mapping, Power BI reporting, AI assistance, security, operations, migration, enablement, business cases, and delivery templates.
```

Expanded positioning:

```text
A Service Intelligence Operating System accelerator for TOPdesk: turn tenant evidence into decision-ready findings, lifecycle analytics, drift detection, AI adoption controls, automation safety reviews, readiness scorecards, runtime gates, local scheduling, SQLite run state, monitoring status, improvement backlogs, and executive narratives. The plugin ships free inspectable skills, scripts, templates, runtime orchestration, and demo assets; tenant access, implementation, hosting, Power BI, TOPdesk, and AI provider costs remain separate.
```

Primary prompts:

- Plan a TOPdesk migration.
- Create a TOPdesk Power BI reporting pack.
- Review TOPdesk OData and API mapping.
- Create a governed TOPdesk AI feature pack with Power BI monitoring.
- Build a proof-of-value sprint pack for TOPdesk AI and reporting.
- Build a TOPdesk tenant drift radar report.
- Create a process debt review from lifecycle and SLA evidence.
- Design an AI adoption ledger for TOPdesk operator suggestions.
- Review a TOPdesk action sequence with an automation safety sandbox.
- Create an executive decision readout from TOPdesk findings.
- Run a TOPdesk service intelligence operating cycle from approved exports.

Localized prompt examples:

- `de-DE`: Plane eine TOPdesk Migration.
- `fr-FR`: Planifie une migration TOPdesk.
- `es-ES`: Planifica una migracion TOPdesk.
- `it-IT`: Pianifica una migrazione TOPdesk.
- `nl-NL`: Plan een TOPdesk-migratie.
- `pl-PL`: Zaplanuj migracje TOPdesk.

## Screenshot Policy

The repository can ship demo screenshots for local/demo publication.
For customer-facing marketplace listings, prefer screenshots from:

- The offline demo lifecycle data pack.
- A sanitized TOPdesk demo tenant.
- A sanitized Power BI report generated from demo data.

Do not publish screenshots containing customer ticket text, caller data, operator notes, attachments, identifiers, or private configuration values.

## Submission Evidence

Attach or retain:

- `dist/topdesk-skill-suite-plugin-<version>.zip`
- `dist/topdesk-skill-suite-plugin-<version>.sha256`
- `PLUGIN_HEALTH.md`
- `PLUGIN_INVENTORY.md`
- `plugin-skills.manifest.json`
- A completed release checklist.
