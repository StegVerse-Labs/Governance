# Dual Quorum Governance Decision Record Example

## Purpose

This example shows how a future Governance Decision Record (GDR) can represent a dual-quorum review without requiring prior chat context.

## Scenario

A proposed governance change requires both human quorum and AI quorum before it can be considered ratified.

## Inputs

```yaml
proposal_id: example-dual-quorum-001
policy_version: draft-0.1
change_class: C
human_quorum:
  threshold: 0.67
  observed: 0.72
ai_quorum:
  threshold: 0.67
  observed: 0.70
drift_score: 32
```

## Expected Governance Output

```yaml
gdr_id: gdr-example-dual-quorum-001
proposal_id: example-dual-quorum-001
decision: require_review
rationale:
  - human quorum met threshold
  - ai quorum met threshold
  - drift score below warning threshold
constraints:
  - produce signed review receipt
  - record policy version
  - preserve quorum evidence
next_step: eligible_for_ratification_review
```

## Notes

This example is not an implementation. It is a documentation bridge between the policy drafts and the existing Governance Decision Record model.
