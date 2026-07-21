#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

OUTPUT = Path("reports/github-complete-history-export.json")
MAX_REPOSITORY_KB = 250_000


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def run(args: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(args, cwd=cwd, env=env, check=True, capture_output=True, text=True, timeout=300)
    return result.stdout


def gh_json(endpoint: str, token: str) -> Any:
    env = dict(os.environ)
    env["GH_TOKEN"] = token
    raw = run(["gh", "api", endpoint, "--paginate"], env=env)
    chunks = [json.loads(line) for line in raw.splitlines() if line.strip()]
    if len(chunks) == 1:
        return chunks[0]
    merged: list[Any] = []
    for chunk in chunks:
        if isinstance(chunk, list):
            merged.extend(chunk)
        elif isinstance(chunk, dict) and isinstance(chunk.get("repositories"), list):
            merged.extend(chunk["repositories"])
    return merged


def safe_records(items: Any, fields: tuple[str, ...]) -> list[dict[str, Any]]:
    if not isinstance(items, list):
        return []
    out = []
    for item in items:
        if not isinstance(item, dict):
            continue
        record = {field: item.get(field) for field in fields}
        record["record_hash"] = digest(record)
        out.append(record)
    return out


def blocked(repo: dict[str, Any], reason: str) -> dict[str, Any]:
    record = {
        "full_name": repo.get("full_name"),
        "state": "BLOCKED_COMPLETE_HISTORY_EXPORT",
        "blockers": [reason],
        "manual_action_required": False,
        "source_material_retained": False,
        "bundle_retained": False,
        "secret_material_included": False,
        "production_mutation_allowed": False,
        "execution_authority": False,
        "traffic_cutover_authority": False,
        "cancellation_authority": False,
        "provider_retirement_authority": False,
        "continuity_receipt_minted": False,
    }
    record["record_hash"] = digest(record)
    return record


def export_repository(repo: dict[str, Any], token: str) -> dict[str, Any]:
    name = str(repo.get("full_name") or "")
    if not name:
        return blocked(repo, "repository_identity_missing")
    if repo.get("disabled"):
        return blocked(repo, "repository_disabled")
    if int(repo.get("size") or 0) > MAX_REPOSITORY_KB:
        return blocked(repo, "repository_exceeds_runner_safety_limit")

    root = Path(tempfile.mkdtemp(prefix="stegverse-history-"))
    mirror = root / "repo.git"
    bundle = root / "repo.bundle"
    verify = root / "verify.git"
    env = dict(os.environ)
    env["GIT_TERMINAL_PROMPT"] = "0"
    url = f"https://x-access-token:{token}@github.com/{name}.git"
    try:
        run(["git", "clone", "--mirror", url, str(mirror)], env=env)
        refs_raw = run(["git", "for-each-ref", "--format=%(refname) %(objectname)"], cwd=mirror)
        refs = sorted(line.strip() for line in refs_raw.splitlines() if line.strip())
        object_count = int(run(["git", "rev-list", "--objects", "--all", "--count"], cwd=mirror).strip() or "0")
        commit_count = int(run(["git", "rev-list", "--all", "--count"], cwd=mirror).strip() or "0")
        run(["git", "bundle", "create", str(bundle), "--all"], cwd=mirror)
        bundle_bytes = bundle.read_bytes()
        bundle_hash = hashlib.sha256(bundle_bytes).hexdigest()
        run(["git", "init", "--bare", str(verify)])
        run(["git", "bundle", "verify", str(bundle)], cwd=verify)
        heads = run(["git", "bundle", "list-heads", str(bundle)], cwd=verify)
        bundle_refs = sorted(line.strip() for line in heads.splitlines() if line.strip())

        owner, repository = name.split("/", 1)
        releases = safe_records(
            gh_json(f"repos/{owner}/{repository}/releases?per_page=100", token),
            ("id", "tag_name", "target_commitish", "draft", "prerelease", "created_at", "published_at"),
        )
        tags = safe_records(
            gh_json(f"repos/{owner}/{repository}/tags?per_page=100", token),
            ("name", "zipball_url", "tarball_url"),
        )
        issues = safe_records(
            gh_json(f"repos/{owner}/{repository}/issues?state=all&per_page=100", token),
            ("id", "number", "state", "locked", "created_at", "updated_at", "closed_at"),
        )
        pulls = safe_records(
            gh_json(f"repos/{owner}/{repository}/pulls?state=all&per_page=100", token),
            ("id", "number", "state", "draft", "created_at", "updated_at", "closed_at", "merged_at"),
        )
        adjacent = {
            "release_count": len(releases),
            "tag_count": len(tags),
            "issue_count": len(issues),
            "pull_request_count": len(pulls),
            "releases_hash": digest(releases),
            "tags_hash": digest(tags),
            "issues_hash": digest(issues),
            "pull_requests_hash": digest(pulls),
        }
        record = {
            "full_name": name,
            "state": "PASS_COMPLETE_HISTORY_EXPORT",
            "repository_id": repo.get("id"),
            "private": repo.get("private"),
            "default_branch": repo.get("default_branch"),
            "ref_count": len(refs),
            "refs_hash": digest(refs),
            "bundle_ref_count": len(bundle_refs),
            "bundle_refs_hash": digest(bundle_refs),
            "bundle_hash": bundle_hash,
            "bundle_size_bytes": len(bundle_bytes),
            "object_count": object_count,
            "commit_count": commit_count,
            "adjacent_state": adjacent,
            "authenticated_read_only": True,
            "source_material_retained": False,
            "bundle_retained": False,
            "secret_material_included": False,
            "manual_action_required": False,
            "production_mutation_allowed": False,
            "execution_authority": False,
            "traffic_cutover_authority": False,
            "cancellation_authority": False,
            "provider_retirement_authority": False,
            "continuity_receipt_minted": False,
        }
        record["record_hash"] = digest(record)
        return record
    except Exception as exc:
        return blocked(repo, f"complete_history_export_failed:{type(exc).__name__}")
    finally:
        shutil.rmtree(root, ignore_errors=True)


def main() -> int:
    token = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    records: list[dict[str, Any]] = []
    blockers: list[str] = []
    if not token:
        blockers.append("github_installation_token_unavailable")
    else:
        try:
            payload = gh_json("installation/repositories?per_page=100", token)
            repositories = payload.get("repositories", []) if isinstance(payload, dict) else payload
            for repo in repositories if isinstance(repositories, list) else []:
                if isinstance(repo, dict):
                    records.append(export_repository(repo, token))
        except Exception as exc:
            blockers.append(f"repository_inventory_failed:{type(exc).__name__}")

    records.sort(key=lambda item: str(item.get("full_name")))
    report = {
        "schema_version": "1.0.0",
        "report_id": "github-complete-history-export",
        "provider_id": "github",
        "state": "COMPLETE_WITH_BLOCKERS" if blockers or any(r["state"].startswith("BLOCKED") for r in records) else "COMPLETE",
        "records": records,
        "repository_count": len(records),
        "passed_repository_count": sum(1 for r in records if r["state"] == "PASS_COMPLETE_HISTORY_EXPORT"),
        "blocked_repository_count": sum(1 for r in records if r["state"] != "PASS_COMPLETE_HISTORY_EXPORT"),
        "blockers": blockers,
        "maximum_repository_kb": MAX_REPOSITORY_KB,
        "authenticated_read_only": bool(token),
        "source_material_retained": False,
        "bundle_retained": False,
        "secret_material_included": False,
        "manual_action_required": False,
        "production_mutation_allowed": False,
        "execution_authority": False,
        "traffic_cutover_authority": False,
        "cancellation_authority": False,
        "provider_retirement_authority": False,
        "continuity_receipt_minted": False,
    }
    report["report_hash"] = digest(report)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
