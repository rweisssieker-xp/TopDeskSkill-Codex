#!/usr/bin/env python3
"""Compare two TOPdesk catalog CSV files and write drift findings."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Sequence


KEY_COLUMNS = ("entity", "entity_set", "table", "endpoint", "field", "property", "name", "option")
TYPE_COLUMNS = ("type", "data_type", "edm_type")
LABEL_COLUMNS = ("label", "display_name", "business_label")
NULL_COLUMNS = ("nullable", "required", "is_required")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare TOPdesk baseline/current catalogs for drift")
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--current", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    return parser.parse_args(argv)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return [{str(k).strip(): (v or "").strip() for k, v in row.items()} for row in csv.DictReader(handle)]


def first(row: dict[str, str], names: Sequence[str]) -> str:
    lower = {k.lower(): v for k, v in row.items()}
    for name in names:
        if lower.get(name.lower()):
            return lower[name.lower()]
    return ""


def key_for(row: dict[str, str]) -> str:
    entity = first(row, ("entity", "entity_set", "table", "endpoint")) or "(unknown-entity)"
    field = first(row, ("field", "property", "name", "option")) or "(unknown-field)"
    return f"{entity}.{field}".lower()


def impact_for(key: str, change: str) -> str:
    text = f"{key} {change}".lower()
    impacts: list[str] = []
    if any(token in text for token in ("sla", "target", "status", "priority", "category", "operator", "branch")):
        impacts.extend(["power_bi", "operations"])
    if any(token in text for token in ("description", "request", "caller", "person", "knowledge", "summary", "comment")):
        impacts.extend(["ai", "security"])
    if any(token in text for token in ("endpoint", "id", "external", "webhook", "action", "required")):
        impacts.append("automation")
    if any(token in text for token in ("person", "caller", "email", "phone", "operator", "branch")):
        impacts.append("security")
    if not impacts:
        impacts.append("review")
    return ";".join(dict.fromkeys(impacts))


def finding(change_type: str, key: str, baseline: str, current: str) -> dict[str, str]:
    impact = impact_for(key, f"{change_type} {baseline} {current}")
    severity = "high" if change_type in {"removed", "type_changed", "required_changed"} else "medium"
    if impact == "review":
        severity = "low"
    return {
        "change_type": change_type,
        "catalog_key": key,
        "severity": severity,
        "impact": impact,
        "baseline": baseline,
        "current": current,
        "recommended_action": "Review tenant mapping, dependent KPIs/prompts/automations, and update evidence docs.",
        "owner": "TOPdesk application manager / BI owner",
        "validation_metric": "Affected report, prompt, or automation reconciles against current tenant evidence.",
    }


def build_findings(baseline_rows: list[dict[str, str]], current_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    baseline = {key_for(row): row for row in baseline_rows}
    current = {key_for(row): row for row in current_rows}
    findings: list[dict[str, str]] = []
    for key in sorted(set(baseline) - set(current)):
        findings.append(finding("removed", key, "present", "missing"))
    for key in sorted(set(current) - set(baseline)):
        findings.append(finding("added", key, "missing", "present"))
    for key in sorted(set(baseline) & set(current)):
        old = baseline[key]
        new = current[key]
        checks = (
            ("type_changed", TYPE_COLUMNS),
            ("label_changed", LABEL_COLUMNS),
            ("required_changed", NULL_COLUMNS),
        )
        for change_type, columns in checks:
            old_value = first(old, columns)
            new_value = first(new, columns)
            if old_value != new_value:
                findings.append(finding(change_type, key, old_value or "(empty)", new_value or "(empty)"))
    return findings


def write_outputs(out_dir: Path, findings: list[dict[str, str]]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "change_type",
        "catalog_key",
        "severity",
        "impact",
        "baseline",
        "current",
        "recommended_action",
        "owner",
        "validation_metric",
    ]
    with (out_dir / "tenant-drift-findings.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(findings)
    by_severity: dict[str, int] = {}
    for row in findings:
        by_severity[row["severity"]] = by_severity.get(row["severity"], 0) + 1
    lines = [
        "# TOPdesk Tenant Drift Report",
        "",
        f"- Findings: {len(findings)}",
        f"- High severity: {by_severity.get('high', 0)}",
        f"- Medium severity: {by_severity.get('medium', 0)}",
        f"- Low severity: {by_severity.get('low', 0)}",
        "",
        "## Top Findings",
        "",
    ]
    for row in findings[:25]:
        lines.append(f"- **{row['severity']}** `{row['catalog_key']}` {row['change_type']}: {row['baseline']} -> {row['current']} ({row['impact']})")
    (out_dir / "tenant-drift-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    findings = build_findings(read_rows(args.baseline), read_rows(args.current))
    write_outputs(args.out_dir, findings)
    print(f"Wrote tenant drift report to {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
