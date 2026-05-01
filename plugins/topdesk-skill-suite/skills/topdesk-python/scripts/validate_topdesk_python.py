#!/usr/bin/env python3
"""Validate baseline quality gates for TOPdesk Python scripts."""

from __future__ import annotations

import argparse
import ast
import py_compile
from pathlib import Path
from typing import Sequence


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"Script not found: {path}"]
    try:
        py_compile.compile(str(path), doraise=True)
    except py_compile.PyCompileError as exc:
        return [str(exc)]

    tree = ast.parse(path.read_text(encoding="utf-8"))
    functions = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
    if "main" not in functions:
        errors.append("Expected a main() function.")
    if "parse_args" not in functions:
        errors.append("Expected a parse_args() function for CLI scripts.")
    if "argparse" not in path.read_text(encoding="utf-8"):
        errors.append("Expected argparse usage for CLI scripts.")
    return errors


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a TOPdesk Python script")
    parser.add_argument("path", type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    errors = validate(args.path)
    if errors:
        for error in errors:
            print(error)
        return 1
    print(f"Python script validation succeeded: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

