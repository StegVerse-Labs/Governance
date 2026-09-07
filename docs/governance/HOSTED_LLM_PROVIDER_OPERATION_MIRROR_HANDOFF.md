# Hosted LLM Provider Operation Governance Mirror Handoff

Updated: 2026-09-06
Repository: `StegVerse-Labs/Governance`
Issue: `#38`
Branch: `feat/hosted-provider-governance-38`

## Goal

Close the governance-profile gap for optional hosted LLM provider operations without moving provider-specific policy, credentials, transport, execution, or custody into Governance.

## Canonical profile

```text
profile_id: hosted-llm-provider-operation.v1
system_id: external-provider.hosted-llm
boundary_id: interlock:hosted-llm-provider-operation
enforcement_class: GOVERNED
operation_id: execute-provider-operation
action_class: EXECUTE
policy_ref: policy.hosted-llm-provider.execute.v1
intr_profile_ref: external-provider-operation
governed_transition_profile_ref: steggate.transition.v1
carrier_profile_ref: heartbeat-derived-intr.v1
evaluator: stegcore.three_layer.evaluate_three_layer
decisions: ALLOW / DENY / FAIL-CLOSED
credential_authority: TV/TVC
authority_effect: NONE
```

`GOVERNED` is intentional: source registration does not claim that all possible hosted-provider network paths are physically impossible to bypass. A particular deployed runtime may prove an enforced boundary separately; this profile does not pre-claim that fact.

## Composition

```text
provider-operation candidate
-> StegOS external-provider-operation exact-packet InTr transport
-> verified transport bindings
-> hosted-llm-provider-operation.v1 Governance profile
-> canonical StegCore three-layer evaluator
-> ALLOW / DENY / FAIL-CLOSED decision receipt
-> ALLOW means eligible for separate consequence authorization only
-> separately valid TV/TVC provider-operation lease
-> provider call
-> response transport / reconstruction
```

The governance decision cannot mint a TVC lease, resolve a provider credential, call Kimi/DeepSeek/etc., create a WorkerCoordinator claim/fence, or substitute for response/egress evidence.

## Fact-resolution boundary

`resolved_facts` in the Governance request must be derived from already-observed runtime evidence by the target-system adapter. A provider worker may not hard-code truthy facts merely to obtain ALLOW. For the Kimi resident proof, the admissible fact basis must include the current WorkerCoordinator task/claim/fence evidence, exact InTr ingress completion, the registered profile/policy binding, current evidence refs, and the separately issued TVC lease/validity window before consequence. Missing or stale evidence must map to DENY/FAIL-CLOSED.

## README impact determination

No root Governance README mutation is required for this profile registration. The existing Universal Governance Connector handoff and repository documentation already define the generic profile-driven arbitrary-system composition layer, decision surface, authority separation, evidence requirements, and TV/TVC credential boundary. This change instantiates that existing public contract for the hosted-LLM system class without changing the connector schema, evaluator, authority model, runtime prerequisite, failure semantics, or release semantics. If a user-facing hosted-provider governance API is added later, README impact must be re-evaluated.

## Validation requirements

- canonical registry schema remains valid;
- the reference example profile remains byte/semantic-equivalent to its fixture;
- every registered profile passes the existing profile validator;
- hosted profile binds `external-provider-operation` and the canonical StegCore evaluator;
- protected consequence remains fail-closed on bypass;
- all authority-transfer flags remain false;
- credential authority remains TV/TVC;
- unknown profile selection remains fail-closed.

## Runtime status

```text
source registration: IN_PROGRESS
StegCore runtime support: EXISTING_GENERIC_RUNTIME
Kimi resident consumer: PENDING
live governance decision: NOT_YET_OBSERVED
live Kimi activation: NOT_YET_PROVEN
```
