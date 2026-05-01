# Documentation Coverage

## Complete Areas

- Plugin manifest, marketplace example, local install/uninstall, validation, packaging, package test, checksums, and CI workflow.
- Skill inventory and generated manifest for bundled skills.
- TOPdesk domain skills for workflows, admin, incidents, changes, assets, knowledge, security, operations, testing, migration, and enablement.
- Data and automation skills for OData/API, tenant mapping, Python, PowerShell, query-to-Power-BI, and data quality.
- Power BI skills for report building, semantic modelling, visual design, report factory, DAX, Power Query, RLS, refresh, reconciliation, and KPI definitions.
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

- Public URLs in `.codex-plugin/plugin.json` are intentionally empty until a repository, homepage, privacy policy, and terms URL exist.
- Screenshots are generated placeholder product visuals, not live Power BI screenshots.
- The suite provides reusable templates and scripts, not a live TOPdesk connector or hosted MCP server.
