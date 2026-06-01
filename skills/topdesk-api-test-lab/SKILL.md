---
name: topdesk-api-test-lab
description: Use when testing live TOPdesk REST/API access, authentication, endpoint availability, paging behavior, response status codes, payload shapes, demo tenants, smoke tests, regression checks, and API readiness before building Power BI, Python, PowerShell, or AI features.
---

# TOPdesk API Test Lab

Use this skill before depending on a TOPdesk tenant for automation, Power BI refresh, migration, or AI workflows.

## Workflow

1. Confirm the base URL, authentication mode, and endpoint list without storing secrets.
2. Run smoke tests for status code, content type, JSON shape, row count, paging, and latency.
3. Separate authentication failures from permission failures and missing endpoints.
4. Record what works, what is blocked, and which features are safe to test live.
5. Feed successful endpoint paths into tenant mapping, Power BI query design, Python, and PowerShell skills.

## Scripts

- Use `scripts/smoke_topdesk_api.py` with `TOPDESK_BASE_URL`, `TOPDESK_USERNAME`, and `TOPDESK_APP_PASSWORD`.
- Optional: pass `--endpoint name=/tas/api/path` to test additional tenant endpoints.

