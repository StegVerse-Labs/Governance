#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any

QUEUE = Path("reports/provider-inventory-queue.json")
OUTPUT = Path("reports/provider-inventory-results.json")


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def github_inventory() -> tuple[str, list[dict[str, Any]], list[str]]:
    token = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    if not token:
        return "BLOCKED_CREDENTIAL_UNAVAILABLE", [], ["github_token_unavailable"]
    env = dict(os.environ)
    env["GH_TOKEN"] = token
    try:
        result = subprocess.run(
            ["gh", "api", "installation/repositories", "--paginate"],
            check=True,
            capture_output=True,
            text=True,
            env=env,
            timeout=90,
        )
        data = json.loads(result.stdout)
        repos = data.get("repositories", []) if isinstance(data, dict) else []
        assets = [
            {
                "full_name": repo.get("full_name"),
                "private": repo.get("private"),
                "archived": repo.get("archived"),
                "default_branch": repo.get("default_branch"),
                "visibility": repo.get("visibility"),
            }
            for repo in repos
            if isinstance(repo, dict)
        ]
        assets.sort(key=lambda item: str(item.get("full_name")))
        return "COLLECTED", assets, []
    except Exception as exc:
        return "BLOCKED_PROVIDER_API", [], [f"github_collection_failed:{type(exc).__name__}"]


def blocked(provider_id: str, reason: str) -> tuple[str, list[dict[str, Any]], list[str]]:
    return "BLOCKED_PROVIDER_API", [], [reason]


def collect(provider_id: str) -> tuple[str, list[dict[str, Any]], list[str]]:
    if provider_id == "github":
        return github_inventory()
    if provider_id == "render":
        return blocked(provider_id, "render_api_credential_or_collector_unavailable")
    if provider_id == "godaddy":
        return blocked(provider_id, "godaddy_api_credential_or_collector_unavailable")
    if provider_id == "pypi":
        return blocked(provider_id, "pypi_account_scope_not_identified")
    if provider_id in {"cloud-space", "unknown-recurring-services"}:
        return "BLOCKED_PROVIDER_IDENTIFICATION", [], ["provider_identity_unresolved"]
    return blocked(provider_id, "collector_not_implemented")


def main() -> int:
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    results = []
    for task in queue.get("tasks", []):
        provider_id = task["dependency_id"]
        state, assets, blockers = collect(provider_id)
        record = {
            "provider_id": provider_id,
            "service_name": task.get("service_name"),
            "queue_state": task.get("inventory_state"),
            "collector_state": state,
            "asset_count": len(assets),
            "assets": assets,
            "blockers": sorted(blockers),
            "source_commit": os.getenv("GITHUB_SHA", "UNBOUND_LOCAL_RUN"),
            "collection_run_id": os.getenv("GITHUB_RUN_ID", "UNBOUND_LOCAL_RUN"),
            "secret_material_included": False,
            "manual_action_required": False,
            "cancellation_authority": False,
            "provider_retirement_authority": False,
            "traffic_cutover_authority": False,
            "master_records_custody_state": "PENDING_AUTOMATED_INGESTION",
        }
        record["payload_hash"] = hashlib.sha256(canonical(record).encode("utf-8")).hexdigest()
        results.append(record)
    results.sort(key=lambda item: item["provider_id"])
    report = {
        "schema_version": "1.0.0",
        "queue_hash": queue.get("queue_hash"),
        "status": "COLLECTED_WITH_BLOCKERS" if any(item["collector_state"] != "COLLECTED" for item in results) else "COLLECTED",
        "results": results,
        "manual_action_required": False,
        "cancellation_authority": False,
        "provider_retirement_authority": False,
    }
    report["report_hash"] = hashlib.sha256(canonical(report).encode("utf-8")).hexdigest()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
