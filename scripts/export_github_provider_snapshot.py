#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any

OUTPUT = Path("reports/github-provider-export-snapshot.json")


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def gh_json(args: list[str]) -> Any:
    env = dict(os.environ)
    token = env.get("GH_TOKEN") or env.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("github_token_unavailable")
    env["GH_TOKEN"] = token
    result = subprocess.run(
        ["gh", "api", *args],
        check=True,
        capture_output=True,
        text=True,
        env=env,
        timeout=120,
    )
    return json.loads(result.stdout)


def main() -> int:
    try:
        payload = gh_json(["installation/repositories", "--paginate"])
        repositories = payload.get("repositories", []) if isinstance(payload, dict) else []
        records: list[dict[str, Any]] = []
        for repo in repositories:
            if not isinstance(repo, dict):
                continue
            record = {
                "repository_id": repo.get("id"),
                "full_name": repo.get("full_name"),
                "private": repo.get("private"),
                "archived": repo.get("archived"),
                "disabled": repo.get("disabled"),
                "visibility": repo.get("visibility"),
                "default_branch": repo.get("default_branch"),
                "fork": repo.get("fork"),
                "size_kb": repo.get("size"),
                "open_issues_count": repo.get("open_issues_count"),
                "pushed_at": repo.get("pushed_at"),
                "updated_at": repo.get("updated_at"),
            }
            record["record_hash"] = digest(record)
            records.append(record)
        records.sort(key=lambda item: str(item.get("full_name")))
        state = "AUTHENTICATED_READ_ONLY_EXPORT_COMPLETE"
        blockers: list[str] = []
    except Exception as exc:
        records = []
        state = "BLOCKED_AUTOMATED_EXPORT_UNAVAILABLE"
        blockers = [f"github_export_failed:{type(exc).__name__}:{exc}"]

    report = {
        "schema_version": "1.0.0",
        "provider_id": "github",
        "state": state,
        "export_scope": "installation_repository_metadata",
        "repository_count": len(records),
        "records": records,
        "blockers": blockers,
        "authenticated_read_only": state == "AUTHENTICATED_READ_ONLY_EXPORT_COMPLETE",
        "secret_material_included": False,
        "repository_contents_included": False,
        "production_mutation_allowed": False,
        "execution_authority": False,
        "traffic_cutover_authority": False,
        "cancellation_authority": False,
        "provider_retirement_authority": False,
        "continuity_receipt_minted": False,
        "manual_action_required": False,
    }
    report["export_hash"] = digest(report)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
