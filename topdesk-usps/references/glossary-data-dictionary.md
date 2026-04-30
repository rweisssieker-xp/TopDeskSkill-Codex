# Glossary and Data Dictionary

Use this file for terminology, canonical naming, KPI definitions, and entity naming decisions.

## TOPdesk Terms

- **Incident / Call**: A user request, issue, or service desk ticket.
- **Caller / Person**: End user or customer connected to a ticket.
- **Operator**: Service desk or back-office user who handles work.
- **Operator Group**: Assignment team.
- **Branch**: Customer organization, site, or tenant-like organizational unit.
- **Supporting Files**: TOPdesk reference/master data such as persons, branches, categories, priorities, suppliers, locations, and operators.
- **Category / Subcategory**: Classification tree used for routing and reporting.
- **Priority**: Importance/urgency indicator, often tied to SLA targets.
- **Status**: Lifecycle state of an incident, change, activity, or knowledge item.
- **Action**: Chronological note, communication, or work log entry on an incident.
- **Change**: Controlled workflow for planned work, approvals, and activities.
- **Activity**: Task or approval step within a change.
- **Asset**: Physical or logical object/configuration item.
- **Knowledge Item**: Article, FAQ, or standard solution.
- **Self-Service Portal (SSP)**: End-user portal for requests and knowledge.
- **Selection**: TOPdesk filter/reporting selection.
- **Action Sequence**: TOPdesk automation sequence.

## Canonical App Naming

Prefer these local names unless the existing project uses different conventions:

| Concept | Preferred table/entity | Notes |
| --- | --- | --- |
| Incident/ticket | `incidents` | Store `topdesk_id` and `topdesk_number` |
| Incident note/reply | `incident_actions` | Include `is_public` |
| Status changes | `incident_status_history` | Append-only |
| Assignment changes | `incident_assignment_history` | Append-only |
| Caller/end user | `persons` | Avoid duplicating operator unless needed |
| Service user | `operators` | Link to person when available |
| Team | `operator_groups` | Assignment dimension |
| Customer/site | `branches` | Key for RLS |
| Classification | `categories` | Module-scoped hierarchy |
| Lifecycle status | `statuses` | Module-scoped |
| CI/object | `assets` | Dynamic fields via value table |
| Knowledge article | `knowledge_items` | Add versions if needed |
| AI output | `ai_suggestions` | Generic auditable suggestions |

## KPI Dictionary

- **Created incidents**: Count of incidents by creation timestamp.
- **Closed incidents**: Count of incidents by closure timestamp.
- **Open backlog**: Incidents not closed at a point in time.
- **SLA compliance**: Closed incidents that met the defined SLA target divided by eligible closed incidents.
- **SLA breach rate**: Closed or open breached incidents divided by eligible incidents.
- **First response time**: Creation to first public operator response or first qualifying action; define explicitly.
- **Resolution time**: Creation to resolved/closed timestamp.
- **Reopen rate**: Reopened incidents divided by closed incidents.
- **Reassignment rate**: Incidents with more than one assignment group/operator divided by incidents.
- **Deflection rate**: Self-service/chatbot sessions resolved without creating a ticket.
- **AI acceptance rate**: Accepted AI suggestions divided by generated suggestions.
- **AI override rate**: Edited/rejected AI suggestions divided by generated suggestions.

## Naming Guidance

- Use `*_at` for timestamps, `*_date` for dates, and `*_id` for local foreign keys.
- Use `topdesk_id` for stable external IDs and `topdesk_number` for human-facing numbers.
- Use `is_*` for booleans.
- Use `Fact*` and `Dim*` names in Power BI semantic models.
- Use business names in report visuals and technical names in database objects.
