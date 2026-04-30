#!/usr/bin/env python3
"""Generate a starter Power BI implementation pack from simple CSV specs.

Inputs:
  --tables tables.csv with columns:
     table,role,source_entity,key,display,incremental_column,rls_column
  --measures measures.csv with columns:
     name,expression,folder,description

Outputs:
  powerquery/<table>.pq
  dax/measures.dax
  tmdl/model.tmdl
  REPORT_SPEC.md
  MAINTENANCE_RUNBOOK.md
"""

from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path


def read_csv(path: str | None) -> list[dict[str, str]]:
    if not path:
        return []
    with open(path, newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def safe_name(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "_-" else "_" for ch in value).strip("_")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def powerquery_for_table(row: dict[str, str]) -> str:
    table = row.get("table", "Table")
    entity = row.get("source_entity") or table
    incremental = row.get("incremental_column", "")
    filter_step = ""
    previous_step = "Typed"
    if incremental:
        filter_step = f''',
    Filtered = Table.SelectRows(
        Typed,
        each [{incremental}] >= RangeStart and [{incremental}] < RangeEnd
    )'''
        previous_step = "Filtered"

    return f'''// Generated starter query for {table}.
// Parameters expected: TopdeskODataUrl, RangeStart, RangeEnd.
let
    Source = OData.Feed(TopdeskODataUrl, null, [Implementation="2.0"]),
    Entity = Source{{[Name="{entity}", Signature="table"]}}[Data],
    Typed = Entity{filter_step}
in
    {previous_step}
'''


def dax_measure(row: dict[str, str]) -> str:
    name = row.get("name", "Measure")
    expression = row.get("expression", "BLANK()")
    description = row.get("description", "")
    lines = []
    if description:
        lines.append(f"-- {description}")
    lines.append(f"{name} :=")
    lines.append(expression)
    return "\n".join(lines)


def tmdl_model(tables: list[dict[str, str]]) -> str:
    lines = [
        "model Model",
        "\tculture: en-US",
        "\tdefaultPowerBIDataSourceVersion: powerBI_V3",
        "",
    ]
    for row in tables:
        table = row.get("table", "Table")
        key = row.get("key", "")
        lines.append(f"table {table}")
        lines.append("\tlineageTag: generated")
        if key:
            lines.append(f"\t// Key column: {key}")
        if row.get("role"):
            lines.append(f"\t// Role: {row['role']}")
        if row.get("rls_column"):
            lines.append(f"\t// RLS candidate: {row['rls_column']}")
        lines.append("")
    return "\n".join(lines)


def report_spec(tables: list[dict[str, str]], measures: list[dict[str, str]]) -> str:
    lines = [
        "# Generated TOPdesk Power BI Pack",
        "",
        "## Tables",
        "",
        "| Table | Role | Source entity | Key | Incremental column | RLS column |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in tables:
        lines.append(
            f"| {row.get('table','')} | {row.get('role','')} | {row.get('source_entity','')} | {row.get('key','')} | {row.get('incremental_column','')} | {row.get('rls_column','')} |"
        )
    lines.extend(["", "## Measures", "", "| Measure | Folder | Description |", "| --- | --- | --- |"])
    for row in measures:
        lines.append(f"| {row.get('name','')} | {row.get('folder','')} | {row.get('description','')} |")
    lines.extend(
        [
            "",
            "## Required Manual Steps",
            "",
            "1. Verify source entity names against TOPdesk OData metadata.",
            "2. Paste Power Query files into Power BI or Dataflow queries.",
            "3. Create relationships and mark `DimDate` as the date table.",
            "4. Add DAX measures.",
            "5. Configure RLS and test named users.",
            "6. Reconcile counts with TOPdesk selections/exports.",
        ]
    )
    return "\n".join(lines) + "\n"


def maintenance_runbook() -> str:
    return """# Power BI Maintenance Runbook

## Refresh Failure

1. Check gateway/credential status.
2. Check TOPdesk OData availability.
3. Check schema drift in source entities.
4. Refresh staging queries.
5. Reconcile row counts before publishing.

## Schema Drift

1. Re-run tenant metadata/catalog generation.
2. Compare field catalog with current model.
3. Update M queries and model fields.
4. Re-run validation and reconciliation.

## Data Quality

1. Review unknown dimensions and missing keys.
2. Assign cleanup owner.
3. Track issue trend in data-quality page.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate TOPdesk Power BI implementation pack.")
    parser.add_argument("--tables", help="CSV table spec")
    parser.add_argument("--measures", help="CSV measure spec")
    parser.add_argument("--out", required=True, help="Output directory")
    args = parser.parse_args()

    out = Path(args.out)
    tables = read_csv(args.tables)
    measures = read_csv(args.measures)

    for row in tables:
        table = row.get("table", "Table")
        write(out / "powerquery" / f"{safe_name(table)}.pq", powerquery_for_table(row))

    write(out / "dax" / "measures.dax", "\n\n".join(dax_measure(row) for row in measures) + "\n")
    write(out / "tmdl" / "model.tmdl", tmdl_model(tables))
    write(out / "REPORT_SPEC.md", report_spec(tables, measures))
    write(out / "MAINTENANCE_RUNBOOK.md", maintenance_runbook())

    print(f"Wrote Power BI pack to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
