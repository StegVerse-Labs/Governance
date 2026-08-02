#!/usr/bin/env python3
"""Create or update the canonical StegTrace bootstrap in a pre-existing repo.

The script is fail-closed and idempotent. It never creates the repository itself.
It writes a durable JSON receipt with COMPLETE, BLOCKED, RETRY,
REVIEW_REQUIRED, or FAILED status.
"""
from __future__ import annotations

import base64
import json
import os
import subprocess
import sys
import time
from pathlib import Path

OWNER = "StegVerse-Labs"
REPO = "StegTrace"
FULL_REPO = f"{OWNER}/{REPO}"
BRANCH = "bootstrap/stegtrace-v0"
RECEIPT = Path("evidence/stegtrace-bootstrap/latest.json")

FILES = {
"README.md": """# StegTrace\n\n> Public protocol and evaluation engine. No credentials or raw private evidence belong in this repository.\n\nStegTrace evaluates bounded signals and emits confidence-scored TRACE Signal Bundles. It does not verify identity, authorize actions, or execute downstream work.\n\n## Boundaries\n- StegID verifies continuity and cryptographic claims.\n- StegTrace evaluates signals and uncertainty.\n- Governance consumes bounded bundles and emits GDR decisions.\n- Application profiles include StegTalk/trace, StegProv/trace, and StegFREEDOM/trace.\n\nRead `STEGTRACE_MIRROR_HANDOFF.md` before changing the engine.\n""",
"STEGTRACE_MIRROR_HANDOFF.md": """# StegTrace Mirror Handoff\n\n- Goal ID: STEGTRACE-ENGINE-V0\n- Repository: StegVerse-Labs/StegTrace\n- Branch: main\n- Goal: activate the shared TRACE evaluation engine and governed application profiles.\n\n## Authority\nGovernance owns the consumer contract. StegTrace owns signal evaluation and bundle production. Applications own domain adapters.\n\n## Required files\nREADME.md; CHANGELOG.md; DISCLAIMER.md; CONFIDENCE_LABELS.md; docs/TRACE_OVERVIEW.md; docs/TRACE_SIGNAL_BUNDLE.md; docs/TRACE_PROFILES.md; docs/TRACE_REEVALUATION_AND_DELTAS.md; schemas/trace_signal_bundle.schema.json; scripts/emit_bundle_example.py; scripts/validate_trace.py; .github/workflows/validate-trace.yml.\n\n## Validation\nRun `python scripts/validate_trace.py`. CI must pass before merge.\n\n## Remaining work\nImplement persistent artifact/evaluation stores, evidence graph, calibrated scoring, and application adapters. No application may treat TRACE confidence as verified truth or execution authority.\n\n## Archive condition\nBootstrap merged, validation passing, and remaining implementation represented by durable issues or task state.\n\nDeveloped files: 12/12 bootstrap files. Goal activation: bootstrap only; runtime engine remains incomplete.\n""",
"CHANGELOG.md": """# Changelog\n\n## [Unreleased]\n- Persistent artifact and evaluation stores\n- Calibrated scoring and reevaluation engine\n\n## [0.1.0] - Bootstrap\n- Added engine boundaries, signal-bundle contract, profiles, schema, example emitter, validator, and CI.\n""",
"DISCLAIMER.md": """# Disclaimer\n\nTRACE outputs are confidence-scored assessments, not declarations of truth, identity, guilt, legal status, or execution authority. Raw private evidence and credentials must not be committed here.\n""",
"CONFIDENCE_LABELS.md": """# Confidence Labels\n\n- VERIFIED: supported by verified inputs or strong independent corroboration.\n- STRONGLY_SUPPORTED: strong evidence with limited remaining gaps.\n- PLAUSIBLE: consistent with some support but unresolved gaps.\n- INDETERMINATE: evidence is insufficient or materially mixed.\n- DISPUTED: credible evidence conflicts.\n- INCONSISTENT: conflicts with stronger established evidence.\n- LIKELY_MISATTRIBUTED_OR_MANIPULATED: strong provenance or integrity failures.\n\nLabels are versioned and may change only through a new evaluation record.\n""",
"docs/TRACE_OVERVIEW.md": """# TRACE Overview\n\nTRACE ingests bounded artifact references and signals, preserves uncertainty, records supporting and counter-signals, and emits reproducible evaluation records. Raw artifacts remain immutable in their owning stores. New data triggers targeted reevaluation rather than mutation of historical assessments.\n""",
"docs/TRACE_SIGNAL_BUNDLE.md": """# TRACE Signal Bundle\n\nThe TRACE Signal Bundle is the only StegTrace output accepted directly by Governance. It contains bundle identity, engine version, subject reference, scored signals, evidence references, limitations, and correlation metadata. It must conform to `schemas/trace_signal_bundle.schema.json`; it must not embed raw evidence or grant authority.\n""",
"docs/TRACE_PROFILES.md": """# TRACE Application Profiles\n\n## StegTalk/trace\nEphemeral, endpoint-local reconstruction and channel confidence; no longitudinal attribution.\n\n## StegProv/trace\nPersistent, multi-source research evaluation, provenance graphs, authorship hypotheses, and contradiction analysis.\n\n## StegFREEDOM/trace\nOversight and institutional-policy evaluation with public audit outputs.\n\nProfiles share StegTrace contracts but maintain separate retention, privacy, and authority rules.\n""",
"docs/TRACE_REEVALUATION_AND_DELTAS.md": """# Reevaluation and Deltas\n\nArtifacts and evaluations are immutable. New evidence creates a new artifact and triggers reevaluation of directly dependent claims plus bounded graph neighbors. Every reevaluation records old and new confidence vectors, label changes, reasons, model/rubric versions, and supersession links. Historical evaluations are never overwritten.\n""",
"schemas/trace_signal_bundle.schema.json": """{\n  \"$schema\": \"https://json-schema.org/draft/2020-12/schema\",\n  \"$id\": \"https://stegverse.org/schemas/trace_signal_bundle.schema.json\",\n  \"title\": \"TRACE Signal Bundle\",\n  \"type\": \"object\",\n  \"additionalProperties\": false,\n  \"required\": [\"bundle_version\", \"bundle_id\", \"produced_at\", \"source\", \"subject\", \"signals\", \"bounds\"],\n  \"properties\": {\n    \"bundle_version\": {\"const\": \"1.0\"},\n    \"bundle_id\": {\"type\": \"string\", \"minLength\": 1},\n    \"produced_at\": {\"type\": \"integer\", \"minimum\": 0},\n    \"source\": {\"type\": \"object\", \"required\": [\"engine\", \"engine_version\", \"run_id\"], \"properties\": {\"engine\": {\"const\": \"StegTrace\"}, \"engine_version\": {\"type\": \"string\"}, \"run_id\": {\"type\": \"string\"}}, \"additionalProperties\": false},\n    \"subject\": {\"type\": \"object\", \"required\": [\"type\", \"ref\"], \"properties\": {\"type\": {\"type\": \"string\"}, \"ref\": {\"type\": \"string\"}}, \"additionalProperties\": false},\n    \"signals\": {\"type\": \"array\", \"minItems\": 1, \"items\": {\"type\": \"object\", \"required\": [\"signal_id\", \"signal_type\", \"confidence\", \"summary\", \"evidence_refs\"], \"properties\": {\"signal_id\": {\"type\": \"string\"}, \"signal_type\": {\"type\": \"string\"}, \"confidence\": {\"type\": \"number\", \"minimum\": 0, \"maximum\": 1}, \"summary\": {\"type\": \"string\"}, \"evidence_refs\": {\"type\": \"array\", \"items\": {\"type\": \"string\"}}}, \"additionalProperties\": false}},\n    \"bounds\": {\"type\": \"object\", \"required\": [\"not_a_fact\", \"not_identity_verification\", \"not_execution_authority\"], \"properties\": {\"not_a_fact\": {\"const\": true}, \"not_identity_verification\": {\"const\": true}, \"not_execution_authority\": {\"const\": true}}, \"additionalProperties\": false}\n  }\n}\n""",
"scripts/emit_bundle_example.py": """#!/usr/bin/env python3\nimport json, time, uuid\nfrom pathlib import Path\nbundle={\"bundle_version\":\"1.0\",\"bundle_id\":f\"tsb-{uuid.uuid4()}\",\"produced_at\":int(time.time()),\"source\":{\"engine\":\"StegTrace\",\"engine_version\":\"0.1.0\",\"run_id\":str(uuid.uuid4())},\"subject\":{\"type\":\"artifact\",\"ref\":\"sha256:example\"},\"signals\":[{\"signal_id\":\"sig-1\",\"signal_type\":\"provenance_gap\",\"confidence\":0.5,\"summary\":\"Example only\",\"evidence_refs\":[\"example:source\"]}],\"bounds\":{\"not_a_fact\":True,\"not_identity_verification\":True,\"not_execution_authority\":True}}\nPath(\"example_trace_signal_bundle.json\").write_text(json.dumps(bundle,indent=2)+\"\\n\")\n""",
"scripts/validate_trace.py": """#!/usr/bin/env python3\nimport json, subprocess, sys\nfrom pathlib import Path\nrequired=[\"README.md\",\"STEGTRACE_MIRROR_HANDOFF.md\",\"docs/TRACE_SIGNAL_BUNDLE.md\",\"schemas/trace_signal_bundle.schema.json\",\"scripts/emit_bundle_example.py\"]\nmissing=[p for p in required if not Path(p).exists()]\nif missing: raise SystemExit(f\"missing required files: {missing}\")\nschema=json.loads(Path(\"schemas/trace_signal_bundle.schema.json\").read_text())\nfor key in (\"$schema\",\"$id\",\"required\",\"properties\"):\n    if key not in schema: raise SystemExit(f\"schema missing {key}\")\nsubprocess.run([sys.executable,\"scripts/emit_bundle_example.py\"],check=True)\nbundle=json.loads(Path(\"example_trace_signal_bundle.json\").read_text())\nfor field in schema[\"required\"]:\n    if field not in bundle: raise SystemExit(f\"example missing {field}\")\nif bundle[\"bounds\"] != {\"not_a_fact\":True,\"not_identity_verification\":True,\"not_execution_authority\":True}: raise SystemExit(\"authority bounds invalid\")\nprint(\"TRACE bootstrap validation passed\")\n""",
".github/workflows/validate-trace.yml": """name: Validate TRACE\non:\n  pull_request:\n  push:\n    branches: [main]\n  workflow_dispatch:\npermissions:\n  contents: read\njobs:\n  validate:\n    runs-on: ubuntu-latest\n    timeout-minutes: 5\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/setup-python@v5\n        with:\n          python-version: '3.11'\n      - run: python scripts/validate_trace.py\n"""
}


def gh(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["gh", *args], text=True, capture_output=True, check=check)


def write_receipt(status: str, detail: str, **extra: object) -> None:
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "task_id": "STEGTRACE-ENGINE-V0-BOOTSTRAP",
        "owner_repository": "StegVerse-Labs/Governance",
        "target_repository": FULL_REPO,
        "status": status,
        "detail": detail,
        "observed_at": int(time.time()),
        **extra,
    }
    RECEIPT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


def api_exists(path: str) -> bool:
    result = gh("api", path, check=False)
    return result.returncode == 0


def main() -> int:
    if not os.environ.get("GH_TOKEN"):
        write_receipt("FAILED", "GH_TOKEN unavailable")
        return 2
    if not api_exists(f"repos/{FULL_REPO}"):
        write_receipt("BLOCKED", "target repository does not exist or token cannot observe it", release_condition=f"GET /repos/{FULL_REPO} returns 200")
        return 0

    default_branch = json.loads(gh("api", f"repos/{FULL_REPO}").stdout)["default_branch"]
    if not api_exists(f"repos/{FULL_REPO}/git/ref/heads/{BRANCH}"):
        base_sha = json.loads(gh("api", f"repos/{FULL_REPO}/git/ref/heads/{default_branch}").stdout)["object"]["sha"]
        gh("api", f"repos/{FULL_REPO}/git/refs", "-X", "POST", "-f", f"ref=refs/heads/{BRANCH}", "-f", f"sha={base_sha}")

    changed = []
    for path, content in FILES.items():
        endpoint = f"repos/{FULL_REPO}/contents/{path}"
        existing = gh("api", endpoint, "-f", f"ref={BRANCH}", check=False)
        encoded = base64.b64encode(content.encode()).decode()
        if existing.returncode == 0:
            data = json.loads(existing.stdout)
            old = base64.b64decode(data["content"]).decode()
            if old == content:
                continue
            gh("api", endpoint, "-X", "PUT", "-f", "message=Update canonical StegTrace bootstrap", "-f", f"content={encoded}", "-f", f"sha={data['sha']}", "-f", f"branch={BRANCH}")
        else:
            gh("api", endpoint, "-X", "PUT", "-f", "message=Install canonical StegTrace bootstrap", "-f", f"content={encoded}", "-f", f"branch={BRANCH}")
        changed.append(path)

    prs = json.loads(gh("api", f"repos/{FULL_REPO}/pulls", "-f", "state=open", "-f", f"head={OWNER}:{BRANCH}").stdout)
    if prs:
        pr_url = prs[0]["html_url"]
    else:
        pr = json.loads(gh("api", f"repos/{FULL_REPO}/pulls", "-X", "POST", "-f", "title=Bootstrap StegTrace v0 engine", "-f", f"head={BRANCH}", "-f", f"base={default_branch}", "-f", "body=Installs the canonical StegTrace engine bootstrap, contract, profiles, schema, validator, workflow, and mirror handoff.").stdout)
        pr_url = pr["html_url"]

    write_receipt("REVIEW_REQUIRED", "bootstrap installed on branch and pull request exists", changed_files=changed, pull_request=pr_url)
    return 0

if __name__ == "__main__":
    sys.exit(main())
