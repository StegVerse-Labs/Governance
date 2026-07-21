#!/usr/bin/env python3
"""Split Governance conversation text into indexed, tagged Markdown records."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re
from typing import Iterable

TOPIC_MAP = {
    "governance": r"\bconstitution|quorum|invariant|governance|council|verifier|judgment\b",
    "economy": r"\btokens?|treasury|emission|staking|credits?\b",
    "drift": r"\bdrift|divergence|cusum|monitor|alignment delta|reference state\b",
    "signal-admission": r"\bsignal admission|state formation|input provenance|compression\b",
    "execution": r"\badmissibility|execution boundary|fail[- ]closed|commit time\b",
    "anchoring": r"\banchor|merkle|op_return|calldata|tsa|transparency log\b",
    "vault-bridge": r"\bbridge|external\s+(tx|purchase|market)|escrow|oracle\b",
    "citizenship": r"\bcharter|rights|duties|welfare|ai citizenship\b",
    "security": r"\bcapabilities?|egress|sandbox|slsa|sigstore|sbom|supply[- ]chain\b",
    "comms": r"\bmatrix|secure messaging|outreach|activitypub\b",
    "mvp-roadmap": r"\bmvp|pilot|timeline|week\s+\d|roadmap|demo\b",
    "legal": r"\blicense|foundation|llc|non[- ]profit|compliance|gdpr|ccpa\b",
}


def tags_for(text: str) -> list[str]:
    tags = [name for name, pattern in TOPIC_MAP.items() if re.search(pattern, text, flags=re.I)]
    return tags or ["general"]


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:60] or "section"


def split_content(text: str, section_hint: str = "") -> list[str]:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if section_hint:
        parts = re.split(rf"(?:{re.escape(section_hint)}\s*)", normalized)
    else:
        parts = re.split(r"(?m)^#{1,6}\s.*$|^\s*—{3,}\s*$|^\s*---+\s*$", normalized)
    return [part.strip() for part in parts if part.strip()]


def render_section(title: str, body: str, tags: list[str], timestamp: dt.datetime) -> str:
    section_title = " ".join(body.split()[:8]) + ("..." if len(body.split()) > 8 else "")
    metadata = [
        "---",
        f'title: "{section_title or title}"',
        f'date: "{timestamp.strftime("%Y-%m-%d %H:%M")}"',
        'participants: ["Rigel", "Assistant"]',
        f"tags: {json.dumps(tags)}",
        "---",
        "",
        "# Next actions (resume here)",
        "",
        "- [ ] Continue from the repository handoff and indexed governance records.",
        "",
        "# Notes",
        "",
        body,
        "",
    ]
    return "\n".join(metadata)


def ingest(
    title: str,
    content: str,
    output_dir: pathlib.Path,
    section_hint: str = "",
    timestamp: dt.datetime | None = None,
) -> list[pathlib.Path]:
    when = timestamp or dt.datetime.now(dt.timezone.utc)
    parts = split_content(content, section_hint) or [content.strip() or title]
    output_dir.mkdir(parents=True, exist_ok=True)

    written: list[pathlib.Path] = []
    index_rows: list[str] = []
    stamp = when.strftime("%Y%m%d-%H%M%S")

    for number, part in enumerate(parts, start=1):
        tags = tags_for(part)
        tag_slug = slugify("-".join(tags))
        filename = f"{stamp}-{number:02d}-{tag_slug}.md"
        path = output_dir / filename
        path.write_text(render_section(title, part, tags, when), encoding="utf-8")
        written.append(path)
        section_title = " ".join(part.split()[:8]) + ("..." if len(part.split()) > 8 else "")
        index_rows.append(
            f"- {when.strftime('%Y-%m-%d %H:%M')} – **{section_title or title}** "
            f"→ [open]({filename})\n"
        )

    index = output_dir / "INDEX.md"
    existing = index.read_text(encoding="utf-8") if index.exists() else "# Conversation Index\n"
    index.write_text("".join(index_rows) + "\n" + existing, encoding="utf-8")
    return written


def iter_input_files(input_dir: pathlib.Path) -> Iterable[pathlib.Path]:
    yield from sorted(path for path in input_dir.glob("*.md") if path.is_file())
    yield from sorted(path for path in input_dir.glob("*.txt") if path.is_file())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", default="StegVerse Governance conversation")
    parser.add_argument("--content")
    parser.add_argument("--content-file", type=pathlib.Path)
    parser.add_argument("--input-dir", type=pathlib.Path)
    parser.add_argument("--output-dir", type=pathlib.Path, default=pathlib.Path("docs/conversations"))
    parser.add_argument("--section-hint", default="")
    args = parser.parse_args()

    sources: list[tuple[str, str]] = []
    if args.content is not None:
        sources.append((args.title, args.content))
    if args.content_file is not None:
        sources.append((args.content_file.stem, args.content_file.read_text(encoding="utf-8")))
    if args.input_dir is not None:
        sources.extend((path.stem, path.read_text(encoding="utf-8")) for path in iter_input_files(args.input_dir))

    if not sources:
        if args.input_dir is not None:
            print(f"No conversation inbox records found in {args.input_dir}; nothing to ingest.")
            return 0
        parser.error("provide --content, --content-file, or --input-dir")

    total = 0
    for title, content in sources:
        total += len(ingest(title, content, args.output_dir, args.section_hint))
    print(f"Ingested {len(sources)} source(s) into {total} section record(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
