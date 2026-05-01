#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a TOPdesk USP battlecard")
    parser.add_argument("--audience", required=True)
    parser.add_argument("--offer", required=True)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    text = f"""# Battlecard: {args.offer}

## Audience
{args.audience}

## Positioning Line

## Pain Points

## Differentiators

## Proof Points

## Objections And Responses

## Demo Flow

## Power BI Evidence

## AI/KI Governance Evidence
"""
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

