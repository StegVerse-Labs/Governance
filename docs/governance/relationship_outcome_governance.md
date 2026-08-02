# Relationship and Outcome Governance Layer

## Purpose

StegVerse must govern not only whether an action is authorized, evidenced, and admissible, but also whether the interaction posture can recruit, preserve, and coordinate the relationships required to reach the declared outcome.

A technically successful signal can still be outcome-negative when its framing repels the people, institutions, collaborators, or communities needed for continuation. Visibility, ranking, proof, and correctness are therefore not sufficient measures of success.

## Governed distinction

The layer separates:

1. **attention success** — the message, artifact, or claim becomes visible;
2. **relationship effect** — the interaction increases or decreases trust, participation, reciprocity, and willingness to continue;
3. **outcome direction** — the observed effect moves the system toward or away from the declared goal;
4. **continuation capacity** — the work can proceed without depending on one person's memory, persuasion, or manual follow-up.

A high-attention result that predictably damages the declared outcome must not be recorded as an unqualified success.

## Required commitment fields

Every governed outreach, collaboration, public framing, or participation campaign should declare:

- `declared_goal`
- `target_participants`
- `desired_relationship_state`
- `framing_posture`
- `participation_cost`
- `expected_constructive_effect`
- `known_repulsion_risks`
- `observation_signals`
- `repair_path`
- `continuation_owner`
- `completion_evidence`

## Decision states

- `ALLOW` — framing and execution are compatible with the declared outcome and preserve a credible participation path.
- `ALLOW_WITH_OBSERVATION` — the action may proceed, but relationship effects must be measured against named signals.
- `REPAIR_REQUIRED` — the action may be technically valid but its posture is likely to damage participation or invert the stated outcome.
- `DENY` — the action's expected relationship effect is materially inconsistent with the declared goal and no bounded repair path exists.

## Core invariants

1. Positive outcome attribution is evaluated by its effect on the declared outcome, not merely by rank, reach, or sentiment label.
2. Negative attribution may be legitimate evidence, but it cannot be counted as constructive outcome success without evidence that it improves the target state.
3. Collaboration cannot be represented as active when no observable invitation, response channel, ownership boundary, or continuation path exists.
4. A task cannot remain indefinitely marked `external`; it must be converted into an observable repository task, a bounded dependency watch, or a documented impossibility receipt.
5. Relationship repair must preserve truth. Constructive framing does not require suppressing adverse evidence.
6. No participant receives execution authority merely by being invited, persuasive, popular, or aligned.

## Operational task loop

The repository-resident task registry and runner implement the continuation mechanism:

1. discover tasks from `automation/governance_task_registry.json`;
2. validate ownership, destination, prerequisites, and completion evidence;
3. execute tasks whose mode is `repository_command` and whose prerequisites are satisfied;
4. observe tasks whose mode is `evidence_watch`;
5. emit a machine-readable status receipt;
6. fail closed when a task has no destination, no observable completion condition, or an unsupported external-only dependency.

This converts "someone needs to do something" into a path, command, evidence condition, and repository owner.

## Activation boundary

This layer is active when:

- its architecture is repository-resident;
- all active tasks name an organization, repository, path, execution mode, and completion condition;
- the task observer runs automatically on push, pull request, and schedule;
- unsupported external-only tasks fail validation rather than halting silently;
- status receipts identify blocked, ready, running, completed, and invalid tasks;
- completed tasks retain evidence sufficient for independent reconstruction.
