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
