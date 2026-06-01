# Automation Sandbox Reference

## Required Controls

- Clear trigger and scope.
- Payload field mapping.
- Idempotency key or duplicate prevention.
- Retry policy and stop condition.
- Dead-letter or failure queue.
- Rollback or disable procedure.
- PII and customer-visible content review.
- Audit fields and monitoring owner.
- Human approval for risky or irreversible actions.

## Go/No-Go

- `go`: no high risks and owner/rollback/monitoring are present.
- `conditional`: medium risks remain but are owned with mitigation.
- `no-go`: any high risk remains for idempotency, rollback, PII, audit, or unattended customer-visible action.
