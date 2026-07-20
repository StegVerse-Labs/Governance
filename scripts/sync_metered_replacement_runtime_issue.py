#!/usr/bin/env python3
"""Create or update the StegCore runtime issue without manual repository work."""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path

STATUS = Path("reports/metered-platform-replacement-status.json")
API = "https://api.github.com"
TARGET_REPO = "StegVerse-Labs/StegCore"
ISSUE_TITLE = "Evaluate metered-platform replacement and retirement boundaries"


def request(method: str, path: str, token: str, payload: dict | None = None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        API + path,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())


def main() -> int:
    token = os.environ.get("STEGCORE_TASK_TOKEN")
    if not token:
        print("STEGCORE_TASK_TOKEN unavailable; emitting fail-closed status without mutation.")
        return 0
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    body = f"""## Machine-owned runtime contract

Source: `StegVerse-Labs/Governance` metered-platform replacement workstream.
Status hash: `{status['status_hash']}`
Verified costs: `{status['verified_cost_count']}`
Retirement-ready providers: `{status['retirement_ready_count']}`

Required runtime cases:
- `ALLOW / replacement.selection_allowed` for bounded design preparation only.
- `DENY / retirement.evidence_incomplete` whenever a required retirement gate is absent.
- Preserve `cancellation_authority=false`, `provider_retirement_authority=false`, and `continuity_receipt_minted=false`.

This issue is synchronized automatically. Provider adapters, custody, cancellation, and retirement execution remain outside StegCore.
"""
    query = urllib.parse.quote(f'repo:{TARGET_REPO} is:issue in:title "{ISSUE_TITLE}"')
    result = request("GET", f"/search/issues?q={query}", token)
    matches = [item for item in result.get("items", []) if item.get("title") == ISSUE_TITLE]
    if matches:
        number = matches[0]["number"]
        request("PATCH", f"/repos/{TARGET_REPO}/issues/{number}", token, {"body": body})
        print(f"Updated {TARGET_REPO}#{number}")
    else:
        created = request("POST", f"/repos/{TARGET_REPO}/issues", token, {"title": ISSUE_TITLE, "body": body})
        print(f"Created {TARGET_REPO}#{created['number']}")
    return 0


if __name__ == "__main__":
    import urllib.parse
    try:
        raise SystemExit(main())
    except urllib.error.HTTPError as exc:
        print(exc.read().decode())
        raise
