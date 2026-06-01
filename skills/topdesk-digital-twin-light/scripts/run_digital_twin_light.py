#!/usr/bin/env python3
"""Run lightweight TOPdesk what-if scenario scoring."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Sequence


FIELDS = [
    "scenario",
    "score",
    "confidence",
    "expected_open_incidents",
    "expected_waiting_hours",
    "expected_handoff_count",
    "expected_reopen_rate_pct",
    "expected_sla_at_risk",
    "recommended_pilot",
    "validation_metric",
]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run TOPdesk Digital Twin Light scenario scoring")
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--scenarios", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    return parser.parse_args(argv)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return [{str(k).strip(): (v or "").strip() for k, v in row.items()} for row in csv.DictReader(handle)]


def num(value: str, default: float = 0.0) -> float:
    try:
        return float((value or "").replace(",", "."))
    except ValueError:
        return default


def baseline_map(rows: list[dict[str, str]]) -> dict[str, float]:
    result: dict[str, float] = {}
    for row in rows:
        metric = (row.get("metric") or row.get("Metric") or "").strip().lower()
        if metric:
            result[metric] = num(row.get("value") or row.get("Value") or "0")
    return result


def get(row: dict[str, str], name: str, default: float = 0.0) -> float:
    lower = {k.lower(): v for k, v in row.items()}
    return num(lower.get(name.lower(), ""), default)


def scenario_name(row: dict[str, str], index: int) -> str:
    lower = {k.lower(): v for k, v in row.items()}
    return lower.get("scenario") or lower.get("name") or f"scenario-{index}"


def score_scenario(base: dict[str, float], row: dict[str, str], index: int) -> dict[str, str]:
    handoff_reduction = get(row, "handoff_reduction_pct") / 100.0
    waiting_reduction = get(row, "waiting_reduction_pct") / 100.0
    reopen_reduction = get(row, "reopen_reduction_pct") / 100.0
    capacity_change = get(row, "capacity_change_pct") / 100.0
    ai_assist = get(row, "ai_assist_pct") / 100.0
    confidence = max(0.0, min(1.0, get(row, "confidence", 0.6)))

    open_incidents = base.get("open_incidents", 0.0)
    waiting = base.get("avg_waiting_hours", 0.0)
    handoffs = base.get("handoff_count", 0.0)
    reopen = base.get("reopen_rate_pct", 0.0)
    sla = base.get("sla_at_risk", 0.0)

    expected_handoffs = max(0.0, handoffs * (1 - handoff_reduction - ai_assist * 0.15))
    expected_waiting = max(0.0, waiting * (1 - waiting_reduction - capacity_change * 0.25 - ai_assist * 0.10))
    expected_reopen = max(0.0, reopen * (1 - reopen_reduction))
    expected_sla = max(0.0, sla * (1 - waiting_reduction * 0.35 - capacity_change * 0.20 - ai_assist * 0.10))
    expected_open = max(0.0, open_incidents * (1 - capacity_change * 0.20 - waiting_reduction * 0.10))

    improvement = (
        (handoffs - expected_handoffs)
        + (waiting - expected_waiting)
        + (reopen - expected_reopen)
        + (sla - expected_sla)
        + (open_incidents - expected_open) * 0.1
    )
    score = improvement * confidence
    name = scenario_name(row, index)
    validation_metric = "Compare baseline vs pilot for waiting hours, handoff count, reopen rate, SLA at risk, and open incidents."
    return {
        "scenario": name,
        "score": f"{score:.2f}",
        "confidence": f"{confidence:.2f}",
        "expected_open_incidents": f"{expected_open:.2f}",
        "expected_waiting_hours": f"{expected_waiting:.2f}",
        "expected_handoff_count": f"{expected_handoffs:.2f}",
        "expected_reopen_rate_pct": f"{expected_reopen:.2f}",
        "expected_sla_at_risk": f"{expected_sla:.2f}",
        "recommended_pilot": f"Pilot '{name}' for 30 days with explicit KPI validation.",
        "validation_metric": validation_metric,
    }


def write_outputs(out_dir: Path, rows: list[dict[str, str]]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    ordered = sorted(rows, key=lambda row: num(row["score"]), reverse=True)
    with (out_dir / "digital-twin-scenarios.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(ordered)
    lines = ["# TOPdesk Digital Twin Light Readout", "", f"- Scenarios compared: {len(ordered)}", ""]
    if ordered:
        best = ordered[0]
        lines.extend(
            [
                "## Recommended Scenario",
                "",
                f"- Scenario: {best['scenario']}",
                f"- Score: {best['score']}",
                f"- Confidence: {best['confidence']}",
                f"- Recommended pilot: {best['recommended_pilot']}",
                "",
                "## Scenario Table",
                "",
                "| Scenario | Score | Confidence | Waiting hours | Handoffs | Reopen % | SLA at risk |",
                "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
            ]
        )
        for row in ordered:
            lines.append(
                f"| {row['scenario']} | {row['score']} | {row['confidence']} | {row['expected_waiting_hours']} | {row['expected_handoff_count']} | {row['expected_reopen_rate_pct']} | {row['expected_sla_at_risk']} |"
            )
    (out_dir / "digital-twin-readout.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    base = baseline_map(read_csv(args.baseline))
    scenarios = [score_scenario(base, row, index + 1) for index, row in enumerate(read_csv(args.scenarios))]
    write_outputs(args.out_dir, scenarios)
    print(f"Wrote digital twin light readout to {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
