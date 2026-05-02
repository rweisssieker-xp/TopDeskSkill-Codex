# Live Demo Test Results

Test target:

```text
https://usatopdesktrial2.topdesk.net
```

Configured user:

```text
raulm09
```

No password, token, or application password is stored in this repository.

## Results

REST API with Basic authentication using the user plus application password works:

| Endpoint | Status | Result |
| --- | ---: | --- |
| `/tas/api/incidents` | 206 | JSON array, first page returns 10 records |
| `/tas/api/persons` | 206 | JSON array, first page returns 10 records |
| `/tas/api/operatorgroups` | 206 | JSON array, first page returns 10 records |
| `/tas/api/branches` | 200 | JSON array, returns branch list |

Reporting OData is present but not permitted for this credential:

| Endpoint | Status | Result |
| --- | ---: | --- |
| `/services/reporting/v2/odata/$metadata` | 403 | Authenticated but not authorized |

Bearer-token authentication did not work for this token; use Basic authentication with `TOPDESK_USERNAME` and `TOPDESK_APP_PASSWORD`.

## Skill Impact

- REST/API, Python, PowerShell, tenant-mapping, data-quality, and workflow skills can be tested against live REST endpoints.
- Power BI/OData metadata parsing still needs a credential with reporting OData permission or a downloaded `$metadata` file.
- The MCP helper can read REST endpoints when `TOPDESK_BASE_URL`, `TOPDESK_USERNAME`, and `TOPDESK_APP_PASSWORD` are set at runtime.

## REST Tenant Profile

`topdesk-tenant-mapping/scripts/profile_topdesk_rest.py` was tested against the demo instance with a limited sample.

Generated local artifacts under ignored `tenant-output/usatopdesktrial2-rest/`:

- `rest_tenant_profile.md`
- `rest_field_catalog.csv`
- `data_quality_findings.csv`
- JSON snapshots for incidents, persons, operator groups, and branches

Sample profile counts:

| Entity | Rows profiled |
| --- | ---: |
| incidents | 100 |
| persons | 100 |
| operatorgroups | 12 |
| branches | 100 |

Readiness summary:

- Power BI candidate fields: 27
- AI candidate fields: 13
- PII-risk fields: 17
- Data-quality findings: 24

## Follow-on Artifact Tests

The generated tenant profile artifacts were used to test additional offline skills:

| Skill | Input | Result |
| --- | --- | --- |
| `topdesk-powerbi-dax` | `rest_field_catalog.csv` | Generated 5 starter DAX measures and a measure catalog |
| `topdesk-sla-optimizer` | `snapshots/incidents.json` | Analyzed 100 incidents and produced 193 SLA/backlog findings |
| `topdesk-compliance-pii` | `rest_field_catalog.csv` | Reviewed 167 fields and produced 22 PII findings |

Observed demo data signals:

- 100 sampled incidents were open.
- 99 sampled incidents had no operator group in the profiled payload.
- 94 sampled incidents had no priority in the profiled payload.
- PII review found 7 high-severity field risks.
