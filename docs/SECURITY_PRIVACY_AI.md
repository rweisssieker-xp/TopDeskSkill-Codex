# Security, Privacy, And AI Guardrails

The plugin is local accelerator software. It does not collect, transmit, or store data by itself. Risk comes from the data and services users connect to it.

## Data Handling Principles

- Keep TOPdesk credentials in environment variables or approved secret stores.
- Do not commit tenant exports, ticket text, caller data, operator notes, assets, or credentials.
- Prefer read-only TOPdesk credentials for profiling and reporting.
- Store customer exports in approved project locations with retention rules.
- Minimize PII before sending data to AI systems.
- Keep source-to-report reconciliation evidence for executive dashboards.

## AI Principles

- Use AI suggestions as decision support unless a production control explicitly approves automation.
- Keep human review for customer-visible responses, classification changes, routing changes, and knowledge publication.
- Log prompt version, model/provider, input scope, output, reviewer decision, and timestamp where practical.
- Evaluate AI on representative tickets before rollout.
- Separate low-risk summarization from high-risk automation.
- Provide a disable path for every automated AI workflow.

## Power BI And Reporting Principles

- Apply row-level security where data visibility differs by team, branch, customer, or role.
- Validate TOPdesk counts against source screens or trusted exports.
- Flag unknown dimensions rather than dropping records silently.
- Separate missing-data risk from operational risk.
- Document refresh ownership, gateway ownership, and failure handling.

## Production Readiness Questions

- Which fields contain PII, special categories, confidential notes, or security-sensitive data?
- Which users may see incident text, caller details, and operator notes in Power BI?
- Which AI provider is approved for customer data?
- Are prompts and outputs retained, and for how long?
- Is there an audit path from dashboard KPI back to source incident and snapshot date?
- Who owns refresh failures, model changes, and KPI definition changes?
