#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a TOPdesk report page spec")
    parser.add_argument("--audience", required=True)
    parser.add_argument("--page-job", required=True)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    text = f"""# Report Page Spec

## Audience
{args.audience}

## Page Job
{args.page_job}

## Layout
- KPI strip:
- Main visual:
- Supporting visuals:
- Exception table:

## Visuals

## Filters

## Drillthrough And Tooltips

## Accessibility

## Validation
"""
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

