#!/usr/bin/env python3
"""Synchronize provider inventory adapter issues from the deterministic queue.

This script emits an issue plan by default and applies it when --apply is used.
It never authorizes cancellation, retirement, credential revocation, DNS transfer,
or traffic cutover.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

QUEUE = Path("reports/provider-inventory-queue.json")


def load_queue() -> dict[str, Any]:
    data = json.loads(QUEUE.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("queue"), list):
        raise SystemExit("invalid provider inventory queue")
    return data


def issue_title(provider_id: str) -> str:
    return f"[adapter] Provider inventory collector: {provider_id}"


def issue_body(item: dict[str, Any], queue_hash: str) -> str:
    actions = "\n".join(f"- [ ] `{action}`" for action in item.get("bounded_actions", []))
    blockers = "\n".join(f"- `{blocker}`" for blocker in item.get("blockers", [])) or "- none"
    return f"""## Machine-owned state

- Provider: `{item['provider_id']}`
- Queue state: `{item['state']}`
- Priority: `{item['priority']}`
- Queue hash: `{queue_hash}`
- Manual action required: `false`

## Bounded collector actions

{actions}

## Current blockers

{blockers}

## Required output

A deterministic, secret-free inventory record containing source commit, collection time, enumerated asset metadata, payload hash, and a Master-Records custody reference.

## Authority boundary

This task grants no cancellation, deletion, credential revocation, DNS transfer, production cutover, provider retirement, execution, or receipt-minting authority. Missing credentials or provider identity must produce a machine-readable blocked result rather than a manual task.
"""


def gh(*args: str) -> str:
    result = subprocess.run(["gh", *args], check=True, capture_output=True, text=True)
    return result.stdout.strip()


def sync(repo: str, item: dict[str, Any], queue_hash: str) -> dict[str, Any]:
    title = issue_title(item["provider_id"])
    body = issue_body(item, queue_hash)
    number = gh("issue", "list", "--repo", repo, "--state", "all", "--search", f"{title} in:title", "--json", "number", "--jq", ".[0].number // empty")
    if number:
        gh("issue", "edit", number, "--repo", repo, "--body", body)
        gh("issue", "reopen", number, "--repo", repo)
        action = "updated"
    else:
        number = gh("issue", "create", "--repo", repo, "--title", title, "--body", body)
        action = "created"
    return {"provider_id": item["provider_id"], "action": action, "issue": number}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--repo", default="StegVerse-Labs/Governance")
    parser.add_argument("--output", default="reports/provider-adapter-dispatch.json")
    args = parser.parse_args()

    queue = load_queue()
    plan = {
        "schema_version": "1.0.0",
        "queue_hash": queue.get("queue_hash"),
        "manual_action_required": False,
        "cancellation_authority": False,
        "provider_retirement_authority": False,
        "dispatch": [],
    }
    for item in queue["queue"]:
        entry = {
            "provider_id": item["provider_id"],
            "title": issue_title(item["provider_id"]),
            "state": item["state"],
            "body": issue_body(item, str(queue.get("queue_hash", ""))),
        }
        if args.apply:
            entry["result"] = sync(args.repo, item, str(queue.get("queue_hash", "")))
        plan["dispatch"].append(entry)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
