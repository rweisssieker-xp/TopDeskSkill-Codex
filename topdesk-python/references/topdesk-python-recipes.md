# TOPdesk Python Recipes

## CSV Profiling

- Use `csv.DictReader`.
- Track row count, blank counts, distinct counts, and sample values per column.
- Emit JSON for automation and Markdown for human review.
- Keep PII samples short and configurable.

## OData Metadata Parsing

- Parse EntityTypes, Properties, NavigationProperties, and EntitySets.
- Normalize names but preserve original casing.
- Output field catalogs with entity, field, type, nullable, and relationship columns.

## API Client

- Keep authentication injectable.
- Add timeout defaults.
- Implement small retry wrappers for transient status codes.
- Do not log full payloads by default.

## Data Quality Findings

- Use stable severity values: `info`, `warning`, `error`.
- Include `entity`, `field`, `rule`, `message`, and optional `sample`.
- Prefer deterministic sorting so diffs are reviewable.

