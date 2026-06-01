# Digital Twin Light Reference

This is a lightweight scenario scorer, not a discrete-event simulation engine.
It uses explicit assumptions to compare options before a controlled pilot.

## Supported Baseline Metrics

- `open_incidents`
- `avg_waiting_hours`
- `handoff_count`
- `reopen_rate_pct`
- `sla_at_risk`
- `operator_capacity_hours`

## Scenario Use

Use the output to choose a pilot:

- routing cleanup
- category cleanup
- SLA focus
- capacity shift
- AI routing or summary support
- handoff reduction initiative

The validation metric should be measured after the pilot with the same KPI definitions.
