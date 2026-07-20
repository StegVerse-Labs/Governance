#!/usr/bin/env python3
"""Validate privacy-safe external cost evidence references."""
from __future__ import annotations

import json
import re
from pathlib import Path

REGISTRY_PATH = Path("data/external_dependency_registry.json")
EVIDENCE_PATH = Path("data/external_cost_evidence.json")
DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
ALLOWED_CADENCE = {"monthly", "annual", "quarterly", "one_time", "variable"}


def main() -> int:
    errors: list[str] = []
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    dependency_ids = {item["id"] for item in registry["dependencies"]}

    privacy = evidence.get("privacy", {})
    for field in ("raw_statements_permitted_in_repository", "credentials_permitted_in_repository", "account_numbers_permitted_in_repository"):
        if privacy.get(field) is not False:
            errors.append(f"privacy boundary must remain false: {field}")
    if privacy.get("evidence_digests_only") is not True:
        errors.append("privacy.evidence_digests_only must be true")

    authority = evidence.get("authority", {})
    if authority.get("cost_evidence_grants_cancellation_authority") is not False:
        errors.append("cost evidence must not grant cancellation authority")
    if authority.get("cost_evidence_grants_retirement_authority") is not False:
        errors.append("cost evidence must not grant retirement authority")
    if authority.get("retirement_requires_gdr") is not True:
        errors.append("retirement must require a GDR")

    seen: set[str] = set()
    for index, record in enumerate(evidence.get("records", [])):
        prefix = f"records[{index}]"
        record_id = record.get("record_id")
        if not isinstance(record_id, str) or not record_id:
            errors.append(f"{prefix}.record_id is required")
        elif record_id in seen:
            errors.append(f"duplicate record_id: {record_id}")
        else:
            seen.add(record_id)
        if record.get("dependency_id") not in dependency_ids:
            errors.append(f"{prefix}.dependency_id is not registered")
        if record.get("billing_cadence") not in ALLOWED_CADENCE:
            errors.append(f"{prefix}.billing_cadence is invalid")
        amount = record.get("normalized_monthly_cost")
        if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount < 0:
            errors.append(f"{prefix}.normalized_monthly_cost must be nonnegative")
        digest = record.get("source_digest")
        if not isinstance(digest, str) or not DIGEST.fullmatch(digest):
            errors.append(f"{prefix}.source_digest must be sha256:<64 lowercase hex>")
        if record.get("verified") is not True:
            errors.append(f"{prefix}.verified must be true before scoring")
        forbidden = {"account_number", "card_number", "credential", "raw_statement", "secret"}
        present = forbidden.intersection(record)
        if present:
            errors.append(f"{prefix} contains forbidden fields: {sorted(present)}")

    if errors:
        print("External cost evidence validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"External cost evidence validation passed ({len(seen)} records).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
