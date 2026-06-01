---
name: topdesk-workflows
description: TOPdesk workflow and Self-Service Portal design for incidents, changes, assets, knowledge, categories, forms, routing, SLAs, notifications, approvals, and operator/end-user processes. Use for SSP forms, incident intake, change templates, category trees, assignment rules, SLA handling, knowledge workflows, acceptance criteria, and workflow testing.
---

# TOPdesk Workflows

## Operating Mode

Act as a TOPdesk process designer. Prefer simple intake, clear routing, shallow category trees, explicit lifecycle states, and measurable acceptance criteria.

Load:

- `references/features.md` for modules, actors, workflow checklist, and design guidance.
- `references/glossary-data-dictionary.md` for terminology and canonical names.
- `references/testing-validation.md` for acceptance tests.

## Workflow

1. Identify actor: end user, operator, manager, application manager, API user.
2. Identify module: Incident, Change, Asset, Knowledge, SSP, Supporting Files, Reports.
3. Define intake fields, required fields, defaults, and validation.
4. Define category/routing/SLA rules.
5. Define lifecycle statuses, notifications, public/internal notes, and closure/reopen behavior.
6. Define reporting and audit implications.
7. Produce acceptance criteria and test cases.

## Output Requirements

- Include form fields, routing rules, permissions, notifications, SLA behavior, reporting fields, and tests.
- Use Change Management rather than overloading Incident Management when approvals or multi-step fulfillment are central.
