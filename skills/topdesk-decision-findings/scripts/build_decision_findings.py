#!/usr/bin/env python3
"""Normalize analysis CSV rows into decision-ready TOPdesk findings."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Sequence


OUTPUT_FIELDS = ["finding", "evidence", "business_impact", "risk", "recommended_action", "owner", "validation_metric"]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build decision-ready findings from CSV rows")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--default-owner", default="Service owner")
    return parser.parse_args(argv)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return [{str(k).strip(): (v or "").strip() for k, v in row.items()} for row in csv.DictReader(handle)]


def pick(row: dict[str, str], *names: str, default: str = "") -> str:
    lower = {k.lower(): v for k, v in row.items()}
    for name in names:
        value = lower.get(name.lower())
        if value:
            return value
    return default


def infer_risk(row: dict[str, str]) -> str:
    text = " ".join(row.values()).lower()
    explicit = pick(row, "risk", "severity", "priority")
    if explicit.lower() in {"high", "medium", "low", "review"}:
        return explicit.lower()
    if any(token in text for token in ("overdue", "breach", "missing target", "removed", "pii", "unowned")):
        return "high"
    if any(token in text for token in ("waiting", "reopen", "handoff", "drift", "changed")):
        return "medium"
    return "review"


def normalize(row: dict[str, str], default_owner: str) -> dict[str, str]:
    finding = pick(row, "finding", "issue", "change_type", "check", "name", default="TOPdesk finding requires review")
    evidence = pick(row, "evidence", "description", "catalog_key", "incident", "details")
    if not evidence:
        evidence = "; ".join(f"{k}={v}" for k, v in row.items() if v)[:500]
    risk = infer_risk(row)
    return {
        "finding": finding,
        "evidence": evidence,
        "business_impact": pick(row, "business_impact", "impact", default="May affect service quality, reporting trust, automation safety, or improvement prioritization."),
        "risk": risk,
        "recommended_action": pick(row, "recommended_action", "action", default="Review with the accountable owner and define the next validation step."),
        "owner": pick(row, "owner", "recommended_owner", default=default_owner),
        "validation_metric": pick(row, "validation_metric", "metric", default="Finding is resolved or risk is accepted with documented evidence."),
    }


def write_outputs(out_dir: Path, findings: list[dict[str, str]]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "decision-ready-findings.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(findings)
    lines = ["# TOPdesk Decision-Ready Findings", "", f"- Findings: {len(findings)}", "", "## Readout", ""]
    for row in findings:
        lines.extend(
            [
                f"### {row['finding']}",
                "",
                f"- Evidence: {row['evidence']}",
                f"- Business impact: {row['business_impact']}",
                f"- Risk: {row['risk']}",
                f"- Recommended action: {row['recommended_action']}",
                f"- Owner: {row['owner']}",
                f"- Validation metric: {row['validation_metric']}",
                "",
            ]
        )
    (out_dir / "decision-ready-findings.md").write_text("\n".join(lines), encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    findings = [normalize(row, args.default_owner) for row in read_csv(args.input)]
    write_outputs(args.out_dir, findings)
    print(f"Wrote decision-ready findings to {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
