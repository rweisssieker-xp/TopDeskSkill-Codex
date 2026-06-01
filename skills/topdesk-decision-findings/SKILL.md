---
name: topdesk-decision-findings
description: Generate decision-ready TOPdesk findings from analysis CSV files, SLA findings, data-quality findings, process-debt outputs, AI governance rows, or manual finding drafts using a standard evidence, impact, risk, action, owner, and validation metric format.
---

# TOPdesk Decision Findings

Use this skill when raw TOPdesk analysis needs to become an action-ready management or backlog artifact.

## Workflow

1. Gather rows from SLA, data-quality, process-debt, AI, drift, readiness, or manual analysis outputs.
2. Run `scripts/build_decision_findings.py` against a CSV input.
3. Review generated owner/action/metric fields and adjust tenant-specific ownership.
4. Use the Markdown readout in steering, proof-of-value, or project backlog work.

## Output Contract

Every finding should include:

- `finding`
- `evidence`
- `business_impact`
- `risk`
- `recommended_action`
- `owner`
- `validation_metric`

## References

- Load `references/decision-findings.md` for field definitions and examples.
