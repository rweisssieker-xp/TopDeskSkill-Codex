# TOPdesk Action Sequences and Automation

Use this file for TOPdesk action sequences, webhooks, API calls, safe automation, retries, and error handling.

## Automation Candidates

- Notify external system on incident creation/update.
- Create follow-up tasks for certain categories.
- Enrich ticket with asset or caller data.
- Trigger approval or change workflow.
- Send internal notification for near-breach or VIP ticket.
- Create integration event for warehouse/Power BI refresh.

## Safety Rules

- Avoid destructive actions without human review.
- Keep customer-visible messages template-based or operator-reviewed.
- Do not auto-close tickets from AI output.
- Use allowlists for categories/actions eligible for automation.
- Log every automation run with source record, payload summary, result, and correlation ID.

## Design Checklist

1. Trigger condition.
2. Preconditions and exclusions.
3. Payload mapping.
4. Target endpoint or TOPdesk action.
5. Authentication and secret handling.
6. Success criteria.
7. Retry behavior.
8. Failure notification.
9. Idempotency key.
10. Audit record.

## Error Handling

- Validation error: record and route to manual queue.
- Authentication error: stop retries and alert owner.
- Rate limit/transient failure: retry with backoff.
- Duplicate: treat as success only when idempotency confirms same target.
- Partial failure: preserve correlation ID and retry only unfinished steps.

## Monitoring

- Runs by action sequence.
- Success/failure rate.
- Average duration.
- Retried runs.
- Dead-letter/manual queue count.
- Most common error reason.
