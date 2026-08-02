#!/usr/bin/env python3
"""Validate, observe, and execute repository-resident Governance tasks."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import subprocess
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "automation/governance_task_registry.json"
DEFAULT_RECEIPT = ROOT / "evidence/task-status/latest.json"
VALID_MODES = {"repository_command", "evidence_watch"}
VALID_STATES = {"ready", "blocked", "running", "completed", "invalid", "failed"}


def load_registry() -> dict[str, Any]:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def validate_task(task: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = [
        "id", "title", "organization", "repository", "path", "mode",
        "prerequisites", "completion_condition", "evidence_path", "status",
    ]
    for field in required:
        if field not in task or task[field] in (None, ""):
            errors.append(f"{task.get('id', '<unknown>')}: missing {field}")
    if task.get("mode") not in VALID_MODES:
        errors.append(f"{task.get('id', '<unknown>')}: unsupported mode")
    if task.get("status") not in VALID_STATES:
        errors.append(f"{task.get('id', '<unknown>')}: unsupported status")
    if task.get("mode") == "repository_command" and not task.get("command"):
        errors.append(f"{task.get('id', '<unknown>')}: repository_command missing command")
    destination = ROOT / str(task.get("path", ""))
    if task.get("path") and not destination.exists():
        errors.append(f"{task.get('id', '<unknown>')}: destination does not exist: {task['path']}")
    condition = task.get("completion_condition", {})
    if not isinstance(condition, dict) or not condition.get("type"):
        errors.append(f"{task.get('id', '<unknown>')}: missing observable completion condition")
    return errors


def condition_met(task: dict[str, Any], command_result: dict[str, Any] | None = None) -> bool:
    condition = task["completion_condition"]
    if condition["type"] == "command_exit":
        return command_result is not None and command_result.get("returncode") == condition.get("expected", 0)
    if condition["type"] == "file_exists":
        return (ROOT / condition["path"]).exists()
    return False


def execute_command(task: dict[str, Any]) -> dict[str, Any]:
    proc = subprocess.run(
        task["command"],
        cwd=ROOT,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=600,
        check=False,
    )
    return {
        "returncode": proc.returncode,
        "output": proc.stdout[-12000:],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--receipt", default=str(DEFAULT_RECEIPT))
    args = parser.parse_args()

    registry = load_registry()
    tasks = registry.get("tasks", [])
    ids = {task.get("id") for task in tasks}
    validation_errors: list[str] = []
    for task in tasks:
        validation_errors.extend(validate_task(task))
        for prerequisite in task.get("prerequisites", []):
            if prerequisite not in ids:
                validation_errors.append(f"{task.get('id')}: unknown prerequisite {prerequisite}")

    receipt: dict[str, Any] = {
        "registry_version": registry.get("registry_version"),
        "observed_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "repository": registry.get("owner"),
        "validation_status": "fail" if validation_errors else "pass",
        "validation_errors": validation_errors,
        "tasks": [],
    }

    completed: set[str] = set()
    for task in tasks:
        result: dict[str, Any] = {
            "id": task.get("id"),
            "destination": f"{task.get('organization')}/{task.get('repository')}:{task.get('path')}",
            "mode": task.get("mode"),
            "state": "invalid" if any(err.startswith(str(task.get('id'))) for err in validation_errors) else task.get("status"),
            "completion_evidence": task.get("evidence_path"),
        }
        if result["state"] == "invalid" or args.validate_only:
            receipt["tasks"].append(result)
            continue
        if not set(task.get("prerequisites", [])).issubset(completed):
            result["state"] = "blocked"
        elif task["mode"] == "repository_command":
            result["state"] = "running"
            command_result = execute_command(task)
            result["command_result"] = command_result
            result["state"] = "completed" if condition_met(task, command_result) else "failed"
        elif task["mode"] == "evidence_watch":
            result["state"] = "completed" if condition_met(task) else "blocked"
        if result["state"] == "completed":
            completed.add(task["id"])
        receipt["tasks"].append(result)

    receipt_path = pathlib.Path(args.receipt)
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))

    failed_states = {"invalid", "failed"}
    if validation_errors or any(item["state"] in failed_states for item in receipt["tasks"]):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
