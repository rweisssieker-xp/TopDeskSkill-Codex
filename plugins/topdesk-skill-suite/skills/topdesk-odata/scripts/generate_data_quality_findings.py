#!/usr/bin/env python3
"""Generate basic data-quality findings from profile_topdesk_export.py output."""

from __future__ import annotations

import argparse
import csv


IMPORTANT_KEYWORDS = {
    "caller": "workflow/reporting",
    "person": "workflow/reporting",
    "branch": "security/rls",
    "category": "routing/reporting",
    "status": "lifecycle/reporting",
    "priority": "sla/reporting",
    "operator": "assignment/reporting",
    "group": "assignment/reporting",
    "asset": "asset/reporting",
    "closed": "lifecycle/reporting",
    "created": "date/reporting",
    "target": "sla/reporting",
}


def severity(empty_count: int, row_count: int, important: bool) -> str:
    if row_count == 0:
        return "low"
    empty_ratio = empty_count / row_count
    if important and empty_ratio >= 0.2:
        return "high"
    if important and empty_ratio > 0:
        return "medium"
    if empty_ratio >= 0.5:
        return "medium"
    return "low"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate data-quality findings from column profile CSV.")
    parser.add_argument("column_profile", help="Path to column_profile.csv")
    parser.add_argument("--out", required=True, help="Output findings CSV")
    args = parser.parse_args()

    findings: list[dict[str, str]] = []
    with open(args.column_profile, newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            column = row["column"]
            lower = column.lower()
            row_count = int(row["row_count"])
            empty_count = int(row["empty_count"])
            distinct_count = int(row["distinct_count"])
            matched = [value for key, value in IMPORTANT_KEYWORDS.items() if key in lower]
            important = bool(matched)
            if empty_count > 0 or distinct_count <= 1 or important:
                findings.append(
                    {
                        "column": column,
                        "finding": "missing values" if empty_count > 0 else "review important field",
                        "severity": severity(empty_count, row_count, important),
                        "impact": matched[0] if matched else "data-quality",
                        "suggested_fix": "Map, backfill, or create unknown member handling",
                        "profile_summary": f"{empty_count} empty of {row_count}; {distinct_count} distinct",
                    }
                )

    with open(args.out, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["column", "finding", "severity", "impact", "suggested_fix", "profile_summary"],
        )
        writer.writeheader()
        writer.writerows(findings)

    print(f"Wrote {len(findings)} findings to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
