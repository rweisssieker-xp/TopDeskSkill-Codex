# TOPdesk Change Management

Use this file for change templates, activities, approvals, risk/impact, scheduling, audit, and change KPIs.

## Change Types

- Standard change: low-risk repeatable workflow.
- Simple change: limited activities and approval.
- Extensive change: multiple phases, approvals, activities, planning, implementation, and evaluation.

## Core Fields

- Change ID / TOPdesk ID / number.
- Requester/person and branch.
- Coordinator/operator.
- Template/type.
- Risk, impact, urgency.
- Status/phase.
- Planned start/end.
- Actual completion.
- Linked incidents, assets, services, suppliers.

## Activity Design

Each activity should have:

- Title and description.
- Owner group/operator.
- Due date.
- Status.
- Dependency/sequence.
- Approval or implementation marker.
- Completion evidence.

## Approval Guidance

- Define approver role, escalation, timeout, and rejection behavior.
- Record approval status and timestamp.
- Keep approval audit immutable.
- Do not allow AI to approve or reject changes.

## Change KPIs

- Changes by type/status/risk.
- Overdue activities.
- Approval duration.
- Implementation success rate.
- Emergency/unplanned change rate.
- Changes linked to incidents.
- Failed/reverted changes.

## Test Cases

- Standard change from template.
- Extensive change with approvals.
- Rejected approval path.
- Overdue activity escalation.
- Asset-linked change impact.
- Closure with required evaluation fields.
