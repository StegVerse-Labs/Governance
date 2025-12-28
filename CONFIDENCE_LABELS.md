# Confidence Labels (StegVerse Standard)

These labels standardize how StegVerse components (including TRACE, Governance, and downstream consumers) communicate certainty.

## Key rule

**Do not claim binary truth unless the system is operating on verified, cryptographically provable inputs.**

When uncertainty exists, express it.

---

## VERIFIED
High confidence supported by cryptographically verified inputs **or** strong independent corroboration with no material contradictions.

## STRONGLY SUPPORTED
Very likely accurate; strong evidence exists but not fully definitive.

## PLAUSIBLE
Consistent and supported by some evidence; meaningful gaps remain.

## INDETERMINATE
Insufficient evidence or mixed signals; cannot responsibly conclude.

## DISPUTED
Credible evidence exists in multiple directions; contradictions unresolved.

## INCONSISTENT
Conflicts with strong established evidence; likely incorrect unless new evidence emerges.

## LIKELY MISATTRIBUTED / MANIPULATED
Strong provenance or integrity failures; should not be relied upon as presented.

---

## Versioning and updates

When new evidence changes confidence:
- create a new evaluation record (do not overwrite history)
- document the reason for change and the signals that changed
