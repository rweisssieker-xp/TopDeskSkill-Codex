# Integration Handbook

Audience: developers, data engineers, and integration owners.

## Integration Rules

- Use dedicated API users.
- Store secrets outside source code.
- Preserve TOPdesk IDs and numbers.
- Make sync idempotent.
- Log integration runs and failures.
- Reconcile counts against TOPdesk.

## Mapping Procedure

1. Collect OData metadata/API samples/exports.
2. Build field catalog.
3. Map IDs, display labels, dates, statuses, and references.
4. Define transformations.
5. Validate with sample records.
6. Document unknowns.

## Error Handling

- Validation errors go to manual queue.
- Authentication failures alert owner.
- Rate limits retry with backoff.
- Duplicates require idempotency check.
- Partial failures keep correlation ID.

## Observability

- Last successful sync.
- Records read/written/failed.
- Error type and affected entity.
- Reconciliation delta.
