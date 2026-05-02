#!/usr/bin/env python3
"""Validate a generated TOPdesk PBIP/PBIR project."""

from __future__ import annotations

import argparse
import json
import re
import urllib.request
from pathlib import Path

from jsonschema import Draft7Validator, RefResolver


SCHEMA_URLS = {
    "report": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/2.0.0/schema.json",
    "page": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.0.0/schema.json",
    "visual": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.0.0/schema.json",
    "pbir": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
    "pbism": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json",
    "visualConfig": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualConfiguration/2.0.0/schema-embedded.json",
    "formatting": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/formattingObjectDefinitions/1.3.0/schema.json",
    "semanticQuery": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/semanticQuery/1.2.0/schema.json",
}

REQUIRED_PRODUCTION_TABLES = {
    "ServicePortfolioSource",
    "ChangeRecordSource",
    "ProblemRecordSource",
    "KnowledgeArticleSource",
    "ExperienceSurveySource",
    "TimeCostSource",
    "AssignmentHistorySource",
    "SecurityValidationEvidence",
    "RefreshMonitoringEvidence",
    "ReleaseSignoffWorkflow",
}

REQUIRED_PRODUCTION_MEASURES = {
    "Service Portfolio Completeness %",
    "Change Stability Score",
    "Problem Candidate Coverage %",
    "Knowledge Deflection Readiness %",
    "XLA Evidence Score",
    "Cost Reporting Readiness %",
    "OLA Reporting Readiness %",
    "Security Validation Coverage",
    "Refresh Monitoring Coverage",
    "Release Signoff Coverage",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_schemas() -> dict[str, dict]:
    schemas = {}
    for url in SCHEMA_URLS.values():
        with urllib.request.urlopen(url, timeout=20) as response:
            schemas[url] = json.load(response)
    return schemas


def extract_model(semantic_model: Path) -> dict[str, dict[str, set[str]]]:
    model: dict[str, dict[str, set[str]]] = {}
    table_dir = semantic_model / "definition" / "tables"
    for path in table_dir.glob("*.tmdl"):
        text = path.read_text(encoding="utf-8")
        measures = set(re.findall(r"\n\s*measure '([^']+)'\s*=", text))
        columns = set(a or b for a, b in re.findall(r"\n\s*column (?:'([^']+)'|([^\s]+))", text))
        model[path.stem] = {"measure": measures, "column": columns}
    return model


def collect_field_refs(value: object) -> list[tuple[str, str, str]]:
    refs: list[tuple[str, str, str]] = []

    def walk(item: object) -> None:
        if isinstance(item, dict):
            if "Measure" in item:
                measure = item["Measure"]
                table = measure.get("Expression", {}).get("SourceRef", {}).get("Entity")
                refs.append(("measure", table, measure.get("Property")))
            if "Column" in item:
                column = item["Column"]
                table = column.get("Expression", {}).get("SourceRef", {}).get("Entity")
                refs.append(("column", table, column.get("Property")))
            for child in item.values():
                walk(child)
        elif isinstance(item, list):
            for child in item:
                walk(child)

    walk(value)
    return refs


def validate(project: Path) -> dict:
    report = project / "topdeskdemo.Report"
    semantic_model = project / "topdeskdemo.SemanticModel"
    definition = report / "definition"
    schemas = load_schemas()

    checks: list[tuple[Path, str]] = [
        (definition / "report.json", "report"),
        (report / "definition.pbir", "pbir"),
        (semantic_model / "definition.pbism", "pbism"),
    ]
    for page_dir in (definition / "pages").glob("ReportSection*"):
        checks.append((page_dir / "page.json", "page"))
    for visual in (definition / "pages").rglob("visual.json"):
        checks.append((visual, "visual"))

    schema_errors = []
    for path, kind in checks:
        data = load_json(path)
        schema = schemas[SCHEMA_URLS[kind]]
        resolver = RefResolver(base_uri=SCHEMA_URLS[kind], referrer=schema, store=schemas)
        for error in Draft7Validator(schema, resolver=resolver).iter_errors(data):
            schema_errors.append({"file": str(path), "path": "/".join(map(str, error.path)), "message": error.message})

    model = extract_model(semantic_model)
    model_errors = []
    missing_tables = sorted(REQUIRED_PRODUCTION_TABLES - set(model))
    if missing_tables:
        model_errors.append({"kind": "missingProductionTables", "items": missing_tables})
    fact_measures = model.get("FactIncident", {}).get("measure", set())
    missing_measures = sorted(REQUIRED_PRODUCTION_MEASURES - fact_measures)
    if missing_measures:
        model_errors.append({"kind": "missingProductionMeasures", "items": missing_measures})
    missing_refs = []
    visual_types: dict[str, int] = {}
    for visual_path in (definition / "pages").rglob("visual.json"):
        visual = load_json(visual_path)
        visual_type = visual.get("visual", {}).get("visualType", "<missing>")
        visual_types[visual_type] = visual_types.get(visual_type, 0) + 1
        for kind, table, name in collect_field_refs(visual):
            if name not in model.get(str(table), {}).get(kind, set()):
                missing_refs.append({"file": str(visual_path), "kind": kind, "table": table, "name": name})

    pages = list((definition / "pages").glob("ReportSection*"))
    result = {
        "project": str(project),
        "schemaChecked": len(checks),
        "schemaErrors": len(schema_errors),
        "missingReferences": len(missing_refs),
        "modelErrors": len(model_errors),
        "jsonFiles": len(list(project.rglob("*.json"))),
        "pages": len(pages),
        "visuals": len(list((definition / "pages").rglob("visual.json"))),
        "factIncidentMeasures": len(model.get("FactIncident", {}).get("measure", set())),
        "tables": len(model),
        "visualTypes": dict(sorted(visual_types.items())),
        "errors": schema_errors[:50],
        "missing": missing_refs[:50],
        "model": model_errors[:50],
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    result = validate(args.project.resolve())
    text = json.dumps(result, indent=2, ensure_ascii=False)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)
    if result["schemaErrors"] or result["missingReferences"] or result["modelErrors"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
