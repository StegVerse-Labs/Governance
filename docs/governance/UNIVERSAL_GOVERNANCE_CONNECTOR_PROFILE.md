# Universal Governance Connector Profile

Status: canonical implementation candidate

## Purpose

The Universal Governance Connector Profile composes existing StegVerse governance and transport primitives so a system can be governed at an enforceable Interlock/InTr boundary without embedding bespoke StegVerse governance logic inside the target system.

It does not introduce a new governance engine.

```text
target system
  -> system-specific thin adapter
  -> Interlock ingress
  -> governed InTr packet
  -> Universal Governance Connector Profile
  -> StegCore three-layer evaluator
  -> governance disposition receipt
  -> Interlock egress
  -> separately-authorized target consequence
  -> post-consequence observation / reconstruction
```

## Existing canonical components

The profile binds existing ecosystem contracts:

- Governance G0-G6 classes and A0-A8 admissibility stages;
- Judgment / Signal Admission / Execution Boundary three-layer model;
- StegGate `steggate.transition.v1` and its `profile_ref`;
- Universal Interlock `policy_or_profile_ref`, `authority_ref`, endpoint identities and receipt semantics;
- Universal InTr transport profile;
- canonical HB-derived InTr carrier;
- `stegcore.three_layer.evaluate_three_layer`;
- Governance-Chain Certification INT authority-separation and reconstruction expectations.

## What varies per system

A connector profile declares only the system-specific variable surface:

```text
system identity
boundary identity
operation classes
policy refs
required governance classes
required admissibility stages
authority/evidence requirements
reversibility
protected consequence classification
enforcement class
bypass disposition
evidence/custody requirements
```

The governance engine, InTr semantics, Interlock semantics, carrier semantics, receipt model, and authority separations remain canonical.

## Enforcement classes

### OBSERVABLE

The connector can observe or report actions, but the target may retain alternate action paths.

### GOVERNED

The declared protected action path requires a valid governance disposition at the connector boundary.

### ENFORCED

The protected consequence has no admitted bypass path around the connector.

A profile MUST NOT claim `ENFORCED` while `bypass_path_declared=true`.

## Decision semantics

The v1 runtime evaluator surface is deliberately narrow:

```text
ALLOW
DENY
FAIL-CLOSED
```

`ALLOW` means the governance evaluator found the transition admissible under the supplied resolved facts and current policy boundary. It does not mint credentials and does not itself execute the target action.

```text
ALLOW != credential authority
ALLOW != consequence execution
ALLOW != continuity receipt
ALLOW != custody
```

A separately authorized consequence layer remains required.

## Fail-closed requirements

The connector fails closed for a protected operation on:

- unknown profile or unsupported profile version;
- unknown operation;
- Interlock/InTr/profile binding mismatch;
- missing required authority reference;
- missing required evidence reference;
- missing or stale policy/delegation/evidence facts;
- signal/state reconstruction failure;
- reference-state drift;
- invalid or unknown execution recoverability;
- bypass attempt for a GOVERNED or ENFORCED protected operation.

## External-system integration rule

A target system can use the universal connector if its protected action surface can be represented by a thin adapter that:

1. creates the governed transition candidate;
2. binds the candidate to Interlock/InTr;
3. supplies already-resolved governance facts/evidence references;
4. refuses protected consequence execution unless the configured governance path succeeds;
5. preserves separate execution authority;
6. returns consequence evidence through Interlock/InTr.

The adapter translates the system API. It does not become the governance engine.

## Relationship to StegGate protocol

The connector does not replace `steggate.transition.v1`. The operation profile references the governed-transition profile and supplies the system-specific mapping required to construct/evaluate it.

## Relationship to Universal Interlock/InTr

Interlock/InTr remains transport and boundary infrastructure. The connector profile determines which governance semantics apply to a packet at the boundary.

```text
transport != governance authority
profile != authority
translation != permission
receipt != execution authority
```

## Relationship to Master Records

Master Records may receive the decision/transport/consequence evidence chain for reconstruction when the profile requires it. Custody remains non-authorizing.

## V1 runtime owner

Governance owns this profile schema and its invariants.

StegCore owns the generic runtime adapter that validates the profile/request binding and invokes `stegcore.three_layer.evaluate_three_layer`.

## Activation boundary

Source/schema validation does not prove that an external system is ENFORCED. A production ENFORCED claim additionally requires evidence that the target system has no admitted alternate protected consequence path and that real requests cannot bypass the governed boundary.
