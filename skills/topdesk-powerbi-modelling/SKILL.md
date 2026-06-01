---
name: topdesk-powerbi-modelling
description: Design, review, and harden Power BI semantic models for TOPdesk data. Use for star schemas, fact/dimension grain, relationships, DAX measure catalogs, calculation groups, field parameters, RLS/OLS, incremental refresh, aggregation tables, reconciliation, tenant mapping, and model documentation for TOPdesk incidents, changes, assets, knowledge, SLAs, operators, branches, and AI features.
---

# TOPdesk Power BI Modelling

Use this skill for semantic modelling decisions after source queries are known or when a model must be reviewed.

## Workflow

1. Fix the fact grain before choosing visuals or writing DAX.
2. Separate facts from dimensions. Prefer conformed dimensions for date, branch, caller/person, operator, operator group, category, priority, status, source, asset, service, and knowledge article.
3. Use explicit measures. Avoid implicit aggregation in report visuals.
4. Define KPI semantics with numerator, denominator, date basis, exclusions, and reconciliation source.
5. Design security early: RLS by branch/customer/operator scope; avoid exposing PII in broad dimensions.
6. Specify refresh: OData/API pagination, incremental policy, historical backfill, refresh windows, and failure checks.
7. Produce model documentation: table list, relationships, measures, RLS, refresh, validation, known tenant assumptions.

## References

- Load `references/model-patterns.md` for model architecture, relationships, and DAX rules.
- Load `references/topdesk-model-catalog.md` for canonical TOPdesk facts, dimensions, and measures.

## Assets

- Use `assets/semantic-model-spec-template.md` for model specifications.
- Use `assets/measure-catalog-template.csv` for DAX backlog planning.

## Scripts

- Use `scripts/new_semantic_model_spec.py` to generate a semantic model starter spec.

