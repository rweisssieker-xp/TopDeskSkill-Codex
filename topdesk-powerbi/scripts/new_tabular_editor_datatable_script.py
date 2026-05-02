#!/usr/bin/env python3
"""Generate a Tabular Editor 2 script that embeds CSV tables as DAX DATATABLEs."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Sequence


TABLES = [
    "FactIncident",
    "DimDate",
    "DimPerson",
    "DimOperatorGroup",
    "DimBranch",
    "DataQualityFindings",
    "SLAFinding",
    "PIIFinding",
]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate TOPdesk Tabular Editor DATATABLE script")
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    return parser.parse_args(argv)


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        return list(reader.fieldnames or []), rows


def dax_string(value: str) -> str:
    return '"' + (value or "").replace('"', '""').replace("\r", " ").replace("\n", " ") + '"'


def datatable_expression(columns: list[str], rows: list[dict[str, str]]) -> str:
    column_defs = ",\n        ".join(f"{dax_string(column)}, STRING" for column in columns)
    row_defs = []
    for row in rows:
        values = ", ".join(dax_string(row.get(column, "")) for column in columns)
        row_defs.append("        { " + values + " }")
    if not row_defs:
        row_defs.append("        { " + ", ".join(dax_string("") for _ in columns) + " }")
    return "DATATABLE(\n        " + column_defs + ",\n        {\n" + ",\n".join(row_defs) + "\n        }\n    )"


def cs_string(value: str) -> str:
    return '@"' + value.replace('"', '""') + '"'


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    chunks: list[str] = [
        "// Generated Tabular Editor 2 script: TOPdesk demo model with embedded DATATABLEs.",
        "var generatedTables = new [] { " + ", ".join('"' + table + '"' for table in TABLES) + " };",
        "foreach (var tableName in generatedTables) { if (Model.Tables.Contains(tableName)) Model.Tables[tableName].Delete(); }",
        "",
    ]
    for table in TABLES:
        columns, rows = read_csv(args.data_dir / f"{table}.csv")
        chunks.append(f'var {table} = Model.AddCalculatedTable("{table}", {cs_string(datatable_expression(columns, rows))});')
        chunks.append(f'{table}.Description = "Generated TOPdesk demo table embedded as DAX DATATABLE.";')
        chunks.append("")

    chunks.append("// Relationships are added after calculated tables are processed and columns are materialized.")
    chunks.append("")

    measures = [
        ("FactIncident", "Incident Count", "COUNTROWS ( FactIncident )", "Core", "#,0"),
        ("FactIncident", "Open Incident Count", 'CALCULATE ( [Incident Count], FactIncident[IsOpen] = "true" )', "Core", "#,0"),
        ("FactIncident", "Closed Incident Count", 'CALCULATE ( [Incident Count], FactIncident[IsClosed] = "true" )', "Core", "#,0"),
        ("FactIncident", "Missing Target Date Count", 'CALCULATE ( [Incident Count], FactIncident[HasTargetDate] = "false" )', "SLA", "#,0"),
        ("FactIncident", "Missing Target Date %", "DIVIDE ( [Missing Target Date Count], [Incident Count] )", "SLA", "0.0%"),
        ("FactIncident", "Unrouted Incident Count", 'CALCULATE ( [Incident Count], FactIncident[HasOperatorGroup] = "false" )', "Routing", "#,0"),
        ("FactIncident", "Routing Coverage %", 'DIVIDE ( CALCULATE ( [Incident Count], FactIncident[HasOperatorGroup] = "true" ), [Incident Count] )', "Routing", "0.0%"),
        ("FactIncident", "Priority Coverage %", 'DIVIDE ( CALCULATE ( [Incident Count], FactIncident[HasPriority] = "true" ), [Incident Count] )', "Data Quality", "0.0%"),
        ("FactIncident", "Category Coverage %", 'DIVIDE ( CALCULATE ( [Incident Count], FactIncident[HasCategory] = "true" ), [Incident Count] )', "Data Quality", "0.0%"),
        ("DataQualityFindings", "Data Quality Findings", "COUNTROWS ( DataQualityFindings )", "Data Quality", "#,0"),
        ("SLAFinding", "SLA Findings", "COUNTROWS ( SLAFinding )", "SLA", "#,0"),
        ("PIIFinding", "PII Findings", "COUNTROWS ( PIIFinding )", "Compliance", "#,0"),
        ("PIIFinding", "High PII Findings", 'CALCULATE ( [PII Findings], PIIFinding[severity] = "high" )', "Compliance", "#,0"),
    ]
    for table, name, expression, folder, fmt in measures:
        chunks.append(f'Model.Tables["{table}"].AddMeasure("{name}", {cs_string(expression)}, "{folder}").FormatString = "{fmt}";')

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(chunks) + "\n", encoding="utf-8")
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
