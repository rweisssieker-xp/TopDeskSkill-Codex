# Documentation Coverage

## Complete Areas

- Plugin manifest, marketplace example, local install/uninstall, validation, packaging, package test, checksums, and CI workflow.
- Marketplace-specific scanner package with root `.codex-plugin/plugin.json`, valid author email, 48 skill entry points, core runtime/analyzer scripts, required docs, and file-count guard below 128 files.
- GitHub manifest URLs, privacy policy, terms of service, local MCP declaration, MCP smoke test, and release tag helper.
- Marketplace submission guide and production readiness gates.
- Demo TOPdesk base URL documented without storing browser session paths.
- Live demo REST/API test result documented without storing the application password.
- REST tenant profiler documented and tested against the demo instance with ignored local output artifacts.
- API test lab, DAX measure generator, SLA backlog optimizer, and PII/compliance scanner documented and tested against ignored demo profile artifacts.
- Skill inventory and generated manifest for bundled skills.
- Complete US-English feature matrix covering all 48 skills with capability, output, buyer persona, and sales angle.
- Primary `en-US` documentation plus European locale guidance in `docs/LOCALIZATION.md`.
- Localized marketplace summaries, prompt starters, and translation quality rules for common European locales.
- TOPdesk domain skills for workflows, admin, incidents, changes, assets, knowledge, security, operations, testing, migration, and enablement.
- Data and automation skills for OData/API, API smoke testing, tenant mapping, Python, PowerShell, query-to-Power-BI, and data quality.
- Power BI skills for report building, semantic modelling, visual design, report factory, DAX generation, Power Query, RLS, refresh, reconciliation, and KPI definitions.
- Operations and governance skills for SLA/backlog analysis, routing quality, PII scanning, data minimization, and compliance review.
- AI skills for feature design, prompts/evals, governance cockpit, feedback loops, RAG/search, cost/value monitoring, and Power BI AI reporting.
- USP and business skills for battlecards, proof-of-value, ROI, executive messaging, handbooks, and delivery planning.

## Verification

Use the plugin gates:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\validate_plugin.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\validate_marketplace_readiness.ps1 -CheckExternalUrls
python .\scripts\test_mcp_server.py
```

The gates verify the marketplace source:

- Root `.codex-plugin/plugin.json`
- 48 bundled skill entry points
- Marketplace docs and root asset references
- Local MCP helper handshake

## Production Gates

- Public URLs in `.codex-plugin/plugin.json` are validated for shape locally; verify live availability again before external marketplace submission.
- Local demonstration screenshots are acceptable for internal publication. Customer-facing screenshots must come from sanitized demo data or approved customer material.
- The suite provides reusable templates, scripts, a local MCP helper, connector preflight/export tooling, local runtime state, and a local status API. Customer-wide hosted operation is an infrastructure decision.
- `en-US` is the canonical source. European locales are supported through localization guidance and prompt starters, not through duplicated per-skill source files.
