# Drift Review Governance Decision Record Example

## Purpose

This example shows how a future Governance Decision Record can represent a drift-review condition before governance erosion becomes operationally dangerous.

## Scenario

Observed governance drift has crossed the review threshold. The system should not treat this as approval or rejection. It should produce a review decision with bounded next steps.

## Inputs

```yaml
proposal_id: example-drift-review-001
policy_version: draft-0.1
change_class: C
drift_score: 83
signals:
  quorum_participation_rate: 0.51
  outcome_divergence: 0.44
  equity_concentration: 0.62
```

## Expected Governance Output

```yaml
gdr_id: gdr-example-drift-review-001
proposal_id: example-drift-review-001
decision: require_review
rationale:
  - drift score reached review threshold
  - outcome divergence requires explanation
  - equity concentration requires distribution review
constraints:
  - delay major parameter changes until review completes
  - preserve drift signal snapshot
  - request dual-quorum review packet
next_step: produce_drift_review_packet
```

## Notes

This example is documentation-only. It should later be mapped to schema fields and test fixtures.
