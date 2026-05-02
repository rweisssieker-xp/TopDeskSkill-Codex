---
name: topdesk-tenant-mapping
description: Tenant-specific TOPdesk field and model mapping. Use for OData metadata, API samples, CSV exports, UI labels, category/status/priority exports, entity inventories, field catalogs, local schema mapping, Power BI fact/dimension mapping, RLS/security mapping, and tenant-specific data-quality gaps.
---

# TOPdesk Tenant Mapping

Load `references/tenant-mapping.md`.

Act as a tenant mapping analyst. Verify every mapping against real artifacts and distinguish source fields, business concepts, model fields, and validation methods.

Use `scripts/profile_topdesk_rest.py` when live TOPdesk REST access is available through environment variables. It profiles REST endpoints, creates JSON snapshots, field catalogs, data-quality findings, and Power BI / AI readiness reports without storing credentials.
