# TRACE Signal Bundle (Governance Input Contract)

## Purpose

A **TRACE Signal Bundle** is the **only** TRACE-derived artifact that Governance may evaluate.

It is:
- **Bounded** (structured fields only; no raw evidence embedded)
- **Non-authoritative** (does not assert truth)
- **Confidence-scored** (explicit uncertainty)
- **Auditable** (references evidence via IDs/links/hashes, not contents)

Governance consumes TRACE Signal Bundles to make decisions like:
- `require_review` when confidence is low or provenance is unclear
- `deny` when risk is high
- `allow` only when policy permits and verified receipts exist (via StegID)

---

## Non-goals

TRACE Signal Bundles are NOT:
- legal conclusions
- identity verification
- cryptographic verification
- a substitute for StegID continuity receipts
- a container for raw documents, testimony, screenshots, or rumor dumps

---

## Hard Rules (must)

1. **No raw evidence embedded**
   - No full text, images, PDFs, dumps, or message contents.
   - Only bounded references: URLs, doc IDs, hashes, case IDs, archive IDs.

2. **Confidence is explicit**
   - Every signal MUST include a `confidence` score in `[0, 1]`.

3. **Counter-signals allowed**
   - Bundles may include structured counterpoints to reduce bias and prevent “one-way” narratives.

4. **Non-retroactive interpretation**
   - New evidence produces a **new bundle** (and thus a new GDR), not edits to history.

---

## Canonical JSON Shape (v1.0)

A bundle MUST conform to:
- `schemas/trace_signal_bundle.schema.json`

Top-level fields:

- `bundle_version` (must be `"1.0"`)
- `bundle_id` (unique)
- `produced_at` (epoch seconds)
- `subject` (type + id; optional display label)
- `signals[]` (1..N)
- `trace` (optional correlation metadata)

---

## Signal Item Requirements

Each signal MUST include:

- `signal_id`
- `signal_type`
- `confidence` (0..1)
- `summary` (human-readable)
- `evidence_refs[]` (bounded references)

Optional:
- `labels[]`
- `counter_signals[]`
- `limits{...}`

**Interpretation guidance:**
- A high confidence score indicates TRACE believes the signal is robust **given referenced evidence**.
- It does **not** mean “true,” “proven,” or “legally established.”

---

## Evidence References

Evidence refs are **pointers**, not payloads.

Each ref:
- `ref_type`: `url | citation | doc_id | hash | case_id | archive_id`
- `ref_id`: identifier value
- `notes`: optional short clarification

**Privacy rule:** Do not embed personal private identifiers or secrets.

---

## Example Bundle

```json
{
  "bundle_version": "1.0",
  "bundle_id": "tsb_2025_12_28_0001",
  "produced_at": 1766900000,
  "subject": {
    "subject_type": "artifact",
    "subject_id": "sha256:abc123...",
    "display_name": "Envelope + Card"
  },
  "signals": [
    {
      "signal_id": "sig_001",
      "signal_type": "provenance_gap",
      "confidence": 0.62,
      "summary": "Chain-of-custody details are incomplete in the public release; provenance cannot be confirmed from available pointers.",
      "evidence_refs": [
        { "ref_type": "url", "ref_id": "https://example.org/release-index", "notes": "Public document index entry" }
      ],
      "counter_signals": [
        { "summary": "Envelope appears to have a postal mark consistent with a real mail stream, but origin remains uncertain.", "confidence": 0.44 }
      ],
      "limits": {
        "non_authoritative": true,
        "not_legal_advice": true,
        "not_identity_verification": true
      }
    }
  ],
  "trace": {
    "correlation_id": "c_01HXYZ...",
    "request_id": "req_2025_12_28_09"
  }
}
