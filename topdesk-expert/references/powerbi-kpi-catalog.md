# TOPdesk Power BI KPI Catalog

Use this file when defining or documenting TOPdesk Power BI KPIs.

## Incident KPIs

| KPI | Definition | Date role | Notes |
| --- | --- | --- | --- |
| Created incidents | Count of incidents by creation date | Created date | Exclude deleted records if documented |
| Closed incidents | Count of incidents closed in period | Closed date | Clarify cancelled tickets |
| Open backlog | Incidents open at selected point in time | Snapshot/as-of date | Historical backlog requires snapshot or as-of calculation |
| SLA compliance % | SLA-met closed incidents / SLA-eligible closed incidents | Closed date | Clarify pause and business-hours logic |
| First response hours | Created timestamp to first qualifying public operator response | Created/first response | Define qualifying action |
| Resolution hours | Created timestamp to resolved/closed timestamp | Closed date | Calendar vs business hours must be explicit |
| Reopen rate % | Reopened incidents / closed incidents | Closed date | Use status history or reopen count |
| Reassignment rate % | Incidents with more than one assignment / incidents | Created date | Assignment group or operator must be specified |
| Near breach count | Open incidents with target within threshold | Current/as-of date | Common threshold: 4 business hours |

## Change KPIs

| KPI | Definition | Notes |
| --- | --- | --- |
| Changes created | Count of changes by creation date | Split by standard/simple/extensive |
| Changes completed | Count by completion date | Clarify cancelled/rejected |
| Approval duration | Request/approval start to final approval | Use activities/approval facts |
| Overdue activities | Open activities past due date | Include owner group/operator |
| Emergency change rate | Emergency/unplanned changes / total changes | Requires reliable type/risk field |
| Failed/reverted changes | Changes marked failed, reverted, or linked to incident | Define source field |

## Asset KPIs

| KPI | Definition | Notes |
| --- | --- | --- |
| Incidents by asset type | Incident count linked to asset type | Requires incident-asset bridge |
| Problematic assets | Assets with incident count above threshold | Rolling window recommended |
| Assets missing owner | Assets without owner/person | Data-quality KPI |
| Assets past lifecycle | Assets beyond lifecycle end date | Needs lifecycle dates |
| Change impact by asset type | Changes linked to assets by type | Requires change-asset bridge |

## Knowledge KPIs

| KPI | Definition | Notes |
| --- | --- | --- |
| Article usage | Count of linked/viewed articles | Depends on available telemetry |
| Deflection candidates | High-volume repeated incidents without knowledge | Use category/resolution similarity |
| Articles overdue review | Published articles past review date | Governance KPI |
| Knowledge-linked resolution % | Closed incidents with linked knowledge / closed incidents | Clarify manual vs suggested link |

## AI/KI KPIs

| KPI | Definition | Notes |
| --- | --- | --- |
| AI suggestions | Count of generated suggestions | By type/model/version |
| Acceptance rate % | Accepted suggestions / generated suggestions | Track by operator/group/category |
| Override rate % | Edited or rejected suggestions / generated suggestions | Include override reason |
| Average confidence | Average confidence by suggestion type | Compare confidence to acceptance |
| Citation coverage % | Response drafts with citations / drafts | RAG quality |
| Deflection rate % | Self-service sessions resolved without ticket / eligible sessions | Requires SSP/chat telemetry |

## Data Quality KPIs

| KPI | Definition | Notes |
| --- | --- | --- |
| Missing branch count | Incidents/assets/persons without branch | RLS risk |
| Missing category count | Incidents without category/subcategory | Reporting/routing risk |
| Unknown dimension count | Facts mapped to unknown dimension member | Model quality |
| Duplicate persons/assets | Candidate duplicates by email/employee/serial | Cleanup backlog |
| Reconciliation delta | Power BI count - TOPdesk trusted count | Must be explained before publish |
