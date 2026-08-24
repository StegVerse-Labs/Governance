#!/usr/bin/env python3
"""Validate the VerFi real-artifact intake contract without claiming an artifact exists."""
from __future__ import annotations

import copy
import json
from pathlib import Path

CONTRACT = Path("docs/examples/interop/verfi_real_artifact_intake_contract.json")
EXPECTED_TYPES = {
    "consent_record",
    "evidence_package",
    "implementation_schema",
    "api_output",
    "execution_verified_token_specimen",
}
EXPECTED_IDENTITY = {
    "artifact_type",
    "source_uri_or_transfer_ref",
    "sha256",
    "byte_length",
    "observed_at",
    "producer_asserted",
}
EXPECTED_TESTS = {
    "ARTIFACT_IDENTITY_BINDING",
    "DIGEST_REPRODUCIBILITY",
    "DISCLOSURE_VERSION_CONTINUITY",
    "CHECKPOINT_CORRECTION_PRESERVATION",
    "AUTHORIZATION_ENABLEMENT_CAUSALITY",
    "COMPREHENSION_MISSING_NEGATIVE",
    "TAMPER_FAIL_CLOSED",
    "TEMPORAL_ORDER_VALIDATION",
    "INDEPENDENT_RECONSTRUCTION",
    "EXTERNAL_TOKEN_NO_AUTHORITY",
}


def load() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    if data.get("contract_version") != "1.0":
        errors.append("contract_version must be 1.0")
    if data.get("external_formalism_id") != "VERFI-HUMAN-TRANSITION-EVIDENCE-001":
        errors.append("unexpected external formalism id")
    if data.get("status") != "READY_FOR_REAL_ARTIFACT_NO_ARTIFACT_BOUND":
        errors.append("contract must remain explicit that no real artifact is bound")
    if data.get("authority_effect") != "NONE_VALIDATION_ONLY":
        errors.append("intake contract must remain validation-only")
    if data.get("artifact_instance_present") is not False:
        errors.append("repository must not fabricate a real VerFi artifact instance")
    if set(data.get("accepted_artifact_types", [])) != EXPECTED_TYPES:
        errors.append("accepted artifact types changed")
    if set(data.get("required_identity_fields", [])) != EXPECTED_IDENTITY:
        errors.append("immutable artifact identity fields changed")
    if set(data.get("required_tests", [])) != EXPECTED_TESTS:
        errors.append("real-artifact test matrix changed")

    outcomes = data.get("mandatory_outcomes", {})
    required_outcomes = {
        "missing_comprehension": ["DENY", "evidence.comprehension_not_established"],
        "integrity_failure": ["FAIL-CLOSED", "evidence.integrity_failure"],
        "temporal_disorder": ["FAIL-CLOSED", "evidence.temporal_disorder"],
        "reconstruction_failure": ["FAIL-CLOSED", "evidence.reconstruction_failure"],
    }
    if outcomes != required_outcomes:
        errors.append("mandatory negative/fail-closed outcomes changed")

    invariants = data.get("authority_invariants", {})
    required_false = {
        "external_provider_execution_authority",
        "external_token_execution_authority",
        "external_token_admissibility_authority",
        "continuity_receipt_minted_by_governance",
        "legal_admissibility_inferred",
        "cognitive_state_proven",
    }
    for key in required_false:
        if invariants.get(key) is not False:
            errors.append(f"{key} must remain false")
    return errors


def assert_mutation_guards(data: dict) -> None:
    mutated = copy.deepcopy(data)
    mutated["artifact_instance_present"] = True
    assert validate(mutated), "fabricated artifact presence must be rejected"

    mutated = copy.deepcopy(data)
    mutated["authority_invariants"]["external_token_execution_authority"] = True
    assert validate(mutated), "external token authority promotion must be rejected"

    mutated = copy.deepcopy(data)
    mutated["mandatory_outcomes"]["missing_comprehension"] = ["ALLOW", "ok"]
    assert validate(mutated), "signature/comprehension collapse must be rejected"

    mutated = copy.deepcopy(data)
    mutated["required_identity_fields"].remove("sha256")
    assert validate(mutated), "artifact intake without immutable digest must be rejected"


if __name__ == "__main__":
    contract = load()
    errors = validate(contract)
    if errors:
        raise SystemExit("VerFi real-artifact intake validation failed: " + "; ".join(errors))
    assert_mutation_guards(contract)
    print("VerFi real-artifact intake contract validation passed: no artifact fabricated, immutable identity required, 10-test matrix preserved, authority remains NONE_VALIDATION_ONLY.")
