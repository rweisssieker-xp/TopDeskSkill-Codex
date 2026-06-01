---
name: topdesk-ai-adoption-ledger
description: Build TOPdesk AI/KI adoption ledgers and monitoring summaries from suggestion logs, operator feedback, acceptance/edit/rejection events, override reasons, confidence, cost estimates, prompt/model versions, and value assumptions.
---

# TOPdesk AI Adoption Ledger

Use this skill when an AI pilot needs measurable adoption evidence from suggestion and feedback logs.

## Workflow

1. Gather AI suggestion logs or feedback exports with suggestion type, status, confidence, override reason, cost, and time-saved assumptions.
2. Run `scripts/build_ai_adoption_ledger.py` to normalize rows and produce adoption metrics.
3. Review acceptance, edit, rejection, override, confidence, and cost signals by suggestion type.
4. Use outputs in AI governance cockpit, proof-of-value readout, or steering decisions.

## Outputs

- `ai-adoption-ledger.csv`
- `ai-adoption-summary.md`

## References

- Load `references/ai-adoption-ledger.md` for metric definitions and interpretation.
