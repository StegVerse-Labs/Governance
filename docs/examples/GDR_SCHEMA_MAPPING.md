# GDR Schema Mapping Notes

## Purpose

This note maps the new example Governance Decision Records to the existing Governance Decision Record concept without requiring prior chat context.

## Example fixtures

- `docs/examples/fixtures/dual_quorum_gdr.json`
- `docs/examples/fixtures/drift_review_gdr.json`

## Field mapping

| Example field | Meaning | Target schema consideration |
| --- | --- | --- |
| `gdr_id` | Stable decision record identifier | Map to GDR id field. |
| `proposal_id` | Governance proposal being evaluated | Map to evaluated input reference. |
| `policy_version` | Policy draft or resolver version | Map to policy/version field. |
| `decision` | Governance result | Must remain bounded to accepted GDR decision vocabulary. |
| `inputs` | Structured evidence summary | Should reference verified input IDs when implementation is wired. |
| `rationale` | Human-readable explanation | Map to rationale/reasons field. |
| `constraints` | Required limits or next checks | Map to constraints/machine hints. |
| `next_step` | Non-binding workflow hint | Keep advisory unless schema explicitly supports workflow transition. |

## Next implementation step

After validation passes, compare fixtures against `schemas/gdr.schema.json` and either:

1. adjust fixtures to match the existing schema exactly; or
2. define an examples-only draft schema under `docs/examples/fixtures/`.

## Rule

Examples must not expand execution authority. They only demonstrate governance reasoning and review boundaries.
