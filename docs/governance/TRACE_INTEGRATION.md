# TRACE Integration (Governance ↔ StegTrace)

## Purpose

This document defines how Governance (StegCore) consumes TRACE outputs without violating privacy or creating attribution/metadata leaks.

Governance uses TRACE to answer:

> “How confident should we be in the local signals that support a policy decision?”

Governance does **not** ask TRACE to identify people, infer authorship, or reveal network identifiers.

---

## Allowed TRACE inputs to Governance

TRACE MAY provide StegCore with:

- **Confidence vectors** for local artifacts (e.g., integrity_confidence, temporal_confidence)
- **Anomaly flags** (e.g., replay bursts, repeated integrity failures)
- **Calibration summaries** (“our estimates are unstable”)
- **Coarse channel health** at the *class* level (e.g., `ble`, `hbbl`, `wifi`) — **local only**

These inputs must be:
- local-first
- minimally identifying
- free of raw payload content

---

## Disallowed requests (must be denied)

StegCore MUST NOT request, and TRACE MUST NOT provide:

- raw message contents or decrypted payloads
- stable peer identifiers or device identifiers (unless explicit user consent and separate policy)
- precise timestamps that enable correlation across sessions
- bearer-specific network identifiers (SSID, BSSID, IPs, phone numbers, tower IDs, etc.)
- “which channel failed” explicit oracle signals in Tier 3 StegTalk mode

---

## How confidence affects decisions

StegCore may apply rules like:

- If `integrity_confidence` < threshold → `deny` or `require_review`
- If `temporal_confidence` is low (possible replay) → `deny`
- If `overall_confidence` is indeterminate → `require_review`
- If calibration is unstable → enforce stricter Tier / padding / reduced telemetry

TRACE is advisory; StegCore is the decision authority.

---

## Privacy defaults

- Metrics are **always on** locally.
- Sharing is **explicit, rare, and coarse**.
- No automatic export of TRACE data from governance.
