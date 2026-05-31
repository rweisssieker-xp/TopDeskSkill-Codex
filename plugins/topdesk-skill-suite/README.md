# TOPdesk Skill Suite Plugin

Codex plugin bundling TOPdesk-focused skills for service management, OData/API mapping, Power BI reporting, AI/KI feature delivery, AI governance cockpits, proof-of-value sprints, migrations, security, operations, testing, enablement, and business positioning.

Primary documentation language: `en-US`.

European language support: see `docs/LOCALIZATION.md` for localized marketplace summaries, prompt starters, and response-language guidance across common European locales. The skill source files remain canonical in `en-US`; users can ask the plugin to answer in a supported locale such as `de-DE`, `fr-FR`, `es-ES`, `it-IT`, `nl-NL`, `pl-PL`, or another locale listed in the localization guide.

## Contents

- `skills/`: bundled `topdesk-*` skills.
- `.codex-plugin/plugin.json`: plugin manifest.
- `scripts/sync_skills.ps1`: refreshes bundled skills from the repository root.
- `scripts/new_plugin_manifest.ps1`: generates `plugin-skills.manifest.json`.
- `scripts/new_plugin_inventory.ps1`: generates `PLUGIN_INVENTORY.md`.
- `scripts/new_plugin_health_report.ps1`: generates `PLUGIN_HEALTH.md`.
- `scripts/generate_plugin_assets.ps1`: generates PNG icon, logo, and screenshot assets.
- `scripts/validate_plugin_config.ps1`: checks `plugin.config.json` against the manifest and bundle.
- `scripts/validate_plugin.ps1`: validates the plugin manifest and bundled skills.
- `scripts/package_plugin.ps1`: creates a distributable plugin zip.
- `scripts/test_plugin_package.ps1`: extracts and smoke-tests the generated zip.
- `scripts/new_plugin_checksums.ps1`: writes SHA256 checksums for release packages.
- `scripts/topdesk_mcp_server.py`: local dependency-free MCP server for TOPdesk/OData helper tools.
- `scripts/test_mcp_server.py`: smoke-tests the MCP server handshake and tool list.
- `scripts/prepare_git_release.ps1`: creates or confirms a local release tag and prints explicit push commands.
- `scripts/install_local_plugin.ps1`: installs the plugin into the local Codex plugin location.
- `scripts/uninstall_local_plugin.ps1`: removes the local plugin installation and marketplace entry.
- `scripts/set_plugin_version.ps1`: updates `.codex-plugin/plugin.json` version.
- `scripts/verify_plugin.ps1`: runs sync, inventory generation, validation, and packaging.
- `.mcp.json`: MCP server declaration for local TOPdesk helper tools.
- `marketplace.local.example.json`: example marketplace entry for local plugin testing.

## Useful Commands

Run from the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\plugins\topdesk-skill-suite\scripts\sync_skills.ps1
powershell -ExecutionPolicy Bypass -File .\plugins\topdesk-skill-suite\scripts\generate_plugin_assets.ps1
powershell -ExecutionPolicy Bypass -File .\plugins\topdesk-skill-suite\scripts\new_plugin_manifest.ps1
powershell -ExecutionPolicy Bypass -File .\plugins\topdesk-skill-suite\scripts\new_plugin_inventory.ps1
powershell -ExecutionPolicy Bypass -File .\plugins\topdesk-skill-suite\scripts\new_plugin_health_report.ps1
powershell -ExecutionPolicy Bypass -File .\plugins\topdesk-skill-suite\scripts\validate_plugin_config.ps1
powershell -ExecutionPolicy Bypass -File .\plugins\topdesk-skill-suite\scripts\validate_plugin.ps1
powershell -ExecutionPolicy Bypass -File .\plugins\topdesk-skill-suite\scripts\package_plugin.ps1
powershell -ExecutionPolicy Bypass -File .\plugins\topdesk-skill-suite\scripts\test_plugin_package.ps1
powershell -ExecutionPolicy Bypass -File .\plugins\topdesk-skill-suite\scripts\new_plugin_checksums.ps1
powershell -ExecutionPolicy Bypass -File .\plugins\topdesk-skill-suite\scripts\verify_plugin.ps1
```

## Example Prompts

Primary `en-US` prompts:

- Plan a TOPdesk migration.
- Create a TOPdesk Power BI reporting pack.
- Review TOPdesk OData and API mapping.
- Create a governed TOPdesk AI feature pack with Power BI monitoring.
- Design a TOPdesk AI governance cockpit in Power BI.
- Build a proof-of-value sprint pack for TOPdesk AI and reporting.
- Create USP battlecards for TOPdesk Power BI and AI.

Localized examples:

- `de-DE`: Plane eine TOPdesk Migration.
- `fr-FR`: Planifie une migration TOPdesk.
- `es-ES`: Planifica una migracion TOPdesk.
- `it-IT`: Pianifica una migrazione TOPdesk.
- `nl-NL`: Plan een TOPdesk-migratie.
- `pl-PL`: Zaplanuj migracje TOPdesk.

## Skill Coverage

The plugin currently bundles 39 skills covering:

- TOPdesk domain, admin configuration, workflows, changes, assets, knowledge, major incidents, operations, testing, and security.
- OData/API discovery, API smoke testing, tenant mapping, data quality, Python, PowerShell, and query-to-Power-BI workflows.
- Power BI reporting, semantic modelling, report factory generation, visual design, DAX measure generation, Power Query, RLS, refresh, and reconciliation.
- AI/KI features, AI feature factory packs, AI governance cockpits, prompt/eval patterns, RAG/search, feedback loops, and Power BI AI monitoring.
- SLA/backlog optimization, routing quality checks, PII/compliance scanning, and live demo readiness analysis.
- USPs, battlecards, proof-of-value sprints, ROI, business cases, delivery planning, handbooks, and enablement.

## Local Install

The install script copies this plugin to `%USERPROFILE%\plugins\topdesk-skill-suite` and updates `%USERPROFILE%\.agents\plugins\marketplace.json`.

```powershell
powershell -ExecutionPolicy Bypass -File .\plugins\topdesk-skill-suite\scripts\install_local_plugin.ps1
```

## Demo Tenant

The plugin does not ship tenant credentials. Configure demo or customer TOPdesk access only through local environment variables:

Observed unauthenticated behavior:

- `/tas/api/incidents`, `/tas/api/persons`, `/tas/api/operatorgroups`, and `/tas/api/branches` return `401`, so the REST API surface is present but requires authentication.
- `/services/reporting/v2/odata/$metadata` returns `401`, so the reporting OData surface is present but requires authentication.
- `/tas/api/odata/$metadata` returns `404` on this demo tenant; use the reporting OData path for Power BI/OData discovery.

Observed authenticated behavior with `TOPDESK_USERNAME` plus `TOPDESK_APP_PASSWORD`:

- REST endpoints such as `/tas/api/incidents`, `/tas/api/persons`, `/tas/api/operatorgroups`, and `/tas/api/branches` are readable.
- Reporting OData `$metadata` returns `403`, so this credential does not have reporting OData permission.
- See `docs/LIVE_DEMO_TEST_RESULTS.md`.

REST profiling:

```powershell
$env:TOPDESK_BASE_URL = "https://your-tenant.topdesk.net"
$env:TOPDESK_USERNAME = "<username>"
$env:TOPDESK_APP_PASSWORD = "<application-password>"
python .\topdesk-tenant-mapping\scripts\profile_topdesk_rest.py --out .\tenant-output\tenant-rest --max-records 100 --page-size 50
```

Follow-on analysis from generated tenant artifacts:

```powershell
python .\topdesk-powerbi-dax\scripts\new_dax_measure_pack.py --field-catalog .\tenant-output\tenant-rest\rest_field_catalog.csv --out-dir .\tenant-output\tenant-rest\dax-pack
python .\topdesk-sla-optimizer\scripts\analyze_sla_backlog.py --incidents .\tenant-output\tenant-rest\snapshots\incidents.json --out-dir .\tenant-output\tenant-rest\sla-analysis
python .\topdesk-compliance-pii\scripts\scan_pii_catalog.py --field-catalog .\tenant-output\tenant-rest\rest_field_catalog.csv --out-dir .\tenant-output\tenant-rest\pii-review
```
