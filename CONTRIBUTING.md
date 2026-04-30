# Contributing

## Scope

Contributions should improve TOPdesk skill behavior, references, scripts, templates, or validation.

## Rules

- Keep skills focused and concise.
- Put detailed material in `references/`, reusable files in `assets/`, and deterministic automation in `scripts/`.
- Do not add secrets, tenant credentials, or private customer data.
- Do not claim exact TOPdesk tenant fields without metadata, API samples, exports, or documented evidence.
- Run validation before submitting changes.

## Validation

```powershell
powershell -ExecutionPolicy Bypass -File .\validate_all_skills.ps1
```

## Pull Requests

Include:

- changed skills/files
- reason for change
- validation output
- any tenant-specific assumptions or placeholders
