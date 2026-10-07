# PRD: PyQuaticus Setup and Week 3 Environment Review

Status: FR-1 through FR-3 verified locally; teammate verification pending  
Created: October 7, 2026  
Updated: October 7, 2026  
Workstream: PyQuaticus and reinforcement learning  
Owners: Akshith Ambekar and Yahya Masri  
Project start: September 21, 2026  
Checkpoint: October 7–9, 2026  
Week 3 completion target: October 11, 2026

## 1. Purpose

Complete the initial PyQuaticus setup and environment investigation required by the proposal's first three weeks. Demonstrate existing agents running, document the game mechanics and observation/action interface, and contribute to the shared English → LTL → RL architecture.

By the October 7–9 checkpoint, setup and tutorial/sample-agent execution should be complete. The Rules Reference Document and shared architecture should have substantial drafts ready for review, with completion targeted for October 11.

This PRD defines expected work. Checklist items remain unchecked until supported by execution or review evidence.

## 2. Context and schedule authority

The project combines natural-language translation, LTL, and RL in maritime capture the flag. The proposal assigns the PyQuaticus/RL pipeline to Akshith and Yahya. Environment research and architecture are shared team tasks; this PRD defines the RL subgroup's contribution.

The proposal's embedded Gantt chart supplies week assignments. The team established September 21 as the project start, giving the following calendar mapping:

| Week | Dates | Proposal tasks | Expected state |
| --- | --- | --- | --- |
| W1 | September 21–27 | 1.1 Install/configure PyQuaticus | Complete before the checkpoint |
| W2 | September 28–October 4 | 1.2 Run MCTF tutorials/sample agents | Complete before the checkpoint |
| W3 | October 5–11 | 1.5 Study rules and observation/action spaces; 2.1 define architecture | Substantial drafts October 7–9; complete October 11 |
| W4 | October 12–18 | 2.2 Define structured LTL output | Follow-on shared task |
| W5 | October 19–25 | 4.1 Establish baseline agent control; 2.3/2.4 define interface and failure handling | Follow-on implementation and specification |
| W6–W7 | October 26–November 8 | 4.2 Define RL states, actions, and rewards | Follow-on learning design |

The earlier PRD bundled a custom runner and event logging into the first task. This revision assigns the baseline control script to W5 and treats detailed logging as proposed follow-on scope requiring agreement.

## 3. Users and needs

| User | Need |
| --- | --- |
| PyQuaticus/RL subgroup | A working simulator and an accurate understanding of its control interface. |
| LTL subgroup | Candidate game propositions, information-access limits, and integration responsibilities. |
| Team and sponsor | Reproducible demonstrations and evidence of progress against the schedule. |

## 4. Current scope

Included through W3:

- Isolated, working PyQuaticus environments for Akshith and Yahya.
- Documented installation commands, tested platform, dependency versions, and upstream revision.
- Completed relevant MCTF tutorials and successful sample-agent execution.
- A reproducible sample-agent demonstration, using upstream examples where sufficient.
- A Rules Reference Document covering game mechanics and the simulator interface.
- A shared architecture draft identifying component responsibilities, information flow, and open decisions.
- A short progress report with completed work, evidence, blockers, and next steps.

Later work:

- A custom baseline control script, scheduled for W5.
- Final structured LTL schema, interface versioning, error codes, and failure-handling specifications, scheduled for W4–W5.
- Formal selection of RL state features, actions, and rewards, scheduled for W6–W7.
- Symbolic-command consumption, task monitors, reward shaping, and safety shields.
- Stationary-red training, patrolling/reactive opponents, checkpoints, and performance evaluation.
- Multi-agent coordination, hardware deployment, and publication experiments.

A 1v1 sample-agent demonstration is preferred because it supports the next experiment. A custom 1v1 runner is a W5 deliverable. Record the team size and configuration of any demonstration used for the current checkpoint.

## 5. Requirements and acceptance evidence

| ID | Requirement | Evidence |
| --- | --- | --- |
| FR-1 | Both owners can import PyQuaticus and launch the simulator in isolated environments. Use the competition branch and record the working commit. | Commands and results for each owner; tested platform and dependency versions. |
| FR-2 | Complete relevant tutorials and successfully run existing sample agents. | Tutorial/example paths, run commands, policy assignments, and observed results. |
| FR-3 | Provide a repeatable demonstration with explicit configuration. | Live demo or recording plus instructions another teammate can follow. |
| FR-4 | Document capture, tagging, cooldowns, boundaries, scoring, and episode completion. | Rules Reference Document tied to source paths and the installed revision. |
| FR-5 | Document observation fields, normalization, agent/team IDs, valid actions, and default rewards. | Interface section explaining how an existing policy receives observations and returns actions. |
| FR-6 | Identify candidate LTL propositions and their evidence sources. Distinguish agent observations from privileged simulator state. | Proposition table with definitions, sources, access level, and unresolved semantics. |
| FR-7 | Contribute to a shared architecture showing translation, validation, task/constraint integration, RL execution, and simulator feedback. | Reviewed diagram and responsibility descriptions; open decisions explicitly listed. |
| FR-8 | Report checkpoint progress accurately. | Completed/in-progress/blocked items, supporting evidence, and next steps. |

Current requirements concern understanding the simulator's existing observations, actions, and rewards. The formal learning design is scheduled for W6–W7.

FR-1 implementation status, October 7: Akshith's macOS ARM environment passed
dependency checks, import, 1v1 reset/step, episode completion, offscreen rendering,
and desktop rendering. See [installation evidence](../setup/fr1-verification.md)
and the repository README for commands, pinned revision, dependency snapshot,
and platform adjustments. Yahya's independent setup verification remains pending,
so the requirement for both owners is still open. Shared-interface work is
deferred.

FR-2 implementation status, October 7: the relevant simulator/example material
has been reviewed, the original upstream attacker/defender script completed,
and short random, attacker/defender, and combined-policy demonstrations passed.
See the [walkthrough](../tutorials/fr2-sample-agents.md) and
[execution evidence](../setup/fr2-verification.md). Teammate walkthroughs remain
pending. Current work covers simulator setup and sample agents; RL training
and shared interfaces are deferred.

FR-3 implementation status, October 7: a saved 1v1 configuration produced a
validated MP4, configuration/provenance records, and per-step traces. Two runs
matched in trajectory and summary on the tested macOS environment. See the
[demonstration guide](../tutorials/fr3-repeatable-demo.md) and
[verification evidence](../setup/fr3-verification.md). Independent teammate
reproduction remains pending.

## 6. Rules Reference Document

The document must answer:

- What counts as flag pickup and completed capture? Where must the carrier return?
- When can an agent tag another? What happens to a carried flag after tagging?
- How are tagged-player recovery and tagger cooldown represented?
- How are field boundaries represented and violations handled?
- What does each agent observe? Which fields are normalized, team-relative, or privileged?
- How are agent IDs and teams represented?
- What actions are valid, and how do they map to movement?
- Which default rewards are active, and how are they assigned?
- What causes termination or truncation, and how does simulated time advance?
- Which observations or state transitions can establish candidate propositions such as `has_enemy_flag`, `capture_completed`, and `tagged`?

Use the installed code as the source of truth for API behavior. Cross-check game semantics against the rules and sponsor notes. Record discrepancies instead of silently choosing an interpretation.

## 7. Shared architecture deliverable

The RL subgroup must help explain the path from validated logic to agent behavior:

```text
English command → LTL translation → validation → task/constraint integration
                                                        ↓
                                              RL policy → action
                                                        ↓
                                                   PyQuaticus
                                                        ↓
                                    observations and game facts → feedback
```

The diagram is a draft architecture. Task monitoring, reward shaping, and shielding remain design choices to evaluate. Describe how logic could affect learning or execution and identify which subgroup owns each boundary.

At W3, include candidate proposition definitions and open integration decisions. Final schema, versioning, error codes, and failure behavior belong to the W4–W5 specifications.

## 8. Checkpoint workflow and artifacts

1. Show the working environment and existing sample agents.
2. Provide the exact setup and demonstration commands.
3. Review the Rules Reference Document draft.
4. Review the shared architecture draft with the LTL subgroup.
5. Record blockers and the remaining work required for October 11.

Proposed repository artifacts:

| Path | Purpose |
| --- | --- |
| `README.md` | Setup, tested environment, and sample-agent run instructions. |
| `docs/rules-reference.md` | Game mechanics, observations, actions, rewards, and proposition candidates. |
| `docs/architecture.md` | Shared diagram, responsibilities, and open design decisions. |
| `docs/progress/2026-10-09.md` | Checkpoint evidence, status, blockers, and next steps. |

These paths are proposed deliverables. Updating this PRD does not establish their completion. Keep local environments and generated run outputs out of version control.

## 9. Validation and completion criteria

October 7–9 checkpoint:

- [ ] Both owners have working environments with setup evidence.
- [x] Relevant simulator/example walkthrough and sample-agent runs are verified locally and documented; teammate walkthrough pending.
- [x] A recorded sample-agent demonstration, saved configuration, and reproducible commands are ready; local repeatability verified.
- [ ] Rules Reference Document has a substantial draft covering section 6.
- [ ] Shared architecture has a substantial draft reviewed with the LTL subgroup.
- [ ] Progress report identifies missing evidence, blockers, and remaining W3 work.

By October 11:

- [ ] Rules Reference Document is complete, with source references and unresolved discrepancies recorded.
- [ ] Shared architecture is reviewed by both subgroups and component responsibilities are agreed.
- [ ] Another teammate can follow the setup/run instructions or any reproduction blocker is explicitly recorded.
- [ ] W4–W5 handoff lists proposition candidates and decisions needed for the LTL format and interface.

Validation uses concrete simulator execution and source review. A trained policy, capture-success target, custom event logger, and repeated headless evaluation are later deliverables.

## 10. Follow-on baseline control task

W5, October 19–25: implement and verify the Baseline Control Script assigned to Akshith and Yahya. Define its final acceptance criteria after inspecting upstream examples and agreeing on the shared interface.

Recommended scope for that task:

- Explicit 1v1 configuration and policy assignments.
- Correct reset/step lifecycle, episode completion handling, and resource cleanup.
- Configuration recording and basic episode results.
- Rendering/headless execution and seed controls where supported.

Detailed event logging is a proposed extension. If adopted, distinguish persistent states from one-time events and mark unavailable signals explicitly. Agree on that scope before making it a deadline requirement.

## 11. Risks and decisions

| Issue | Required action |
| --- | --- |
| Installation or platform incompatibility | Record the tested dependency combination, adjustments, and unresolved failures. |
| API drift | Pin the working revision and reference it in interface documentation. |
| Unknown boundaries and a future safety shield | Specify information available to the policy, logger, and shield before training. |
| Ambiguous LTL integration | Identify the mechanism connecting logic to observations, rewards, or allowed actions. |
| Schedule inconsistencies | Reconcile summary bars and detailed tasks. Tier 3 extends through W15 and RL evaluation through W16, while Phase 1 is budgeted at 12 weeks. |
| Scope added to the early checkpoint | Keep W3 acceptance tied to setup, research, and architecture; schedule added implementation explicitly. |

## 12. References

- Team project proposal, sections 5 and 9.2, and its embedded Gantt chart: task ownership, deliverables, and week assignments.
- Team-confirmed project start date: September 21, 2026.
- Sponsor meeting notes: semester-one tiers and subgroup responsibilities.
- [MCTF software setup](https://www.mctf26.com/installation).
- [MCTF game rules](https://www.mctf26.com/rules).
- [MCTF training guide](https://www.mctf26.com/training).
- [PyQuaticus repository](https://github.com/mit-ll-trusted-autonomy/pyquaticus).
