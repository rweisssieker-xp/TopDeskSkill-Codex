#!/usr/bin/env python3
"""Profile a TOPdesk tenant through REST API endpoints."""

from __future__ import annotations

import argparse
import base64
import csv
import json
import os
import sys
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any, Sequence


DEFAULT_ENDPOINTS = {
    "incidents": "/tas/api/incidents",
    "persons": "/tas/api/persons",
    "operatorgroups": "/tas/api/operatorgroups",
    "branches": "/tas/api/branches",
}

PII_HINTS = {"email", "phone", "mobile", "name", "caller", "person", "address", "login"}
POWERBI_HINTS = {
    "id",
    "number",
    "status",
    "category",
    "subcategory",
    "priority",
    "impact",
    "urgency",
    "branch",
    "caller",
    "operator",
    "operatorGroup",
    "creationDate",
    "callDate",
    "closedDate",
    "targetDate",
    "responseDate",
    "sla",
}
AI_HINTS = {
    "briefDescription",
    "request",
    "requests",
    "category",
    "subcategory",
    "priority",
    "impact",
    "urgency",
    "operatorGroup",
    "status",
    "targetDate",
}


def auth_header(username: str, app_password: str) -> str:
    raw = f"{username}:{app_password}".encode("utf-8")
    return "Basic " + base64.b64encode(raw).decode("ascii")


def request_json(base_url: str, path: str, username: str, app_password: str, page_size: int, start: int) -> Any:
    joiner = "&" if "?" in path else "?"
    url = f"{base_url.rstrip('/')}{path}{joiner}start={start}&page_size={page_size}"
    request = urllib.request.Request(
        url,
        headers={"Authorization": auth_header(username, app_password), "Accept": "application/json"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"{path} returned HTTP {exc.code}") from exc


def fetch_endpoint(
    base_url: str,
    path: str,
    username: str,
    app_password: str,
    max_records: int,
    page_size: int,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    start = 0
    while len(rows) < max_records:
        payload = request_json(base_url, path, username, app_password, page_size, start)
        if not isinstance(payload, list):
            raise RuntimeError(f"{path} returned {type(payload).__name__}, expected list")
        if not payload:
            break
        rows.extend(item for item in payload if isinstance(item, dict))
        if len(payload) < page_size:
            break
        start += page_size
    return rows[:max_records]


def flatten_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (str, int, float, bool)):
        return str(value)
    if isinstance(value, dict):
        for key in ("name", "number", "id", "groupName", "dynamicName"):
            if key in value and value[key] is not None:
                return str(value[key])
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    if isinstance(value, list):
        return f"[{len(value)} items]"
    return str(value)


def infer_type(values: list[Any]) -> str:
    sample = [value for value in values if value is not None and value != ""]
    if not sample:
        return "empty"
    if all(isinstance(value, bool) for value in sample):
        return "boolean"
    if all(isinstance(value, int) and not isinstance(value, bool) for value in sample):
        return "integer"
    if all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in sample):
        return "number"
    if all(isinstance(value, dict) for value in sample):
        return "object"
    if all(isinstance(value, list) for value in sample):
        return "array"
    text_values = [str(value) for value in sample]
    if sum("T" in value and "-" in value for value in text_values) >= max(1, int(len(text_values) * 0.8)):
        return "datetime"
    return "text"


def profile_rows(entity: str, rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    keys = sorted({key for row in rows for key in row.keys()})
    result: list[dict[str, str]] = []
    for key in keys:
        values = [row.get(key) for row in rows]
        flat = [flatten_value(value) for value in values]
        non_empty = [value for value in flat if value]
        counts = Counter(non_empty)
        lower = key.lower()
        result.append(
            {
                "entity": entity,
                "field": key,
                "inferred_type": infer_type(values),
                "row_count": str(len(rows)),
                "non_empty_count": str(len(non_empty)),
                "empty_count": str(len(rows) - len(non_empty)),
                "distinct_count": str(len(counts)),
                "sample_values": "; ".join(value for value, _ in counts.most_common(3))[:500],
                "pii_risk": "yes" if any(hint in lower for hint in PII_HINTS) else "no",
                "powerbi_candidate": "yes" if key in POWERBI_HINTS else "no",
                "ai_candidate": "yes" if key in AI_HINTS else "no",
            }
        )
    return result


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def data_quality_findings(profile: list[dict[str, str]]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for row in profile:
        row_count = int(row["row_count"])
        empty_count = int(row["empty_count"])
        distinct_count = int(row["distinct_count"])
        important = row["powerbi_candidate"] == "yes" or row["ai_candidate"] == "yes"
        if row_count == 0:
            continue
        if empty_count > 0 and important:
            severity = "high" if empty_count / row_count >= 0.2 else "medium"
            findings.append(
                {
                    "entity": row["entity"],
                    "field": row["field"],
                    "severity": severity,
                    "finding": "important field has missing values",
                    "impact": "Power BI / AI readiness",
                    "details": f"{empty_count} empty of {row_count}",
                }
            )
        if important and distinct_count <= 1 and row_count > 1:
            findings.append(
                {
                    "entity": row["entity"],
                    "field": row["field"],
                    "severity": "low",
                    "finding": "important field has low variance",
                    "impact": "filtering / modelling",
                    "details": f"{distinct_count} distinct values",
                }
            )
    return findings


def markdown_report(path: Path, counts: dict[str, int], profile: list[dict[str, str]], findings: list[dict[str, str]]) -> None:
    powerbi_fields = [row for row in profile if row["powerbi_candidate"] == "yes"]
    ai_fields = [row for row in profile if row["ai_candidate"] == "yes"]
    pii_fields = [row for row in profile if row["pii_risk"] == "yes"]
    lines = [
        "# TOPdesk REST Tenant Profile",
        "",
        "Credentials are not stored in this report.",
        "",
        "## Snapshot Counts",
        "",
        "| Entity | Rows profiled |",
        "| --- | ---: |",
    ]
    for entity, count in counts.items():
        lines.append(f"| {entity} | {count} |")
    lines.extend(
        [
            "",
            "## Readiness Summary",
            "",
            f"- Power BI candidate fields: {len(powerbi_fields)}",
            f"- AI candidate fields: {len(ai_fields)}",
            f"- PII-risk fields: {len(pii_fields)}",
            f"- Data-quality findings: {len(findings)}",
            "",
            "## Power BI Model Starter",
            "",
            "- `FactIncident`: incident records from `/tas/api/incidents`.",
            "- `DimPerson`: caller/person records from `/tas/api/persons`.",
            "- `DimOperatorGroup`: operator group records from `/tas/api/operatorgroups`.",
            "- `DimBranch`: branch records from `/tas/api/branches`.",
            "- Recommended date roles: creation, call, target, response, closed, completed.",
            "- Recommended RLS review: branch, caller/person, operator/operator group.",
            "",
            "## AI/KI Readiness",
            "",
            "- Classification/routing can use description, request text, category, priority, impact, urgency, operator group, status.",
            "- Summary and RAG features must separate operator-only notes from customer-visible text.",
            "- PII minimization is required for person, caller, email, phone, login, and name fields.",
            "- Feedback/audit tables are still needed for governed AI suggestions.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Profile TOPdesk REST endpoints for Power BI and AI readiness")
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--max-records", type=int, default=250)
    parser.add_argument("--page-size", type=int, default=100)
    parser.add_argument("--endpoint", action="append", help="Optional name=path endpoint override")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    base_url = os.environ.get("TOPDESK_BASE_URL", "").rstrip("/")
    username = os.environ.get("TOPDESK_USERNAME", "")
    app_password = os.environ.get("TOPDESK_APP_PASSWORD", "")
    if not base_url or not username or not app_password:
        print("TOPDESK_BASE_URL, TOPDESK_USERNAME, and TOPDESK_APP_PASSWORD are required.", file=sys.stderr)
        return 2

    endpoints = dict(DEFAULT_ENDPOINTS)
    if args.endpoint:
        endpoints = {}
        for item in args.endpoint:
            name, sep, path = item.partition("=")
            if not sep or not name or not path:
                print(f"Invalid endpoint format: {item}", file=sys.stderr)
                return 2
            endpoints[name] = path

    args.out.mkdir(parents=True, exist_ok=True)
    snapshots = args.out / "snapshots"
    snapshots.mkdir(parents=True, exist_ok=True)

    all_profile: list[dict[str, str]] = []
    counts: dict[str, int] = {}
    for entity, path in endpoints.items():
        rows = fetch_endpoint(base_url, path, username, app_password, args.max_records, args.page_size)
        counts[entity] = len(rows)
        (snapshots / f"{entity}.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        all_profile.extend(profile_rows(entity, rows))

    profile_fields = [
        "entity",
        "field",
        "inferred_type",
        "row_count",
        "non_empty_count",
        "empty_count",
        "distinct_count",
        "sample_values",
        "pii_risk",
        "powerbi_candidate",
        "ai_candidate",
    ]
    write_csv(args.out / "rest_field_catalog.csv", all_profile, profile_fields)

    findings = data_quality_findings(all_profile)
    write_csv(args.out / "data_quality_findings.csv", findings, ["entity", "field", "severity", "finding", "impact", "details"])
    markdown_report(args.out / "rest_tenant_profile.md", counts, all_profile, findings)

    print(f"Wrote REST tenant profile to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

