---
name: topdesk-visual-design
description: Design Power BI report pages and dashboard UX for TOPdesk service-management analytics. Use for visual hierarchy, page layouts, KPI cards, trend charts, matrix/table design, drill-through, tooltip pages, filters/slicers, color semantics, accessibility, executive/operator/application-manager views, incident/change/asset/knowledge dashboards, and report storytelling.
---

# TOPdesk Visual Design

Use this skill when the user needs a report layout, dashboard UX, wireframe, visual critique, or Power BI page specification.

## Workflow

1. Identify audience: executive, service desk lead, operator, application manager, process owner, customer/branch manager.
2. Define the page job: monitor, diagnose, compare, explain, reconcile, or act.
3. Keep hierarchy compact: top KPI strip, main diagnostic visual, supporting breakdowns, exception table, filters.
4. Use stable TOPdesk color semantics: status/severity colors only where they encode meaning; avoid decorative gradients.
5. Prefer visuals that match the question: cards for totals, line charts for trends, bar charts for ranked categories, matrices for operational queues, scatter only for true correlation.
6. Add drill-through and tooltip pages for details instead of overloading the overview.
7. Include validation and accessibility notes: contrast, label clarity, keyboard/filter behavior, PII visibility, export needs.

## References

- Load `references/report-design-patterns.md` for TOPdesk dashboard layouts and visual rules.
- Load `references/page-wireframes.md` for reusable page patterns.

## Assets

- Use `assets/report-page-spec-template.md` for Power BI page specs.
- Use `assets/topdesk-report-theme.json` as a restrained Power BI theme baseline.

## Scripts

- Use `scripts/new_report_page_spec.py` to generate a page spec from audience and page type.

