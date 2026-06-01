#!/usr/bin/env python3
"""Build an AI adoption ledger from TOPdesk AI suggestion logs."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path
from typing import Sequence


LEDGER_FIELDS = [
    "suggestion_id",
    "suggestion_type",
    "status",
    "override_reason",
    "confidence",
    "cost_estimate",
    "time_saved_minutes",
    "prompt_version",
    "model_version",
]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build TOPdesk AI adoption ledger")
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


def num(value: str) -> float:
    try:
        return float(value.replace(",", "."))
    except ValueError:
        return 0.0


def normalize_status(value: str) -> str:
    text = value.strip().lower()
    if text in {"accepted", "accept", "used", "approved"}:
        return "accepted"
    if text in {"edited", "modified", "changed"}:
        return "edited"
    if text in {"rejected", "reject", "dismissed", "declined"}:
        return "rejected"
    return text or "unknown"


def normalize(row: dict[str, str], index: int) -> dict[str, str]:
    return {
        "suggestion_id": pick(row, "suggestion_id", "id", "event_id", default=f"row-{index}"),
        "suggestion_type": pick(row, "suggestion_type", "type", "use_case", default="unknown"),
        "status": normalize_status(pick(row, "status", "operator_action", "result")),
        "override_reason": pick(row, "override_reason", "reason", "rejection_reason"),
        "confidence": pick(row, "confidence", "score"),
        "cost_estimate": pick(row, "cost_estimate", "cost"),
        "time_saved_minutes": pick(row, "time_saved_minutes", "time_saved", "minutes_saved"),
        "prompt_version": pick(row, "prompt_version", "prompt"),
        "model_version": pick(row, "model_version", "model"),
    }


def write_outputs(out_dir: Path, ledger: list[dict[str, str]]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "ai-adoption-ledger.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=LEDGER_FIELDS)
        writer.writeheader()
        writer.writerows(ledger)
    total = len(ledger)
    statuses = Counter(row["status"] for row in ledger)
    by_type: dict[str, Counter[str]] = defaultdict(Counter)
    confidence_values = [num(row["confidence"]) for row in ledger if row["confidence"]]
    total_cost = sum(num(row["cost_estimate"]) for row in ledger)
    total_time = sum(num(row["time_saved_minutes"]) for row in ledger)
    for row in ledger:
        by_type[row["suggestion_type"]][row["status"]] += 1
    rate = lambda count: (count / total * 100.0) if total else 0.0
    lines = [
        "# TOPdesk AI Adoption Summary",
        "",
        f"- Suggestions generated: {total}",
        f"- Acceptance rate: {rate(statuses['accepted']):.1f}%",
        f"- Edit rate: {rate(statuses['edited']):.1f}%",
        f"- Rejection rate: {rate(statuses['rejected']):.1f}%",
        f"- Override rate: {rate(statuses['edited'] + statuses['rejected']):.1f}%",
        f"- Average confidence: {(sum(confidence_values) / len(confidence_values)):.3f}" if confidence_values else "- Average confidence: n/a",
        f"- Estimated cost: {total_cost:.4f}",
        f"- Estimated time saved minutes: {total_time:.1f}",
        "",
        "## By Suggestion Type",
        "",
    ]
    for suggestion_type, counts in sorted(by_type.items()):
        type_total = sum(counts.values())
        lines.append(f"- {suggestion_type}: {type_total} generated, {counts['accepted']} accepted, {counts['edited']} edited, {counts['rejected']} rejected")
    (out_dir / "ai-adoption-summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    ledger = [normalize(row, index + 1) for index, row in enumerate(read_csv(args.input))]
    write_outputs(args.out_dir, ledger)
    print(f"Wrote AI adoption ledger to {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
