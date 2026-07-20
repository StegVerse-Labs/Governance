#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tarfile
import tempfile
from pathlib import Path
from typing import Any

OUTPUT = Path("reports/github-default-branch-reconstruction.json")
MAX_PROVIDER_SIZE_KB = 250_000


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def run(args: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> str:
    completed = subprocess.run(
        args,
        cwd=cwd,
        env=env,
        check=True,
        capture_output=True,
        text=True,
        timeout=300,
    )
    return completed.stdout.strip()


def installation_repositories(env: dict[str, str]) -> list[dict[str, Any]]:
    raw = run(["gh", "api", "installation/repositories", "--paginate"], env=env)
    value = json.loads(raw)
    repositories = value.get("repositories", []) if isinstance(value, dict) else []
    result = []
    for repo in repositories:
        if not isinstance(repo, dict):
            continue
        full_name = str(repo.get("full_name") or "").strip()
        default_branch = str(repo.get("default_branch") or "").strip()
        if full_name and default_branch:
            result.append({
                "full_name": full_name,
                "default_branch": default_branch,
                "private": bool(repo.get("private")),
                "archived": bool(repo.get("archived")),
                "disabled": bool(repo.get("disabled")),
                "size_kb": int(repo.get("size") or 0),
            })
    return sorted(result, key=lambda item: item["full_name"])


def filesystem_manifest(root: Path) -> list[dict[str, Any]]:
    manifest: list[dict[str, Any]] = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        relative = path.relative_to(root).as_posix()
        manifest.append({
            "path": relative,
            "size": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        })
    return manifest


def blocked(repo: dict[str, Any], state: str, reason: str) -> dict[str, Any]:
    record = {
        "repository": repo["full_name"],
        "default_branch": repo["default_branch"],
        "provider_size_kb": repo["size_kb"],
        "state": state,
        "blockers": [reason],
        "manual_action_required": False,
        "read_only_operation": True,
        "temporary_source_destroyed": True,
        "source_content_retained": False,
        "source_content_uploaded": False,
        "production_mutation_allowed": False,
        "execution_authority": False,
        "traffic_cutover_authority": False,
        "cancellation_authority": False,
        "provider_retirement_authority": False,
        "continuity_receipt_minted": False,
    }
    record["record_hash"] = digest(record)
    return record


def verify(repo: dict[str, Any], token: str) -> dict[str, Any]:
    if repo["archived"]:
        return blocked(repo, "BLOCKED_ARCHIVED_REPOSITORY", "repository_archived")
    if repo["disabled"]:
        return blocked(repo, "BLOCKED_DISABLED_REPOSITORY", "repository_disabled")
    if repo["size_kb"] > MAX_PROVIDER_SIZE_KB:
        return blocked(repo, "BLOCKED_RUNNER_SAFETY_LIMIT", "provider_reported_size_exceeds_250000_kb")

    root = Path(tempfile.mkdtemp(prefix="stegverse-github-reconstruction-"))
    clone = root / "clone"
    archive = root / "default-branch.tar"
    restored = root / "restored"
    try:
        url = f"https://x-access-token:{token}@github.com/{repo['full_name']}.git"
        safe_env = dict(os.environ)
        safe_env["GIT_TERMINAL_PROMPT"] = "0"
        run([
            "git", "clone", "--depth", "1", "--single-branch", "--branch",
            repo["default_branch"], url, str(clone),
        ], env=safe_env)
        commit = run(["git", "rev-parse", "HEAD"], cwd=clone)
        tree = run(["git", "rev-parse", "HEAD^{tree}"], cwd=clone)
        tree_listing = run(["git", "ls-tree", "-r", "--full-tree", "HEAD"], cwd=clone)
        subprocess.run(
            ["git", "archive", "--format=tar", "--output", str(archive), "HEAD"],
            cwd=clone,
            check=True,
            timeout=300,
        )
        archive_sha256 = hashlib.sha256(archive.read_bytes()).hexdigest()
        restored.mkdir()
        with tarfile.open(archive, "r") as tar:
            tar.extractall(restored, filter="data")
        manifest = filesystem_manifest(restored)
        reconstructed_manifest_hash = digest(manifest)
        passed = bool(commit and tree and tree_listing and manifest)
        record = {
            "repository": repo["full_name"],
            "default_branch": repo["default_branch"],
            "provider_size_kb": repo["size_kb"],
            "state": "PASS_DEFAULT_BRANCH_RECONSTRUCTION" if passed else "BLOCKED_RECONSTRUCTION_EMPTY",
            "source_commit": commit,
            "source_tree": tree,
            "source_tree_listing_hash": hashlib.sha256(tree_listing.encode("utf-8")).hexdigest(),
            "archive_sha256": archive_sha256,
            "reconstructed_file_count": len(manifest),
            "reconstructed_manifest_hash": reconstructed_manifest_hash,
            "blockers": [] if passed else ["reconstruction_manifest_empty"],
            "manual_action_required": False,
            "read_only_operation": True,
            "temporary_source_destroyed": True,
            "source_content_retained": False,
            "source_content_uploaded": False,
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
        return blocked(repo, "BLOCKED_AUTOMATED_CLONE_OR_RECONSTRUCTION", f"{type(exc).__name__}")
    finally:
        shutil.rmtree(root, ignore_errors=True)


def main() -> int:
    token = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    if not token:
        repositories: list[dict[str, Any]] = []
        records: list[dict[str, Any]] = []
        source_state = "BLOCKED_AUTOMATED_CREDENTIAL_UNAVAILABLE"
    else:
        env = dict(os.environ)
        env["GH_TOKEN"] = token
        try:
            repositories = installation_repositories(env)
            records = [verify(repo, token) for repo in repositories]
            source_state = "COLLECTED"
        except Exception as exc:
            repositories = []
            records = []
            source_state = f"BLOCKED_PROVIDER_API:{type(exc).__name__}"

    report = {
        "schema_version": "1.0.0",
        "report_id": "github-default-branch-reconstruction",
        "source_state": source_state,
        "repository_count": len(repositories),
        "passed_repository_count": sum(1 for item in records if item["state"] == "PASS_DEFAULT_BRANCH_RECONSTRUCTION"),
        "blocked_repository_count": sum(1 for item in records if item["state"] != "PASS_DEFAULT_BRANCH_RECONSTRUCTION"),
        "records": records,
        "scope": "default_branch_snapshot_only",
        "history_complete": False,
        "issues_complete": False,
        "releases_complete": False,
        "manual_action_required": False,
        "read_only_operation": True,
        "temporary_source_destroyed": True,
        "source_content_retained": False,
        "source_content_uploaded": False,
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
