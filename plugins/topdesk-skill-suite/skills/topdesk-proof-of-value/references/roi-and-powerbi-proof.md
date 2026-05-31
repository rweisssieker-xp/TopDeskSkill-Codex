# ROI And Power BI Proof

## ROI Drivers

- Manual reporting hours avoided.
- Reassignment reduction.
- Waiting time reduction by status.
- Waiting time reduction by operator group.
- Backlog aging reduction from daily snapshots.
- Earlier bottleneck detection and escalation prevention.
- Faster SLA-risk focus.
- Knowledge deflection.
- Data cleanup prioritization.
- AI draft/summary time saved.

## Power BI Proof Pages

- Baseline Overview
- SLA Risk
- Data Quality
- AI Value
- Lifecycle Bottlenecks
- Backlog Snapshot Trend
- ROI Assumptions

## Measures

- Baseline Tickets
- Estimated Minutes Saved
- Estimated Hours Saved
- Estimated Value
- PoV Coverage %
- Data Quality Findings
- SLA At Risk
- Average Time In Status Hours
- P90 Time In Status Hours
- Average Time In Operator Group Hours
- P90 Time In Operator Group Hours
- Reassignment Rate
- Snapshot Open Incidents
- Backlog Age Bucket Count

## Lifecycle ROI Hypotheses

Use conservative, separately stated assumptions:

```text
monthly_waiting_hours_reduced =
  monthly_ticket_volume
  * average_waiting_minutes_reduced_per_ticket
  / 60

monthly_waiting_value =
  monthly_waiting_hours_reduced
  * blended_operator_hourly_cost
```

Additional value can be estimated from:

- Avoided escalation handling for aged tickets.
- Reduced handoff effort when reassignment rate falls.
- Reduced SLA breach handling through earlier queue visibility.
- Reduced management reporting time because daily snapshots preserve trend history.
