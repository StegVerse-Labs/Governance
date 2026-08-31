# Universal Governance External-System Adapter Contract

The adapter is the only system-specific software required by the Universal Governance Connector architecture.

It translates a native action boundary into the canonical registered Governance request and translates the returned governance decision into a candidate for a separately-authorized target consequence.

```text
native action
  -> thin adapter
  -> registered Governance profile
  -> Interlock/InTr
  -> StegCore evaluation
  -> ALLOW / DENY / FAIL-CLOSED
  -> thin adapter
  -> separate consequence authority
  -> target consequence
```

The adapter is not a governance engine and does not contain policy logic.

## Required invariants

```text
adapter != governance authority
adapter != credential authority
adapter != execution authority
ALLOW != execute
unknown native operation -> FAIL_CLOSED
missing consequence authority -> FAIL_CLOSED
missing required evidence -> FAIL_CLOSED
ENFORCED + bypass_path_declared=true -> invalid adapter
ENFORCED requires bypass evidence
credential authority = TV/TVC
authority_effect = NONE
```

## Enforcement claim

`OBSERVABLE`, `GOVERNED`, and `ENFORCED` describe the deployment boundary, not merely source capability.

An adapter may declare `ENFORCED` only when:
- its Governance connector profile also declares `ENFORCED`;
- no admitted protected-consequence bypass exists;
- bypass-negative-control evidence is available;
- the live deployment is separately observed before any activation claim.

Source validation cannot establish live ENFORCED activation.


## Exact candidate hash

The external adapter uses `stegverse.external-native-action-candidate.v1`.

Before requesting Governance, it canonicalizes:

```json
{
  "candidate_ref": "<stable native candidate reference>",
  "native_operation": "<native operation>",
  "parameters": {}
}
```

and binds the SHA-256 digest into `candidate_hash` on the Governance request.

The exact hash must later match the StegGate deterministic execution request. This closes the parameter-substitution gap between governance admission and target consequence.

```text
candidate identity != exact candidate state
candidate_ref + candidate_hash are both required
hash binding != authority
```
