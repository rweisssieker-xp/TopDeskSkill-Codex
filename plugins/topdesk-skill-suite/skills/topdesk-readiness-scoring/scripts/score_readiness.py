#!/usr/bin/env python3
"""Build TOPdesk readiness scorecards from evidence checklist CSV files."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from typing import Sequence


DIMENSIONS = ("reporting", "ai", "data_trust", "automation", "security", "operations", "tenant_mapping")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score TOPdesk readiness")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
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


def normalize_status(value: str) -> str:
    text = value.strip().lower()
    if text in {"green", "ready", "complete", "yes", "ok"}:
        return "green"
    if text in {"amber", "partial", "in progress", "risk", "some"}:
        return "amber"
    if text in {"red", "missing", "blocked", "no", "unknown"}:
        return "red"
    return "amber" if text else "red"


def build_scores(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    by_dimension: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        dimension = pick(row, "dimension", "area", "category", default="general").lower().replace(" ", "_")
        by_dimension[dimension].append(row)
    output: list[dict[str, str]] = []
    for dimension in sorted(set(DIMENSIONS) | set(by_dimension)):
        items = by_dimension.get(dimension, [])
        statuses = [normalize_status(pick(row, "status", "score", "ready", "evidence_status")) for row in items]
        if not statuses:
            score = "red"
        elif "red" in statuses:
            score = "red"
        elif "amber" in statuses:
            score = "amber"
        else:
            score = "green"
        blockers = [
            pick(row, "blocker", "gap", "notes", "evidence", default="Missing evidence")
            for row, status in zip(items, statuses)
            if status in {"red", "amber"}
        ]
        output.append(
            {
                "dimension": dimension,
                "score": score,
                "evidence_items": str(len(items)),
                "blockers": " | ".join(blockers[:5]) if blockers else "",
                "recommended_action": action_for(dimension, score),
            }
        )
    return output


def action_for(dimension: str, score: str) -> str:
    if score == "green":
        return "Keep evidence current and proceed through the release gate."
    actions = {
        "reporting": "Complete field catalog, KPI definitions, reconciliation, and refresh ownership.",
        "ai": "Define approved use case, PII review, eval set, feedback loop, and human approval.",
        "data_trust": "Run data-quality checks and reconcile source counts before executive reporting.",
        "automation": "Complete trigger, payload, idempotency, retry, rollback, audit, and owner review.",
        "security": "Confirm RLS, PII minimization, secret handling, retention, and access boundaries.",
        "operations": "Assign owner, runbook, monitoring, release gate, and disable procedure.",
        "tenant_mapping": "Collect OData/API metadata, sample records, UI labels, and option exports.",
    }
    return actions.get(dimension, "Document missing evidence and assign an owner.")


def write_outputs(out_dir: Path, scores: list[dict[str, str]]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    fieldnames = ["dimension", "score", "evidence_items", "blockers", "recommended_action"]
    with (out_dir / "readiness-scorecard.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(scores)
    lines = ["# TOPdesk Readiness Scorecard", "", "| Dimension | Score | Evidence items | Recommended action |", "| --- | --- | ---: | --- |"]
    for row in scores:
        lines.append(f"| {row['dimension']} | {row['score']} | {row['evidence_items']} | {row['recommended_action']} |")
    lines.extend(["", "## Blockers", ""])
    for row in scores:
        if row["blockers"]:
            lines.append(f"- **{row['dimension']}**: {row['blockers']}")
    (out_dir / "readiness-scorecard.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    scores = build_scores(read_csv(args.input))
    write_outputs(args.out_dir, scores)
    print(f"Wrote readiness scorecard to {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
