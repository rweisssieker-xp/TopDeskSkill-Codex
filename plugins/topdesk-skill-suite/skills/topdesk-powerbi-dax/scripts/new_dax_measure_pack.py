#!/usr/bin/env python3
"""Generate a TOPdesk DAX starter pack from a tenant field catalog."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Sequence


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create TOPdesk DAX measure starter files")
    parser.add_argument("--field-catalog", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    return parser.parse_args(argv)


def read_fields(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def has_field(rows: list[dict[str, str]], entity: str, field: str) -> bool:
    return any(row.get("entity") == entity and row.get("field") == field for row in rows)


def measure_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    measures = [
        {
            "measure": "Incident Count",
            "table": "FactIncident",
            "expression": "COUNTROWS ( FactIncident )",
            "business_definition": "Number of incident records in the current filter context.",
        }
    ]
    if has_field(rows, "incidents", "closed"):
        measures.append(
            {
                "measure": "Closed Incident Count",
                "table": "FactIncident",
                "expression": "CALCULATE ( [Incident Count], KEEPFILTERS ( FactIncident[closed] = TRUE () ) )",
                "business_definition": "Incidents marked closed in TOPdesk.",
            }
        )
    if has_field(rows, "incidents", "targetDate"):
        measures.append(
            {
                "measure": "Incidents With Target Date",
                "table": "FactIncident",
                "expression": "CALCULATE ( [Incident Count], NOT ISBLANK ( FactIncident[targetDate] ) )",
                "business_definition": "Incidents with a populated target date for SLA or planning analysis.",
            }
        )
    if has_field(rows, "incidents", "operatorGroup"):
        measures.append(
            {
                "measure": "Operator Group Routed Incidents",
                "table": "FactIncident",
                "expression": "CALCULATE ( [Incident Count], NOT ISBLANK ( FactIncident[operatorGroup] ) )",
                "business_definition": "Incidents assigned to an operator group.",
            }
        )
    if has_field(rows, "incidents", "priority"):
        measures.append(
            {
                "measure": "Priority Coverage %",
                "table": "FactIncident",
                "expression": "DIVIDE ( CALCULATE ( [Incident Count], NOT ISBLANK ( FactIncident[priority] ) ), [Incident Count] )",
                "business_definition": "Share of incidents with priority populated.",
            }
        )
    return measures


def write_outputs(out_dir: Path, measures: list[dict[str, str]]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    dax_lines: list[str] = []
    for item in measures:
        dax_lines.extend([f"-- {item['business_definition']}", f"{item['measure']} = {item['expression']}", ""])
    (out_dir / "topdesk-measures.dax").write_text("\n".join(dax_lines), encoding="utf-8")
    with (out_dir / "measure-catalog.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["measure", "table", "business_definition", "expression"])
        writer.writeheader()
        writer.writerows(measures)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    rows = read_fields(args.field_catalog)
    measures = measure_rows(rows)
    write_outputs(args.out_dir, measures)
    print(f"Wrote {len(measures)} measures to {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

