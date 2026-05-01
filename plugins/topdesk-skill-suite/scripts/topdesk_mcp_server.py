#!/usr/bin/env python3
"""Minimal MCP server for TOPdesk Skill Suite local utilities.

The server is dependency-free and exposes safe helper tools. Live TOPdesk access is
GET-only and requires TOPDESK_BASE_URL plus TOPDESK_API_TOKEN.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
from typing import Any


SERVER_NAME = "topdesk-skill-suite"
SERVER_VERSION = "0.1.0"


def read_message() -> dict[str, Any] | None:
    headers: dict[str, str] = {}
    while True:
        line = sys.stdin.buffer.readline()
        if not line:
            return None
        if line in (b"\r\n", b"\n"):
            break
        key, _, value = line.decode("ascii").partition(":")
        headers[key.lower()] = value.strip()
    length = int(headers.get("content-length", "0"))
    if length <= 0:
        return None
    return json.loads(sys.stdin.buffer.read(length).decode("utf-8"))


def write_message(payload: dict[str, Any]) -> None:
    body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    sys.stdout.buffer.write(f"Content-Length: {len(body)}\r\n\r\n".encode("ascii"))
    sys.stdout.buffer.write(body)
    sys.stdout.buffer.flush()


def result(request_id: Any, payload: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": payload}


def error(request_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def text_content(text: str) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": text}]}


def tool_list() -> dict[str, Any]:
    return {
        "tools": [
            {
                "name": "topdesk_config_status",
                "description": "Show whether TOPdesk MCP environment variables are configured.",
                "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
            },
            {
                "name": "topdesk_build_odata_url",
                "description": "Build a TOPdesk OData URL from entity, select, filter, orderby, top, and skip.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "entity": {"type": "string"},
                        "select": {"type": "array", "items": {"type": "string"}},
                        "filter": {"type": "string"},
                        "orderby": {"type": "string"},
                        "top": {"type": "integer"},
                        "skip": {"type": "integer"},
                    },
                    "required": ["entity"],
                    "additionalProperties": False,
                },
            },
            {
                "name": "topdesk_get",
                "description": "Perform a GET request against TOPdesk relative path. Requires TOPDESK_BASE_URL and TOPDESK_API_TOKEN.",
                "inputSchema": {
                    "type": "object",
                    "properties": {"path": {"type": "string"}},
                    "required": ["path"],
                    "additionalProperties": False,
                },
            },
        ]
    }


def call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if name == "topdesk_config_status":
        status = {
            "base_url_configured": bool(os.environ.get("TOPDESK_BASE_URL")),
            "api_token_configured": bool(os.environ.get("TOPDESK_API_TOKEN")),
        }
        return text_content(json.dumps(status, indent=2))
    if name == "topdesk_build_odata_url":
        base = os.environ.get("TOPDESK_BASE_URL", "https://example.topdesk.net").rstrip("/")
        entity = str(arguments["entity"]).strip("/")
        query: dict[str, str] = {}
        if arguments.get("select"):
            query["$select"] = ",".join(arguments["select"])
        if arguments.get("filter"):
            query["$filter"] = str(arguments["filter"])
        if arguments.get("orderby"):
            query["$orderby"] = str(arguments["orderby"])
        if arguments.get("top") is not None:
            query["$top"] = str(arguments["top"])
        if arguments.get("skip") is not None:
            query["$skip"] = str(arguments["skip"])
        qs = urllib.parse.urlencode(query, safe="$, '():/")
        url = f"{base}/tas/api/odata/{entity}"
        if qs:
            url = f"{url}?{qs}"
        return text_content(url)
    if name == "topdesk_get":
        base = os.environ.get("TOPDESK_BASE_URL", "").rstrip("/")
        token = os.environ.get("TOPDESK_API_TOKEN", "")
        if not base or not token:
            raise ValueError("TOPDESK_BASE_URL and TOPDESK_API_TOKEN are required for topdesk_get.")
        path = str(arguments["path"]).lstrip("/")
        request = urllib.request.Request(
            f"{base}/{path}",
            headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
            method="GET",
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = response.read().decode("utf-8")
        return text_content(payload)
    raise ValueError(f"Unknown tool: {name}")


def handle(message: dict[str, Any]) -> dict[str, Any] | None:
    method = message.get("method")
    request_id = message.get("id")
    if method == "initialize":
        return result(
            request_id,
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
            },
        )
    if method == "tools/list":
        return result(request_id, tool_list())
    if method == "tools/call":
        params = message.get("params", {})
        try:
            return result(request_id, call_tool(params.get("name", ""), params.get("arguments", {}) or {}))
        except Exception as exc:
            return error(request_id, -32000, str(exc))
    if request_id is None:
        return None
    return error(request_id, -32601, f"Unsupported method: {method}")


def main() -> int:
    while True:
        message = read_message()
        if message is None:
            return 0
        response = handle(message)
        if response is not None:
            write_message(response)


if __name__ == "__main__":
    raise SystemExit(main())

