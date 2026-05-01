# AI Feature Factory

## Feature Pack Sections

- Use case and user workflow.
- Data contract: input, output, confidence, explanation, source references, model/prompt version.
- Prompt design and JSON schema.
- Evaluation dataset and metrics.
- Feedback loop and audit storage.
- Security and PII controls.
- Rollout mode and rollback.
- Power BI monitoring model and measures.
- Business value and acceptance criteria.

## AI Modes

- Suggest-only: default for new features.
- Approval-required: operator confirms before changes or customer-visible text.
- Limited auto-apply: only low-risk, high-confidence, reversible updates with audit.

## Release Gates

- Historical eval set passes target quality.
- Sensitive category false positives reviewed.
- RLS and permission-aware retrieval tested.
- Operator pilot feedback captured.
- Power BI monitoring page ready before production.

