#!/usr/bin/env python3
"""TOPdesk automation CLI template."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence


def build_payload(input_path: Path) -> dict:
    return {
        "input": str(input_path.resolve()),
        "status": "generated",
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TOPdesk automation CLI template")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.input.exists():
        raise FileNotFoundError(f"Input not found: {args.input}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(build_payload(args.input), indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

