#!/usr/bin/env python3
"""Analyze TOPdesk lifecycle CSVs for process debt findings."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path
from typing import Sequence


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze TOPdesk process debt from lifecycle CSVs")
    parser.add_argument("--incidents", type=Path, help="Incident snapshot CSV")
    parser.add_argument("--assignments", type=Path, help="Assignment transition CSV")
    parser.add_argument("--statuses", type=Path, help="Status transition CSV")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--handoff-threshold", type=int, default=4)
    parser.add_argument("--waiting-hours-threshold", type=float, default=72.0)
    return parser.parse_args(argv)


def read_csv(path: Path | None) -> list[dict[str, str]]:
    if not path:
        return []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return [{str(k).strip(): (v or "").strip() for k, v in row.items()} for row in csv.DictReader(handle)]


def get(row: dict[str, str], *names: str) -> str:
    lower = {k.lower(): v for k, v in row.items()}
    for name in names:
        value = lower.get(name.lower())
        if value:
            return value
    return ""


def number(value: str) -> float:
    try:
        return float(value.replace(",", "."))
    except ValueError:
        return 0.0


def make_finding(finding: str, evidence: str, impact: str, risk: str, action: str, owner: str, metric: str) -> dict[str, str]:
    return {
        "finding": finding,
        "evidence": evidence,
        "business_impact": impact,
        "risk": risk,
        "recommended_action": action,
        "owner": owner,
        "validation_metric": metric,
    }


def build_findings(args: argparse.Namespace) -> list[dict[str, str]]:
    incidents = read_csv(args.incidents)
    assignments = read_csv(args.assignments)
    statuses = read_csv(args.statuses)
    findings: list[dict[str, str]] = []

    assignment_counts: Counter[str] = Counter()
    groups_by_incident: dict[str, set[str]] = defaultdict(set)
    for row in assignments:
        incident = get(row, "incident", "incident_id", "incident_key", "number")
        group = get(row, "operator_group", "operatorGroup", "group", "assignment_group")
        if incident:
            assignment_counts[incident] += 1
            if group:
                groups_by_incident[incident].add(group)
    for incident, count in assignment_counts.items():
        if count >= args.handoff_threshold:
            findings.append(
                make_finding(
                    "handoff loop risk",
                    f"Incident {incident} has {count} assignment transitions across {len(groups_by_incident[incident])} groups.",
                    "Repeated handoffs increase waiting time and ownership ambiguity.",
                    "high",
                    "Review routing rules, category ownership, and assignment escalation.",
                    "Service desk lead",
                    "Handoff count per incident below threshold.",
                )
            )

    waiting_by_status: Counter[str] = Counter()
    for row in statuses:
        status = get(row, "status", "status_name", "from_status", "to_status")
        duration = number(get(row, "duration_hours", "hours", "duration"))
        if any(token in status.lower() for token in ("wait", "hold", "pending", "customer")) and duration >= args.waiting_hours_threshold:
            waiting_by_status[status or "(unknown)"] += 1
    for status, count in waiting_by_status.items():
        findings.append(
            make_finding(
                "waiting zone debt",
                f"{count} status intervals exceeded {args.waiting_hours_threshold:g} hours in {status}.",
                "Long waiting zones hide SLA risk and customer communication gaps.",
                "medium",
                "Define owner, escalation, and customer-response cadence for waiting statuses.",
                "Process owner",
                "P90 waiting-zone duration reduced.",
            )
        )

    category_groups: dict[str, set[str]] = defaultdict(set)
    reopen_counts: Counter[str] = Counter()
    missing_owner = 0
    for row in incidents:
        category = get(row, "category", "category_name", "callType", "subcategory") or "(unknown category)"
        group = get(row, "operator_group", "operatorGroup", "group")
        if group:
            category_groups[category].add(group)
        else:
            missing_owner += 1
        reopened = get(row, "reopened", "reopen", "reopen_count", "reopenCount")
        if reopened.lower() in {"true", "yes"} or number(reopened) > 0:
            reopen_counts[category] += 1
    for category, groups in category_groups.items():
        if len(groups) >= 4:
            findings.append(
                make_finding(
                    "category routing debt",
                    f"Category {category} appears across {len(groups)} operator groups.",
                    "Broad routing spread can create avoidable reassignment and unclear ownership.",
                    "medium",
                    "Review category tree and routing matrix for clear first-owner mapping.",
                    "TOPdesk application manager",
                    "Distinct operator groups per category reduced.",
                )
            )
    for category, count in reopen_counts.items():
        if count >= 3:
            findings.append(
                make_finding(
                    "reopen pattern",
                    f"Category {category} has {count} reopened incidents in the sample.",
                    "Reopens indicate closure-quality, knowledge, or intake gaps.",
                    "medium",
                    "Review closure criteria and knowledge coverage for this category.",
                    "Service desk lead",
                    "Reopen rate reduced for category.",
                )
            )
    if missing_owner:
        findings.append(
            make_finding(
                "stale or missing ownership",
                f"{missing_owner} incidents have no operator group in the sample.",
                "Missing ownership delays triage and weakens accountability.",
                "high",
                "Route unowned incidents and fix intake/routing rules.",
                "Service desk lead",
                "Open incidents without operator group equals zero.",
            )
        )
    return findings


def write_outputs(out_dir: Path, findings: list[dict[str, str]]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    fieldnames = ["finding", "evidence", "business_impact", "risk", "recommended_action", "owner", "validation_metric"]
    with (out_dir / "process-debt-findings.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(findings)
    lines = ["# TOPdesk Process Debt Report", "", f"- Findings: {len(findings)}", "", "## Findings", ""]
    for row in findings:
        lines.append(f"- **{row['risk']}** {row['finding']}: {row['evidence']} Action: {row['recommended_action']}")
    (out_dir / "process-debt-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    findings = build_findings(args)
    write_outputs(args.out_dir, findings)
    print(f"Wrote process debt report to {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
