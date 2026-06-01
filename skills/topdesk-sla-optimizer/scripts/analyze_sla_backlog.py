#!/usr/bin/env python3
"""Analyze TOPdesk incident snapshots for SLA and backlog readiness."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze TOPdesk incidents for SLA and backlog risks")
    parser.add_argument("--incidents", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    return parser.parse_args(argv)


def load_rows(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("Incident snapshot must be a JSON array")
    return [row for row in payload if isinstance(row, dict)]


def label(value: Any) -> str:
    if value is None or value == "":
        return "(empty)"
    if isinstance(value, dict):
        for key in ("name", "id", "number", "groupName"):
            if key in value and value[key]:
                return str(value[key])
        return json.dumps(value, ensure_ascii=False, sort_keys=True)[:120]
    return str(value)


def parse_date(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    text = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed


def build_findings(rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    now = datetime.now(timezone.utc)
    findings: list[dict[str, str]] = []
    for row in rows:
        number = label(row.get("number") or row.get("id"))
        closed = bool(row.get("closed"))
        target = parse_date(row.get("targetDate"))
        priority = label(row.get("priority"))
        operator_group = label(row.get("operatorGroup"))
        if not closed and not target:
            findings.append(
                {
                    "incident": number,
                    "severity": "high",
                    "finding": "open incident without target date",
                    "priority": priority,
                    "operator_group": operator_group,
                    "action": "Set or validate SLA target date.",
                }
            )
        if not closed and target and target < now:
            findings.append(
                {
                    "incident": number,
                    "severity": "high",
                    "finding": "open incident past target date",
                    "priority": priority,
                    "operator_group": operator_group,
                    "action": "Review breach, ownership, and next action.",
                }
            )
        if not closed and operator_group == "(empty)":
            findings.append(
                {
                    "incident": number,
                    "severity": "medium",
                    "finding": "open incident without operator group",
                    "priority": priority,
                    "operator_group": operator_group,
                    "action": "Route to an accountable group.",
                }
            )
    return findings


def write_report(out_dir: Path, rows: list[dict[str, Any]], findings: list[dict[str, str]]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    group_counts = Counter(label(row.get("operatorGroup")) for row in rows)
    priority_counts = Counter(label(row.get("priority")) for row in rows)
    open_count = sum(1 for row in rows if not bool(row.get("closed")))
    lines = [
        "# TOPdesk SLA Backlog Analysis",
        "",
        f"- Incidents analyzed: {len(rows)}",
        f"- Open incidents: {open_count}",
        f"- Findings: {len(findings)}",
        "",
        "## Operator Group Distribution",
        "",
    ]
    for name, count in group_counts.most_common(10):
        lines.append(f"- {name}: {count}")
    lines.extend(["", "## Priority Distribution", ""])
    for name, count in priority_counts.most_common(10):
        lines.append(f"- {name}: {count}")
    (out_dir / "sla-backlog-analysis.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    with (out_dir / "sla-findings.csv").open("w", newline="", encoding="utf-8") as handle:
        fieldnames = ["incident", "severity", "finding", "priority", "operator_group", "action"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(findings)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    rows = load_rows(args.incidents)
    findings = build_findings(rows)
    write_report(args.out_dir, rows, findings)
    print(f"Wrote SLA analysis to {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

