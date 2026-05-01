# TOPdesk Skill Suite Plugin

Codex plugin bundling TOPdesk-focused skills for service management, OData/API mapping, Power BI reporting, AI/KI feature delivery, AI governance cockpits, proof-of-value sprints, migrations, security, operations, testing, enablement, and business positioning.

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

- Plane eine TOPdesk Migration.
- Erstelle ein TOPdesk Power BI Reporting Pack.
- Pruefe TOPdesk OData und API Mapping.
- Erstelle ein governed TOPdesk AI Feature Pack mit Power BI Monitoring.
- Designe ein TOPdesk AI Governance Cockpit in Power BI.
- Baue ein Proof-of-Value Sprint Pack fuer TOPdesk AI und Reporting.
- Erstelle USP Battlecards fuer TOPdesk Power BI und AI/KI.

## Skill Coverage

The plugin currently bundles 35 skills covering:

- TOPdesk domain, admin configuration, workflows, changes, assets, knowledge, major incidents, operations, testing, and security.
- OData/API discovery, tenant mapping, data quality, Python, PowerShell, and query-to-Power-BI workflows.
- Power BI reporting, semantic modelling, report factory generation, visual design, DAX, Power Query, RLS, refresh, and reconciliation.
- AI/KI features, AI feature factory packs, AI governance cockpits, prompt/eval patterns, RAG/search, feedback loops, and Power BI AI monitoring.
- USPs, battlecards, proof-of-value sprints, ROI, business cases, delivery planning, handbooks, and enablement.

## Local Install

The install script copies this plugin to `%USERPROFILE%\plugins\topdesk-skill-suite` and updates `%USERPROFILE%\.agents\plugins\marketplace.json`.

```powershell
powershell -ExecutionPolicy Bypass -File .\plugins\topdesk-skill-suite\scripts\install_local_plugin.ps1
```
