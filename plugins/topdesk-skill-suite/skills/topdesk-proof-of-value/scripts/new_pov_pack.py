#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence


ROI = """driver,baseline_volume,minutes_saved_per_item,hourly_rate,estimated_value,notes
manual_reporting,0,0,0,0,
ai_ticket_summary,0,0,0,0,
reassignment_reduction,0,0,0,0,
sla_risk_focus,0,0,0,0,
knowledge_deflection,0,0,0,0,
"""


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a TOPdesk proof-of-value pack")
    parser.add_argument("--name", required=True)
    parser.add_argument("--out-dir", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "proof-of-value-plan.md").write_text(f"# Proof Of Value Plan: {args.name}\n", encoding="utf-8")
    (args.out_dir / "roi-calculator.csv").write_text(ROI, encoding="utf-8")
    print(f"Wrote {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

