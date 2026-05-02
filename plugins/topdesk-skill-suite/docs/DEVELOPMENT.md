# Plugin Development

## Workflow

Use the plugin verification script as the default local gate:

```powershell
powershell -ExecutionPolicy Bypass -File .\plugins\topdesk-skill-suite\scripts\verify_plugin.ps1
```

The gate performs:

- sync root `topdesk-*` skills into the plugin bundle
- regenerate PNG plugin assets
- regenerate plugin skill manifest and inventory
- regenerate health report
- validate bundled skills
- package the plugin zip
- test the generated zip by extracting and validating it
- write SHA256 checksums

## Versioning

Update the plugin manifest version with:

```powershell
powershell -ExecutionPolicy Bypass -File .\plugins\topdesk-skill-suite\scripts\set_plugin_version.ps1 -Version 0.2.0
```

Then run `verify_plugin.ps1` and review `CHANGELOG.md`.

## Local Install

```powershell
powershell -ExecutionPolicy Bypass -File .\plugins\topdesk-skill-suite\scripts\install_local_plugin.ps1
```

This copies the plugin to `%USERPROFILE%\plugins\topdesk-skill-suite` and updates `%USERPROFILE%\.agents\plugins\marketplace.json`.

## Demo TOPdesk Tenant

Use the base URL only:

```text
https://usatopdesktrial2.topdesk.net
```

Do not store browser session paths such as `/tas/secure/mango/window/...` or timestamp query parameters as API configuration.

For reporting/OData discovery, use:

```text
https://usatopdesktrial2.topdesk.net/services/reporting/v2/odata/$metadata
```

Unauthenticated requests return `401`, which confirms that authentication is required before live metadata or records can be read.

Configured non-secret demo username:

```text
raulm09
```

Set `TOPDESK_APP_PASSWORD` or `TOPDESK_API_TOKEN` only in your local environment. Do not commit passwords or tokens.
