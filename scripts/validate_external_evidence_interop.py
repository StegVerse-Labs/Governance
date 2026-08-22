#!/usr/bin/env python3
"""Validate external evidence envelopes and bounded provider-specific governance lanes."""
from __future__ import annotations

import json
import pathlib
import sys
from typing import Any

FIXTURE_DIR = pathlib.Path("docs/examples/interop")
VERFI_PROFILE = FIXTURE_DIR / "verfi_transition_cases.json"
EXPECTED = {
    "external_evidence_valid.json": ("ALLOW", "ok"),
    "external_evidence_stale.json": ("DENY", "evidence.stale"),
    "external_evidence_drifted.json": ("FAIL-CLOSED", "evidence.reference_state_drift"),
    "external_evidence_incomplete.json": ("DENY", "evidence.incomplete"),
    "external_evidence_unauthorized.json": ("DENY", "evidence.provider_unauthorized"),
}
PROVIDER_TYPES = {"telemetry", "attestation", "verification", "composite"}
RESULTS = {"ALLOW", "DENY", "FAIL-CLOSED"}
VERFI_CASES = {
    "CLEAN_SEQUENCE": ("ALLOW", "ok"),
    "COMPREHENSION_MISSING": ("DENY", "evidence.comprehension_not_established"),
    "DISCLOSURE_DRIFT": ("FAIL-CLOSED", "evidence.disclosure_drift"),
    "AUTHORIZATION_LAPSED": ("DENY", "authorization.lapsed"),
    "EVIDENCE_TAMPER": ("FAIL-CLOSED", "evidence.integrity_failure"),
    "TEMPORAL_DISORDER": ("FAIL-CLOSED", "evidence.temporal_disorder"),
    "AMBIGUOUS_COMPREHENSION": ("DENY", "evidence.comprehension_ambiguous"),
    "OVER_COLLECTION": ("DENY", "evidence.minimization_failure"),
    "INDEPENDENT_RECONSTRUCTION": ("ALLOW", "ok"),
    "HUMAN_MACHINE_SYMMETRY": ("DENY", "comparison.no_execution_authority"),
}


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


def evaluate_verfi(case: dict[str, Any]) -> tuple[str, str]:
    if case.get("id") == "HUMAN_MACHINE_SYMMETRY":
        return "DENY", "comparison.no_execution_authority"
    if case.get("evidence_integrity") is not True:
        return "FAIL-CLOSED", "evidence.integrity_failure"
    if case.get("temporal_order_valid") is not True:
        return "FAIL-CLOSED", "evidence.temporal_disorder"
    if case.get("presented_hash") != case.get("authorized_hash"):
        return "FAIL-CLOSED", "evidence.disclosure_drift"
    if case.get("comprehension") == "ABSENT":
        return "DENY", "evidence.comprehension_not_established"
    if case.get("comprehension") != "DISTINGUISHABLE":
        return "DENY", "evidence.comprehension_ambiguous"
    if case.get("authorization_valid_at_commit") is not True:
        return "DENY", "authorization.lapsed"
    if case.get("minimum_information_satisfied") is not True:
        return "DENY", "evidence.minimization_failure"
    if case.get("reconstructable") is not True:
        return "FAIL-CLOSED", "evidence.reconstruction_failure"
    return "ALLOW", "ok"


def validate_verfi_profile(path: pathlib.Path, data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    require(data, ("profile_version", "external_formalism_id", "provider_profile", "authority_effect", "cases", "mandatory_invariants"), "VerFi profile", errors, path)
    if data.get("profile_version") != "1.0":
        errors.append(f"{path}: profile_version must be 1.0")
    if data.get("external_formalism_id") != "VERFI-HUMAN-TRANSITION-EVIDENCE-001":
        errors.append(f"{path}: unexpected external_formalism_id")
    if data.get("authority_effect") != "NONE_VALIDATION_ONLY":
        errors.append(f"{path}: external profile must remain validation-only")

    invariants = data.get("mandatory_invariants")
    require(invariants, (
        "signature_cannot_substitute_for_comprehension",
        "external_provider_execution_authority",
        "continuity_receipt_minted",
        "human_machine_comparison_grants_authority",
    ), "mandatory_invariants", errors, path)
    if isinstance(invariants, dict):
        if invariants.get("signature_cannot_substitute_for_comprehension") is not True:
            errors.append(f"{path}: signature/comprehension separation must be true")
        for field in ("external_provider_execution_authority", "continuity_receipt_minted", "human_machine_comparison_grants_authority"):
            if invariants.get(field) is not False:
                errors.append(f"{path}: {field} must remain false")

    cases = data.get("cases")
    if not isinstance(cases, list):
        errors.append(f"{path}: cases must be a list")
        return errors
    if len(cases) != 10:
        errors.append(f"{path}: expected 10 VerFi governance-lane cases")

    by_id: dict[str, dict[str, Any]] = {}
    for index, case in enumerate(cases):
        require(case, (
            "id", "disclosure", "comprehension", "authorization_valid_at_commit", "signature",
            "presented_hash", "authorized_hash", "evidence_integrity", "temporal_order_valid",
            "minimum_information_satisfied", "reconstructable", "expected",
        ), f"cases[{index}]", errors, path)
        if isinstance(case, dict) and isinstance(case.get("id"), str):
            by_id[case["id"]] = case

    if set(by_id) != set(VERFI_CASES):
        errors.append(f"{path}: VerFi case identifiers do not match required governance matrix")

    for case_id, expected in VERFI_CASES.items():
        case = by_id.get(case_id)
        if not case:
            continue
        declared = case.get("expected", {})
        if not isinstance(declared, dict) or (declared.get("result"), declared.get("reason_code")) != expected:
            errors.append(f"{path}: {case_id} declared expectation must be {expected}")
        observed = evaluate_verfi(case)
        if observed != expected:
            errors.append(f"{path}: {case_id} deterministic result {observed} != {expected}")

    missing = by_id.get("COMPREHENSION_MISSING")
    if missing:
        if missing.get("signature") is not True or missing.get("disclosure") is not True:
            errors.append(f"{path}: comprehension-missing negative lane must retain disclosure and signature")
        if evaluate_verfi(missing) != ("DENY", "evidence.comprehension_not_established"):
            errors.append(f"{path}: signature must not substitute for comprehension evidence")

    symmetry = by_id.get("HUMAN_MACHINE_SYMMETRY")
    if symmetry and symmetry.get("comparison_only") is not True:
        errors.append(f"{path}: HUMAN_MACHINE_SYMMETRY must remain comparison_only")

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

    verfi, verfi_load_errors = load(VERFI_PROFILE)
    errors.extend(verfi_load_errors)
    if verfi is not None:
        errors.extend(validate_verfi_profile(VERFI_PROFILE, verfi))

    if errors:
        print("External evidence interoperability validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"External evidence interoperability validation passed for {len(EXPECTED)} canonical envelopes plus {len(VERFI_CASES)} VerFi governance-lane cases.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
