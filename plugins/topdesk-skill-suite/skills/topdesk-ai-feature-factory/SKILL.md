---
name: topdesk-ai-feature-factory
description: Generate complete governed AI/KI feature packs for TOPdesk. Use for turning an AI use case into feature scope, data contract, prompt design, JSON output schema, evaluation dataset, feedback loop, audit fields, rollout gates, Power BI monitoring measures, RLS/PII controls, and operator-facing acceptance criteria.
---

# TOPdesk AI Feature Factory

Use this skill when a TOPdesk AI/KI idea must become an implementable and monitorable feature.

## Workflow

1. Classify the feature: classification, routing, summary, response draft, RAG/search, duplicate detection, SLA risk, chatbot, or agentic workflow.
2. Define the data contract: inputs, outputs, confidence, explanation, source references, model/prompt version, feedback, retention, and permissions.
3. Specify safety mode: suggest-only, approval-required, or limited auto-apply with rollback.
4. Create prompt/schema/eval artifacts and Power BI monitoring requirements.
5. Define release gates: offline evaluation, pilot, operator feedback, regression pack, drift monitoring.
6. Include business value: time saved, reassignment reduction, SLA risk reduction, deflection, quality and audit benefits.

## References

- Load `references/ai-feature-factory.md` for pack structure, feature patterns, and rollout gates.
- Load `references/powerbi-ai-monitoring.md` for AI monitoring model, DAX, pages, and validation.

## Assets

- Use `assets/ai-feature-pack-template.md`.
- Use `assets/ai-eval-dataset-template.csv`.
- Use `assets/ai-monitoring-measures.dax`.

## Scripts

- Use `scripts/new_ai_feature_pack.py` to generate a starter feature pack.

