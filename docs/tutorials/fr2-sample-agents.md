# FR-2 Simulator tutorials and sample agents

This walkthrough introduces the simulator loop and PyQuaticus's existing random,
attacker, defender, and combined heuristic policies. Complete FR-1 setup first.
The examples use the pinned competition revision and the tracked compatibility
patches installed by `scripts/setup_pyquaticus.sh`.

## 1. Review setup and the environment loop

Read the upstream README and `test/rand_env_test.py` under `.local/pyquaticus`.
The random example demonstrates this sequence:

1. Construct `PyQuaticusEnv` with a team size and game configuration.
2. Call `reset()` to receive observations and information.
3. Build an action dictionary keyed by agent IDs.
4. Call `step(actions)` to receive observations, rewards, termination,
   truncation, and information.
5. Stop when the episode ends and close the environment.

The pinned random script enables a GPS field and a human display. Our short
demonstrations use the default non-GPS field so startup needs no map downloads.
Run from the repository root, after activating `.venv`:

```bash
python scripts/run_sample_agents.py --example random
```

This runs two agents taking seeded random discrete actions for 120 simulated
seconds. A successful run validates execution; random actions offer no capture
strategy.

## 2. Run existing attacker and defender policies

Read these upstream files:

- `test/base_policy_test.py`: policy construction, assignments, and episode loop.
- `pyquaticus/base_policies/README.MD`: supported policies and their state inputs.
- `pyquaticus/base_policies/base_attack.py`: flag-seeking and return behavior.
- `pyquaticus/base_policies/base_defend.py`: defensive behavior.

Then run:

```bash
python scripts/run_sample_agents.py --example attack-defend
python scripts/run_sample_agents.py --example attack-defend --render human --seconds 12
```

The demonstration assigns `agent_0` (blue) to upstream `BaseAttacker` and
`agent_1` (red) to upstream `BaseDefender`, both in `medium` mode. It uses their
`compute_action(observations, info)` methods unchanged. Actions are checked
against each agent's declared discrete action space before stepping.

The upstream policies read global state through `info`, which gives them more
information than a decentralized policy may receive. Record this assumption
when using them as future training opponents or evaluation baselines.

## 3. Run the combined heuristic

Read `test/heuristic_test.py` and
`pyquaticus/base_policies/base_combined.py`, then run:

```bash
python scripts/run_sample_agents.py --example combined --render rgb_array
```

This assigns upstream `Heuristic_CTF_Agent` in `hard` mode to both agents on each
team. It uses a 2v2 environment and `si` dynamics, following the upstream
heuristic example. The local demonstration uses discrete actions and normalized
observations; the upstream example requests continuous actions from its policies
and disables observation normalization.

An initial 1v1 combined-policy check emitted empty-teammate mean/variance
warnings. The 2v2 configuration avoids that warning in the verified run.
Use the 1v1 attacker/defender example for the initial capstone environment.

## 4. Inspect results

The demonstration prints its assignments and final summary. Results are saved
under `runs/fr2/<example>/<render>-seed<seed>-<seconds>s/`:

- `summary.json`: full input configuration, assignments, seed, mode, steps,
  simulated time, end reason, and final capture/grab/tag counters.
- `frame.png`: final Pygame surface when rendering is enabled.
- `trajectory.json` and `metadata.json`: per-step trace and runtime provenance,
  added for the [FR-3 repeatability demonstration](fr3-repeatable-demo.md).

Counters are read from the simulator's final state in blue/red order. They are
episode totals. No transition-level event detector is included. Repeating the
same example/settings replaces its saved output.

All examples default to seed 7, 120 simulated seconds, and speedup factor 10.
The policies remain heuristic; there is no optimization or learned checkpoint.

## 5. Run the upstream example directly

The original attacker/defender script was executed successfully on the tested
macOS ARM machine after applying the optional-MOOS patch. To reproduce its
offscreen display execution in Bash:

```bash
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python .local/pyquaticus/test/base_policy_test.py
```

This retains the script's 2v2 configuration, 600-second simulated duration,
speedup factor 8, and `competition_easy` policies. It takes longer than the
local short demos because it draws frames through the human-render path.
Its waypoint-string actions trigger upstream action-space auto-detection
warnings. Record those warnings when reviewing its output.

## 6. Locate the later RL training path

Review the [MCTF training guide](https://www.mctf26.com/training) and
`.local/pyquaticus/rl_test/train_3v3.py` to locate environment creation, policy
mapping, PPO configuration, and reward assignment. The installed revision's
reward examples are in `pyquaticus/utils/rewards.py`; inspect that path when
following website references.

The training source was reviewed for orientation. Training execution, RLlib
installation, and framework selection belong to subsequent work. Keyboard
control, GPS-map demonstrations, and hardware deployment are optional follow-up
examples and have no execution claim in this walkthrough.

## Windows commands

Follow the [platform guide](../setup/platform-guide.md), including the
optional-MOOS patch, then invoke the environment directly:

```powershell
.venv\Scripts\python.exe scripts/run_sample_agents.py --example random
.venv\Scripts\python.exe scripts/run_sample_agents.py --example attack-defend
.venv\Scripts\python.exe scripts/run_sample_agents.py --example combined --render rgb_array
```

Windows execution remains pending teammate verification. Record your platform
and observed results before claiming completion there.

See [FR-2 verification evidence](../setup/fr2-verification.md) for measured results.
