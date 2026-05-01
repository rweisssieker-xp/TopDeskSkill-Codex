#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence


TEMPLATE = """# Query To Power BI Spec

## Business Question
{question}

## Grain
- Define one row per business event or snapshot.

## Source
- Select TOPdesk OData, API, CSV export, SQL view, or warehouse source.

## Query Plan
- Entity/table:
- Filters:
- Fields:
- Pagination/incremental boundary:

## Model Mapping
- Fact:
- Dimensions:
- Relationships:

## Measures
- Add explicit DAX measure list with definitions.

## Report Requirements
- Audience:
- Page:
- Visuals:

## Security And PII
- Add RLS and PII notes.

## Validation
- Add reconciliation source and checks.
"""


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a TOPdesk query-to-Power-BI spec")
    parser.add_argument("--question", required=True)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(TEMPLATE.format(question=args.question), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
