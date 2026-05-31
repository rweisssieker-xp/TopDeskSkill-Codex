# USP Battlecards

## Persona Angles

- CIO: governed intelligence, reduced delivery risk, reusable platform.
- CFO: measurable ROI, reporting effort reduction, better investment decisions.
- Service desk lead: fewer reassignments, SLA focus, operator productivity.
- Service desk lead: bottleneck evidence, shorter waiting time, fewer avoidable handoffs.
- Operator: better summaries, suggested replies, less context switching.
- Application manager: cleaner configuration, better tenant mapping, safer changes.
- Security/privacy: audit, PII controls, RLS, approval gates.

## Competitors

- Manual Excel reporting.
- Generic ChatGPT prompts.
- Pure Power BI implementation.
- Pure TOPdesk consulting.
- Point automation scripts.
- Separate process-mining platforms.

## Battlecard Fields

- Positioning line.
- Top pains.
- Differentiators.
- Proof points.
- Objections and answers.
- Demo moment.
- Power BI evidence.
- AI/KI governance evidence.

## Lifecycle Analytics Battlecard

Positioning line:

- "TOPdesk reporting that explains where incidents waited, not only how many are open."

Top pains:

- Current-state reports hide earlier status and assignment changes.
- Teams cannot prove where tickets stalled or why SLA risk increased.
- Reassignment and handoff loops are visible anecdotally but not measured consistently.
- Daily backlog trend is hard to reconstruct after tickets move or close.

Differentiators:

- Status transition fact with duration and sequence.
- Assignment transition fact with operator-group duration and handoff sequence.
- Daily snapshot fact for stichtag backlog, aging, and open/closed state.
- Power BI-ready KPIs for waiting time, reassignment rate, P90 duration, and bottleneck ranking.
- Demo lifecycle CSVs for workshops before production history is connected.

Proof points:

- Generated demo pack includes `FactIncidentDailySnapshot`, `FactStatusTransition`, and `FactAssignmentTransition`.
- Lifecycle validation checks required fields, interval order, duration math, and sequence continuity.
- SQL, DAX, Power Query, and model references all point to the same fact pattern.

Objections and answers:

- "TOPdesk already shows the ticket status." Response: "That is the current or ticket-level view. The lifecycle model preserves each interval, so you can measure how long a ticket stayed in every status and group."
- "We do not have perfect historical events yet." Response: "Use event history where available and daily snapshots from the first run onward. The model separates exact transitions from snapshot evidence, so gaps are explicit."
- "Process mining sounds too large." Response: "This is a focused TOPdesk lifecycle layer in Power BI: status paths, handoffs, waiting time, and backlog aging without a separate platform rollout."

Demo moment:

- Pick one incident and show the status timeline, assignment timeline, and daily snapshots side by side.
- Then aggregate to average/P90 time in status and operator group.
- Finish with a ranked bottleneck table by group, status, priority, or category.

Power BI evidence:

- Cards: open snapshot incidents, average time in status, average time in operator group, reassignment rate.
- Trend: open incident days by snapshot date.
- Bar chart: P90 duration by operator group or status.
- Detail table: incident key, sequence, status/group, valid from, valid to, duration.
