#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def frame(payload: dict) -> bytes:
    body = json.dumps(payload).encode("utf-8")
    return f"Content-Length: {len(body)}\r\n\r\n".encode("ascii") + body


def main() -> int:
    server = Path(__file__).with_name("topdesk_mcp_server.py")
    request = frame({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}) + frame(
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
    )
    proc = subprocess.run(
        [sys.executable, str(server)],
        input=request,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=10,
        check=False,
    )
    output = proc.stdout.decode("utf-8", errors="replace")
    if proc.returncode != 0:
        print(proc.stderr.decode("utf-8", errors="replace"))
        return proc.returncode
    if "topdesk_build_odata_url" not in output:
        print(output)
        return 1
    print("MCP server smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

