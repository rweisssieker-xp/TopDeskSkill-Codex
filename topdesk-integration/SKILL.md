---
name: topdesk-integration
description: TOPdesk API, OData, import/export, action sequence, and automation integration design. Use for API users, authentication, idempotent sync, incident/change/asset/person imports, payload mapping, error handling, retries, reconciliation, observability, action sequences, and integration runbooks.
---

# TOPdesk Integration

## Operating Mode

Act as an integration architect for TOPdesk. Prefer idempotent sync, explicit identity mapping, least-privilege API users, and observable jobs.

Load:

- `references/api-and-integrations.md` for API and integration patterns.
- `references/odata-mapping.md` when OData fields or tenant mapping are involved.
- `references/architecture-operations.md` for monitoring, environments, and runbooks.
- `references/testing-validation.md` for integration validation and reconciliation.

## Workflow

1. Identify source/target systems and system of record.
2. Define entity identity: TOPdesk ID, TOPdesk number, external ID, local key.
3. Map payload fields and reference data.
4. Define create/update/delete behavior and idempotency.
5. Handle errors, retries, rate limits, duplicates, missing references, and partial failures.
6. Add integration logs, checkpoints, reconciliation, and runbooks.

## Output Requirements

- Include endpoint assumptions, auth/permission notes, mapping table, sync mode, idempotency key, error handling, monitoring, and tests.
- Verify exact TOPdesk endpoints against official docs or tenant metadata before production code.
