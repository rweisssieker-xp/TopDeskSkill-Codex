---
name: topdesk-digital-twin-light
description: Run lightweight TOPdesk service desk what-if scenario scoring from baseline KPIs and scenario assumptions for routing, SLA thresholds, operator capacity, category cleanup, AI assistance, handoff reduction, and backlog improvement decisions.
---

# TOPdesk Digital Twin Light

Use this skill when a team needs a concrete, inspectable what-if comparison before changing TOPdesk routing, SLA focus, capacity, categories, or AI-assisted triage.

## Workflow

1. Gather a baseline KPI CSV and a scenario assumptions CSV.
2. Run `scripts/run_digital_twin_light.py`.
3. Review scenario score, expected KPI movement, assumptions, confidence, and recommended pilot.
4. Present the result as decision support. Do not present it as a forecast guarantee.

## Inputs

Baseline CSV columns:

- `metric`
- `value`

Scenario CSV columns:

- `scenario`
- `handoff_reduction_pct`
- `waiting_reduction_pct`
- `reopen_reduction_pct`
- `capacity_change_pct`
- `ai_assist_pct`
- `confidence`

## Outputs

- `digital-twin-scenarios.csv`
- `digital-twin-readout.md`

## References

- Load `references/digital-twin-light.md` for supported scenario interpretation.
