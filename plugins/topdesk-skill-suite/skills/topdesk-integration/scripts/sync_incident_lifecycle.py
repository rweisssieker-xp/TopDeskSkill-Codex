#!/usr/bin/env python3
"""Build TOPdesk incident lifecycle import files for history and daily snapshots.

The script supports two practical source modes:

- API mode reads TOPdesk REST endpoints using TOPDESK_BASE_URL,
  TOPDESK_USERNAME, and TOPDESK_APP_PASSWORD.
- File mode reads exported JSON arrays for incidents and optional history/audit
  events.

Outputs are CSV files shaped for the repository's canonical model:

- incident_daily_snapshots.csv
- incident_status_history.csv
- incident_assignment_history.csv
- FactStatusTransition.csv
- FactAssignmentTransition.csv
"""

from __future__ import annotations

import argparse
import base64
import csv
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence


DEFAULT_INCIDENTS_ENDPOINT = "/tas/api/incidents"
STATUS_HINTS = {"status", "processingstatus", "processing_status"}
ASSIGNMENT_HINTS = {
    "operatorgroup",
    "operator_group",
    "assignedgroup",
    "assigned_group",
    "operator",
    "assignee",
    "assignedoperator",
    "assigned_operator",
}


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create TOPdesk incident lifecycle CSV imports")
    parser.add_argument("--out", required=True, type=Path, help="Output directory")
    parser.add_argument("--snapshot-date", default=date.today().isoformat(), help="Snapshot date in YYYY-MM-DD format")
    parser.add_argument("--incidents-json", type=Path, help="Incident JSON array export. If omitted, API mode is used.")
    parser.add_argument("--history-json", type=Path, help="History/audit/event JSON array export")
    parser.add_argument("--incidents-endpoint", default=DEFAULT_INCIDENTS_ENDPOINT)
    parser.add_argument("--history-endpoint", help="Optional API endpoint that returns status/group history events")
    parser.add_argument("--page-size", type=int, default=100)
    parser.add_argument("--max-records", type=int, default=0, help="Optional maximum records per endpoint; 0 means no limit")
    parser.add_argument("--write-raw", action="store_true", help="Store raw API JSON payloads under out/raw")
    return parser.parse_args(argv)


def auth_header(username: str, app_password: str) -> str:
    raw = f"{username}:{app_password}".encode("utf-8")
    return "Basic " + base64.b64encode(raw).decode("ascii")


def endpoint_url(base_url: str, path: str, start: int, page_size: int) -> str:
    parsed = urllib.parse.urlsplit(path)
    query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    query.extend([("start", str(start)), ("page_size", str(page_size))])
    path_with_query = urllib.parse.urlunsplit(("", "", parsed.path, urllib.parse.urlencode(query), ""))
    return f"{base_url.rstrip('/')}{path_with_query}"


def request_json(base_url: str, path: str, username: str, app_password: str, start: int, page_size: int) -> Any:
    request = urllib.request.Request(
        endpoint_url(base_url, path, start, page_size),
        headers={"Authorization": auth_header(username, app_password), "Accept": "application/json"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"{path} returned HTTP {exc.code}") from exc


def fetch_endpoint(base_url: str, path: str, username: str, app_password: str, page_size: int, max_records: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    start = 0
    while True:
        payload = request_json(base_url, path, username, app_password, start, page_size)
        if isinstance(payload, dict) and isinstance(payload.get("results"), list):
            page = payload["results"]
        elif isinstance(payload, list):
            page = payload
        else:
            raise RuntimeError(f"{path} returned {type(payload).__name__}, expected list or results list")
        page_rows = [row for row in page if isinstance(row, dict)]
        rows.extend(page_rows)
        if max_records and len(rows) >= max_records:
            return rows[:max_records]
        if len(page_rows) < page_size:
            return rows
        start += page_size


def load_json_array(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, list):
        raise ValueError(f"{path} must contain a JSON array")
    return [row for row in payload if isinstance(row, dict)]


def first_value(row: dict[str, Any], keys: Iterable[str]) -> Any:
    for key in keys:
        if key in row and row[key] not in (None, ""):
            return row[key]
    return ""


def nested_id(value: Any) -> str:
    if isinstance(value, dict):
        for key in ("id", "uuid", "number", "topdesk_id", "value"):
            if value.get(key) not in (None, ""):
                return str(value[key])
    if value not in (None, "") and not isinstance(value, (list, tuple, dict)):
        return str(value)
    return ""


def nested_label(value: Any) -> str:
    if isinstance(value, dict):
        for key in ("name", "groupName", "dynamicName", "displayName", "label", "number", "id", "value"):
            if value.get(key) not in (None, ""):
                return str(value[key])
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    if value is None:
        return ""
    if isinstance(value, list):
        return f"[{len(value)} items]"
    return str(value)


def bool_text(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return "true" if value.strip().lower() in {"true", "1", "yes", "ja"} else "false"
    return "true" if bool(value) else "false"


def timestamp_text(value: Any) -> str:
    if value in (None, ""):
        return ""
    return str(value)


def parse_datetime(value: str) -> datetime | None:
    if not value:
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed


def hours_between(start: str, end: str) -> str:
    start_dt = parse_datetime(start)
    end_dt = parse_datetime(end)
    if not start_dt or not end_dt:
        return ""
    return f"{max((end_dt - start_dt).total_seconds(), 0) / 3600.0:.6f}"


def incident_id(row: dict[str, Any]) -> str:
    return str(first_value(row, ("id", "topdesk_id", "incidentId", "incident_id", "unid", "number")))


def incident_number(row: dict[str, Any]) -> str:
    return str(first_value(row, ("number", "topdesk_number", "incidentNumber", "callNumber")))


def build_daily_snapshots(incidents: list[dict[str, Any]], snapshot_date: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for incident in incidents:
        status = first_value(incident, ("status", "processingStatus", "processing_status"))
        group = first_value(incident, ("operatorGroup", "assignedGroup", "operator_group", "assigned_group"))
        operator = first_value(incident, ("operator", "assignee", "assignedOperator", "assigned_operator"))
        rows.append(
            {
                "snapshot_date": snapshot_date,
                "incident_id": incident_id(incident),
                "topdesk_id": incident_id(incident),
                "topdesk_number": incident_number(incident),
                "status_id": nested_id(status),
                "status_name": nested_label(status),
                "assigned_group_id": nested_id(group),
                "assigned_group_name": nested_label(group),
                "assigned_operator_id": nested_id(operator),
                "assigned_operator_name": nested_label(operator),
                "priority_id": nested_id(first_value(incident, ("priority",))),
                "priority_name": nested_label(first_value(incident, ("priority",))),
                "category_id": nested_id(first_value(incident, ("category",))),
                "category_name": nested_label(first_value(incident, ("category",))),
                "branch_id": nested_id(first_value(incident, ("branch", "callerBranch"))),
                "branch_name": nested_label(first_value(incident, ("branch", "callerBranch"))),
                "created_at": timestamp_text(first_value(incident, ("creationDate", "callDate", "created_at", "createdAt"))),
                "modified_at": timestamp_text(first_value(incident, ("modificationDate", "modified_at", "modifiedAt"))),
                "target_at": timestamp_text(first_value(incident, ("targetDate", "target_at", "targetAt"))),
                "closed_at": timestamp_text(first_value(incident, ("closedDate", "completedDate", "closed_at", "closedAt"))),
                "is_closed": bool_text(first_value(incident, ("closed", "isClosed", "is_closed"))),
                "snapshot_loaded_at": datetime.now(timezone.utc).isoformat(),
            }
        )
    return rows


def lower_field(value: Any) -> str:
    return str(value or "").replace(" ", "").replace("-", "").lower()


def event_field(event: dict[str, Any]) -> str:
    return lower_field(first_value(event, ("field", "fieldName", "attribute", "property", "name", "changeType", "type")))


def event_changed_at(event: dict[str, Any]) -> str:
    return timestamp_text(first_value(event, ("changedAt", "changeDate", "timestamp", "date", "actionDate", "createdAt", "occurredAt")))


def event_actor_id(event: dict[str, Any]) -> str:
    return nested_id(first_value(event, ("changedBy", "actor", "operator", "person", "user")))


def event_incident_id(event: dict[str, Any]) -> str:
    value = first_value(event, ("incidentId", "incident_id", "cardId", "entityId", "entity_id", "ticketId", "callId"))
    if value:
        return nested_id(value)
    incident = first_value(event, ("incident", "ticket", "call", "card"))
    return nested_id(incident)


def old_new_values(event: dict[str, Any]) -> tuple[Any, Any]:
    old_value = first_value(event, ("oldValue", "old_value", "from", "fromValue", "previousValue", "before"))
    new_value = first_value(event, ("newValue", "new_value", "to", "toValue", "currentValue", "after"))
    if isinstance(event.get("change"), dict):
        change = event["change"]
        old_value = old_value or first_value(change, ("oldValue", "from", "before"))
        new_value = new_value or first_value(change, ("newValue", "to", "after"))
    return old_value, new_value


def is_status_event(event: dict[str, Any]) -> bool:
    field = event_field(event)
    return any(hint in field for hint in STATUS_HINTS)


def is_assignment_event(event: dict[str, Any]) -> bool:
    field = event_field(event)
    return any(hint in field for hint in ASSIGNMENT_HINTS)


def build_status_history(events: list[dict[str, Any]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, event in enumerate(events, start=1):
        if not is_status_event(event):
            continue
        old_value, new_value = old_new_values(event)
        changed_at = event_changed_at(event)
        inc_id = event_incident_id(event)
        if not inc_id or not changed_at or not nested_id(new_value):
            continue
        rows.append(
            {
                "id": str(first_value(event, ("id", "eventId")) or f"status-{index}"),
                "incident_id": inc_id,
                "from_status_id": nested_id(old_value),
                "from_status_name": nested_label(old_value),
                "to_status_id": nested_id(new_value),
                "to_status_name": nested_label(new_value),
                "changed_by_operator_id": event_actor_id(event),
                "changed_at": changed_at,
                "reason": nested_label(first_value(event, ("reason", "memo", "description", "comment"))),
            }
        )
    return sorted(rows, key=lambda row: (row["incident_id"], row["changed_at"], row["id"]))


def build_assignment_history(events: list[dict[str, Any]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, event in enumerate(events, start=1):
        if not is_assignment_event(event):
            continue
        old_value, new_value = old_new_values(event)
        changed_at = event_changed_at(event)
        inc_id = event_incident_id(event)
        if not inc_id or not changed_at or not nested_id(new_value):
            continue
        field = event_field(event)
        is_operator = "operator" in field and "group" not in field
        rows.append(
            {
                "id": str(first_value(event, ("id", "eventId")) or f"assignment-{index}"),
                "incident_id": inc_id,
                "from_group_id": "" if is_operator else nested_id(old_value),
                "from_group_name": "" if is_operator else nested_label(old_value),
                "to_group_id": "" if is_operator else nested_id(new_value),
                "to_group_name": "" if is_operator else nested_label(new_value),
                "from_operator_id": nested_id(old_value) if is_operator else "",
                "from_operator_name": nested_label(old_value) if is_operator else "",
                "to_operator_id": nested_id(new_value) if is_operator else "",
                "to_operator_name": nested_label(new_value) if is_operator else "",
                "changed_by_operator_id": event_actor_id(event),
                "changed_at": changed_at,
                "reason": nested_label(first_value(event, ("reason", "memo", "description", "comment"))),
            }
        )
    return sorted(rows, key=lambda row: (row["incident_id"], row["changed_at"], row["id"]))


def closed_at_by_incident(incidents: list[dict[str, Any]]) -> dict[str, str]:
    result: dict[str, str] = {}
    for incident in incidents:
        inc_id = incident_id(incident)
        if not inc_id:
            continue
        result[inc_id] = timestamp_text(first_value(incident, ("closedDate", "completedDate", "closed_at", "closedAt")))
    return result


def build_status_transition_facts(status_rows: list[dict[str, str]], incident_closed_at: dict[str, str]) -> list[dict[str, str]]:
    now_text = datetime.now(timezone.utc).isoformat()
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in status_rows:
        grouped.setdefault(row["incident_id"], []).append(row)
    facts: list[dict[str, str]] = []
    for inc_id, rows in grouped.items():
        ordered = sorted(rows, key=lambda row: (row["changed_at"], row["id"]))
        for index, row in enumerate(ordered, start=1):
            valid_to = ordered[index]["changed_at"] if index < len(ordered) else incident_closed_at.get(inc_id) or now_text
            facts.append(
                {
                    "TransitionKey": row["id"],
                    "IncidentKey": inc_id,
                    "StatusSequence": str(index),
                    "FromStatusId": row["from_status_id"],
                    "FromStatusName": row["from_status_name"],
                    "ToStatusId": row["to_status_id"],
                    "ToStatusName": row["to_status_name"],
                    "ChangedByOperatorId": row["changed_by_operator_id"],
                    "ValidFromAt": row["changed_at"],
                    "ValidToAt": valid_to,
                    "DurationHours": hours_between(row["changed_at"], valid_to),
                    "Reason": row["reason"],
                }
            )
    return facts


def build_assignment_transition_facts(assignment_rows: list[dict[str, str]], incident_closed_at: dict[str, str]) -> list[dict[str, str]]:
    now_text = datetime.now(timezone.utc).isoformat()
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in assignment_rows:
        grouped.setdefault(row["incident_id"], []).append(row)
    facts: list[dict[str, str]] = []
    for inc_id, rows in grouped.items():
        ordered = sorted(rows, key=lambda row: (row["changed_at"], row["id"]))
        for index, row in enumerate(ordered, start=1):
            valid_to = ordered[index]["changed_at"] if index < len(ordered) else incident_closed_at.get(inc_id) or now_text
            facts.append(
                {
                    "TransitionKey": row["id"],
                    "IncidentKey": inc_id,
                    "AssignmentSequence": str(index),
                    "FromOperatorGroupId": row["from_group_id"],
                    "FromOperatorGroupName": row["from_group_name"],
                    "OperatorGroupId": row["to_group_id"],
                    "OperatorGroupName": row["to_group_name"],
                    "FromOperatorId": row["from_operator_id"],
                    "FromOperatorName": row["from_operator_name"],
                    "OperatorId": row["to_operator_id"],
                    "OperatorName": row["to_operator_name"],
                    "ChangedByOperatorId": row["changed_by_operator_id"],
                    "ValidFromAt": row["changed_at"],
                    "ValidToAt": valid_to,
                    "DurationHours": hours_between(row["changed_at"], valid_to),
                    "Reason": row["reason"],
                }
            )
    return facts


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def report(
    out: Path,
    incidents: list[dict[str, Any]],
    events: list[dict[str, Any]],
    status_rows: list[dict[str, str]],
    assignment_rows: list[dict[str, str]],
    snapshot_rows: list[dict[str, str]],
    status_facts: list[dict[str, str]],
    assignment_facts: list[dict[str, str]],
) -> None:
    lines = [
        "# TOPdesk Incident Lifecycle Import",
        "",
        "| Artifact | Rows |",
        "| --- | ---: |",
        f"| Source incidents | {len(incidents)} |",
        f"| Source history events | {len(events)} |",
        f"| Daily snapshots | {len(snapshot_rows)} |",
        f"| Status history | {len(status_rows)} |",
        f"| Assignment history | {len(assignment_rows)} |",
        f"| FactStatusTransition | {len(status_facts)} |",
        f"| FactAssignmentTransition | {len(assignment_facts)} |",
        "",
        "## Notes",
        "",
        "- Daily snapshots are suitable for backlog-as-of and approximate aging.",
        "- Status and assignment history are exact only when the source event feed contains every relevant field change.",
        "- The script writes display names beside IDs so mappings can be reviewed before loading into a relational model.",
        "- Credentials are never written to the output.",
    ]
    (out / "incident_lifecycle_import_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)

    if args.incidents_json:
        incidents = load_json_array(args.incidents_json)
    else:
        base_url = os.environ.get("TOPDESK_BASE_URL", "").strip()
        username = os.environ.get("TOPDESK_USERNAME", "").strip()
        app_password = os.environ.get("TOPDESK_APP_PASSWORD", "")
        if not base_url or not username or not app_password:
            print("Set TOPDESK_BASE_URL, TOPDESK_USERNAME, and TOPDESK_APP_PASSWORD or pass --incidents-json.", file=sys.stderr)
            return 2
        incidents = fetch_endpoint(base_url, args.incidents_endpoint, username, app_password, args.page_size, args.max_records)
        if args.write_raw:
            write_json(args.out / "raw" / "incidents.json", incidents)

    if args.history_json:
        events = load_json_array(args.history_json)
    elif args.history_endpoint:
        base_url = os.environ.get("TOPDESK_BASE_URL", "").strip()
        username = os.environ.get("TOPDESK_USERNAME", "").strip()
        app_password = os.environ.get("TOPDESK_APP_PASSWORD", "")
        if not base_url or not username or not app_password:
            print("Set TOPDESK_BASE_URL, TOPDESK_USERNAME, and TOPDESK_APP_PASSWORD for --history-endpoint.", file=sys.stderr)
            return 2
        events = fetch_endpoint(base_url, args.history_endpoint, username, app_password, args.page_size, args.max_records)
        if args.write_raw:
            write_json(args.out / "raw" / "history.json", events)
    else:
        events = []

    snapshot_rows = build_daily_snapshots(incidents, args.snapshot_date)
    status_rows = build_status_history(events)
    assignment_rows = build_assignment_history(events)
    closed_map = closed_at_by_incident(incidents)
    status_facts = build_status_transition_facts(status_rows, closed_map)
    assignment_facts = build_assignment_transition_facts(assignment_rows, closed_map)

    write_csv(
        args.out / "incident_daily_snapshots.csv",
        snapshot_rows,
        [
            "snapshot_date",
            "incident_id",
            "topdesk_id",
            "topdesk_number",
            "status_id",
            "status_name",
            "assigned_group_id",
            "assigned_group_name",
            "assigned_operator_id",
            "assigned_operator_name",
            "priority_id",
            "priority_name",
            "category_id",
            "category_name",
            "branch_id",
            "branch_name",
            "created_at",
            "modified_at",
            "target_at",
            "closed_at",
            "is_closed",
            "snapshot_loaded_at",
        ],
    )
    write_csv(
        args.out / "incident_status_history.csv",
        status_rows,
        ["id", "incident_id", "from_status_id", "from_status_name", "to_status_id", "to_status_name", "changed_by_operator_id", "changed_at", "reason"],
    )
    write_csv(
        args.out / "incident_assignment_history.csv",
        assignment_rows,
        [
            "id",
            "incident_id",
            "from_group_id",
            "from_group_name",
            "to_group_id",
            "to_group_name",
            "from_operator_id",
            "from_operator_name",
            "to_operator_id",
            "to_operator_name",
            "changed_by_operator_id",
            "changed_at",
            "reason",
        ],
    )
    write_csv(
        args.out / "FactStatusTransition.csv",
        status_facts,
        [
            "TransitionKey",
            "IncidentKey",
            "StatusSequence",
            "FromStatusId",
            "FromStatusName",
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
        args.out / "FactAssignmentTransition.csv",
        assignment_facts,
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
    report(args.out, incidents, events, status_rows, assignment_rows, snapshot_rows, status_facts, assignment_facts)
    print(f"Wrote incident lifecycle import files to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
