#!/usr/bin/env python3
"""Smoke-test the reusable conversation ingestion engine."""
from __future__ import annotations

import datetime as dt
import pathlib
import tempfile

from ingest_conversation import ingest


def main() -> int:
    sample = """Judgment conditions must support refusal and recoverability.

---

Signal admission must preserve provenance before state formation.

---

Execution must fail closed when the reference state cannot be reconstructed.
"""
    fixed = dt.datetime(2026, 7, 14, 0, 0, tzinfo=dt.timezone.utc)
    with tempfile.TemporaryDirectory() as tmp:
        output_dir = pathlib.Path(tmp) / "conversations"
        written = ingest(
            title="Judgment Signal Execution Smoke Test",
            content=sample,
            output_dir=output_dir,
            timestamp=fixed,
        )
        if len(written) != 3:
            raise SystemExit(f"expected 3 section files, found {len(written)}")
        index = output_dir / "INDEX.md"
        if not index.exists():
            raise SystemExit("conversation index was not created")
        index_text = index.read_text(encoding="utf-8")
        for path in written:
            if not path.exists() or path.name not in index_text:
                raise SystemExit(f"missing indexed output for {path.name}")
            text = path.read_text(encoding="utf-8")
            if "# Next actions (resume here)" not in text:
                raise SystemExit(f"missing continuation marker in {path.name}")
        if not any("signal-admission" in path.name for path in written):
            raise SystemExit("signal-admission tagging was not exercised")
        if not any("execution" in path.name for path in written):
            raise SystemExit("execution tagging was not exercised")
    print("Conversation ingestion smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
