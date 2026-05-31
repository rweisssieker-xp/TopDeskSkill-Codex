---
name: topdesk-automation-sandbox
description: Review TOPdesk action sequences, webhooks, scheduled jobs, integration scripts, and automation designs for trigger quality, payload mapping, idempotency, retry behavior, rollback, dead-letter handling, PII, audit, human approval, and production go/no-go risk.
---

# TOPdesk Automation Sandbox

Use this skill before a TOPdesk automation changes tickets, sends notifications, updates external systems, or affects customer-visible communication.

## Workflow

1. Gather an automation design CSV or checklist with trigger, payload, idempotency, retry, rollback, PII, audit, monitoring, and approval fields.
2. Run `scripts/review_automation_risk.py`.
3. Review the generated automation risk card.
4. Do not call it production-safe unless rollback, monitoring, ownership, and approval boundaries are explicit.

## Outputs

- `automation-risk-findings.csv`
- `automation-risk-card.md`

## References

- Load `references/automation-sandbox.md` for checks and go/no-go interpretation.
