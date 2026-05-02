---
name: topdesk-powerbi-dax
description: Use when creating, reviewing, or standardizing Power BI DAX measures for TOPdesk incidents, SLAs, backlog, routing, operators, branches, AI governance, adoption, quality, cost, risk, and executive service-management dashboards.
---

# TOPdesk Power BI DAX

Use this skill after the semantic model grain is known and before visuals are finalized.

## Workflow

1. Define each measure with business meaning, grain, date basis, and exclusions.
2. Prefer explicit measures for counts, backlog, SLA, MTTA, MTTR, reopen rate, routing quality, and AI adoption.
3. Keep date intelligence tied to conformed `DimDate` and clearly named date roles.
4. Use disconnected parameter tables for KPI switching only when it improves report UX.
5. Validate every measure against REST/API samples or exported reconciliation totals.

## Assets

- Use `assets/topdesk-core-measures.dax` as a starter measure pack.

## Scripts

- Use `scripts/new_dax_measure_pack.py` with a tenant field catalog to generate a customized DAX starter pack and measure catalog.

