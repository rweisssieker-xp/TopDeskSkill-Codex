# Release Checklist

- Run `scripts/sync_skills.ps1`.
- Run `scripts/generate_plugin_assets.ps1`.
- Run `scripts/new_plugin_manifest.ps1`.
- Run `scripts/new_plugin_inventory.ps1`.
- Run `scripts/new_plugin_health_report.ps1`.
- Run `scripts/validate_plugin_config.ps1`.
- Run `scripts/validate_plugin.ps1`.
- Run `scripts/package_plugin.ps1`.
- Run `scripts/test_plugin_package.ps1`.
- Run `scripts/new_plugin_checksums.ps1`.
- Confirm `dist/topdesk-skill-suite-plugin-<version>.zip` exists.
- Confirm `dist/topdesk-skill-suite-plugin-<version>.sha256` exists.
- Review `.codex-plugin/plugin.json` version and user-facing descriptions.
- Review `PLUGIN_INVENTORY.md` for expected skill count and artifacts.
