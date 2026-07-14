#!/usr/bin/env python3
"""Validate example GDR JSON fixtures and three-layer governance invariants."""
from __future__ import annotations

import json
import pathlib
import sys
from typing import Any

REQUIRED_FIELDS = [
    "gdr_version",
    "decision_id",
    "decision",
    "policy",
    "evaluated_inputs",
    "issued_at",
    "rationale",
]

ALLOWED_DECISIONS = {"allow", "deny", "require_review", "recommend"}
ALLOWED_EXECUTION_RESULTS = {"ALLOW", "DENY", "FAIL-CLOSED"}
NEGATIVE_FIXTURES = {
    "condition_degraded_judgment_gdr.json": "condition_degraded_judgment",
    "signal_admission_drift_gdr.json": "signal_admission_drift",
    "governance_validation_of_drift_gdr.json": "governance_validation_of_drift",
}
POSITIVE_FIXTURE = "three_layer_positive_control_gdr.json"
REPLAY_BASELINE = "three_layer_replay_baseline_gdr.json"
REPLAY_MUTATED = "three_layer_replay_mutated_gdr.json"
THREE_LAYER_FIXTURES = {
    *NEGATIVE_FIXTURES,
    POSITIVE_FIXTURE,
    REPLAY_BASELINE,
    REPLAY_MUTATED,
}


def require_fields(
    errors: list[str], path: pathlib.Path, value: Any, fields: tuple[str, ...], label: str
) -> None:
    if not isinstance(value, dict):
        errors.append(f"{path}: {label} must be an object")
        return
    for field in fields:
        if field not in value:
            errors.append(f"{path}: {label} missing {field}")


def validate_base_fixture(path: pathlib.Path, data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"{path}: missing {field}")
    if data.get("gdr_version") != "1.0":
        errors.append(f"{path}: gdr_version must be 1.0")
    if data.get("decision") not in ALLOWED_DECISIONS:
        errors.append(f"{path}: unsupported decision {data.get('decision')}")

    require_fields(errors, path, data.get("policy"), ("policy_id", "policy_version"), "policy")
    require_fields(errors, path, data.get("evaluated_inputs"), ("source", "receipt_ids"), "evaluated_inputs")

    if not isinstance(data.get("issued_at"), int):
        errors.append(f"{path}: issued_at must be an integer")
    if not isinstance(data.get("rationale"), str) or not data.get("rationale", "").strip():
        errors.append(f"{path}: rationale must be a non-empty string")
    return errors


def validate_three_layer_shape(path: pathlib.Path, data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    require_fields(
        errors,
        path,
        data.get("judgment_conditions"),
        (
            "workload_state",
            "time_pressure",
            "isolation_state",
            "refusal_available",
            "operator_recoverability",
            "condition_receipt_ids",
        ),
        "judgment_conditions",
    )
    require_fields(
        errors,
        path,
        data.get("signal_admission"),
        (
            "admitted_signal_refs",
            "excluded_signal_refs",
            "transformations",
            "missing_inputs",
            "uncertainty_state",
            "reference_state_hash",
            "authorized_reference_state_hash",
            "reconstruction_available",
        ),
        "signal_admission",
    )
    require_fields(
        errors,
        path,
        data.get("execution_boundary"),
        (
            "actor_authority_ref",
            "policy_ref",
            "delegation_ref",
            "evidence_refs",
            "affected_entity_refs",
            "recoverability_profile",
            "validity_window",
            "result",
            "receipt_ref",
        ),
        "execution_boundary",
    )
    require_fields(
        errors,
        path,
        data.get("runtime_expectation"),
        ("result", "reason_code", "continuity_receipt_minted"),
        "runtime_expectation",
    )

    execution = data.get("execution_boundary", {})
    runtime = data.get("runtime_expectation", {})
    if isinstance(execution, dict) and execution.get("result") not in ALLOWED_EXECUTION_RESULTS:
        errors.append(f"{path}: unsupported execution result {execution.get('result')}")
    if isinstance(runtime, dict):
        if runtime.get("result") != execution.get("result"):
            errors.append(f"{path}: runtime result must match execution-boundary result")
        if runtime.get("continuity_receipt_minted") is not False:
            errors.append(f"{path}: StegCore must not mint a Continuity receipt")
    return errors


def validate_named_fixture(path: pathlib.Path, data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    execution = data.get("execution_boundary", {})
    judgment = data.get("judgment_conditions", {})
    signal = data.get("signal_admission", {})

    if path.name in NEGATIVE_FIXTURES:
        expected_failure_class = NEGATIVE_FIXTURES[path.name]
        if data.get("expected_failure_class") != expected_failure_class:
            errors.append(f"{path}: expected_failure_class must be {expected_failure_class}")

    if path.name == "condition_degraded_judgment_gdr.json":
        if judgment.get("refusal_available") is not False:
            errors.append(f"{path}: degraded judgment fixture must make refusal unavailable")
        if data.get("decision") != "deny" or execution.get("result") != "DENY":
            errors.append(f"{path}: degraded judgment must deny execution")

    if path.name == "signal_admission_drift_gdr.json":
        if signal.get("reconstruction_available") is not False:
            errors.append(f"{path}: signal drift fixture must be unreconstructable")
        if not signal.get("missing_inputs"):
            errors.append(f"{path}: signal drift fixture must identify missing inputs")
        if signal.get("reference_state_hash") == signal.get("authorized_reference_state_hash"):
            errors.append(f"{path}: signal drift fixture must use a shifted reference state")
        if execution.get("result") != "DENY":
            errors.append(f"{path}: signal drift must deny execution")

    if path.name in {"governance_validation_of_drift_gdr.json", REPLAY_MUTATED}:
        controls = data.get("control_assertions")
        require_fields(
            errors,
            path,
            controls,
            ("authority_check", "policy_check", "reference_state_continuity", "execution_permitted"),
            "control_assertions",
        )
        if isinstance(controls, dict):
            if controls.get("authority_check") != "pass" or controls.get("policy_check") != "pass":
                errors.append(f"{path}: authority and policy controls must pass")
            if controls.get("reference_state_continuity") != "fail":
                errors.append(f"{path}: reference-state continuity must fail")
            if controls.get("execution_permitted") is not False:
                errors.append(f"{path}: execution must not be permitted")
        if execution.get("result") != "FAIL-CLOSED":
            errors.append(f"{path}: shifted-state validation must fail closed")

    if path.name in {POSITIVE_FIXTURE, REPLAY_BASELINE}:
        if judgment.get("refusal_available") is not True:
            errors.append(f"{path}: positive case must preserve refusal availability")
        if judgment.get("operator_recoverability") != "available":
            errors.append(f"{path}: positive case must preserve operator recoverability")
        if signal.get("reconstruction_available") is not True:
            errors.append(f"{path}: positive case must be reconstructable")
        if signal.get("missing_inputs"):
            errors.append(f"{path}: positive case must not omit required inputs")
        if signal.get("reference_state_hash") != signal.get("authorized_reference_state_hash"):
            errors.append(f"{path}: positive case must preserve reference-state continuity")
        if data.get("decision") != "allow" or execution.get("result") != "ALLOW":
            errors.append(f"{path}: positive case must allow execution")

    return errors


def validate_replay_pair(
    fixture_dir: pathlib.Path, loaded: dict[str, dict[str, Any]]
) -> list[str]:
    errors: list[str] = []
    baseline = loaded.get(REPLAY_BASELINE)
    mutated = loaded.get(REPLAY_MUTATED)
    if baseline is None or mutated is None:
        return errors

    if baseline.get("replay_case_id") != mutated.get("replay_case_id"):
        errors.append(f"{fixture_dir}: replay pair must share replay_case_id")
    if baseline.get("policy") != mutated.get("policy"):
        errors.append(f"{fixture_dir}: replay pair must keep policy unchanged")

    baseline_execution = baseline.get("execution_boundary", {})
    mutated_execution = mutated.get("execution_boundary", {})
    for field in ("actor_authority_ref", "policy_ref", "delegation_ref"):
        if baseline_execution.get(field) != mutated_execution.get(field):
            errors.append(f"{fixture_dir}: replay pair must keep {field} unchanged")

    baseline_signal = baseline.get("signal_admission", {})
    mutated_signal = mutated.get("signal_admission", {})
    if baseline_signal.get("admitted_signal_refs") == mutated_signal.get("admitted_signal_refs"):
        errors.append(f"{fixture_dir}: replay mutation must change admitted signals")
    if baseline_signal.get("reference_state_hash") == mutated_signal.get("reference_state_hash"):
        errors.append(f"{fixture_dir}: replay mutation must change reference-state hash")
    if baseline_execution.get("result") != "ALLOW" or mutated_execution.get("result") != "FAIL-CLOSED":
        errors.append(f"{fixture_dir}: replay outcome must change from ALLOW to FAIL-CLOSED")
    return errors


def load_fixture(path: pathlib.Path) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, [f"{path}: cannot load JSON: {exc}"]
    if not isinstance(data, dict):
        return None, [f"{path}: fixture root must be an object"]
    return data, []


def main() -> int:
    fixture_dir = pathlib.Path("docs/examples/fixtures")
    errors: list[str] = []
    fixtures = sorted(fixture_dir.glob("*.json"))
    if not fixtures:
        print("No GDR fixtures found.")
        return 1

    fixture_names = {fixture.name for fixture in fixtures}
    for required_fixture in THREE_LAYER_FIXTURES:
        if required_fixture not in fixture_names:
            errors.append(f"{fixture_dir}: missing required fixture {required_fixture}")

    loaded: dict[str, dict[str, Any]] = {}
    for fixture in fixtures:
        data, load_errors = load_fixture(fixture)
        errors.extend(load_errors)
        if data is None:
            continue
        loaded[fixture.name] = data
        errors.extend(validate_base_fixture(fixture, data))
        if fixture.name in THREE_LAYER_FIXTURES:
            errors.extend(validate_three_layer_shape(fixture, data))
            errors.extend(validate_named_fixture(fixture, data))

    errors.extend(validate_replay_pair(fixture_dir, loaded))

    if errors:
        print("GDR example fixture validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"GDR example fixture validation passed for {len(fixtures)} fixtures, "
        f"including {len(THREE_LAYER_FIXTURES)} required three-layer cases."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
