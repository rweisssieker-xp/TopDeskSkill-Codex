# Power BI AI Monitoring

## Facts

- `FactAISuggestion`: one row per AI suggestion.
- `FactAIFeedback`: one row per accept/edit/reject event.
- `FactAIPromptRun`: one row per prompt/model execution.
- `FactAIEvaluation`: one row per eval case result.
- `FactAICost`: one row per cost/token event.

## Dimensions

- `DimDate`, `DimAIFeature`, `DimModelVersion`, `DimPromptVersion`, `DimOperator`, `DimBranch`, `DimCategory`, `DimRiskClass`.

## Core Measures

- Suggestions
- Acceptance Rate
- Edit Rate
- Rejection Rate
- Average Confidence
- Low Confidence Suggestions
- Override Reasons
- Eval Pass Rate
- Estimated Minutes Saved
- Estimated Cost
- Cost Per Accepted Suggestion
- SLA Risk Suggestions

## Pages

- Executive AI Value
- Operator Adoption
- Quality And Evaluation
- Cost And Usage
- Risk And Compliance
- Feature Drillthrough

