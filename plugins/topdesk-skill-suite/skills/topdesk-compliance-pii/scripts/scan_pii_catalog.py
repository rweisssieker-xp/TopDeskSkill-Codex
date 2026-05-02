#!/usr/bin/env python3
"""Scan a TOPdesk field catalog for likely PII exposure."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Sequence


PII_KEYWORDS = {
    "name": "identity",
    "email": "contact",
    "mail": "contact",
    "phone": "contact",
    "mobile": "contact",
    "address": "location",
    "caller": "identity",
    "person": "identity",
    "login": "account",
    "employee": "employment",
    "request": "free text",
    "description": "free text",
}


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan TOPdesk field catalog for PII risks")
    parser.add_argument("--field-catalog", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    return parser.parse_args(argv)


def classify(field: str) -> tuple[str, str]:
    lower = field.lower()
    for keyword, category in PII_KEYWORDS.items():
        if keyword in lower:
            if category == "free text":
                return category, "high"
            if category in {"contact", "account"}:
                return category, "high"
            return category, "medium"
    return "", ""


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    with args.field_catalog.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    findings: list[dict[str, str]] = []
    for row in rows:
        category, severity = classify(row.get("field", ""))
        if not category and row.get("pii_risk") != "yes":
            continue
        findings.append(
            {
                "entity": row.get("entity", ""),
                "field": row.get("field", ""),
                "category": category or "possible pii",
                "severity": severity or "medium",
                "non_empty_count": row.get("non_empty_count", ""),
                "recommendation": "Mask, aggregate, remove from broad models, or restrict with RLS/OLS before report or AI use.",
            }
        )

    with (args.out_dir / "pii-field-findings.csv").open("w", newline="", encoding="utf-8") as handle:
        fieldnames = ["entity", "field", "category", "severity", "non_empty_count", "recommendation"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(findings)

    high_count = sum(1 for item in findings if item["severity"] == "high")
    lines = [
        "# TOPdesk PII Review",
        "",
        f"- Fields reviewed: {len(rows)}",
        f"- PII findings: {len(findings)}",
        f"- High severity fields: {high_count}",
        "",
        "Do not publish raw sample values unless they are explicitly approved demo data.",
    ]
    (args.out_dir / "pii-review.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(findings)} PII findings to {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

