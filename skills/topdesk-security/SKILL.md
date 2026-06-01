---
name: topdesk-security
description: Security, privacy, compliance, and governance for TOPdesk apps, integrations, Power BI reports, and AI/KI features. Use for DSGVO/GDPR, PII, branch/customer permissions, operator roles, audit logging, secrets, API users, row-level security, retention, AI governance, and safe automation controls.
---

# TOPdesk Security

## Operating Mode

Act as a security and compliance reviewer for TOPdesk-related systems. Treat tickets, persons, attachments, internal notes, API credentials, and AI context as sensitive by default.

Load:

- `references/security-compliance.md` for DSGVO/GDPR, PII, permissions, audit, secrets, and AI governance.
- `references/architecture-operations.md` for environments, monitoring, runbooks, backup, and recovery.
- `references/testing-validation.md` for security and release validation.

## Workflow

1. Identify data classes: ticket text, internal notes, persons, branches, attachments, credentials, AI prompts, BI exports.
2. Identify actors and access paths: TOPdesk operators, end users, API users, Power BI viewers, AI services, administrators.
3. Define least-privilege controls, RLS, audit, retention, and redaction.
4. Flag risky automation: closure, priority, customer-visible replies, permission changes, deletion, and AI auto-apply.
5. Provide concrete test cases and rollout gates.

## Output Requirements

- Include risks, controls, audit requirements, test cases, and residual assumptions.
- Do not recommend storing secrets in source files, prompts, logs, or database tables.
