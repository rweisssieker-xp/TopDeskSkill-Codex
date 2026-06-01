#!/usr/bin/env python3
"""Manage local TOPdesk runtime secrets protected with Windows DPAPI."""

from __future__ import annotations

import argparse
import base64
import ctypes
import json
import os
import sys
from pathlib import Path
from typing import Sequence


SECRET_KEYS = ("TOPDESK_BASE_URL", "TOPDESK_USERNAME", "TOPDESK_APP_PASSWORD")


class DataBlob(ctypes.Structure):
    _fields_ = [("cbData", ctypes.c_uint), ("pbData", ctypes.POINTER(ctypes.c_byte))]


def bytes_from_blob(blob: DataBlob) -> bytes:
    return ctypes.string_at(blob.pbData, blob.cbData)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manage TOPdesk Service Intelligence local secrets")
    sub = parser.add_subparsers(dest="command", required=True)
    create = sub.add_parser("set", help="Write encrypted secrets from environment variables")
    create.add_argument("--store", type=Path, required=True)
    create.add_argument("--allow-missing", action="store_true")
    show = sub.add_parser("show", help="Show configured secret names without values")
    show.add_argument("--store", type=Path, required=True)
    env = sub.add_parser("print-env", help="Print PowerShell environment assignments")
    env.add_argument("--store", type=Path, required=True)
    return parser.parse_args(argv)


def protect(value: str) -> str:
    if os.name != "nt":
        raise RuntimeError("Windows DPAPI secret store requires Windows")
    data = value.encode("utf-8")
    input_buffer = ctypes.create_string_buffer(data)
    input_blob = DataBlob(len(data), ctypes.cast(input_buffer, ctypes.POINTER(ctypes.c_byte)))
    output_blob = DataBlob()
    if not ctypes.windll.crypt32.CryptProtectData(ctypes.byref(input_blob), None, None, None, None, 0, ctypes.byref(output_blob)):
        raise ctypes.WinError()
    try:
        return base64.b64encode(bytes_from_blob(output_blob)).decode("ascii")
    finally:
        ctypes.windll.kernel32.LocalFree(output_blob.pbData)


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


def read_store(path: Path) -> dict[str, str]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def write_store(path: Path, values: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "format": "windows-dpapi-user",
        "secrets": {key: protect(value) for key, value in values.items()},
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def set_secrets(path: Path, allow_missing: bool) -> int:
    values = {key: os.environ.get(key, "") for key in SECRET_KEYS}
    missing = [key for key, value in values.items() if not value]
    if missing and not allow_missing:
        print(f"Missing environment variables: {', '.join(missing)}", file=sys.stderr)
        return 2
    write_store(path, {key: value for key, value in values.items() if value})
    print(f"Wrote encrypted secret store: {path}")
    return 0


def show(path: Path) -> int:
    payload = read_store(path)
    names = sorted((payload.get("secrets") or {}).keys())
    print(json.dumps({"store": str(path), "format": payload.get("format", ""), "secrets": names}, indent=2))
    return 0


def print_env(path: Path) -> int:
    payload = read_store(path)
    secrets = payload.get("secrets") or {}
    for key in SECRET_KEYS:
        if key in secrets:
            value = unprotect(secrets[key]).replace("'", "''")
            print(f"$env:{key} = '{value}'")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.command == "set":
        return set_secrets(args.store, args.allow_missing)
    if args.command == "show":
        return show(args.store)
    if args.command == "print-env":
        return print_env(args.store)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
