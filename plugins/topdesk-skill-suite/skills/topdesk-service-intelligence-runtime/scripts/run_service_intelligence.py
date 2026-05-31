#!/usr/bin/env python3
"""Run a local TOPdesk Service Intelligence operating cycle."""

from __future__ import annotations

import argparse
import csv
import html
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[2]


MODULES = {
    "tenant_drift": {
        "script": ROOT / "topdesk-tenant-drift" / "scripts" / "compare_tenant_drift.py",
        "required": ("baseline_catalog", "current_catalog"),
        "args": lambda inputs, out: ["--baseline", inputs["baseline_catalog"], "--current", inputs["current_catalog"], "--out-dir", str(out)],
    },
    "process_debt": {
        "script": ROOT / "topdesk-process-debt" / "scripts" / "analyze_process_debt.py",
        "required": (),
        "optional": (("incidents", "--incidents"), ("assignments", "--assignments"), ("statuses", "--statuses")),
        "args": lambda inputs, out: optional_args(inputs, (("incidents", "--incidents"), ("assignments", "--assignments"), ("statuses", "--statuses"))) + ["--out-dir", str(out)],
    },
    "ai_adoption_ledger": {
        "script": ROOT / "topdesk-ai-adoption-ledger" / "scripts" / "build_ai_adoption_ledger.py",
        "required": ("ai_usage",),
        "args": lambda inputs, out: ["--input", inputs["ai_usage"], "--out-dir", str(out)],
    },
    "automation_sandbox": {
        "script": ROOT / "topdesk-automation-sandbox" / "scripts" / "review_automation_risk.py",
        "required": ("automation_scenarios",),
        "args": lambda inputs, out: ["--input", inputs["automation_scenarios"], "--out-dir", str(out)],
    },
    "readiness_scoring": {
        "script": ROOT / "topdesk-readiness-scoring" / "scripts" / "score_readiness.py",
        "required": ("readiness_checklist",),
        "args": lambda inputs, out: ["--input", inputs["readiness_checklist"], "--out-dir", str(out)],
    },
    "digital_twin_light": {
        "script": ROOT / "topdesk-digital-twin-light" / "scripts" / "run_digital_twin_light.py",
        "required": ("digital_twin_baseline", "digital_twin_scenarios"),
        "args": lambda inputs, out: ["--baseline", inputs["digital_twin_baseline"], "--scenarios", inputs["digital_twin_scenarios"], "--out-dir", str(out)],
    },
}


def optional_args(inputs: dict[str, str], pairs: Sequence[tuple[str, str]]) -> list[str]:
    args: list[str] = []
    for key, flag in pairs:
        if inputs.get(key):
            args.extend([flag, inputs[key]])
    return args


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the TOPdesk Service Intelligence Runtime")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def load_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_inputs(config_path: Path, config: dict[str, Any]) -> dict[str, str]:
    base = config_path.parent
    resolved: dict[str, str] = {}
    for key, raw in (config.get("inputs") or {}).items():
        if not raw:
            continue
        path = Path(str(raw))
        resolved[key] = str(path if path.is_absolute() else (base / path).resolve())
    return resolved


def connector_gate(config: dict[str, Any]) -> dict[str, Any]:
    connector = config.get("connector") or {}
    enabled = bool(connector.get("enabled"))
    names = [
        connector.get("base_url_env") or "TOPDESK_BASE_URL",
        connector.get("username_env") or "TOPDESK_USERNAME",
        connector.get("password_env") or "TOPDESK_APP_PASSWORD",
    ]
    missing = [name for name in names if not os.environ.get(str(name))]
    return {
        "enabled": enabled,
        "mode": connector.get("mode", "exports"),
        "missing_env": missing if enabled else [],
        "status": "green" if not enabled else ("green" if not missing else "red"),
    }


def build_plan(config_path: Path, config: dict[str, Any], out_dir: Path) -> dict[str, Any]:
    inputs = resolve_inputs(config_path, config)
    enabled_modules = config.get("modules") or {}
    runs: list[dict[str, Any]] = []
    blockers: list[str] = []
    for name, spec in MODULES.items():
        if not enabled_modules.get(name, False):
            runs.append({"module": name, "enabled": False, "status": "skipped"})
            continue
        missing = [key for key in spec.get("required", ()) if not inputs.get(key) or not Path(inputs[key]).exists()]
        script = Path(spec["script"])
        if not script.exists():
            missing.append(f"script:{script}")
        module_out = out_dir / name.replace("_", "-")
        command = [sys.executable, str(script)] + spec["args"](inputs, module_out)
        status = "blocked" if missing else "ready"
        if missing:
            blockers.append(f"{name}: missing {', '.join(missing)}")
        runs.append({"module": name, "enabled": True, "status": status, "missing": missing, "out_dir": str(module_out), "command": command})
    if enabled_modules.get("executive_narrative", False):
        findings_path = out_dir / "process-debt" / "process-debt-findings.csv"
        script = ROOT / "topdesk-executive-narrative" / "scripts" / "build_executive_narrative.py"
        missing = [] if findings_path.exists() else ["process-debt findings generated during same run"]
        runs.append(
            {
                "module": "executive_narrative",
                "enabled": True,
                "status": "deferred" if missing else "ready",
                "missing": missing,
                "out_dir": str(out_dir / "executive-narrative"),
                "command": [sys.executable, str(script), "--findings", str(findings_path), "--out-dir", str(out_dir / "executive-narrative")],
            }
        )
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tenant": config.get("tenant") or {},
        "connector": connector_gate(config),
        "governance": config.get("governance") or {},
        "runs": runs,
        "blockers": blockers,
    }


def run_modules(plan: dict[str, Any]) -> None:
    for item in plan["runs"]:
        if item["status"] not in {"ready", "deferred"}:
            continue
        if item["module"] == "executive_narrative" and item["status"] == "deferred":
            continue
        result = subprocess.run(item["command"], cwd=str(ROOT), text=True, capture_output=True)
        item["exit_code"] = result.returncode
        item["stdout"] = result.stdout.strip()
        item["stderr"] = result.stderr.strip()
        item["status"] = "passed" if result.returncode == 0 else "failed"
    for item in plan["runs"]:
        if item["module"] == "executive_narrative" and item["enabled"]:
            findings = Path(item["command"][item["command"].index("--findings") + 1])
            if findings.exists():
                result = subprocess.run(item["command"], cwd=str(ROOT), text=True, capture_output=True)
                item["exit_code"] = result.returncode
                item["stdout"] = result.stdout.strip()
                item["stderr"] = result.stderr.strip()
                item["status"] = "passed" if result.returncode == 0 else "failed"
            else:
                item["status"] = "blocked"
                item["missing"] = ["process-debt findings"]


def write_gates(out_dir: Path, plan: dict[str, Any]) -> None:
    rows = [
        {"gate": "connector", "status": plan["connector"]["status"], "evidence": ";".join(plan["connector"].get("missing_env", [])) or "configured or not enabled"},
        {"gate": "input evidence", "status": "red" if plan["blockers"] else "green", "evidence": " | ".join(plan["blockers"]) or "required inputs available"},
        {"gate": "governance owner", "status": "green" if plan["governance"].get("owner") else "amber", "evidence": plan["governance"].get("owner", "owner missing")},
        {"gate": "retention", "status": "green" if plan["governance"].get("retention_days") else "amber", "evidence": str(plan["governance"].get("retention_days", "retention missing"))},
        {"gate": "production approval", "status": plan["governance"].get("production_gate", "amber"), "evidence": plan["governance"].get("approval_reference", "approval reference missing")},
    ]
    with (out_dir / "operational-gates.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["gate", "status", "evidence"])
        writer.writeheader()
        writer.writerows(rows)


def write_readouts(out_dir: Path, plan: dict[str, Any], dry_run: bool) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "runtime-plan.json").write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")
    with (out_dir / "runtime-history.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"generated_at": plan["generated_at"], "dry_run": dry_run, "runs": plan["runs"], "blockers": plan["blockers"]}, ensure_ascii=False) + "\n")
    lines = [
        "# TOPdesk Service Intelligence Runtime Readout",
        "",
        f"- Generated at: {plan['generated_at']}",
        f"- Tenant: {plan.get('tenant', {}).get('name', 'unknown')}",
        f"- Environment: {plan.get('tenant', {}).get('environment', 'unknown')}",
        f"- Mode: {'dry run' if dry_run else 'execution'}",
        f"- Connector gate: {plan['connector']['status']}",
        f"- Blockers: {len(plan['blockers'])}",
        "",
        "## Modules",
        "",
    ]
    for item in plan["runs"]:
        lines.append(f"- **{item['module']}**: {item['status']}")
    if plan["blockers"]:
        lines.extend(["", "## Blockers", ""])
        lines.extend(f"- {blocker}" for blocker in plan["blockers"])
    (out_dir / "runtime-readout.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    cards = "\n".join(f"<li><strong>{html.escape(item['module'])}</strong>: {html.escape(item['status'])}</li>" for item in plan["runs"])
    blockers = "\n".join(f"<li>{html.escape(blocker)}</li>" for blocker in plan["blockers"]) or "<li>No blockers for enabled modules.</li>"
    dashboard = f"""<!doctype html>
<html lang="en">
<meta charset="utf-8">
<title>TOPdesk Service Intelligence Runtime</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 32px; color: #17202a; }}
main {{ max-width: 960px; margin: 0 auto; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; }}
.card {{ border: 1px solid #d5dbe3; border-radius: 8px; padding: 14px; }}
h1, h2 {{ margin-bottom: 8px; }}
code {{ background: #eef2f7; padding: 2px 4px; border-radius: 4px; }}
</style>
<main>
<h1>TOPdesk Service Intelligence Runtime</h1>
<div class="grid">
<section class="card"><h2>Tenant</h2><p>{html.escape(str(plan.get('tenant', {}).get('name', 'unknown')))}</p></section>
<section class="card"><h2>Environment</h2><p>{html.escape(str(plan.get('tenant', {}).get('environment', 'unknown')))}</p></section>
<section class="card"><h2>Connector</h2><p>{html.escape(plan['connector']['status'])}</p></section>
<section class="card"><h2>Run</h2><p>{'Dry run' if dry_run else 'Execution'}</p></section>
</div>
<h2>Modules</h2>
<ul>{cards}</ul>
<h2>Blockers</h2>
<ul>{blockers}</ul>
<p>Evidence files: <code>runtime-plan.json</code>, <code>operational-gates.csv</code>, <code>runtime-history.jsonl</code>.</p>
</main>
</html>
"""
    (out_dir / "runtime-dashboard.html").write_text(dashboard, encoding="utf-8")
    write_gates(out_dir, plan)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    config = load_config(args.config)
    plan = build_plan(args.config, config, args.out_dir)
    if not args.dry_run:
        run_modules(plan)
    write_readouts(args.out_dir, plan, args.dry_run)
    print(f"Wrote runtime readout to {args.out_dir}")
    return 0 if not any(item.get("status") == "failed" for item in plan["runs"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
