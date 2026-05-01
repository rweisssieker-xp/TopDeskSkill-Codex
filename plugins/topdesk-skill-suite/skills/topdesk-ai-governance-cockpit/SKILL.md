---
name: topdesk-ai-governance-cockpit
description: Design Power BI governance cockpits for TOPdesk AI/KI features. Use for AI monitoring datasets, semantic models, DAX measures, report pages, prompt/model version tracking, suggestion acceptance, override reasons, confidence drift, cost, token usage, SLA impact, PII/policy findings, feedback loops, evaluation results, RLS, and audit reporting.
---

# TOPdesk AI Governance Cockpit

Use this skill when AI/KI usage needs measurable governance, operational monitoring, and executive reporting.

## Workflow

1. Define monitoring grain: suggestion, prompt run, feedback event, evaluation run, source chunk, or cost event.
2. Model facts and dimensions for Power BI: AI suggestions, prompt runs, feedback, evaluations, embeddings/source chunks, costs, users, dates, branches, feature type.
3. Add DAX measures for adoption, quality, risk, cost, and business impact.
4. Design pages: executive governance, operator adoption, quality/evals, cost, risk/compliance, feature drill-through.
5. Apply RLS and PII minimization before exposing examples or prompts.
6. Define refresh, retention, anomaly alerts, and release gates.

## References

- Load `references/governance-cockpit-model.md` for model and report architecture.
- Load `references/governance-kpis.md` for KPI definitions and DAX guidance.

## Assets

- Use `assets/governance-cockpit-spec-template.md`.
- Use `assets/ai-governance-measures.dax`.
- Use `assets/ai-governance-theme.json`.

## Scripts

- Use `scripts/new_governance_cockpit_spec.py` to generate a cockpit spec.

