# Process Debt Reference

## Debt Patterns

| Pattern | Signal | Typical action |
| --- | --- | --- |
| Handoff loop | High assignment count per incident or repeated group sequence. | Review routing rules and category ownership. |
| Waiting zone | Long duration in waiting/on-hold/customer-info status. | Clarify customer communication and escalation rules. |
| Stale ownership | Long open age with empty or unchanged operator group. | Assign owner and escalation cadence. |
| Reopen pattern | Reopened incidents by category/group. | Review closure quality and knowledge articles. |
| Category-routing waste | Many groups for one category. | Clean category tree and routing matrix. |
| SLA risk hotspot | Overdue or missing target dates clustered by group/category. | Fix SLA mapping and workload focus. |

## Finding Format

Each output row should be usable as a backlog candidate:

- `finding`
- `evidence`
- `business_impact`
- `risk`
- `recommended_action`
- `owner`
- `validation_metric`
