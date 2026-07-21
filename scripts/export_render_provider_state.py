#!/usr/bin/env python3
"""Export privacy-safe Render provider evidence with deterministic blocked states."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import subprocess
import tempfile
import urllib.error
import urllib.request
from typing import Any

SCHEMA = "stegverse.governance.render_provider_state.v1"
CONFIG_NAMES = {"render.yaml", "render.yml"}
MAX_REPOSITORIES = 500


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def sha256(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, text=True, capture_output=True, check=False)


def installation_repositories() -> list[dict[str, Any]]:
    result = run("gh", "api", "--paginate", "installation/repositories")
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "installation repository discovery failed")
    repos: list[dict[str, Any]] = []
    decoder = json.JSONDecoder()
    text = result.stdout.strip()
    while text:
        payload, index = decoder.raw_decode(text)
        repos.extend(payload.get("repositories", []))
        text = text[index:].lstrip()
    return repos[:MAX_REPOSITORIES]


def discover_configs(repositories: list[dict[str, Any]], token: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for repo in sorted(repositories, key=lambda x: x.get("full_name", "")):
        full_name = repo.get("full_name")
        default_branch = repo.get("default_branch")
        if not full_name or not default_branch or repo.get("archived") or repo.get("disabled"):
            continue
        with tempfile.TemporaryDirectory(prefix="render-config-") as directory:
            url = f"https://x-access-token:{token}@github.com/{full_name}.git"
            clone = run("git", "clone", "--quiet", "--depth", "1", "--single-branch", "--branch", default_branch, url, directory)
            if clone.returncode != 0:
                records.append({"repository": full_name, "state": "BLOCKED_CONFIG_DISCOVERY", "config_paths": []})
                continue
            found: list[dict[str, Any]] = []
            root = pathlib.Path(directory)
            for path in sorted(root.rglob("*")):
                if not path.is_file() or path.name.lower() not in CONFIG_NAMES or ".git" in path.parts:
                    continue
                raw = path.read_bytes()
                found.append({
                    "path": str(path.relative_to(root)),
                    "content_sha256": hashlib.sha256(raw).hexdigest(),
                    "size_bytes": len(raw),
                })
            records.append({
                "repository": full_name,
                "default_branch": default_branch,
                "state": "CONFIG_DISCOVERED" if found else "NO_RENDER_CONFIG_DISCOVERED",
                "config_paths": found,
            })
    return records


def render_api_metadata(api_key: str) -> tuple[str, list[dict[str, Any]], list[str]]:
    request = urllib.request.Request(
        "https://api.render.com/v1/services?limit=100",
        headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.load(response)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as exc:
        return "BLOCKED_RENDER_API", [], [f"render_api_unavailable:{type(exc).__name__}"]

    services: list[dict[str, Any]] = []
    for item in payload:
        service = item.get("service", item) if isinstance(item, dict) else {}
        if not isinstance(service, dict):
            continue
        safe = {
            "id": service.get("id"),
            "name": service.get("name"),
            "type": service.get("type"),
            "status": service.get("status"),
            "region": service.get("region"),
            "created_at": service.get("createdAt"),
            "updated_at": service.get("updatedAt"),
            "repository": service.get("repo"),
            "branch": service.get("branch"),
            "auto_deploy": service.get("autoDeploy"),
        }
        services.append(safe)
    services.sort(key=lambda x: (str(x.get("name")), str(x.get("id"))))
    return "AUTHENTICATED_RENDER_METADATA", services, []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    token = os.environ.get("GH_TOKEN", "")
    render_key = os.environ.get("RENDER_API_KEY", "")
    blockers: list[str] = []
    repositories: list[dict[str, Any]] = []
    configs: list[dict[str, Any]] = []

    if token:
        try:
            repositories = installation_repositories()
            configs = discover_configs(repositories, token)
        except Exception as exc:  # deterministic evidence, not operator task
            blockers.append(f"repository_discovery_unavailable:{type(exc).__name__}")
    else:
        blockers.append("github_token_unavailable")

    if render_key:
        api_state, services, api_blockers = render_api_metadata(render_key)
        blockers.extend(api_blockers)
    else:
        api_state, services = "BLOCKED_RENDER_API_CREDENTIAL_UNAVAILABLE", []
        blockers.append("render_api_credential_unavailable")

    config_count = sum(len(record.get("config_paths", [])) for record in configs)
    state = "RENDER_STATE_EXPORTED" if services else "BLOCKED_PARTIAL_RENDER_STATE"
    report: dict[str, Any] = {
        "schema": SCHEMA,
        "provider_id": "render",
        "state": state,
        "api_state": api_state,
        "installation_repository_count": len(repositories),
        "repository_config_record_count": len(configs),
        "render_config_file_count": config_count,
        "service_count": len(services),
        "repository_configs": configs,
        "services": services,
        "blockers": sorted(set(blockers)),
        "environment_values_retained": False,
        "deploy_hooks_retained": False,
        "credentials_retained": False,
        "raw_secret_material_retained": False,
        "manual_action_required": False,
        "production_mutation_allowed": False,
        "execution_authority": False,
        "traffic_cutover_authority": False,
        "cancellation_authority": False,
        "provider_retirement_authority": False,
        "continuity_receipt_minted": False,
    }
    report["report_sha256"] = sha256(report)
    output = pathlib.Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
