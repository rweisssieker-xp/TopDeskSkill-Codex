# TOPdesk Feature Reference

Use this file for helpdesk feature, workflow, and module questions. Verify release-specific details against official TOPdesk documentation when exact behavior matters.

## Core Modules

- **Incident Management**: Register, classify, assign, prioritize, resolve, and close user calls/incidents. Typical fields include caller, brief description, request text, category/subcategory, impact, urgency, priority, status, operator/group, target date, actions, attachments, and linked assets/persons.
- **Self-Service Portal (SSP)**: End-user entry point for submitting requests, viewing ticket status, browsing knowledge items, and using service forms. Design SSP flows around simple forms, visible status, and clear routing.
- **Knowledge Management**: Knowledge base articles/FAQs/standard solutions for operators and end users. Consider visibility, publication status, ownership, review dates, search terms, and links from incidents.
- **Change Management**: Standard/simple or extensive changes, approvals, activities, planning, risk/impact, templates, and implementation/evaluation phases. Use for controlled workflows such as onboarding, access requests, infrastructure changes, and multi-step fulfillment.
- **Asset Management**: Assets/objects, types, templates, fields, relations, lifecycle status, ownership, location, supplier, contract links, and incident/change links. Modern TOPdesk Asset Management is API-oriented and can replace older configuration/object management setups.
- **Problem Management**: Root-cause analysis, known errors, workarounds, and links to related incidents.
- **Operations/Task Management**: Planned and recurring operational activities.
- **Contract and Service Level Management**: Contracts, services, SLAs, target dates, escalation, and reporting.
- **Supporting Files**: Persons, operators, branches, departments, suppliers, locations/rooms, categories, priorities, and other reference data.
- **Reports and Selections**: Operational reporting and reusable filters for incidents, changes, assets, persons, and management views.

## Important Actors

- **Person/caller**: End user/customer record. Usually linked to branch, department, location, contact details, and permissions/SSP access.
- **Operator**: Service desk or back-office user who handles work. Operators may belong to operator groups and permission groups.
- **Application manager**: Configures modules, forms, categories, permissions, action sequences, imports, and integrations.
- **API user**: Dedicated account with least-privilege permission groups for integrations.

## Workflow Checklist

When analyzing or designing a TOPdesk workflow, cover:

1. Intake channel: SSP, email, operator entry, API, monitoring tool, Teams, or import.
2. Classification: category, subcategory, service, asset, branch, priority, impact/urgency.
3. Routing: operator group, operator, escalation, reassignment rules.
4. Lifecycle: states, required fields per transition, closure rules, reopen behavior.
5. Communication: action notes, emails, public/private comments, notifications, templates.
6. SLA: target dates, pauses, breached/near-breach handling, reporting.
7. Links: related incidents, changes, assets, persons, knowledge items, attachments.
8. Reporting: KPIs, selections, audit trail, export/OData needs.

## Common Design Guidance

- Use Change Management rather than a large incident form when fulfillment needs approvals, staged activities, or multiple teams.
- Use Knowledge Management to reduce repeated incidents; link knowledge items from incident categories and common resolutions.
- Keep category trees shallow enough for reliable routing and reporting.
- Store external system IDs explicitly when integrating TOPdesk with another app.
- Separate internal operator notes from end-user-visible communication.
- Model status history and action logs as append-only records when building a custom app.
- For AI-assisted workflows, keep the operator in control for customer-visible replies, closure decisions, priority changes, and destructive updates.
- For AI feature design, load `ai-features.md`.
- For acceptance tests covering these workflows, load `testing-validation.md`.
