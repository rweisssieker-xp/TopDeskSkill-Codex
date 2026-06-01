---
name: topdesk-executive-narrative
description: Generate management-ready TOPdesk executive narratives from decision-ready findings, readiness scorecards, drift findings, process-debt reports, AI adoption ledgers, automation risk cards, and proof-of-value outputs.
---

# TOPdesk Executive Narrative

Use this skill when technical TOPdesk findings need to become a concise steering or management readout.

## Workflow

1. Gather a decision-ready findings CSV or any CSV with finding, evidence, impact, risk, action, owner, and metric fields.
2. Run `scripts/build_executive_narrative.py`.
3. Review the generated one-page narrative and next-30-days plan.
4. Keep tenant-specific numbers traceable to the source finding rows.

## Outputs

- `executive-narrative.md`
- `executive-actions.csv`

## References

- Load `references/executive-narrative.md` for narrative sections and tone.
