#!/usr/bin/env python3
"""Review TOPdesk automation designs and produce risk cards."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Sequence


CHECKS = [
    ("trigger", "high", "Define a clear trigger and scope."),
    ("payload_mapping", "high", "Document source-to-target payload fields."),
    ("idempotency", "high", "Add idempotency key or duplicate prevention."),
    ("retry_policy", "medium", "Define retry count, backoff, and stop condition."),
    ("dead_letter", "medium", "Define failed-message handling or review queue."),
    ("rollback", "high", "Document disable and rollback procedure."),
    ("pii_review", "high", "Review PII and customer-visible content exposure."),
    ("audit_logging", "high", "Log actor, timestamp, input, output, and correlation id."),
    ("monitoring_owner", "medium", "Assign owner for failed runs and alerts."),
    ("human_approval", "medium", "Require approval for high-impact or customer-visible actions."),
]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Review TOPdesk automation risk")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    return parser.parse_args(argv)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return [{str(k).strip(): (v or "").strip() for k, v in row.items()} for row in csv.DictReader(handle)]


def pick(row: dict[str, str], name: str) -> str:
    lower = {k.lower(): v for k, v in row.items()}
    return lower.get(name.lower(), "")


def present(value: str) -> bool:
    return value.strip().lower() in {"yes", "true", "present", "ok", "documented", "defined", "1"} or len(value.strip()) > 5


def build_findings(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for index, row in enumerate(rows, start=1):
        automation = pick(row, "automation") or pick(row, "name") or f"automation-{index}"
        for field, severity, action in CHECKS:
            if not present(pick(row, field)):
                findings.append(
                    {
                        "automation": automation,
                        "risk": severity,
                        "missing_control": field,
                        "recommended_action": action,
                        "go_no_go_effect": "no-go" if severity == "high" else "conditional",
                    }
                )
    return findings


def write_outputs(out_dir: Path, findings: list[dict[str, str]]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    fieldnames = ["automation", "risk", "missing_control", "recommended_action", "go_no_go_effect"]
    with (out_dir / "automation-risk-findings.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(findings)
    high = sum(1 for row in findings if row["risk"] == "high")
    medium = sum(1 for row in findings if row["risk"] == "medium")
    verdict = "go" if not findings else ("no-go" if high else "conditional")
    lines = [
        "# TOPdesk Automation Risk Card",
        "",
        f"- Verdict: {verdict}",
        f"- High risks: {high}",
        f"- Medium risks: {medium}",
        "",
        "## Findings",
        "",
    ]
    for row in findings:
        lines.append(f"- **{row['risk']}** {row['automation']} missing `{row['missing_control']}`: {row['recommended_action']}")
    (out_dir / "automation-risk-card.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    findings = build_findings(read_csv(args.input))
    write_outputs(args.out_dir, findings)
    print(f"Wrote automation risk card to {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
