# Tenant Drift Reference

## Drift Types

| Drift | Meaning | Typical impact |
| --- | --- | --- |
| Added field | New field appears in current evidence. | Model extension, prompt context, data-quality opportunity. |
| Removed field | Baseline field missing in current evidence. | Broken Power BI query, prompt mapping, automation payload. |
| Type change | Field type differs. | DAX/Power Query conversion, validation, schema contract. |
| Label change | UI/business label differs. | Documentation, report labels, operator training. |
| Required/nullability change | Required or nullable shape differs. | Data-quality rules, forms, integration validation. |
| Option change | Category/status/priority/group option changed. | Filters, routing, RLS, AI classification labels. |

## Impact Classes

- `power_bi`: field, type, label, KPI dependency, or filter changes.
- `ai`: prompt context, classification label, retrieval source, or feedback field changes.
- `automation`: payload, trigger field, endpoint, idempotency key, or required value changes.
- `security`: person, caller, operator, branch, permission, PII, or RLS-related changes.
- `operations`: owner, group, status, category, refresh, or runbook changes.

## Remediation Pattern

Use the output as a decision-ready finding:

```text
finding: Field removed from current tenant catalog.
evidence: Baseline had incidents.targetDate, current catalog does not.
business impact: SLA-risk measures and breach filters may fail or change meaning.
risk: High for Power BI and operations.
recommended action: Validate tenant field mapping and update KPI dependency map.
owner: BI owner plus TOPdesk application manager.
validation metric: Reconciled open incidents with target date.
```
