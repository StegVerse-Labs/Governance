# Metered dependency migration — Governance policy candidate
Status: SOURCE-ONLY DRAFT; no admitted new Goal Task ID or execution authority.
Recovery: Governance issue #46; historical PR #3 at `4932782a853629addd44fac1f30be77028bdff4b`.
Canonical collision owner: `ENTERPRISE-HOST-PROVIDER-ERADICATION-001` (Task Registry generation 213, ACTIVE; COSV `40000100100000`).
This policy is intentionally provider-neutral. It must not restore named third-party host assumptions, provider-specific workflows, deploy targets, credentials, or active platform inventory.

## Authority
Governance owns decision contracts and synthetic conformance fixtures. The Task Registry records work intent, not authorization; WorkerCoordinator owns execution claims, Interlock/InTr owns governed transitions, and Master Records owns evidence custody and reconstruction. Only a separately admitted, scoped GDR plus authentic required custody and migration evidence may authorize retirement. A repository fixture is never an issued decision or runtime receipt.

Selection for inventory, dependency mapping, successor design or preparation for parallel operation cannot cancel, retire, delete, revoke credentials, or cut over production traffic. A failed or missing gate is a denial; unknown cost is not zero.

## Required verified retirement gates
1. Asset and ownership inventory complete.
2. Data export independently verified.
3. Successor health verified at the actual consequence boundary.
4. Parallel operation passed with attributable results.
5. Rollback and restoration verified.
6. Credential rotation verified by its authorized owner.
7. Traffic cutover verified.
8. Master Records custody and reconstruction for the governing evidence recorded.
9. Separate retirement-scoped Governance Decision Record issued on verified inputs.

These gates apply to any provider. A source patch, CI pass or synthetic fixture does not satisfy them. Actual cancellation and account closure are independently recorded consequences and cannot be inferred from GDR issuance.

## Recovery boundary
The historical branch has 67 commits beyond its July merge base and overlaps 165 newer main commits at the generation-213 review. Its provider-specific workflows, invented priority assignments, and nominal financial figures are not carried forward. Existing native owner `ENTERPRISE-HOST-PROVIDER-ERADICATION-001` retains source removal; StegCore issue #26 retains runtime evaluator ownership. Other provider adapter, historical-export and billing discovery ideas require collision/owner disposition before implementation.
