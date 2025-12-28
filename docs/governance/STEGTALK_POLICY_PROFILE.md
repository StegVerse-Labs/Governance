# StegTalk Policy Profile (Governance View)

## Purpose

This document expresses StegTalk security tier behaviors as governance-enforceable constraints.

StegCore uses these rules to gate StegTalk actions.

---

## Core invariants (all tiers)

- E2EE required for payload
- Integrity checks required (MAC/AEAD)
- Replay protection required (droplet_id or MAC prefix LRU/Bloom)
- No unauthenticated receipts
- Deterministic policy decisions for given inputs

---

## Tier 1 — Minimum StegVerse Security

Allowed:
- single bearer delivery
- authenticated receipts

Constraints:
- no receipts that disclose bearer/network specifics
- no stable sender identifiers unless explicitly configured

---

## Tier 2 — Strong Privacy (recommended default)

Preferred:
- ≥2 bearers when available

Required:
- enforce per-bearer safety when multi-bearer used: `c_i <= k - 1`
- timing jitter and batching enabled (within configured bounds)
- padding buckets enabled for payload sizes when configured

Receipts:
- coarse and channel-agnostic (`ASSEMBLED`, `NEED_MORE`)
- no “channel health” claims

---

## Tier 3 — Maximum Privacy

Preferred:
- ≥3 independent bearers when available (cap configurable)
- receiver-discovery supported (no plaintext receiver ID)

Required:
- `c_i <= k - 1` for all bearers used
- optionally enforce subset constraint for small bearer subsets when required by policy
- strong padding buckets + jitter (more aggressive than Tier 2)
- **no explicit channel-oracle feedback**
  - receiver does not send “channel X blocked”
  - sender adapts via local inference and coarse receipts only

Optional (user-controlled):
- micro-cover traffic
- dead-drop pull scheduling

---

## Governance decisions

StegCore should implement decisions such as:

- `CAN_SEND(...)`:
  - deny if required continuity receipts missing
  - require_review if confidence indeterminate
  - allow_with_constraints to force Tier 3 or disable certain bearers

- `CAN_ACK(...)`:
  - deny for Tier 3 oracle-dangerous receipt types

- `CAN_STORE(...)`:
  - enforce retention caps for Tier 3
