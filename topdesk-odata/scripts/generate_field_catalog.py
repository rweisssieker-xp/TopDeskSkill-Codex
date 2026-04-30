#!/usr/bin/env python3
"""Generate a Markdown field catalog from parse_odata_metadata.py CSV output."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict


def read_csv(path: str) -> list[dict[str, str]]:
    with open(path, newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Markdown OData field catalog.")
    parser.add_argument("--entity-sets", required=True, help="Path to entity_sets.csv")
    parser.add_argument("--properties", required=True, help="Path to properties.csv")
    parser.add_argument("--navigation", required=True, help="Path to navigation_properties.csv")
    parser.add_argument("--out", required=True, help="Output Markdown path")
    args = parser.parse_args()

    entity_sets = read_csv(args.entity_sets)
    properties = read_csv(args.properties)
    navigations = read_csv(args.navigation)

    props_by_type: dict[str, list[dict[str, str]]] = defaultdict(list)
    navs_by_type: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in properties:
        props_by_type[row["entity_type"]].append(row)
    for row in navigations:
        navs_by_type[row["entity_type"]].append(row)

    lines: list[str] = [
        "# TOPdesk OData Field Catalog",
        "",
        "Generated from tenant OData metadata. Verify business meaning with sample rows, UI labels, and TOPdesk admins.",
        "",
        "## Entity Sets",
        "",
        "| Entity set | Entity type |",
        "| --- | --- |",
    ]

    for row in entity_sets:
        lines.append(f"| {row['entity_set']} | {row['entity_type_name']} |")

    for row in entity_sets:
        type_name = row["entity_type_name"]
        lines.extend(["", f"## {row['entity_set']} ({type_name})", "", "### Properties", ""])
        lines.extend(["| Property | Type | Nullable | Key | Business concept | Model field | Notes |", "| --- | --- | --- | --- | --- | --- | --- |"])
        for prop in props_by_type.get(type_name, []):
            lines.append(
                f"| {prop['property']} | {prop['type']} | {prop['nullable']} | {prop['is_key']} |  |  |  |"
            )
        lines.extend(["", "### Navigation Properties", ""])
        lines.extend(["| Navigation | Type | Nullable | Partner | Relationship notes |", "| --- | --- | --- | --- | --- |"])
        for nav in navs_by_type.get(type_name, []):
            lines.append(
                f"| {nav['navigation']} | {nav['type']} | {nav['nullable']} | {nav['partner']} |  |"
            )

    with open(args.out, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")

    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
