#!/usr/bin/env python3
"""Evaluate a StegCore release candidate without creating a tag or release."""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any

SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")


def load(path: pathlib.Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: root must be an object")
    return value


def canonical_hash(value: dict[str, Any]) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha256(payload.encode("utf-8")).hexdigest()


def project_version(pyproject: pathlib.Path) -> str:
    for line in pyproject.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("version") and "=" in line:
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise ValueError("project version not found")


def tag_exists(repository_url: str, tag: str) -> bool:
    result = subprocess.run(
        ["git", "ls-remote", "--tags", repository_url, f"refs/tags/{tag}", f"refs/tags/{tag}^{{}}"],
        check=True,
        capture_output=True,
        text=True,
    )
    return bool(result.stdout.strip())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", type=pathlib.Path, required=True)
    parser.add_argument("--candidate", type=pathlib.Path, required=True)
    parser.add_argument("--runtime", type=pathlib.Path, required=True)
    parser.add_argument("--readiness", type=pathlib.Path, required=True)
    parser.add_argument("--downstream", type=pathlib.Path, required=True)
    parser.add_argument("--freshness", type=pathlib.Path, required=True)
    parser.add_argument("--pyproject", type=pathlib.Path, required=True)
    parser.add_argument("--repository-url", required=True)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    args = parser.parse_args()

    policy = load(args.policy)
    candidate = load(args.candidate)
    runtime = load(args.runtime)
    readiness = load(args.readiness)
    downstream = load(args.downstream)
    freshness = load(args.freshness)

    checks: dict[str, dict[str, Any]] = {}

    def check(name: str, passed: bool, observed: Any) -> None:
        checks[name] = {"status": "pass" if passed else "fail", "observed": observed}

    required_fields = policy.get("required_candidate_fields", [])
    missing = [field for field in required_fields if not candidate.get(field)]
    check("candidate_shape", not missing, {"missing": missing})

    version = str(candidate.get("version", ""))
    tag = str(candidate.get("tag", ""))
    check("semantic_version", bool(SEMVER.fullmatch(version)), version)
    check("tag_matches_version", tag == f"v{version}", tag)
    check("version_matches_project", version == project_version(args.pyproject), project_version(args.pyproject))

    check("runtime_validation", runtime.get("status") == "pass", runtime.get("status"))
    check("runtime_commit_binding", candidate.get("stegcore_commit") == runtime.get("stegcore_commit"), runtime.get("stegcore_commit"))
    check("runtime_hash_binding", candidate.get("runtime_evidence_hash") == runtime.get("evidence_hash"), runtime.get("evidence_hash"))

    check("downstream_verification", downstream.get("status") == "pass" and downstream.get("passing_gates") == downstream.get("required_gates"), downstream.get("status"))
    check("downstream_hash_binding", candidate.get("downstream_results_hash") == downstream.get("results_hash"), downstream.get("results_hash"))

    check("governance_freshness", freshness.get("status") == "pass" and freshness.get("revalidation_required") is False, freshness.get("status"))
    check("freshness_hash_binding", candidate.get("governance_freshness_hash") == freshness.get("freshness_hash"), freshness.get("freshness_hash"))

    readiness_gates = readiness.get("gates", {})
    check("readiness_runtime", readiness_gates.get("runtime_validation") == "pass", readiness_gates.get("runtime_validation"))
    check("readiness_downstream", readiness_gates.get("downstream_verification") == "pass", readiness_gates.get("downstream_verification"))
    check("release_still_unclaimed", readiness.get("release_permitted") is False and readiness.get("tag_permitted") is False, {"release_permitted": readiness.get("release_permitted"), "tag_permitted": readiness.get("tag_permitted")})

    try:
        exists = tag_exists(args.repository_url, tag)
        check("tag_unique", not exists, {"tag": tag, "exists": exists})
    except Exception as exc:
        check("tag_unique", False, {"error": str(exc)})

    failed = [name for name, result in checks.items() if result["status"] != "pass"]
    decision = "ALLOW" if not failed else "DENY"
    reasons = ["all independent release-policy gates passed"] if not failed else [f"failed gate: {name}" for name in failed]

    artifact: dict[str, Any] = {
        "artifact_type": "governance.release_decision",
        "schema_version": "1.0",
        "policy_id": policy.get("policy_id"),
        "decision_owner": policy.get("decision_owner"),
        "subject_repository": candidate.get("repository"),
        "candidate_version": version,
        "candidate_tag": tag,
        "candidate_commit": candidate.get("stegcore_commit"),
        "decision": decision,
        "checks": checks,
        "reasons": reasons,
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "next_permitted_action": "create annotated tag only" if decision == "ALLOW" else "repair failed gates and re-evaluate",
        "authority_boundary": policy.get("authority_boundary"),
        "release_created": False,
        "tag_created": False,
        "deployment_authorized": False,
        "continuity_receipt_minted": False,
    }
    artifact["decision_hash"] = canonical_hash(artifact)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{decision}: {', '.join(reasons)}")
    return 0 if decision == "ALLOW" else 1


if __name__ == "__main__":
    raise SystemExit(main())
