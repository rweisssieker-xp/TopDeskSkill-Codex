# Documentation Coverage

## Complete Areas

- Plugin manifest, marketplace example, local install/uninstall, validation, packaging, package test, checksums, and CI workflow.
- GitHub manifest URLs, privacy policy, terms of service, local MCP declaration, MCP smoke test, and release tag helper.
- Demo TOPdesk base URL documented without storing browser session paths.
- Live demo REST/API test result documented without storing the application password.
- REST tenant profiler documented and tested against the demo instance with ignored local output artifacts.
- API test lab, DAX measure generator, SLA backlog optimizer, and PII/compliance scanner documented and tested against ignored demo profile artifacts.
- Skill inventory and generated manifest for bundled skills.
- Primary `en-US` documentation plus European locale guidance in `docs/LOCALIZATION.md`.
- Localized marketplace summaries, prompt starters, and translation quality rules for common European locales.
- TOPdesk domain skills for workflows, admin, incidents, changes, assets, knowledge, security, operations, testing, migration, and enablement.
- Data and automation skills for OData/API, API smoke testing, tenant mapping, Python, PowerShell, query-to-Power-BI, and data quality.
- Power BI skills for report building, semantic modelling, visual design, report factory, DAX generation, Power Query, RLS, refresh, reconciliation, and KPI definitions.
- Operations and governance skills for SLA/backlog analysis, routing quality, PII scanning, data minimization, and compliance review.
- AI/KI skills for feature design, prompts/evals, governance cockpit, feedback loops, RAG/search, cost/value monitoring, and Power BI AI reporting.
- USP and business skills for battlecards, proof-of-value, ROI, executive messaging, handbooks, and delivery planning.

## Verification

Use the plugin gate:

```powershell
powershell -ExecutionPolicy Bypass -File .\plugins\topdesk-skill-suite\scripts\verify_plugin.ps1
```

The gate regenerates the plugin docs and package evidence:

- `plugin-skills.manifest.json`
- `PLUGIN_INVENTORY.md`
- `PLUGIN_HEALTH.md`
- `dist/topdesk-skill-suite-plugin-<version>.zip`
- `dist/topdesk-skill-suite-plugin-<version>.sha256`

## Known Non-Blocking Gaps

- Public URLs in `.codex-plugin/plugin.json` point to the configured repository paths; verify them again before publishing outside the local/demo workflow.
- Screenshots are generated placeholder product visuals, not live Power BI screenshots.
- The suite provides reusable templates and scripts, not a live TOPdesk connector or hosted MCP server.
- `en-US` is the canonical source. European locales are supported through localization guidance and prompt starters, not through duplicated per-skill source files.
