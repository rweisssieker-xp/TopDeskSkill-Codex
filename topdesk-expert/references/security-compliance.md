# Security, Privacy, and Compliance for TOPdesk

Use this file for DSGVO/GDPR, PII, permissions, audit, secrets, retention, AI governance, and safe automation.

For environment separation, runbooks, backup, recovery, and monitoring, load `architecture-operations.md`.

## Data Classification

Common sensitive data:

- Names, email addresses, phone numbers, employee IDs.
- Branch/customer affiliation.
- HR, medical, legal, payroll, security, access, and disciplinary tickets.
- Passwords, tokens, license keys, IPs, device identifiers.
- Internal operator notes and supplier-only comments.

Handle sensitive categories with stricter AI review and reporting access.

## Permission Model

Model these separately:

- TOPdesk operator permissions.
- Local app roles.
- Power BI row-level security.
- AI retrieval permissions.
- API user scopes.

Do not assume visibility in one system grants visibility in another.

## Audit Requirements

Audit these events:

- Ticket status, priority, assignment, closure, deletion.
- Changes to caller/person, branch, category, SLA target.
- AI suggestions accepted/applied/rejected.
- Customer-visible AI reply drafts sent.
- Permission and RLS changes.
- Integration imports/exports and failures.

Audit records should include actor, timestamp, source, before/after summary, and correlation ID.

## Secrets Handling

- Keep TOPdesk API credentials, app passwords, OAuth secrets, and Power BI gateway credentials out of source files.
- Use environment variables, managed identity, secret vaults, or deployment secrets.
- Redact secrets from logs and AI prompts.
- Rotate credentials for API users and disable unused accounts.

## GDPR/DSGVO Checklist

- Define purpose and legal basis for processing helpdesk data.
- Minimize fields sent to AI services and BI datasets.
- Respect retention/deletion rules for incidents, attachments, and logs.
- Support access/export/deletion requests where legally required.
- Avoid using personal data for model training unless explicitly approved.
- Document subprocessors and data residency for external AI services.

## AI Governance

- Start AI features in suggest-only mode.
- Require human approval for external messages, closure, escalation, priority, and sensitive categories.
- Version prompts and models.
- Log source records and retrieved context references.
- Monitor acceptance, overrides, false positives, and drift.
- Provide rollback for auto-applied changes.
- Make AI-generated content visible as generated/draft inside the operator workflow.

## Power BI Security

- Use RLS by branch/customer/team where needed.
- Remove or mask PII in executive dashboards.
- Avoid exporting sensitive detail tables to broad audiences.
- Validate RLS with named test users before publish.
- Document refresh credentials and gateway ownership.
