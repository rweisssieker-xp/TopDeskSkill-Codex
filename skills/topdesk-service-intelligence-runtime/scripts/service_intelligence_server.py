#!/usr/bin/env python3
"""Serve local Service Intelligence runtime status from SQLite and monitoring JSON."""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Sequence
from urllib.parse import urlparse


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Serve TOPdesk Service Intelligence local runtime API")
    parser.add_argument("--state-db", type=Path, required=True)
    parser.add_argument("--monitoring-json", type=Path)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--token-env", default="SERVICE_INTELLIGENCE_ADMIN_TOKEN")
    return parser.parse_args(argv)


def rows(conn: sqlite3.Connection, sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    conn.row_factory = sqlite3.Row
    return [dict(row) for row in conn.execute(sql, params).fetchall()]


def read_monitoring(path: Path | None) -> dict[str, Any]:
    if not path or not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def html_page(monitoring: dict[str, Any], recent_runs: list[dict[str, Any]]) -> str:
    cards = "\n".join(
        f"<tr><td>{run.get('run_id')}</td><td>{run.get('generated_at')}</td><td>{run.get('status')}</td><td>{run.get('tenant')}</td><td>{run.get('environment')}</td></tr>"
        for run in recent_runs
    )
    status = monitoring.get("status", "unknown")
    return f"""<!doctype html>
<html lang="en">
<meta charset="utf-8">
<title>TOPdesk Service Intelligence</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 32px; color: #17202a; }}
main {{ max-width: 1040px; margin: 0 auto; }}
.badge {{ display: inline-block; padding: 4px 8px; border-radius: 6px; background: #eef2f7; }}
table {{ border-collapse: collapse; width: 100%; }}
td, th {{ border-bottom: 1px solid #d8dee8; padding: 8px; text-align: left; }}
</style>
<main>
<h1>TOPdesk Service Intelligence</h1>
<p>Status: <span class="badge">{status}</span></p>
<p>Connector: {monitoring.get('connector_status', 'unknown')} | Blockers: {monitoring.get('blocker_count', 'unknown')}</p>
<h2>Recent Runs</h2>
<table><thead><tr><th>ID</th><th>Generated</th><th>Status</th><th>Tenant</th><th>Environment</th></tr></thead><tbody>{cards}</tbody></table>
</main>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    state_db: Path
    monitoring_json: Path | None
    token: str

    def authorized(self) -> bool:
        if not self.token:
            return True
        return self.headers.get("Authorization", "") == f"Bearer {self.token}"

    def send_payload(self, status: int, payload: Any, content_type: str = "application/json") -> None:
        body = payload if isinstance(payload, bytes) else json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if not self.authorized():
            self.send_payload(401, {"error": "unauthorized"})
            return
        parsed = urlparse(self.path)
        monitoring = read_monitoring(self.monitoring_json)
        with sqlite3.connect(self.state_db) as conn:
            if parsed.path == "/health":
                self.send_payload(200, {"status": monitoring.get("status", "unknown"), "state_db_exists": self.state_db.exists(), "monitoring": monitoring})
            elif parsed.path == "/api/runs":
                self.send_payload(200, rows(conn, "select run_id, generated_at, tenant, environment, dry_run, status, out_dir, blockers from runtime_runs order by run_id desc limit 50"))
            elif parsed.path == "/api/modules":
                self.send_payload(200, rows(conn, "select run_id, module, enabled, status, exit_code, out_dir, stderr from module_runs order by run_id desc, module"))
            elif parsed.path in {"/", "/dashboard"}:
                recent = rows(conn, "select run_id, generated_at, tenant, environment, status from runtime_runs order by run_id desc limit 20")
                self.send_payload(200, html_page(monitoring, recent).encode("utf-8"), "text/html; charset=utf-8")
            else:
                self.send_payload(404, {"error": "not found"})


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    Handler.state_db = args.state_db
    Handler.monitoring_json = args.monitoring_json
    Handler.token = os.environ.get(args.token_env, "")
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Serving TOPdesk Service Intelligence on http://{args.host}:{args.port}")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

