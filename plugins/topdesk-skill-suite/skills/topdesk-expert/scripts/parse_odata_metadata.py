#!/usr/bin/env python3
"""Extract OData metadata into CSV catalogs.

Usage:
  python parse_odata_metadata.py metadata.xml --out out_dir

The script is intentionally generic. TOPdesk tenants can expose different
entity names and optional fields, so this tool catalogs what the target
metadata actually contains instead of relying on hard-coded names.
"""

from __future__ import annotations

import argparse
import csv
import os
import xml.etree.ElementTree as ET


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def child_text_attr(element: ET.Element, child_name: str, attr: str) -> list[str]:
    values: list[str] = []
    for child in element:
        if local_name(child.tag) == child_name and attr in child.attrib:
            values.append(child.attrib[attr])
    return values


def parse_metadata(path: str) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    tree = ET.parse(path)
    root = tree.getroot()

    entity_types: dict[str, ET.Element] = {}
    entity_sets: list[dict[str, str]] = []
    properties: list[dict[str, str]] = []
    navigations: list[dict[str, str]] = []

    for element in root.iter():
        if local_name(element.tag) == "EntityType":
            name = element.attrib.get("Name", "")
            if name:
                entity_types[name] = element

    for container in root.iter():
        if local_name(container.tag) != "EntityContainer":
            continue
        for entity_set in container:
            if local_name(entity_set.tag) != "EntitySet":
                continue
            entity_set_name = entity_set.attrib.get("Name", "")
            entity_type = entity_set.attrib.get("EntityType", "")
            entity_type_name = entity_type.rsplit(".", 1)[-1]
            entity_sets.append(
                {
                    "entity_set": entity_set_name,
                    "entity_type": entity_type,
                    "entity_type_name": entity_type_name,
                }
            )

    for type_name, entity_type in entity_types.items():
        keys = set(child_text_attr(entity_type.find("./{*}Key") or ET.Element("Key"), "PropertyRef", "Name"))
        for child in entity_type:
            kind = local_name(child.tag)
            if kind == "Property":
                prop_name = child.attrib.get("Name", "")
                properties.append(
                    {
                        "entity_type": type_name,
                        "property": prop_name,
                        "type": child.attrib.get("Type", ""),
                        "nullable": child.attrib.get("Nullable", "true"),
                        "is_key": "true" if prop_name in keys else "false",
                    }
                )
            elif kind == "NavigationProperty":
                navigations.append(
                    {
                        "entity_type": type_name,
                        "navigation": child.attrib.get("Name", ""),
                        "type": child.attrib.get("Type", ""),
                        "nullable": child.attrib.get("Nullable", ""),
                        "partner": child.attrib.get("Partner", ""),
                    }
                )

    return entity_sets, properties, navigations


def write_csv(path: str, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract OData metadata catalogs.")
    parser.add_argument("metadata_xml", help="Path to OData $metadata XML file")
    parser.add_argument("--out", default="odata_catalog", help="Output directory")
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)
    entity_sets, properties, navigations = parse_metadata(args.metadata_xml)

    write_csv(
        os.path.join(args.out, "entity_sets.csv"),
        entity_sets,
        ["entity_set", "entity_type", "entity_type_name"],
    )
    write_csv(
        os.path.join(args.out, "properties.csv"),
        properties,
        ["entity_type", "property", "type", "nullable", "is_key"],
    )
    write_csv(
        os.path.join(args.out, "navigation_properties.csv"),
        navigations,
        ["entity_type", "navigation", "type", "nullable", "partner"],
    )

    print(f"Wrote {len(entity_sets)} entity sets")
    print(f"Wrote {len(properties)} properties")
    print(f"Wrote {len(navigations)} navigation properties")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
