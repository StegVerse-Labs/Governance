# Governance Classes and Admissibility Stages

Status: canonical conceptual taxonomy candidate

Authority boundary: this document classifies governance and admissibility functions. It does not grant execution authority, mint continuity, establish legal standing, or replace repository-specific policy, delegation, validation, or runtime controls.

## Purpose

StegVerse uses governance, admissibility, continuity, and reconstruction as related but distinct functions.

```text
governance defines the control structure
admissibility evaluates a transition within that structure
continuity determines what survived the transition
reconstruction establishes why that conclusion is warranted
```

A transition must not be described as simply "governed" or "admissible" when only one layer has been evaluated.

## Governance classes

### G0 — Descriptive governance

Defines the governed entity, present state, declared identity, capabilities, dependencies, boundaries, and claimed continuity thread.

G0 creates no authority. It establishes the object and context of governance.

### G1 — Normative governance

Defines the applicable constitution, policy, invariants, constraints, prohibited transitions, and required outcomes.

G1 states what should be permitted or prohibited. It does not prove that a particular actor may apply or alter those rules.

### G2 — Authority governance

Determines standing to propose, review, approve, refuse, override, delegate, revoke, or execute a transition.

Relevant properties include role, scope, jurisdiction, consent, quorum, delegation, expiration, revocation, and conflict of interest.

```text
approval != authority
participation != standing
visibility != jurisdiction
```

### G3 — Procedural governance

Defines the process by which a decision must be formed, challenged, escalated, recorded, and resolved.

A substantively reasonable result may remain procedurally inadmissible.

### G4 — Runtime governance

Evaluates the proposed transition against current state, current policy, current delegation, current evidence, and environmental constraints at the execution boundary.

```text
valid when proposed != valid when committed
```

### G5 — Continuity governance

Determines whether the resulting state remains an admissible successor in the same continuity thread.

Execution success does not establish continuity preservation.

### G6 — Recovery governance

Controls rollback, quarantine, fork recognition, remediation, succession review, authority restoration, and operation under degraded human or machine authority.

A boundary is not fully admissible merely because it is maintainable while the operator and system remain coherent. Recovery and authority degradation must also be governed.

## Admissibility stages

Let a transition candidate be:

\[
T:S_i\rightarrow S_{i+1}
\]

The transition receives a stage vector rather than one undifferentiated label:

\[
\mathbf{A}(T)=(a_0,a_1,a_2,a_3,a_4,a_5,a_6,a_7,a_8)
\]

Each element records `PASS`, `FAIL`, `UNKNOWN`, `NOT_RUN`, or another schema-defined state.

### A0 — Formation admissibility

Is the candidate well formed and bound to identifiable states, actors, policy references, evidence references, and declared intent?

Malformed candidates are not eligible for later promotion.

### A1 — Structural admissibility

Does the proposed successor preserve the required invariant projection?

\[
\pi_I(S_i)=\pi_I(S_{i+1})
\]

Literal state equality is not required. Preservation of the designated invariant set is required.

### A2 — Causal admissibility

Can the successor legitimately be derived from the predecessor through the claimed transformation?

Functional resemblance is insufficient. A replacement state may look correct while belonging to another continuity thread.

### A3 — Evidentiary admissibility

Is the evidence sufficient, attributable, current, integrity-protected, and appropriate to support the claimed transition?

A true proposition can remain inadmissible when it cannot be adequately established.

### A4 — Authority admissibility

Did every actor exercise valid standing within scope at the relevant time?

This stage checks delegation, consent, role, jurisdiction, quorum, expiration, and revocation.

### A5 — Procedural admissibility

Were all required review, challenge, sequencing, notice, refusal, and escalation procedures satisfied?

Authorized actors cannot silently bypass required process.

### A6 — Commit-time admissibility

Do all necessary conditions remain valid immediately before execution?

\[
\operatorname{Adm}_{t_c}(T,S_i,E,\Pi,\Gamma)=1
\]

Policy drift, state drift, revoked delegation, expired evidence, or changed environmental conditions may invalidate a previously approved transition.

### A7 — Continuity admissibility

After execution, does the observed successor remain in the same governed continuity thread?

\[
\mathcal{C}(S_{i+1})=\mathcal{C}(S_i)\oplus T
\]

This stage is evaluated against the actual resulting state, not merely the intended result.

### A8 — Reconstruction admissibility

Can a qualified independent observer reconstruct the decision, evidence, authority, procedure, execution boundary, result, and continuity determination?

Replay alone is insufficient when policy, delegation, state, or evidence must be independently reconstructed.

## Combined transition result

A transition is fully admissible only when every required stage for its authority class passes:

\[
\operatorname{Adm}(T)=\bigwedge_{k\in R(T)} a_k
\]

where `R(T)` is the stage set required for that transition class.

The stage vector must be retained even when an aggregate result is emitted.

Example:

```json
{
  "transition_id": "example-001",
  "aggregate": "DENY",
  "stages": {
    "A0_formation": "PASS",
    "A1_structural": "PASS",
    "A2_causal": "PASS",
    "A3_evidentiary": "PASS",
    "A4_authority": "PASS",
    "A5_procedural": "PASS",
    "A6_commit_time": "FAIL",
    "A7_continuity": "NOT_RUN",
    "A8_reconstruction": "NOT_RUN"
  },
  "reason": "delegation revoked before commit"
}
```

The `DENY` result does not erase the completed stage evidence.

## Failure dispositions

Failure of continuity or admissibility must not be collapsed into one generic error. Permitted dispositions include:

- `DENY` — execution prohibited before commit;
- `CORRUPT` — execution occurred but resulting state or evidence is invalid;
- `REPLACEMENT` — successor does not belong to the claimed continuity thread;
- `FORK` — multiple successor claims remain independently live;
- `QUARANTINE` — state retained without promotion pending review;
- `UNKNOWN` — evidence is insufficient for a defensible determination.

## Multi-perspective evaluation

Admissibility may differ across bounded observational or jurisdictional regions:

\[
\operatorname{Adm}_{R_a}(T)=1,\qquad
\operatorname{Adm}_{R_b}(T)=0
\]

A disagreement is not automatically a defect. It may be necessary evidence defining incompatible authority, policy, evidence, or state constraints.

The system must preserve those region-specific results rather than forcing artificial consensus.

## Minimal machine-readable record

A conforming record should identify at least:

```text
transition_id
pre_state_ref
post_state_ref
transformation_ref
governance_classes_invoked
required_admissibility_stages
stage_results
policy_refs
delegation_refs
evidence_refs
commit_time
observer_or_reconstructor_refs
aggregate_result
failure_disposition
continuity_result
```

## Presentation sequence

This taxonomy supports a modular teaching and publication sequence:

1. State, change, and identity
2. Continuity threads
3. Structural invariants
4. Governance classes
5. Admissibility stages
6. Authority, standing, and consent
7. Evidence and causal reconstruction
8. Procedural governance
9. Commit-time admissibility
10. Execution and continuity verification
11. Forks, replacement, corruption, and quarantine
12. Recovery under degraded authority
13. Multi-entity and multi-perspective governance
14. Receipts, replay, and independent reconstruction
15. Operational implementation

## Integration boundary

Canonical architecture and schema ownership remain in `StegVerse-Labs/Governance`.

Possible downstream publication or implementation targets, only after their current handoffs permit mutation, include:

```text
StegVerse-Labs/admissibility-wiki
GCAT-BCAT-Engine/Publisher
StegVerse-Labs/Site
StegVerse-002/stegguardian-wiki
StegVerse-Labs/StegCore
```

Propagation must preserve the distinction between conceptual taxonomy, validator implementation, runtime enforcement, public explanation, and independent evidence.
