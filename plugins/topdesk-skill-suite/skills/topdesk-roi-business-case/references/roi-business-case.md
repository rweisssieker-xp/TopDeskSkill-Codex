# TOPdesk ROI and Business Case

Use this file for ROI models, executive cases, benefit quantification, and value baselines.

## ROI Inputs

- Monthly ticket volume.
- Minutes spent on triage per ticket.
- Minutes saved by classification/routing.
- Minutes saved by summaries/draft replies.
- Operator hourly cost.
- Current reassignment rate.
- Current SLA breach rate.
- Manual reporting hours per month.
- Integration/import correction hours per month.

## ROI Formula

```text
monthly_time_saved_hours =
  ticket_volume * minutes_saved_per_ticket / 60

monthly_labor_value =
  monthly_time_saved_hours * blended_hourly_cost

annual_labor_value =
  monthly_labor_value * 12
```

## Benefit Categories

- Labor time saved.
- Reduced SLA breach handling.
- Reduced reassignment.
- Reduced manual reporting.
- Reduced data cleanup.
- Faster onboarding.
- Better management decisions.
- Lower compliance remediation risk.

## Executive Case Structure

1. Current pain.
2. Proposed capability.
3. Quantified benefits.
4. Risk controls.
5. Implementation phases.
6. Required inputs.
7. Success metrics.
