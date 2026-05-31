# Demo Dashboard Storyboard

Use this storyboard to present the plugin with demo data before connecting a customer tenant.

## Available Demo Assets

- `skills/topdesk-powerbi/assets/demo-lifecycle/FactIncidentDailySnapshot.csv`
- `skills/topdesk-powerbi/assets/demo-lifecycle/FactStatusTransition.csv`
- `skills/topdesk-powerbi/assets/demo-lifecycle/FactAssignmentTransition.csv`
- `assets/screenshot-overview.png`
- `assets/screenshot-powerbi.png`
- `assets/screenshot-ai-governance.png`

## Demo Narrative

1. Start with the overview screenshot and explain that the plugin is free open-source accelerator material.
2. Open the lifecycle CSVs and show that incidents are represented as dated snapshots plus transition facts.
3. Explain that this enables dwell-time KPIs by status, assignment group, and day.
4. Show the Power BI screenshot as the target reporting shape: operational KPIs, backlog, SLA, data quality, and lifecycle analytics.
5. Show the AI governance screenshot as the control layer for prompts, evals, feedback, adoption, and risk.
6. Close with the commercial model: no plugin fee, paid value comes from setup, modelling, rollout, and managed improvement.

## Recommended Demo Pages

| Page | Main Question | Visuals |
| --- | --- | --- |
| Executive Overview | Where is service performance improving or degrading? | KPI strip, SLA trend, backlog trend, risk list. |
| Lifecycle Flow | How long do incidents stay in each status? | Status dwell-time matrix, transition counts, reopened trend. |
| Assignment Flow | Which groups hold work longest? | Group dwell-time, handoff count, ageing by group. |
| Data Quality | Can we trust the KPIs? | Missing fields, unknown dimensions, orphan references, coverage trend. |
| AI/KI Insights | Which AI suggestions are useful and governed? | Suggestion quality, human acceptance, review queue, exception rate. |
| Proof Of Value | What changed in five days? | Findings, effort, ROI assumptions, next-step backlog. |

## Demo KPIs

- Open incidents.
- New incidents per day.
- Closed incidents per day.
- Median age of open incidents.
- SLA at risk.
- Status dwell time in hours.
- Assignment group dwell time in hours.
- Reopen rate.
- Handoff count per incident.
- Missing category, branch, caller, target date, or assignment group.
- AI suggestion acceptance rate.
- AI suggestion override rate.
- Knowledge article gap count.

## Customer Validation Questions

- Are all relevant status changes represented in the source data or daily snapshots?
- Are assignment groups stable enough for trend reporting?
- Which statuses count as waiting, active work, resolved, or closed?
- Which TOPdesk fields are mandatory for trusted KPI reporting?
- Which AI/KI use cases may use ticket text, and which require anonymization?

