---
name: topdesk-powershell
description: Advanced PowerShell automation for TOPdesk delivery and operations. Use for writing, reviewing, hardening, testing, or packaging PowerShell scripts that work with TOPdesk APIs, OData exports, CSV/JSON artifacts, tenant mapping, Power BI refresh operations, migration batches, runbooks, Windows scheduled tasks, CI scripts, validation gates, and safe local automation.
---

# TOPdesk PowerShell

Use this skill for production-grade PowerShell in TOPdesk projects.

## Workflow

1. Define the operational boundary: local file processing, TOPdesk API/OData, Power BI, install task, migration, or CI.
2. Prefer advanced functions with `[CmdletBinding()]`, explicit parameters, `Set-StrictMode -Version Latest`, and `$ErrorActionPreference = "Stop"`.
3. Keep secrets out of source. Accept tokens through environment variables, SecretManagement, or parameters that are never logged.
4. Use `-LiteralPath` for concrete file paths and validate destructive targets before deletion or replacement.
5. Emit objects for pipelines; use `Write-Verbose` for progress and `Write-Error`/exceptions for failures.
6. Add validation and a dry-run path for changes that touch remote systems or many files.
7. Run `scripts/Test-TopdeskPowerShellScript.ps1` against generated scripts when practical.

## References

Load only what is needed:

- `references/powershell-patterns.md` for script architecture, error handling, logging, file safety, API calls, and packaging.
- `references/topdesk-powershell-recipes.md` for TOPdesk-specific API/OData, migration, validation, and Power BI recipes.

## Assets

Use `assets/topdesk-script-template.ps1` as the starting point for new scripts.

