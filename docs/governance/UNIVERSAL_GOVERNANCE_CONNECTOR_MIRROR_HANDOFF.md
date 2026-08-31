# Universal Governance Connector Mirror Handoff

Updated: 2026-08-31
Repository: StegVerse-Labs/Governance
Issue: #26
Branch: feature/universal-governance-connector
State: SOURCE_IMPLEMENTATION_IN_PROGRESS
Authority effect: NONE
Execution authority: NONE
Credential authority: TV/TVC

## Goal

Create the canonical profile-driven composition layer that allows an arbitrary internal or external system to place an enforceable action boundary behind StegVerse Interlock/InTr without embedding bespoke StegVerse governance logic in that system.

## Existing canonical pieces to reuse

This lane MUST compose rather than replace:

```text
Governance:
  G0-G6 governance classes
  A0-A8 admissibility stages
  judgment / signal-admission / execution-boundary architecture

ara-admissibility-interop:
  steggate.transition.v1
  profile_ref
  authority_ref
  intent_ref
  evidence_refs

StegOS Universal Interlock:
  policy_or_profile_ref
  authority_ref
  source/destination endpoint identities
  InTr packet/receipt transport semantics

StegCore:
  stegcore.three_layer.evaluate_three_layer
  deterministic ALLOW / DENY / FAIL-CLOSED runtime result

admissibility-wiki certification:
  INT governed-interlock evidence/authority-separation properties
```

## Missing composition layer

Before this issue, no canonical artifact binds these pieces into one reusable per-system profile.

The missing object is:

```text
SYSTEM
  -> governance connector profile
  -> Interlock ingress
  -> governed InTr packet
  -> canonical Governance/StegCore evaluator
  -> governance disposition receipt
  -> Interlock egress
  -> SYSTEM consequence boundary
```

## Connector-profile responsibilities

A profile declares, but does not itself authorize:

- system identity and boundary identity;
- admitted operation classes;
- mapping from operation to Governance classes and admissibility stages;
- StegGate governed-transition profile reference;
- StegCore evaluator reference;
- Interlock/InTr profile reference;
- policy reference requirements;
- authority-reference requirements;
- evidence requirements;
- consequence/reversibility classification;
- bypass behavior;
- decision/receipt requirements;
- post-consequence observation/reconstruction requirements.

## Mandatory invariants

```text
transport != governance authority
Interlock != governance authority
InTr packet != governance decision
profile declaration != execution authority
governance ALLOW != credential authority
governance ALLOW != consequence execution by itself
HB / derived carrier != governance authority
Master Records custody != governance authority
verification != authority
successful translation != permission
unknown operation -> FAIL_CLOSED
missing required profile/policy/authority/evidence -> FAIL_CLOSED
bypass of an ENFORCED operation -> FAIL_CLOSED
```

TV/TVC remains credential authority.

## Enforcement classes

```text
OBSERVABLE
  packets/evidence may be observed but protected consequence may have alternate paths

GOVERNED
  protected consequence requires a governance disposition at the declared boundary

ENFORCED
  protected consequence has no admitted bypass path around the governed boundary
```

A profile MUST NOT claim ENFORCED unless its adapter/deployment can actually prevent alternate consequence paths.

## Ownership boundary

```text
Governance
  connector-profile schema, invariants, fixtures, validator, release semantics

StegCore
  generic runtime connector implementation and runtime receipts

StegOS / Interlock / InTr
  packet movement and boundary transport

TV/TVC
  credential authority

target-system adapter
  system-specific translation and consequence invocation under its own authority

Master Records
  custody/reconstruction only
```

## Planned source surfaces

```text
docs/governance/UNIVERSAL_GOVERNANCE_CONNECTOR_PROFILE.md
schemas/universal_governance_connector_profile.schema.json
fixtures/universal-governance-connector/profile.example.json
scripts/validate_universal_governance_connector_profile.py
.github/workflows/universal-governance-connector.yml
```

## Lifecycle

```text
IMPLEMENTED: IN_PROGRESS
VALIDATED: false
MERGED: false
STEGCORE_RUNTIME_ADAPTER: false
CROSS_REPO_CONTRACT_VALIDATED: false
LIVE_EXTERNAL_ENFORCED_SYSTEM: false
ACTIVATED: false
COMPLETE: false
```


## Canonical InTr request contract — issue #28

The connector payload is now explicitly serialized as:

```text
schema: stegverse.governance-connector.request/v1
schema file: schemas/universal_governance_connector_request.schema.json
fixture: fixtures/universal-governance-connector/request.example.json
InTr profile: governance-external-action
```

Transport-owned values such as the Interlock exchange id, InTr packet id, hop receipts, and HB-derived carrier signal are not self-asserted by this payload. They are supplied/verified by the transport boundary.

The payload carries only the per-transition governance candidate and already-resolved facts required by the canonical StegCore three-layer evaluator.


## Canonical profile registry — issue #30

The reusable Governance connector now has an explicit discovery/selection surface:

```text
schema: stegverse.governance-connector-registry.v1
schema file: schemas/universal_governance_connector_registry.schema.json
registry: specs/universal-governance-connector-profiles.v1.json
credential_authority: TV/TVC
authority_effect: NONE
```

The registry contains exact connector-profile objects. `profile_id` values must be unique. Each embedded profile is validated by the existing connector-profile validator. Unknown profile selection fails closed.

The first entry is the already-validated `example.external-system.v1` profile. Registry validation requires that entry to remain semantically identical to the canonical profile fixture rather than becoming an independently drifting copy.

```text
registry discovery != governance authority
profile lookup != policy decision
registered != activated
registered != ENFORCED deployment
unknown profile -> FAIL_CLOSED
```

StegCore is the runtime consumer and should resolve profiles by `profile_id` from a pinned Governance registry snapshot rather than application-specific hard coding.


## Thin external-system adapter contract — issue #32

The remaining per-system variable implementation is now formalized as:

```text
schema: stegverse.governance-external-adapter.v1
schema file: schemas/universal_governance_external_adapter.schema.json
fixture: fixtures/universal-governance-connector/external-adapter.example.json
validator: scripts/validate_universal_governance_external_adapter.py
```

The adapter binds a native system operation to a registered Governance operation and declares native input/evidence mapping. It contains no governance policy.

Protected consequences require a separate consequence authority reference. Governance `ALLOW` makes a candidate eligible for that separate authority check; it does not execute the consequence.

```text
adapter != governance engine
adapter != execution authority
adapter != credential authority
ALLOW != consequence execution
ENFORCED + bypass -> invalid
ENFORCED source contract != live ENFORCED observation
credential authority = TV/TVC
authority_effect = NONE
```

The reference adapter claims `ENFORCED` at source-contract level only and includes bypass-negative-control evidence references. Live ENFORCED activation remains unclaimed until a real deployed target boundary proves the protected consequence cannot bypass the governed path.
