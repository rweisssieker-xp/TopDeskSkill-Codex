#!/usr/bin/env python3
"""Profile TOPdesk CSV exports for mapping and data-quality work.

Usage:
  python profile_topdesk_export.py incidents.csv --out profile

The script emits column statistics that help map tenant exports to the
canonical schema and Power BI model.
"""

from __future__ import annotations

import argparse
import csv
import os
from collections import Counter
from datetime import datetime


DATE_FORMATS = (
    "%Y-%m-%d",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M:%S%z",
    "%d.%m.%Y",
    "%d.%m.%Y %H:%M",
    "%d/%m/%Y",
    "%m/%d/%Y",
)


def parse_bool(value: str) -> bool | None:
    normalized = value.strip().lower()
    if normalized in {"true", "yes", "ja", "j", "1", "x"}:
        return True
    if normalized in {"false", "no", "nein", "n", "0"}:
        return False
    return None


def parse_date(value: str) -> bool:
    text = value.strip()
    if not text:
        return False
    for fmt in DATE_FORMATS:
        try:
            datetime.strptime(text, fmt)
            return True
        except ValueError:
            pass
    return False


def infer_type(values: list[str]) -> str:
    sample = [value.strip() for value in values if value.strip()]
    if not sample:
        return "empty"

    bool_count = sum(parse_bool(value) is not None for value in sample)
    int_count = 0
    number_count = 0
    date_count = 0
    for value in sample:
        normalized = value.replace(",", ".")
        try:
            int(normalized)
            int_count += 1
        except ValueError:
            pass
        try:
            float(normalized)
            number_count += 1
        except ValueError:
            pass
        if parse_date(value):
            date_count += 1

    threshold = max(1, int(len(sample) * 0.8))
    if bool_count >= threshold:
        return "boolean"
    if int_count >= threshold:
        return "integer"
    if number_count >= threshold:
        return "number"
    if date_count >= threshold:
        return "date_or_datetime"
    return "text"


def profile_csv(path: str, delimiter: str | None = None) -> tuple[int, list[dict[str, str]]]:
    with open(path, newline="", encoding="utf-8-sig") as handle:
        sample = handle.read(4096)
        handle.seek(0)
        dialect = csv.Sniffer().sniff(sample) if delimiter is None else csv.excel
        if delimiter is not None:
            dialect.delimiter = delimiter
        reader = csv.DictReader(handle, dialect=dialect)
        columns = reader.fieldnames or []
        values_by_column: dict[str, list[str]] = {column: [] for column in columns}
        row_count = 0
        for row in reader:
            row_count += 1
            for column in columns:
                values_by_column[column].append(row.get(column, ""))

    profile_rows: list[dict[str, str]] = []
    for column, values in values_by_column.items():
        non_empty = [value for value in values if value.strip()]
        unique_values = Counter(non_empty)
        top_values = "; ".join(f"{value} ({count})" for value, count in unique_values.most_common(5))
        profile_rows.append(
            {
                "column": column,
                "inferred_type": infer_type(values),
                "row_count": str(row_count),
                "non_empty_count": str(len(non_empty)),
                "empty_count": str(row_count - len(non_empty)),
                "distinct_count": str(len(unique_values)),
                "top_values": top_values[:1000],
            }
        )
    return row_count, profile_rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Profile a TOPdesk CSV export.")
    parser.add_argument("csv_file", help="Path to CSV export")
    parser.add_argument("--out", default="export_profile", help="Output directory")
    parser.add_argument("--delimiter", help="Optional delimiter override, e.g. ';'")
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)
    row_count, profile_rows = profile_csv(args.csv_file, args.delimiter)
    out_path = os.path.join(args.out, "column_profile.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "column",
                "inferred_type",
                "row_count",
                "non_empty_count",
                "empty_count",
                "distinct_count",
                "top_values",
            ],
        )
        writer.writeheader()
        writer.writerows(profile_rows)

    print(f"Profiled {row_count} rows")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
