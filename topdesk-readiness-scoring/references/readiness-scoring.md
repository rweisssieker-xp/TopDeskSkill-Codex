# Readiness Scoring Reference

## Dimensions

| Dimension | Evidence examples |
| --- | --- |
| Reporting | Field catalog, KPI definitions, Power BI owner, refresh approach. |
| AI | Approved use case, PII review, prompt/eval pack, feedback loop. |
| Data trust | Reconciliation, source counts, data-quality findings, known exceptions. |
| Automation | Trigger, payload, idempotency, rollback, audit, monitoring. |
| Security/privacy | RLS, PII minimization, secret handling, retention, approval gates. |
| Operations | Runbook, owner, alerting, release gate, disable procedure. |
| Tenant mapping | OData/API access, sample records, UI label mapping, option exports. |

## Scores

- `green`: evidence complete and no blocker.
- `amber`: partial evidence or manageable risk.
- `red`: missing critical evidence or unresolved blocker.
