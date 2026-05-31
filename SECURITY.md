# Security Policy

## Sensitive Data

Do not commit:

- TOPdesk credentials
- API tokens or app passwords
- Power BI gateway credentials
- customer exports containing personal data
- ticket text with PII or internal notes
- production tenant URLs when confidential

## Reporting Issues

For security issues, do not open a public issue with secrets or customer data. Share a minimal description and affected files through the approved private channel for the project.

## AI/KI Safety

AI-related skills must preserve:

- human review for customer-visible communication
- PII minimization
- permission-aware retrieval
- auditability of model/prompt versions and suggestions
- rollback/disable paths for automated behavior

## Reporting And Snapshot Safety

- Use read-only TOPdesk credentials for profiling and reporting where possible.
- Keep daily snapshots and lifecycle history in approved storage with retention rules.
- Reconcile Power BI incident counts against TOPdesk source screens or trusted exports.
- Flag unknown dimensions and missing source keys instead of dropping records silently.
- Apply row-level security when dashboards include ticket text, caller data, branch data, customer data, or operator notes.

## Free Tool Boundary

The plugin and skill assets are free open-source accelerator material. This does not include TOPdesk access, Power BI licensing, gateways, hosting, AI provider usage, implementation services, support, or managed operation.
