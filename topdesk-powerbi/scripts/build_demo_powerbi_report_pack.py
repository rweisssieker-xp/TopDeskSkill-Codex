#!/usr/bin/env python3
"""Build a Power BI import pack from TOPdesk demo tenant artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable, Sequence


DATE_FIELDS = ["creationDate", "callDate", "targetDate", "responseDate", "completedDate", "closedDate", "modificationDate"]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a TOPdesk Power BI report implementation pack")
    parser.add_argument("--tenant-profile", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=Path("powerbi_pack/topdesk-demo-report"))
    return parser.parse_args(argv)


def load_json(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError(f"{path} must contain a JSON array")
    return [row for row in payload if isinstance(row, dict)]


def load_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def nested_id(value: Any) -> str:
    if isinstance(value, dict):
        for key in ("id", "number"):
            if value.get(key):
                return str(value[key])
    return ""


def nested_label(value: Any) -> str:
    if value is None or value == "":
        return "(blank)"
    if isinstance(value, dict):
        for key in ("name", "groupName", "dynamicName", "number", "id"):
            if value.get(key):
                return str(value[key])
        return "(object)"
    return str(value)


def first_non_blank_label(*values: Any) -> str:
    for value in values:
        candidate = nested_label(value)
        if candidate != "(blank)":
            return candidate
    return "(blank)"


def first_non_blank_id(*values: Any) -> str:
    for value in values:
        candidate = nested_id(value)
        if candidate:
            return candidate
    return ""


def dt(value: Any) -> str:
    if not isinstance(value, str) or not value:
        return ""
    return value[:10]


def bool_value(value: Any) -> str:
    return "true" if bool(value) else "false"


def iso_datetime(day: str, hour: int) -> str:
    return f"{day}T{hour:02d}:00:00+00:00" if day else ""


def hours_between(start: str, end: str) -> str:
    if not start or not end:
        return ""
    start_dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
    end_dt = datetime.fromisoformat(end.replace("Z", "+00:00"))
    return f"{max((end_dt - start_dt).total_seconds(), 0) / 3600.0:.2f}"


def demo_value(value: Any, fallback: str) -> str:
    text = str(value or "").strip()
    if not text or text == "(blank)":
        return fallback
    return text


def pseudonym(value: str, prefix: str) -> str:
    if not value:
        return ""
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:10]
    return f"{prefix}-{digest}"


def fact_incidents(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    facts: list[dict[str, Any]] = []
    for row in rows:
        incident_id = str(row.get("id", ""))
        caller_id = nested_id(row.get("caller"))
        operator_group_id = nested_id(row.get("operatorGroup"))
        branch_id = first_non_blank_id(row.get("branch"), row.get("callerBranch"))
        target = dt(row.get("targetDate"))
        closed = bool(row.get("closed"))
        facts.append(
            {
                "IncidentId": incident_id,
                "IncidentNumber": row.get("number", ""),
                "Status": nested_label(row.get("status")),
                "Category": nested_label(row.get("category")),
                "Subcategory": nested_label(row.get("subcategory")),
                "Priority": nested_label(row.get("priority")),
                "Impact": nested_label(row.get("impact")),
                "Urgency": nested_label(row.get("urgency")),
                "OperatorGroupId": operator_group_id,
                "OperatorGroup": nested_label(row.get("operatorGroup")),
                "BranchId": branch_id,
                "Branch": first_non_blank_label(row.get("branch"), row.get("callerBranch")),
                "CallerKey": pseudonym(caller_id, "person"),
                "CreationDate": dt(row.get("creationDate")),
                "CallDate": dt(row.get("callDate")),
                "TargetDate": target,
                "ResponseDate": dt(row.get("responseDate")),
                "CompletedDate": dt(row.get("completedDate")),
                "ClosedDate": dt(row.get("closedDate")),
                "IsClosed": bool_value(closed),
                "IsOpen": bool_value(not closed),
                "HasTargetDate": bool_value(bool(target)),
                "HasPriority": bool_value(nested_label(row.get("priority")) != "(blank)"),
                "HasOperatorGroup": bool_value(nested_label(row.get("operatorGroup")) != "(blank)"),
                "HasCategory": bool_value(nested_label(row.get("category")) != "(blank)"),
            }
        )
    return facts


def fact_incident_daily_snapshots(facts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    snapshots: list[dict[str, Any]] = []
    for fact in facts:
        created = fact.get("CreationDate", "")
        if not created:
            continue
        try:
            start = date.fromisoformat(str(created))
        except ValueError:
            continue
        closed_date = fact.get("ClosedDate", "")
        if isinstance(closed_date, str) and closed_date:
            end = min(start + timedelta(days=4), date.fromisoformat(closed_date))
        else:
            end = start + timedelta(days=4)
        current = start
        day_index = 0
        while current <= end:
            if day_index == 0:
                status = "New"
                group = "Service Desk Intake"
                group_id = "demo-group-intake"
            elif day_index == 1:
                status = "In Progress"
                group = demo_value(fact.get("OperatorGroup"), "Second Line")
                group_id = demo_value(fact.get("OperatorGroupId"), "demo-group-second-line")
            elif day_index == 2:
                status = "Waiting"
                group = demo_value(fact.get("OperatorGroup"), "Second Line")
                group_id = demo_value(fact.get("OperatorGroupId"), "demo-group-second-line")
            elif day_index == 3:
                status = "Waiting"
                group = "Resolution Team"
                group_id = "demo-group-resolution"
            else:
                status = "Resolved" if fact.get("IsClosed") == "true" else "In Progress"
                group = "Resolution Team"
                group_id = "demo-group-resolution"
            snapshots.append(
                {
                    "SnapshotDate": current.isoformat(),
                    "IncidentKey": fact.get("IncidentId", ""),
                    "TopdeskNumber": fact.get("IncidentNumber", ""),
                    "StatusId": status.lower().replace(" ", "-"),
                    "StatusName": status,
                    "OperatorGroupId": group_id,
                    "OperatorGroupName": group,
                    "OperatorId": f"demo-operator-{(day_index % 3) + 1}",
                    "OperatorName": f"Demo Operator {(day_index % 3) + 1}",
                    "PriorityId": str(fact.get("Priority", "")).lower().replace(" ", "-"),
                    "PriorityName": fact.get("Priority", ""),
                    "CategoryId": str(fact.get("Category", "")).lower().replace(" ", "-"),
                    "CategoryName": fact.get("Category", ""),
                    "BranchId": fact.get("BranchId", ""),
                    "BranchName": fact.get("Branch", ""),
                    "CreatedAt": iso_datetime(created, 8),
                    "TargetAt": iso_datetime(str(fact.get("TargetDate", "")), 17),
                    "ClosedAt": iso_datetime(closed_date, 16),
                    "IsClosed": "true" if fact.get("IsClosed") == "true" and current.isoformat() >= str(closed_date or "9999-12-31") else "false",
                }
            )
            current += timedelta(days=1)
            day_index += 1
    return snapshots


def fact_status_transitions(facts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for fact in facts:
        incident_id = fact.get("IncidentId", "")
        created = fact.get("CreationDate", "")
        if not incident_id or not created:
            continue
        day0 = date.fromisoformat(str(created))
        intervals = [
            ("new", "New", "in-progress", "In Progress", iso_datetime(day0.isoformat(), 8), iso_datetime((day0 + timedelta(days=1)).isoformat(), 9)),
            ("in-progress", "In Progress", "waiting", "Waiting", iso_datetime((day0 + timedelta(days=1)).isoformat(), 9), iso_datetime((day0 + timedelta(days=2)).isoformat(), 13)),
            ("waiting", "Waiting", "resolved", "Resolved", iso_datetime((day0 + timedelta(days=2)).isoformat(), 13), iso_datetime((day0 + timedelta(days=4)).isoformat(), 16)),
        ]
        for sequence, (from_id, from_name, to_id, to_name, valid_from, valid_to) in enumerate(intervals, start=1):
            rows.append(
                {
                    "TransitionKey": f"{incident_id}-status-{sequence}",
                    "IncidentKey": incident_id,
                    "StatusSequence": sequence,
                    "FromStatusId": from_id,
                    "FromStatusName": from_name,
                    "StatusId": from_id,
                    "StatusName": from_name,
                    "ToStatusId": to_id,
                    "ToStatusName": to_name,
                    "ChangedByOperatorId": f"demo-operator-{sequence}",
                    "ValidFromAt": valid_from,
                    "ValidToAt": valid_to,
                    "DurationHours": hours_between(valid_from, valid_to),
                    "Reason": "Demo lifecycle transition",
                }
            )
    return rows


def fact_assignment_transitions(facts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for fact in facts:
        incident_id = fact.get("IncidentId", "")
        created = fact.get("CreationDate", "")
        if not incident_id or not created:
            continue
        day0 = date.fromisoformat(str(created))
        target_group_id = demo_value(fact.get("OperatorGroupId"), "demo-group-second-line")
        target_group = demo_value(fact.get("OperatorGroup"), "Second Line")
        intervals = [
            ("", "", "demo-group-intake", "Service Desk Intake", iso_datetime(day0.isoformat(), 8), iso_datetime((day0 + timedelta(days=1)).isoformat(), 9)),
            ("demo-group-intake", "Service Desk Intake", target_group_id, target_group, iso_datetime((day0 + timedelta(days=1)).isoformat(), 9), iso_datetime((day0 + timedelta(days=3)).isoformat(), 11)),
            (target_group_id, target_group, "demo-group-resolution", "Resolution Team", iso_datetime((day0 + timedelta(days=3)).isoformat(), 11), iso_datetime((day0 + timedelta(days=4)).isoformat(), 16)),
        ]
        for sequence, (from_group_id, from_group, group_id, group, valid_from, valid_to) in enumerate(intervals, start=1):
            rows.append(
                {
                    "TransitionKey": f"{incident_id}-assignment-{sequence}",
                    "IncidentKey": incident_id,
                    "AssignmentSequence": sequence,
                    "FromOperatorGroupId": from_group_id,
                    "FromOperatorGroupName": from_group,
                    "OperatorGroupId": group_id,
                    "OperatorGroupName": group,
                    "FromOperatorId": f"demo-operator-{max(sequence - 1, 1)}" if from_group_id else "",
                    "FromOperatorName": f"Demo Operator {max(sequence - 1, 1)}" if from_group_id else "",
                    "OperatorId": f"demo-operator-{sequence}",
                    "OperatorName": f"Demo Operator {sequence}",
                    "ChangedByOperatorId": f"demo-operator-{sequence}",
                    "ValidFromAt": valid_from,
                    "ValidToAt": valid_to,
                    "DurationHours": hours_between(valid_from, valid_to),
                    "Reason": "Demo routing handoff",
                }
            )
    return rows


def dim_persons(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for row in rows:
        person_id = str(row.get("id", ""))
        result.append(
            {
                "CallerKey": pseudonym(person_id, "person"),
                "PersonStatus": nested_label(row.get("status")),
                "BranchId": nested_id(row.get("branch")),
                "Branch": nested_label(row.get("branch")),
                "Department": nested_label(row.get("department")),
                "JobTitlePresent": bool_value(bool(row.get("jobTitle"))),
                "EmailPresent": bool_value(bool(row.get("email"))),
                "PhonePresent": bool_value(bool(row.get("phoneNumber") or row.get("mobileNumber"))),
                "IsManager": bool_value(bool(row.get("isManager"))),
            }
        )
    return result


def dim_operator_groups(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "OperatorGroupId": str(row.get("id", "")),
            "OperatorGroup": row.get("groupName", ""),
            "Status": nested_label(row.get("status")),
            "BranchId": nested_id(row.get("branch")),
            "Branch": nested_label(row.get("branch")),
            "FirstLine": bool_value(bool(row.get("firstLineCallOperator"))),
            "SecondLine": bool_value(bool(row.get("secondLineCallOperator"))),
        }
        for row in rows
    ]


def dim_branches(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{"BranchId": str(row.get("id", "")), "Branch": row.get("name", "")} for row in rows]


def dim_date(facts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    dates: list[date] = []
    for row in facts:
        for field in ["CreationDate", "CallDate", "TargetDate", "ResponseDate", "CompletedDate", "ClosedDate"]:
            value = row.get(field)
            if isinstance(value, str) and value:
                try:
                    dates.append(date.fromisoformat(value))
                except ValueError:
                    pass
    if not dates:
        return []
    current = min(dates)
    end = max(dates)
    rows: list[dict[str, Any]] = []
    while current <= end:
        rows.append(
            {
                "Date": current.isoformat(),
                "Year": current.year,
                "MonthNumber": current.month,
                "Month": current.strftime("%Y-%m"),
                "Quarter": f"Q{((current.month - 1) // 3) + 1}",
                "Weekday": current.strftime("%A"),
            }
        )
        current += timedelta(days=1)
    return rows


def count_by(rows: Iterable[dict[str, Any]], field: str) -> dict[str, int]:
    result: dict[str, int] = {}
    for row in rows:
        key = str(row.get(field) or "(blank)")
        result[key] = result.get(key, 0) + 1
    return result


def write_powerquery(out: Path, csv_names: list[str]) -> None:
    query_dir = out / "powerquery"
    query_dir.mkdir(parents=True, exist_ok=True)
    (query_dir / "README.md").write_text(
        "# Power Query Import\n\nCreate a text parameter `ReportRoot` that points to this pack folder, then paste the table queries.\n",
        encoding="utf-8",
    )
    for name in csv_names:
        table = Path(name).stem
        query = f"""// Query: {table}
let
    Source = Csv.Document(File.Contents(ReportRoot & "\\data\\{name}"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true])
in
    PromotedHeaders
"""
        (query_dir / f"{table}.pq").write_text(query, encoding="utf-8")


def write_dax(out: Path) -> None:
    dax = """-- TOPdesk Demo Report Measures
Incident Count = COUNTROWS ( FactIncident )
Open Incident Count = CALCULATE ( [Incident Count], FactIncident[IsOpen] = "true" )
Closed Incident Count = CALCULATE ( [Incident Count], FactIncident[IsClosed] = "true" )
Incidents With Target Date = CALCULATE ( [Incident Count], FactIncident[HasTargetDate] = "true" )
Missing Target Date Count = CALCULATE ( [Incident Count], FactIncident[HasTargetDate] = "false" )
Missing Target Date % = DIVIDE ( [Missing Target Date Count], [Incident Count] )
Routed Incident Count = CALCULATE ( [Incident Count], FactIncident[HasOperatorGroup] = "true" )
Unrouted Incident Count = CALCULATE ( [Incident Count], FactIncident[HasOperatorGroup] = "false" )
Routing Coverage % = DIVIDE ( [Routed Incident Count], [Incident Count] )
Priority Coverage % = DIVIDE ( CALCULATE ( [Incident Count], FactIncident[HasPriority] = "true" ), [Incident Count] )
Category Coverage % = DIVIDE ( CALCULATE ( [Incident Count], FactIncident[HasCategory] = "true" ), [Incident Count] )
Data Quality Findings = COUNTROWS ( DataQualityFindings )
SLA Findings = COUNTROWS ( SLAFinding )
PII Findings = COUNTROWS ( PIIFinding )
High PII Findings = CALCULATE ( [PII Findings], PIIFinding[severity] = "high" )
Snapshot Incident Days = COUNTROWS ( FactIncidentDailySnapshot )
Snapshot Open Incident Days = CALCULATE ( [Snapshot Incident Days], FactIncidentDailySnapshot[IsClosed] = "false" )
Status Transitions = COUNTROWS ( FactStatusTransition )
Average Time In Status Hours = AVERAGE ( FactStatusTransition[DurationHours] )
Assignment Transitions = COUNTROWS ( FactAssignmentTransition )
Reassigned Incidents = CALCULATE ( DISTINCTCOUNT ( FactAssignmentTransition[IncidentKey] ), FactAssignmentTransition[AssignmentSequence] > 1 )
Average Time In Operator Group Hours = AVERAGE ( FactAssignmentTransition[DurationHours] )
"""
    (out / "dax").mkdir(parents=True, exist_ok=True)
    (out / "dax" / "topdesk-demo-measures.dax").write_text(dax, encoding="utf-8")


def write_theme(out: Path) -> None:
    theme = {
        "name": "TOPdesk Service Operations",
        "dataColors": ["#2563EB", "#059669", "#F59E0B", "#DC2626", "#7C3AED", "#0891B2", "#64748B"],
        "background": "#FFFFFF",
        "foreground": "#0F172A",
        "tableAccent": "#2563EB",
        "visualStyles": {"*": {"*": {"fontFamily": [{"fontFamily": "Segoe UI"}]}}},
    }
    (out / "theme").mkdir(parents=True, exist_ok=True)
    (out / "theme" / "topdesk-service-operations-theme.json").write_text(json.dumps(theme, indent=2), encoding="utf-8")


def write_report_spec(out: Path, summary: dict[str, Any]) -> None:
    text = f"""# TOPdesk Demo Power BI Report

## Purpose

Import-ready Power BI implementation pack for a TOPdesk Operations, SLA, Data Quality, and Compliance report.

## Generated Data

- Incidents: {summary['incidents']}
- Persons: {summary['persons']}
- Operator groups: {summary['operatorgroups']}
- Branches: {summary['branches']}
- Daily snapshot rows: {summary['daily_snapshots']}
- Status transition rows: {summary['status_transitions']}
- Assignment transition rows: {summary['assignment_transitions']}
- Data-quality findings: {summary['data_quality_findings']}
- SLA findings: {summary['sla_findings']}
- PII findings: {summary['pii_findings']}

## Model

- `FactIncident` at one row per incident.
- `FactIncidentDailySnapshot` at one row per incident per demo snapshot date.
- `FactStatusTransition` contains synthetic status intervals for lifecycle/aging demos.
- `FactAssignmentTransition` contains synthetic operator-group handoff intervals.
- `DimDate` with date roles for creation, call, target, response, completed, and closed dates.
- `DimPerson` is pseudonymized and excludes names, emails, phone numbers, login names, request text, and comments.
- `DimOperatorGroup` and `DimBranch` support routing and branch slicing.
- `DataQualityFindings`, `SLAFinding`, and `PIIFinding` provide operational action tables.

## Pages

1. Executive Overview: KPI cards for incident count, open backlog, routing coverage, priority coverage, target-date coverage, and high PII findings.
2. Service Desk Operations: backlog by operator group, status, priority, branch, and daily trend.
3. SLA & Backlog Risk: SLA findings table, missing target dates, unrouted incidents, and priority gaps.
4. Data Quality: missing-field findings, field coverage, quality trend placeholders, and cleanup owner notes.
5. PII & Compliance: PII findings by entity/severity plus minimization recommendations.
6. Info: source, refresh timestamp, KPI definitions, exclusions, and RLS notes.

## Relationships

- `FactIncident[CreationDate]` many-to-one `DimDate[Date]` as active default date relation.
- Additional inactive date relations for target, response, completed, and closed dates.
- `FactIncident[OperatorGroupId]` many-to-one `DimOperatorGroup[OperatorGroupId]`.
- `FactIncident[BranchId]` many-to-one `DimBranch[BranchId]`.
- `FactIncident[CallerKey]` many-to-one `DimPerson[CallerKey]`.
- `FactIncidentDailySnapshot[IncidentKey]` many-to-one `FactIncident[IncidentId]`.
- `FactStatusTransition[IncidentKey]` many-to-one `FactIncident[IncidentId]`.
- `FactAssignmentTransition[IncidentKey]` many-to-one `FactIncident[IncidentId]`.

## Build Steps In Power BI Desktop

1. Create parameter `ReportRoot` with the absolute folder path of this pack.
2. Paste the `.pq` queries from `powerquery/` or import the CSV files from `data/`.
3. Set data types, create relationships, and mark `DimDate` as the date table.
4. Paste measures from `dax/topdesk-demo-measures.dax`.
5. Import `theme/topdesk-service-operations-theme.json`.
6. Build pages from this spec and reconcile counts against `REPORT_SPEC.md`.

## Security Notes

This pack uses sanitized CSV tables. Raw request text, names, email addresses, phone numbers, login names, and comments are intentionally excluded.
"""
    (out / "REPORT_SPEC.md").write_text(text, encoding="utf-8")


def write_build_guide(out: Path) -> None:
    text = """# Build In Power BI Desktop

## Fast Path

1. Open Power BI Desktop.
2. Get Data > Text/CSV and import every CSV from `data/`.
3. Set booleans stored as `true`/`false` text to True/False if preferred.
4. Set date columns in `FactIncident` and `DimDate[Date]` to Date.
5. Create the relationships listed in `REPORT_SPEC.md`.
6. Paste the measures from `dax/topdesk-demo-measures.dax`.
7. View > Themes > Browse for themes and import `theme/topdesk-service-operations-theme.json`.

## Recommended Pages

- Executive Overview: KPI cards and trend.
- Service Desk Operations: group, priority, status, and branch breakdowns.
- Incident Lifecycle: status duration, operator-group handoffs, and snapshot aging.
- SLA & Backlog Risk: `SLAFinding` table plus missing target/routing KPIs.
- Data Quality: `DataQualityFindings` table and severity breakdown.
- PII & Compliance: `PIIFinding` table by entity and severity.

## Suggested Visuals

Executive Overview:
- Cards: `Incident Count`, `Open Incident Count`, `Routing Coverage %`, `Priority Coverage %`, `Missing Target Date %`, `High PII Findings`.
- Line chart: `Incident Count` by `DimDate[Date]`.
- Bar chart: `Open Incident Count` by `FactIncident[OperatorGroup]`.

SLA & Backlog Risk:
- Table: `SLAFinding[incident]`, `SLAFinding[severity]`, `SLAFinding[finding]`, `SLAFinding[action]`.
- Bar chart: `SLA Findings` by `SLAFinding[finding]`.
- Donut or bar: `Incident Count` by `FactIncident[Priority]`.

Incident Lifecycle:
- Cards: `Status Transitions`, `Assignment Transitions`, `Average Time In Status Hours`, `Average Time In Operator Group Hours`.
- Bar chart: `Average Time In Operator Group Hours` by `FactAssignmentTransition[OperatorGroupName]`.
- Line chart: `Snapshot Open Incident Days` by `FactIncidentDailySnapshot[SnapshotDate]`.
- Table: `FactAssignmentTransition[IncidentKey]`, `FactAssignmentTransition[OperatorGroupName]`, `FactAssignmentTransition[ValidFromAt]`, `FactAssignmentTransition[ValidToAt]`, `FactAssignmentTransition[DurationHours]`.

Data Quality:
- Matrix: `DataQualityFindings[entity]`, `DataQualityFindings[field]`, count by severity.
- Bar chart: `Data Quality Findings` by `DataQualityFindings[severity]`.

PII & Compliance:
- Bar chart: `PII Findings` by `PIIFinding[severity]`.
- Table: `PIIFinding[entity]`, `PIIFinding[field]`, `PIIFinding[recommendation]`.
"""
    (out / "BUILD_IN_POWER_BI.md").write_text(text, encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.tenant_profile
    snapshots = root / "snapshots"
    incidents = load_json(snapshots / "incidents.json")
    persons = load_json(snapshots / "persons.json")
    operatorgroups = load_json(snapshots / "operatorgroups.json")
    branches = load_json(snapshots / "branches.json")
    facts = fact_incidents(incidents)
    daily_snapshots = fact_incident_daily_snapshots(facts)
    status_transitions = fact_status_transitions(facts)
    assignment_transitions = fact_assignment_transitions(facts)
    data_dir = args.out / "data"
    write_csv(
        data_dir / "FactIncident.csv",
        facts,
        [
            "IncidentId",
            "IncidentNumber",
            "Status",
            "Category",
            "Subcategory",
            "Priority",
            "Impact",
            "Urgency",
            "OperatorGroupId",
            "OperatorGroup",
            "BranchId",
            "Branch",
            "CallerKey",
            "CreationDate",
            "CallDate",
            "TargetDate",
            "ResponseDate",
            "CompletedDate",
            "ClosedDate",
            "IsClosed",
            "IsOpen",
            "HasTargetDate",
            "HasPriority",
            "HasOperatorGroup",
            "HasCategory",
        ],
    )
    write_csv(data_dir / "DimPerson.csv", dim_persons(persons), ["CallerKey", "PersonStatus", "BranchId", "Branch", "Department", "JobTitlePresent", "EmailPresent", "PhonePresent", "IsManager"])
    write_csv(data_dir / "DimOperatorGroup.csv", dim_operator_groups(operatorgroups), ["OperatorGroupId", "OperatorGroup", "Status", "BranchId", "Branch", "FirstLine", "SecondLine"])
    write_csv(data_dir / "DimBranch.csv", dim_branches(branches), ["BranchId", "Branch"])
    write_csv(data_dir / "DimDate.csv", dim_date(facts), ["Date", "Year", "MonthNumber", "Month", "Quarter", "Weekday"])
    write_csv(
        data_dir / "FactIncidentDailySnapshot.csv",
        daily_snapshots,
        [
            "SnapshotDate",
            "IncidentKey",
            "TopdeskNumber",
            "StatusId",
            "StatusName",
            "OperatorGroupId",
            "OperatorGroupName",
            "OperatorId",
            "OperatorName",
            "PriorityId",
            "PriorityName",
            "CategoryId",
            "CategoryName",
            "BranchId",
            "BranchName",
            "CreatedAt",
            "TargetAt",
            "ClosedAt",
            "IsClosed",
        ],
    )
    write_csv(
        data_dir / "FactStatusTransition.csv",
        status_transitions,
        [
            "TransitionKey",
            "IncidentKey",
            "StatusSequence",
            "FromStatusId",
            "FromStatusName",
            "StatusId",
            "StatusName",
            "ToStatusId",
            "ToStatusName",
            "ChangedByOperatorId",
            "ValidFromAt",
            "ValidToAt",
            "DurationHours",
            "Reason",
        ],
    )
    write_csv(
        data_dir / "FactAssignmentTransition.csv",
        assignment_transitions,
        [
            "TransitionKey",
            "IncidentKey",
            "AssignmentSequence",
            "FromOperatorGroupId",
            "FromOperatorGroupName",
            "OperatorGroupId",
            "OperatorGroupName",
            "FromOperatorId",
            "FromOperatorName",
            "OperatorId",
            "OperatorName",
            "ChangedByOperatorId",
            "ValidFromAt",
            "ValidToAt",
            "DurationHours",
            "Reason",
        ],
    )
    dq = load_csv(root / "data_quality_findings.csv")
    sla = load_csv(root / "sla-analysis" / "sla-findings.csv")
    pii = load_csv(root / "pii-review" / "pii-field-findings.csv")
    write_csv(data_dir / "DataQualityFindings.csv", dq, ["entity", "field", "severity", "finding", "impact", "details"])
    write_csv(data_dir / "SLAFinding.csv", sla, ["incident", "severity", "finding", "priority", "operator_group", "action"])
    write_csv(data_dir / "PIIFinding.csv", pii, ["entity", "field", "category", "severity", "non_empty_count", "recommendation"])
    write_powerquery(
        args.out,
        [
            "FactIncident.csv",
            "DimPerson.csv",
            "DimOperatorGroup.csv",
            "DimBranch.csv",
            "DimDate.csv",
            "FactIncidentDailySnapshot.csv",
            "FactStatusTransition.csv",
            "FactAssignmentTransition.csv",
            "DataQualityFindings.csv",
            "SLAFinding.csv",
            "PIIFinding.csv",
        ],
    )
    write_dax(args.out)
    write_theme(args.out)
    write_report_spec(
        args.out,
        {
            "incidents": len(incidents),
            "persons": len(persons),
            "operatorgroups": len(operatorgroups),
            "branches": len(branches),
            "daily_snapshots": len(daily_snapshots),
            "status_transitions": len(status_transitions),
            "assignment_transitions": len(assignment_transitions),
            "data_quality_findings": len(dq),
            "sla_findings": len(sla),
            "pii_findings": len(pii),
        },
    )
    write_build_guide(args.out)
    print(f"Wrote TOPdesk Power BI report pack to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
