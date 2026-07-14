#!/usr/bin/env python3
"""Validate external evidence envelopes and their bounded commitment mappings."""
from __future__ import annotations

import json
import pathlib
import sys
from typing import Any

FIXTURE_DIR = pathlib.Path("docs/examples/interop")
EXPECTED = {
    "external_evidence_valid.json": ("ALLOW", "ok"),
    "external_evidence_stale.json": ("DENY", "evidence.stale"),
    "external_evidence_drifted.json": ("FAIL-CLOSED", "evidence.reference_state_drift"),
    "external_evidence_incomplete.json": ("DENY", "evidence.incomplete"),
    "external_evidence_unauthorized.json": ("DENY", "evidence.provider_unauthorized"),
}
PROVIDER_TYPES = {"telemetry", "attestation", "verification", "composite"}
RESULTS = {"ALLOW", "DENY", "FAIL-CLOSED"}


def require(obj: Any, fields: tuple[str, ...], label: str, errors: list[str], path: pathlib.Path) -> None:
    if not isinstance(obj, dict):
        errors.append(f"{path}: {label} must be an object")
        return
    for field in fields:
        if field not in obj:
            errors.append(f"{path}: {label} missing {field}")


def load(path: pathlib.Path) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, [f"{path}: cannot load JSON: {exc}"]
    if not isinstance(value, dict):
        return None, [f"{path}: root must be an object"]
    return value, []


def validate(path: pathlib.Path, data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    require(data, (
        "external_evidence_envelope_version", "envelope_id", "provider", "subject",
        "capture", "claims", "integrity", "authorization", "freshness",
        "evidence_refs", "prior_hash", "issued_at", "commitment_candidate",
        "runtime_expectation",
    ), "envelope", errors, path)

    if data.get("external_evidence_envelope_version") != "1.0":
        errors.append(f"{path}: external_evidence_envelope_version must be 1.0")

    provider = data.get("provider")
    require(provider, ("provider_id", "provider_type", "public_key_ref", "declared_scope"), "provider", errors, path)
    if isinstance(provider, dict) and provider.get("provider_type") not in PROVIDER_TYPES:
        errors.append(f"{path}: unsupported provider_type {provider.get('provider_type')}")

    require(data.get("subject"), ("actor_ref", "target_ref", "workload_ref"), "subject", errors, path)
    require(data.get("capture"), ("started_at", "ended_at", "execution_context", "reference_state_hash"), "capture", errors, path)
    require(data.get("integrity"), ("content_digest", "signature_algorithm", "signature", "chain_valid"), "integrity", errors, path)
    require(data.get("authorization"), ("provider_authorized", "authorization_ref", "scope_match"), "authorization", errors, path)
    require(data.get("freshness"), ("valid_from", "valid_until", "evaluated_at", "is_current"), "freshness", errors, path)

    claims = data.get("claims")
    if not isinstance(claims, list):
        errors.append(f"{path}: claims must be a list")
    else:
        for index, claim in enumerate(claims):
            require(claim, ("claim_id", "claim_type", "value", "evidence_digest"), f"claims[{index}]", errors, path)

    candidate = data.get("commitment_candidate")
    require(candidate, (
        "candidate_id", "actor_ref", "target_ref", "scope", "action",
        "execution_context", "policy_ref", "delegation_ref", "consent_ref",
        "identity_ref", "evidence_refs", "evidence_digests", "capture_interval",
        "prior_hash", "validity_window", "reference_state_hash",
        "authorized_reference_state_hash", "recoverability_profile",
        "provider_authorization_ref", "evidence_provider_execution_authority",
    ), "commitment_candidate", errors, path)

    runtime = data.get("runtime_expectation")
    require(runtime, ("result", "reason_code", "continuity_receipt_minted"), "runtime_expectation", errors, path)
    if isinstance(runtime, dict) and runtime.get("result") not in RESULTS:
        errors.append(f"{path}: unsupported result {runtime.get('result')}")

    expected = EXPECTED[path.name]
    if isinstance(runtime, dict) and (runtime.get("result"), runtime.get("reason_code")) != expected:
        errors.append(f"{path}: expected result/reason {expected}")
    if isinstance(runtime, dict) and runtime.get("continuity_receipt_minted") is not False:
        errors.append(f"{path}: Governance/StegCore must not mint a Continuity receipt")
    if isinstance(candidate, dict) and candidate.get("evidence_provider_execution_authority") is not False:
        errors.append(f"{path}: evidence provider must not receive execution authority")

    authorization = data.get("authorization", {})
    freshness = data.get("freshness", {})
    capture = data.get("capture", {})
    if path.name == "external_evidence_valid.json":
        if not claims:
            errors.append(f"{path}: valid case must contain claims")
        if authorization.get("provider_authorized") is not True or authorization.get("scope_match") is not True:
            errors.append(f"{path}: valid case requires authorized provider and matching scope")
        if freshness.get("is_current") is not True:
            errors.append(f"{path}: valid case requires current evidence")
        if capture.get("reference_state_hash") != candidate.get("authorized_reference_state_hash"):
            errors.append(f"{path}: valid case must preserve reference-state continuity")
    elif path.name == "external_evidence_stale.json" and freshness.get("is_current") is not False:
        errors.append(f"{path}: stale case must set is_current=false")
    elif path.name == "external_evidence_drifted.json" and capture.get("reference_state_hash") == candidate.get("authorized_reference_state_hash"):
        errors.append(f"{path}: drifted case must change reference-state hash")
    elif path.name == "external_evidence_incomplete.json" and claims:
        errors.append(f"{path}: incomplete case must omit claims")
    elif path.name == "external_evidence_unauthorized.json" and authorization.get("provider_authorized") is not False:
        errors.append(f"{path}: unauthorized case must set provider_authorized=false")

    return errors


def main() -> int:
    errors: list[str] = []
    loaded: dict[str, dict[str, Any]] = {}
    for name in EXPECTED:
        path = FIXTURE_DIR / name
        if not path.exists():
            errors.append(f"{FIXTURE_DIR}: missing required fixture {name}")
            continue
        data, load_errors = load(path)
        errors.extend(load_errors)
        if data is not None:
            loaded[name] = data
            errors.extend(validate(path, data))

    valid = loaded.get("external_evidence_valid.json", {})
    drifted = loaded.get("external_evidence_drifted.json", {})
    if valid and drifted:
        for section, field in (("provider", "provider_id"), ("commitment_candidate", "policy_ref"), ("commitment_candidate", "delegation_ref")):
            if valid.get(section, {}).get(field) != drifted.get(section, {}).get(field):
                errors.append(f"{FIXTURE_DIR}: drift replay must preserve {section}.{field}")

    if errors:
        print("External evidence interoperability validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"External evidence interoperability validation passed for {len(EXPECTED)} canonical cases.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
