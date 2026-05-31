---
name: topdesk-process-debt
description: Analyze TOPdesk lifecycle, incident, SLA, status-transition, assignment-transition, and reopen evidence for process debt such as handoff loops, waiting zones, stale ownership, long runners, category-routing waste, and improvement backlog candidates.
---

# TOPdesk Process Debt

Use this skill when a user wants to turn TOPdesk operational friction into evidence-backed improvement work.

## Workflow

1. Gather lifecycle evidence: incident snapshots, status transitions, assignment transitions, SLA findings, reopen flags, category/status/operator-group fields.
2. Run `scripts/analyze_process_debt.py` when CSV exports are available.
3. Review findings for handoff loops, waiting zones, stale ownership, reopen patterns, long runners, and routing/category debt.
4. Convert findings into an improvement backlog with owner, recommended action, and validation metric.
5. Use the generated CSV and Markdown report as the process-debt evidence pack for backlog and management review.

## Outputs

- `process-debt-findings.csv`
- `process-debt-report.md`

## References

- Load `references/process-debt.md` for debt patterns, severity, and remediation examples.
