# TOPdesk Skill Suite

This repository contains a TOPdesk-focused Codex skill suite for service-management workflows, database schema design, OData/API mapping, Power BI reporting, AI/KI assistance, security, operations, migration, enablement, and business positioning.

## Contents

- `topdesk-expert`: broad cross-domain TOPdesk expert skill.
- Focused skills for Power BI, AI, OData, schema, workflows, security, testing, integration, operations, migration, enablement, handbooks, USPs, and more.
- Utility scripts for OData metadata parsing and CSV export profiling.
- Template assets for DAX, Power Query, SQL views, runbooks, and test cases.
- Plugin distribution under `plugins/topdesk-skill-suite`.
- Plugin-ready docs for installation, free-tool commercial positioning, demo dashboard storytelling, and security/privacy/AI guardrails.
- Root indexes:
  - `SKILL_INDEX.md`
  - `HANDBOOK_INDEX.md`
  - `FORWARD_TEST_PROMPTS.md`

## Validate

Run locally:

```powershell
powershell -ExecutionPolicy Bypass -File .\validate_all_skills.ps1
```

The validation script:

- validates all skill folders with `quick_validate.py`
- compiles Python scripts
- checks for open markers such as `TODO`, `FIXME`, `TBD`
- removes generated `__pycache__` folders

## Utility Commands

Create a release zip:

```powershell
powershell -ExecutionPolicy Bypass -File .\package_release.ps1
```

Prepare a forward-test run sheet:

```powershell
powershell -ExecutionPolicy Bypass -File .\new_forward_test_results.ps1
```

Build a tenant mapping report from artifacts:

```powershell
powershell -ExecutionPolicy Bypass -File .\new_tenant_mapping_report.ps1 -TenantName "Example" -MetadataXml ".\metadata.xml" -CsvExports ".\incidents.csv"
```

Generate skill manifest and inventory:

```powershell
powershell -ExecutionPolicy Bypass -File .\new_skill_manifest.ps1
powershell -ExecutionPolicy Bypass -File .\new_skill_inventory_report.ps1
powershell -ExecutionPolicy Bypass -File .\new_skill_index.ps1
```

Generate a Power BI implementation pack:

```powershell
python .\topdesk-powerbi\scripts\generate_powerbi_pack.py --tables .\tables.csv --measures .\measures.csv --out .\powerbi_pack
```

Build and verify the Codex plugin package:

```powershell
powershell -ExecutionPolicy Bypass -File .\plugins\topdesk-skill-suite\scripts\verify_plugin.ps1
```

Plugin handover docs:

- `plugins/topdesk-skill-suite/docs/INSTALLATION_AND_RELEASE.md`
- `plugins/topdesk-skill-suite/docs/COMMERCIAL_MODEL.md`
- `plugins/topdesk-skill-suite/docs/DEMO_DASHBOARD_STORYBOARD.md`
- `plugins/topdesk-skill-suite/docs/SECURITY_PRIVACY_AI.md`
- `plugins/topdesk-skill-suite/docs/ONE_PAGER.md`

The plugin, skills, scripts, templates, and demo assets are free open-source accelerator material. TOPdesk licenses, Power BI licenses, gateways, hosting, AI provider usage, implementation, customization, training, support, and managed operation are separate.

## Install Locally

Development location:

```text
C:\tmp\topdeskskill
```

For Codex auto-discovery, copy selected skill folders to:

```text
C:\Users\weiss\.codex\skills
```

Validate after copying.
