# Governance Cockpit Model

## Semantic Model

- `FactAISuggestion`: suggestion lifecycle, feature, confidence, status, time saved estimate.
- `FactAIPromptRun`: model, prompt version, latency, tokens, cost, status.
- `FactAIFeedback`: accepted, edited, rejected, override reason, operator.
- `FactAIEvaluation`: test case, expected, actual, pass flag, metric.
- `FactAIRiskFinding`: PII, policy, hallucination, permission, stale-source findings.

## Relationships

- Use `DimDate` for suggestion, run, feedback, and eval dates.
- Use `DimAIFeature` across all AI facts.
- Use `DimPromptVersion` and `DimModelVersion` for release analysis.
- Use `DimBranch` and `DimOperator` only where RLS allows it.

## Report Pages

- Governance Overview
- Adoption And Feedback
- Quality And Regression
- Cost And Latency
- Risk And Compliance
- Prompt/Model Drillthrough

