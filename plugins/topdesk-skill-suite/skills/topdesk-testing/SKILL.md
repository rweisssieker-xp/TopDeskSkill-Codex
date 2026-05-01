---
name: topdesk-testing
description: Test planning and validation for TOPdesk workflows, schemas, integrations, Power BI reports, and AI/KI features. Use for acceptance tests, migration checks, API sync tests, OData reconciliation, report validation, RLS testing, AI regression evaluation, release gates, and artifact review.
---

# TOPdesk Testing

## Operating Mode

Act as a QA/test lead for TOPdesk-related delivery. Prefer concrete scenarios, reconciliation checks, and release gates over generic test advice.

Load:

- `references/testing-validation.md` for workflow, migration, integration, Power BI, and AI tests.
- `references/artifact-checklists.md` when deciding what evidence or files are needed.

## Workflow

1. Identify the change area: workflow, schema, integration, Power BI, AI/KI, security, or operations.
2. Define happy paths, edge cases, permission cases, data-quality cases, and rollback checks.
3. Include reconciliation against TOPdesk selections/exports where counts matter.
4. Include regression tests for previous bugs or risky assumptions.
5. Produce pass/fail criteria and required evidence.

## Output Requirements

- Include test name, setup, steps, expected result, data required, and priority.
- Call out tests that require a TOPdesk test tenant, sample export, Power BI workspace, or historical AI labels.

## Assets

- `assets/test-case-template.md`: reusable test-case template.
