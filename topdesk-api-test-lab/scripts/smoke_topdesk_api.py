#!/usr/bin/env python3
"""Run TOPdesk REST API smoke checks without storing credentials."""

from __future__ import annotations

import argparse
import base64
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Sequence


DEFAULT_ENDPOINTS = {
    "incidents": "/tas/api/incidents",
    "persons": "/tas/api/persons",
    "operatorgroups": "/tas/api/operatorgroups",
    "branches": "/tas/api/branches",
    "reporting_odata_metadata": "/services/reporting/v2/odata/$metadata",
}


def parse_endpoint(value: str) -> tuple[str, str]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("Endpoint must use name=/path format")
    name, path = value.split("=", 1)
    if not name or not path.startswith("/"):
        raise argparse.ArgumentTypeError("Endpoint must use name=/path format")
    return name, path


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Smoke-test TOPdesk API endpoints")
    parser.add_argument("--out", type=Path, default=Path("topdesk-api-smoke.md"))
    parser.add_argument("--page-size", type=int, default=10)
    parser.add_argument("--endpoint", action="append", type=parse_endpoint, default=[])
    return parser.parse_args(argv)


def auth_header(username: str, app_password: str) -> str:
    raw = f"{username}:{app_password}".encode("utf-8")
    return "Basic " + base64.b64encode(raw).decode("ascii")


def request_endpoint(base_url: str, path: str, username: str, app_password: str, page_size: int) -> dict[str, Any]:
    joiner = "&" if "?" in path else "?"
    url = f"{base_url.rstrip('/')}{path}{joiner}start=0&page_size={page_size}"
    request = urllib.request.Request(
        url,
        headers={"Authorization": auth_header(username, app_password), "Accept": "application/json"},
        method="GET",
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read()
            elapsed_ms = int((time.perf_counter() - started) * 1000)
            content_type = response.headers.get("Content-Type", "")
            shape = "bytes"
            rows = ""
            if "json" in content_type:
                payload = json.loads(body.decode("utf-8"))
                shape = type(payload).__name__
                rows = str(len(payload)) if isinstance(payload, list) else ""
            return {
                "status": str(response.status),
                "content_type": content_type,
                "shape": shape,
                "rows": rows,
                "elapsed_ms": str(elapsed_ms),
                "result": "ok",
            }
    except urllib.error.HTTPError as exc:
        elapsed_ms = int((time.perf_counter() - started) * 1000)
        return {
            "status": str(exc.code),
            "content_type": exc.headers.get("Content-Type", ""),
            "shape": "",
            "rows": "",
            "elapsed_ms": str(elapsed_ms),
            "result": "permission/auth/error" if exc.code in {401, 403} else "error",
        }


def write_report(path: Path, base_url: str, rows: list[dict[str, str]]) -> None:
    lines = [
        "# TOPdesk API Smoke Test",
        "",
        f"Target: `{base_url}`",
        "",
        "Credentials are not stored in this report.",
        "",
        "| Endpoint | Status | Shape | Rows | Latency ms | Result |",
        "| --- | ---: | --- | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['path']}` | {row['status']} | {row['shape']} | {row['rows']} | {row['elapsed_ms']} | {row['result']} |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    base_url = os.environ.get("TOPDESK_BASE_URL", "").strip()
    username = os.environ.get("TOPDESK_USERNAME", "").strip()
    app_password = os.environ.get("TOPDESK_APP_PASSWORD", "")
    if not base_url or not username or not app_password:
        raise SystemExit("Set TOPDESK_BASE_URL, TOPDESK_USERNAME, and TOPDESK_APP_PASSWORD")

    endpoints = dict(DEFAULT_ENDPOINTS)
    endpoints.update(dict(args.endpoint))
    rows: list[dict[str, str]] = []
    for name, path in endpoints.items():
        result = request_endpoint(base_url, path, username, app_password, args.page_size)
        rows.append({"name": name, "path": path, **{key: str(value) for key, value in result.items()}})
    write_report(args.out, base_url, rows)
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

