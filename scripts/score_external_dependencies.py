#!/usr/bin/env python3
"""Score external dependencies without granting cancellation or retirement authority."""
from __future__ import annotations

import json
from pathlib import Path

REGISTRY = Path("data/external_dependency_registry.json")
EVIDENCE = Path("data/external_cost_evidence.json")
OUTPUT = Path("reports/external-dependency-priority.json")

LEVEL = {"UNASSESSED": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def evidence_totals(evidence: dict) -> dict[str, float]:
    totals: dict[str, float] = {}
    for record in evidence.get("records", []):
        dependency_id = record["dependency_id"]
        monthly = float(record["normalized_monthly_cost"])
        totals[dependency_id] = totals.get(dependency_id, 0.0) + monthly
    return totals


def cost_score(monthly_cost: float | None) -> int:
    if monthly_cost is None:
        return 0
    if monthly_cost >= 500:
        return 4
    if monthly_cost >= 200:
        return 3
    if monthly_cost >= 50:
        return 2
    if monthly_cost > 0:
        return 1
    return 0


def main() -> int:
    registry = load_json(REGISTRY)
    evidence = load_json(EVIDENCE)
    totals = evidence_totals(evidence)
    scored = []

    for dep in registry["dependencies"]:
        verified_cost = totals.get(dep["id"])
        score = (
            cost_score(verified_cost) * 4
            + LEVEL[dep["lock_in_risk"]] * 3
            + LEVEL[dep["operational_criticality"]] * 3
            + LEVEL[dep["sovereignty_impact"]] * 3
        )
        scored.append({
            "dependency_id": dep["id"],
            "verified_monthly_cost": verified_cost,
            "score": score,
            "migration_phase": dep["migration_phase"],
            "cancellation_blockers": dep["cancellation_blockers"],
            "retirement_authorized": False,
        })

    scored.sort(key=lambda item: (-item["score"], item["dependency_id"]))
    output = {
        "schema_version": "1.0.0",
        "status": "PRIORITIZATION_ONLY",
        "authority": {
            "score_grants_cancellation_authority": False,
            "score_grants_retirement_authority": False,
            "retirement_requires_gdr": True,
        },
        "dependencies": scored,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT} with {len(scored)} dependencies.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
