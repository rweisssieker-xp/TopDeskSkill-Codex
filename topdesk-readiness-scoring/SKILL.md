---
name: topdesk-readiness-scoring
description: Score TOPdesk reporting, AI/KI, data trust, automation, security/privacy, tenant mapping, and operations readiness from evidence checklists, proof-of-value inputs, production gates, or project intake artifacts.
---

# TOPdesk Readiness Scoring

Use this skill before investing in production reporting, AI/KI, automation, migration, or managed improvement work.

## Workflow

1. Gather evidence checklist rows for reporting, AI, data trust, automation, security, operations, and tenant mapping.
2. Run `scripts/score_readiness.py`.
3. Review red/amber/green scores and blockers.
4. Convert blockers into a next-step roadmap or proof-of-value backlog.

## Outputs

- `readiness-scorecard.csv`
- `readiness-scorecard.md`

## References

- Load `references/readiness-scoring.md` for dimensions and evidence expectations.
