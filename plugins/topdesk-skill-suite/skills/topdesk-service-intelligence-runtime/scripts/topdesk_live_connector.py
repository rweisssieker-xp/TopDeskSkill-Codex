#!/usr/bin/env python3
"""Minimal TOPdesk connector utility for preflight checks and approved endpoint exports."""

from __future__ import annotations

import argparse
import base64
import ctypes
import csv
import json
import os
import sys
from pathlib import Path
from typing import Any, Sequence
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


ENV_BASE_URL = "TOPDESK_BASE_URL"
ENV_USERNAME = "TOPDESK_USERNAME"
ENV_PASSWORD = "TOPDESK_APP_PASSWORD"


class DataBlob(ctypes.Structure):
    _fields_ = [("cbData", ctypes.c_uint), ("pbData", ctypes.POINTER(ctypes.c_byte))]


def bytes_from_blob(blob: DataBlob) -> bytes:
    return ctypes.string_at(blob.pbData, blob.cbData)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TOPdesk live connector helper")
    sub = parser.add_subparsers(dest="command", required=True)
    preflight = sub.add_parser("preflight", help="Check required environment variables without fetching data")
    preflight.add_argument("--secret-store", type=Path, help="Optional local DPAPI secret store")
    export = sub.add_parser("export", help="Export one approved TOPdesk endpoint")
    export.add_argument("--endpoint", required=True, help="Relative endpoint such as /tas/api/incidents")
    export.add_argument("--out", type=Path, required=True, help="Output JSON or CSV file")
    export.add_argument("--format", choices=("json", "csv"), default="json")
    export.add_argument("--limit", type=int, default=1000)
    export.add_argument("--secret-store", type=Path, help="Optional local DPAPI secret store")
    return parser.parse_args(argv)


def unprotect(value: str) -> str:
    if os.name != "nt":
        raise RuntimeError("Windows DPAPI secret store requires Windows")
    encrypted = base64.b64decode(value)
    input_buffer = ctypes.create_string_buffer(encrypted)
    input_blob = DataBlob(len(encrypted), ctypes.cast(input_buffer, ctypes.POINTER(ctypes.c_byte)))
    output_blob = DataBlob()
    if not ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(input_blob), None, None, None, None, 0, ctypes.byref(output_blob)):
        raise ctypes.WinError()
    try:
        return bytes_from_blob(output_blob).decode("utf-8")
    finally:
        ctypes.windll.kernel32.LocalFree(output_blob.pbData)


def secret_store_values(path: Path | None) -> dict[str, str]:
    if not path:
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {key: unprotect(value) for key, value in (payload.get("secrets") or {}).items()}


def credentials(secret_store: Path | None = None) -> tuple[str, str, str]:
    secrets = secret_store_values(secret_store)
    base_url = (os.environ.get(ENV_BASE_URL) or secrets.get(ENV_BASE_URL, "")).strip().rstrip("/") + "/"
    username = (os.environ.get(ENV_USERNAME) or secrets.get(ENV_USERNAME, "")).strip()
    password = os.environ.get(ENV_PASSWORD) or secrets.get(ENV_PASSWORD, "")
    return base_url, username, password


def preflight(secret_store: Path | None = None) -> int:
    base_url, username, password = credentials(secret_store)
    missing = [name for name, value in ((ENV_BASE_URL, base_url), (ENV_USERNAME, username), (ENV_PASSWORD, password)) if not value or value == "/"]
    result = {
        "base_url_configured": bool(base_url and base_url != "/"),
        "username_configured": bool(username),
        "password_configured": bool(password),
        "ready_for_live_fetch": not missing,
        "missing": missing,
    }
    print(json.dumps(result, indent=2))
    return 0 if not missing else 2


def request_json(endpoint: str, limit: int, secret_store: Path | None = None) -> Any:
    base_url, username, password = credentials(secret_store)
    if not base_url or base_url == "/" or not username or not password:
        raise RuntimeError("TOPdesk credentials are incomplete. Run preflight first.")
    url = urljoin(base_url, endpoint.lstrip("/"))
    if "page_size=" not in url and "limit=" not in url and "size=" not in url:
        separator = "&" if "?" in url else "?"
        url = f"{url}{separator}page_size={limit}"
    token = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
    req = Request(url, headers={"Authorization": f"Basic {token}", "Accept": "application/json"})
    with urlopen(req, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def rows_from_payload(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        rows = payload
    elif isinstance(payload, dict):
        rows = payload.get("results") or payload.get("data") or payload.get("items") or [payload]
    else:
        rows = [{"value": payload}]
    return [row if isinstance(row, dict) else {"value": row} for row in rows]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value for key, value in row.items()})


def export_endpoint(args: argparse.Namespace) -> int:
    try:
        payload = request_json(args.endpoint, args.limit, args.secret_store)
    except (HTTPError, URLError, RuntimeError) as exc:
        print(f"Export failed: {exc}", file=sys.stderr)
        return 1
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.format == "json":
        args.out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    else:
        write_csv(args.out, rows_from_payload(payload))
    print(f"Wrote {args.out}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.command == "preflight":
        return preflight(args.secret_store)
    if args.command == "export":
        return export_endpoint(args)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

