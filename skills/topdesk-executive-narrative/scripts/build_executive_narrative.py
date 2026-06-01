#!/usr/bin/env python3
"""Build a TOPdesk executive narrative from decision-ready findings."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path
from typing import Sequence


ACTION_FIELDS = ["priority", "owner", "recommended_action", "validation_metric", "source_finding"]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build TOPdesk executive narrative")
    parser.add_argument("--findings", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--title", default="TOPdesk Executive Decision Readout")
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


def risk(row: dict[str, str]) -> str:
    value = pick(row, "risk", "severity", "priority", default="review").lower()
    if value in {"critical", "high", "medium", "low", "review"}:
        return "high" if value == "critical" else value
    return "review"


def finding(row: dict[str, str]) -> str:
    return pick(row, "finding", "issue", "change_type", "dimension", default="TOPdesk finding")


def evidence(row: dict[str, str]) -> str:
    return pick(row, "evidence", "details", "blockers", "catalog_key", default="Evidence available in source row.")


def build_actions(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    priority_order = {"high": 0, "medium": 1, "review": 2, "low": 3}
    ordered = sorted(rows, key=lambda row: priority_order.get(risk(row), 9))
    actions: list[dict[str, str]] = []
    for row in ordered[:12]:
        actions.append(
            {
                "priority": risk(row),
                "owner": pick(row, "owner", "recommended_owner", default="Service owner"),
                "recommended_action": pick(row, "recommended_action", "action", default="Review finding and agree next action."),
                "validation_metric": pick(row, "validation_metric", "metric", default="Action closed with evidence or risk accepted."),
                "source_finding": finding(row),
            }
        )
    return actions


def write_outputs(out_dir: Path, rows: list[dict[str, str]], title: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    counts = Counter(risk(row) for row in rows)
    actions = build_actions(rows)
    with (out_dir / "executive-actions.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=ACTION_FIELDS)
        writer.writeheader()
        writer.writerows(actions)
    top_rows = sorted(rows, key=lambda row: {"high": 0, "medium": 1, "review": 2, "low": 3}.get(risk(row), 9))[:6]
    lines = [
        f"# {title}",
        "",
        "## Executive Summary",
        "",
        f"The current TOPdesk evidence contains {len(rows)} decision findings: {counts.get('high', 0)} high-risk, {counts.get('medium', 0)} medium-risk, {counts.get('low', 0)} low-risk, and {counts.get('review', 0)} review items.",
        "The recommended management action is to assign owners to the highest-risk findings and validate progress with the listed metrics over the next 30 days.",
        "",
        "## Current Situation",
        "",
        "The findings indicate where service quality, reporting trust, AI adoption, automation safety, or operational readiness need attention.",
        "",
        "## Evidence Highlights",
        "",
    ]
    for row in top_rows:
        lines.append(f"- **{risk(row)}** {finding(row)}: {evidence(row)}")
    lines.extend(
        [
            "",
            "## Business Impact",
            "",
            "Unresolved findings can increase waiting time, weaken KPI trust, reduce AI adoption, create automation risk, or delay production readiness.",
            "",
            "## Decisions Needed",
            "",
        ]
    )
    for action in actions[:5]:
        lines.append(f"- Assign **{action['owner']}** to `{action['source_finding']}` and validate with: {action['validation_metric']}")
    lines.extend(["", "## Next 30 Days", ""])
    lines.extend(
        [
            "1. Confirm accountable owners for high-risk findings.",
            "2. Close missing evidence or accept residual risk explicitly.",
            "3. Run the relevant TOPdesk skill/script again after remediation.",
            "4. Compare validation metrics against the baseline.",
            "5. Decide whether to scale, pause, or redesign the initiative.",
            "",
            "## Action Table",
            "",
            "| Priority | Owner | Action | Validation metric | Source finding |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for action in actions:
        lines.append(
            f"| {action['priority']} | {action['owner']} | {action['recommended_action']} | {action['validation_metric']} | {action['source_finding']} |"
        )
    (out_dir / "executive-narrative.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    write_outputs(args.out_dir, read_csv(args.findings), args.title)
    print(f"Wrote executive narrative to {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
