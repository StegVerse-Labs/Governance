# Metered Platform Replacement and Sovereign Infrastructure

## Purpose

This policy governs the identification, prioritization, replacement, and retirement of external platforms whose incremental, usage-based, seat-based, storage-based, transaction-based, or renewal-based billing materially burdens StegVerse operations.

The objective is not merely cost reduction. The objective is to reduce dependency, lock-in, data fragmentation, execution fragility, and externally imposed operating limits while preserving continuity during migration.

## Initial confirmed replacement targets

The initial dependency register includes:

- Render;
- PyPI and related package-distribution dependencies;
- GitHub;
- cloud storage and compute services;
- GoDaddy;
- additional recurring services not yet identified from financial records.

A named platform is a replacement candidate, not an immediate cancellation instruction.

## Governing principle

External platforms may be used as temporary carriers, adapters, mirrors, or transition infrastructure. They must not become permanent unexamined authorities over StegVerse identity, source, packages, deployment, storage, routing, receipts, governance, or continuity.

StegVerse-native replacements must favor:

1. predictable operating cost;
2. user and ecosystem control;
3. portable data and open formats;
4. local or federated execution where practical;
5. interoperable adapters during migration;
6. auditable custody and transition receipts;
7. fail-closed migration gates;
8. avoidance of recreating exploitative incremental billing inside StegVerse.

## Required dependency record

Every external dependency must be represented by a machine-readable record containing at least:

- service identity and category;
- current purpose;
- known billing model;
- known cost or `unknown` status;
- renewal or billing cadence;
- account owner or responsible organization where known;
- data, secrets, packages, workflows, domains, or deployments held by the service;
- lock-in and outage risk;
- replacement priority;
- proposed StegVerse destination;
- migration phase;
- cancellation blockers;
- evidence required before retirement.

Unknown cost is itself an actionable condition and must not be interpreted as zero cost.

## Replacement priority

Priority is determined from four factors:

1. financial drain;
2. operational criticality;
3. lock-in or migration difficulty;
4. sovereignty impact.

The highest-priority targets are services with high recurring cost, critical custody or execution roles, difficult export paths, or the ability to interrupt the ecosystem unilaterally.

## Migration phases

Each dependency progresses through these phases:

```text
DISCOVERED
-> COST_VERIFICATION
-> DEPENDENCY_MAPPED
-> REPLACEMENT_DESIGNED
-> PARALLEL_OPERATION
-> MIGRATION_VERIFIED
-> RETIREMENT_AUTHORIZED
-> RETIRED
```

No dependency may move directly from `DISCOVERED` to `RETIRED`.

## Retirement gates

A service may be retired only when all applicable gates pass:

- data export is complete and verified;
- secrets and credentials are rotated or revoked;
- DNS and domain records are preserved where applicable;
- packages and artifacts are mirrored or replaced;
- workflows and deployments have verified successors;
- rollback or recovery paths exist;
- downstream references are updated;
- required custody and continuity evidence exists;
- no unresolved billing, renewal, or account-ownership issue remains;
- a Governance Decision Record authorizes retirement.

Cancellation without these gates is prohibited because financial relief does not justify destroying continuity.

## Initial replacement map

| External platform | Current role | Initial StegVerse replacement direction |
|---|---|---|
| Render | application and service hosting | StegVerse deployment runtime with portable build and service manifests |
| PyPI | Python package distribution and dependency retrieval | governed package registry, signed mirrors, and reproducible package bundles |
| GitHub | source control, issues, CI, releases, packages, collaboration | federated StegVerse source forge with Git interoperability and governed mirrors |
| Cloud space | object storage, backups, databases, compute, or file synchronization | StegVerse storage, custody, backup, and compute fabric with quota transparency |
| GoDaddy | domain registration, renewals, and possibly DNS | governed domain portfolio, registrar portability, DNS custody, and renewal controls |
| Unknown recurring services | unresolved financial drain | statement and invoice discovery pipeline feeding the dependency register |

## Authority boundaries

The dependency register does not authorize cancellation.

A replacement design does not prove migration.

Parallel operation does not prove successor reliability.

Cost savings do not override custody, continuity, security, legal, contractual, or recovery requirements.

A platform marked `RETIREMENT_AUTHORIZED` is not retired until external billing and service termination are independently confirmed.

## Ecosystem integration

This workstream should eventually connect to:

- Master-Records for dependency, cost, migration, and retirement evidence;
- StegCore for policy evaluation and retirement decisions;
- Site for human-readable cost and migration status;
- Publisher for approved public declarations;
- admissibility-wiki for migration and retirement gate definitions;
- stegguardian-wiki for operational and recovery safeguards.

## Definition of activation

The workstream reaches initial activation when:

1. the dependency register is repository-resident and validator-enforced;
2. every known paid platform has a record;
3. unknown costs are explicitly tracked;
4. replacement priorities are computed or assigned;
5. no cancellation can be represented as complete without the required gates;
6. the first high-priority platform has a verified replacement design and migration plan.
