#!/usr/bin/env python3
"""Persist and verify Governance Decision Records inside KnowledgeVault.

KnowledgeVault preserves the decision package. It does not become a governance,
continuity, cryptographic-verification, or execution authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

FORMAT = "stegverse.knowledgevault.gdr/v1"
KV_RELATIVE_ROOT = Path("_System/Governance/Decisions")
VALID_DECISIONS = {"allow", "deny", "require_review", "recommend"}


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sha256_uri(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _require(mapping: dict[str, Any], key: str) -> Any:
    if key not in mapping:
        raise ValueError(f"missing required field: {key}")
    return mapping[key]


def normalize_gdr(gdr: dict[str, Any]) -> dict[str, Any]:
    _require(gdr, "gdr_version")
    _require(gdr, "decision_id")
    decision = _require(gdr, "decision")
    if decision not in VALID_DECISIONS:
        raise ValueError(f"unsupported decision: {decision}")
    policy = _require(gdr, "policy")
    if not isinstance(policy, dict):
        raise ValueError("policy must be an object")
    _require(policy, "policy_id")
    _require(policy, "policy_version")
    evaluated = _require(gdr, "evaluated_inputs")
    if not isinstance(evaluated, dict):
        raise ValueError("evaluated_inputs must be an object")
    _require(evaluated, "source")
    receipt_ids = _require(evaluated, "receipt_ids")
    if not isinstance(receipt_ids, list):
        raise ValueError("evaluated_inputs.receipt_ids must be a list")
    _require(gdr, "issued_at")
    _require(gdr, "rationale")
    return json.loads(canonical_bytes(gdr).decode("utf-8"))


def build_package(
    gdr: dict[str, Any],
    *,
    continuity_record_refs: list[str] | None = None,
    execution_envelope_ref: str | None = None,
) -> dict[str, Any]:
    normalized = normalize_gdr(gdr)
    package = {
        "format": FORMAT,
        "gdr": normalized,
        "continuity_record_refs": sorted(set(continuity_record_refs or [])),
        "execution_envelope_ref": execution_envelope_ref,
        "knowledge_vault_role": "durable_persistence_only",
        "knowledge_vault_governance_authority": False,
        "knowledge_vault_continuity_authority": False,
        "governance_execution_authority": False,
        "continuity_receipt_minted": False,
        "cryptographic_verification_performed": False,
    }
    package["package_hash"] = sha256_uri(canonical_bytes(package))
    return package


def verify_package(package: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    if _require(package, "format") != FORMAT:
        reasons.append("unsupported format")
    try:
        gdr = normalize_gdr(_require(package, "gdr"))
    except (TypeError, ValueError) as exc:
        reasons.append(str(exc))
        gdr = {}

    for field in (
        "knowledge_vault_governance_authority",
        "knowledge_vault_continuity_authority",
        "governance_execution_authority",
        "continuity_receipt_minted",
        "cryptographic_verification_performed",
    ):
        if package.get(field) is not False:
            reasons.append(f"{field} must be false")

    claimed = _require(package, "package_hash")
    unhashed = dict(package)
    unhashed.pop("package_hash", None)
    actual = sha256_uri(canonical_bytes(unhashed))
    if claimed != actual:
        reasons.append("package hash mismatch")

    return {
        "decision": "ALLOW" if not reasons else "BLOCK",
        "decision_id": gdr.get("decision_id"),
        "gdr_decision": gdr.get("decision"),
        "package_hash": actual,
        "reasons": reasons,
    }


def package_path(vault_root: Path, decision_id: str) -> Path:
    safe = "".join(c if c.isalnum() or c in "-_." else "_" for c in decision_id)
    if not safe:
        raise ValueError("decision_id must contain a usable character")
    return vault_root / KV_RELATIVE_ROOT / f"{safe}.json"


def persist(vault_root: Path, package: dict[str, Any]) -> Path:
    result = verify_package(package)
    if result["decision"] != "ALLOW":
        raise ValueError("refusing to persist invalid GDR package: " + "; ".join(result["reasons"]))
    decision_id = str(package["gdr"]["decision_id"])
    path = package_path(vault_root, decision_id)
    if path.exists():
        existing = json.loads(path.read_text(encoding="utf-8"))
        if canonical_bytes(existing) != canonical_bytes(package):
            raise ValueError("refusing to overwrite an existing historical GDR package")
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(package) + b"\n")
    return path


def load_and_verify(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("GDR package must be a JSON object")
    return verify_package(data)


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create")
    create.add_argument("vault_root", type=Path)
    create.add_argument("gdr", type=Path)
    create.add_argument("--continuity-record-ref", action="append", default=[])
    create.add_argument("--execution-envelope-ref")

    verify = sub.add_parser("verify")
    verify.add_argument("package", type=Path)

    args = parser.parse_args()
    if args.command == "verify":
        result = load_and_verify(args.package)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["decision"] == "ALLOW" else 1

    gdr = json.loads(args.gdr.read_text(encoding="utf-8"))
    if not isinstance(gdr, dict):
        raise SystemExit("BLOCK: GDR must be a JSON object")
    package = build_package(
        gdr,
        continuity_record_refs=args.continuity_record_ref,
        execution_envelope_ref=args.execution_envelope_ref,
    )
    path = persist(args.vault_root, package)
    print(json.dumps({"decision": "ALLOW", "path": str(path), "package_hash": package["package_hash"]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
