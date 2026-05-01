# PowerShell Patterns

## Baseline Script Shape

- Start with `[CmdletBinding(SupportsShouldProcess = $true)]` when the script can change files, local state, or remote systems.
- Set `$ErrorActionPreference = "Stop"` and `Set-StrictMode -Version Latest`.
- Use typed parameters and `ValidateNotNullOrEmpty`, `ValidateSet`, or `ValidateScript` where possible.
- Return objects instead of formatted text when downstream automation may consume results.
- Keep formatting (`Format-Table`, colors) at the command boundary, not inside reusable functions.

## File Safety

- Use `Resolve-Path` and compare absolute paths before recursive delete, move, or overwrite.
- Use `-LiteralPath` for resolved paths.
- Never build destructive commands as strings.
- For generated outputs, write to a staging path first, then replace the target only after validation.

## Error Handling

- Throw for invariant violations and unrecoverable states.
- Wrap remote calls with contextual errors that include endpoint/resource names but not secrets.
- Use `try/catch` around network and file boundary operations.
- Keep `Write-Verbose` useful: inputs, counts, output paths, timing, but no credentials or PII-heavy payload dumps.

## HTTP/API

- Use `Invoke-RestMethod` for JSON APIs and `Invoke-WebRequest` when raw response details matter.
- Build query strings with `[System.Web.HttpUtility]::ParseQueryString("")` or `[uriBuilder]` instead of string concatenation for complex filters.
- Add retry only for transient failures: 429, 408, and selected 5xx.
- Respect pagination and rate limits.

## Testing

- Validate syntax with PowerShell parser before execution.
- For pure functions, add Pester tests if the repo uses Pester.
- For scripts without Pester, add a `-WhatIf` or `-DryRun` smoke path and test it.

