# TOPdesk API and Integration Reference

Use this file for API, action sequence, import/export, automation, and integration tasks. Verify exact endpoints in the official TOPdesk API documentation for the target environment/version.

For deployment, monitoring, retry runbooks, environments, and operational ownership, load `architecture-operations.md`.

## General Principles

- Use a dedicated API user with least-privilege permission groups.
- Treat TOPdesk instance URL, credentials, application passwords, and API tokens as secrets.
- Preserve both TOPdesk `id`/UUID-style identifiers and human-facing numbers where available.
- Make imports idempotent with external IDs or deterministic matching keys.
- Log request IDs, payload summaries, response status, and TOPdesk identifiers, but do not log secrets.
- Retry only safe transient failures; avoid blind retry of non-idempotent create calls.

## Common API Areas

- Incident API: create/update incidents, actions/replies, attachments, links, and status/assignment updates.
- Change Management API: create changes and activities, update workflow fields, link persons/assets where supported.
- Asset Management API: asset templates, assets, fields, uploads, and asset relations.
- Knowledge Base API: knowledge items and publication/search behavior; note that older knowledge endpoints may be deprecated in newer releases.
- Supporting Files APIs: persons, operators, branches, departments, suppliers, rooms/locations, categories, and reference data.
- OData/reporting: read-optimized exports for BI and reporting; relationship names can differ from REST/API concepts.
- Action Sequences: TOPdesk-side automation that can call external endpoints or chain TOPdesk actions.

## Integration Design Checklist

1. Identify the system of record for each entity.
2. Decide sync direction: TOPdesk to app, app to TOPdesk, or bidirectional.
3. Define identity mapping: `topdesk_id`, `topdesk_number`, `external_id`, source system, and unique constraints.
4. Define payload mapping and field transformations.
5. Define permission model for the API user.
6. Define error handling: validation failures, missing references, duplicates, rate limits, authentication failures.
7. Define replay/idempotency behavior.
8. Define observability: integration logs, dead-letter queue, reconciliation reports.

## Payload Mapping Pattern

When mapping TOPdesk data into a local schema, document each field:

| Local field | TOPdesk source | Transform | Required | Notes |
| --- | --- | --- | --- | --- |
| `topdesk_id` | API `id` | string/UUID | yes | Stable integration key |
| `number` | API ticket/change number | string | often | Human-facing reference |
| `caller_person_id` | caller/person object | lookup by `id` | module-dependent | May require pre-sync |
| `branch_id` | branch object | lookup by `id` | recommended | Important for reporting |
| `status_id` | status field | lookup/map | yes | Preserve history separately |
| `updated_at` | modification date | timezone-normalized timestamp | yes | Needed for incremental sync |

## Endpoint Verification

Before writing production code, verify:

- Exact endpoint path and HTTP method in official TOPdesk API docs.
- Required permissions for the API user.
- Whether identifiers are UUIDs, numbers, or both.
- Whether PATCH supports partial update for the target fields.
- Attachment upload format and size limits.
- HTML/text support for memo/action fields.
- Pagination, filtering, sorting, and date format behavior.

## OData and BI Notes

- OData table names and relationships may not mirror REST endpoint names.
- Some relationships require bridge/link tables or nested navigation properties.
- Person groups, categories, and module-specific supporting files may need separate mapping tables.
- For BI models, prefer documented IDs and stable keys rather than display names.
- For Power BI-specific modeling, DAX, refresh, and dashboard layout, load `powerbi.md`.
- For tenant-specific OData metadata discovery and field mapping, load `odata-mapping.md`.
- For integration test scenarios and reconciliation checks, load `testing-validation.md`.
