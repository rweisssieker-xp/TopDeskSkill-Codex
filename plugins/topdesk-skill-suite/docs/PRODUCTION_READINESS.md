# Production Readiness Gates

This plugin is ready as a local/open-source accelerator when `scripts/verify_plugin.ps1` passes.
Production use with customer TOPdesk data needs these gates to be completed for the specific tenant.

## Gate 1: Tenant Access

- Use a named TOPdesk API user or application credential with the minimum required read/write scope.
- Store `TOPDESK_BASE_URL`, `TOPDESK_USERNAME`, and `TOPDESK_APP_PASSWORD` in local environment variables, the DPAPI secret store, or a customer-managed vault.
- Confirm REST and OData permission boundaries before enabling Power BI refreshes, automation, or AI workflows.

## Gate 2: Real Data Mapping

- Export or profile the tenant metadata and representative records.
- Generate a field catalog and validate category, status, priority, branch, operator group, person, asset, incident, change, and knowledge mappings.
- Treat bundled sample field names and demo lifecycle files as examples until tenant evidence confirms them.

## Gate 3: Reporting Evidence

- Reconcile incident, backlog, SLA, reassignment, branch, and operator-group counts against TOPdesk UI selections or controlled exports.
- Capture customer-approved screenshots only from anonymized or approved demo data.
- Keep generated plugin screenshots for marketplace/demo shape when no customer-approved visuals are available.

## Gate 4: Privacy And AI

- Run the PII catalog scanner before exporting field catalogs, screenshots, report pages, prompts, or logs.
- Review prompt inputs, retrieval sources, generated summaries, and feedback storage with the customer privacy owner.
- Do not send ticket text, caller data, operator notes, attachments, or knowledge articles to an AI provider unless the customer has approved the processing path.

## Gate 5: Operations

- Define the owner for refresh failures, API errors, automation retries, and AI disable switches.
- Document rollback and disable procedures for every action sequence, scheduler job, MCP helper, or integration script.
- Confirm monitoring, retention, backup, and audit expectations before production scheduling.
- Use `topdesk-service-intelligence-runtime` to produce `operational-gates.csv`, `runtime-history.jsonl`, and `runtime-readout.md` before moving from local exports to repeated operation.

## Gate 5a: Runtime And Connector

- Run connector preflight before any live export.
- Keep live export endpoints explicit and approved; do not use broad endpoint crawling by default.
- Keep runtime configs free of secrets. Use environment variables, the DPAPI secret store, or a customer-managed vault.
- Treat `runtime-dashboard.html` as local evidence unless it has been sanitized for publication.
- Decide whether the customer wants local execution, the implemented Windows Scheduled Task mode, the local status API, or customer-wide enterprise operation with organization monitoring and support.

## Gate 6: Commercial Boundary

- State that the plugin license fee is zero.
- Separate TOPdesk licenses, Power BI licenses, gateways, hosting, AI provider usage, implementation, customization, training, support, and managed operation.
- Keep customer-specific statements out of the open-source repository unless approved for publication.
