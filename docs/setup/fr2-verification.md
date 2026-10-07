# FR-2 Sample-agent execution evidence

Verified October 7, 2026, on Akshith's macOS 27.0 ARM64 environment using Python
3.10.20 and PyQuaticus competition commit
`475d670650ec5d49691ba707cd1054c4e45d8053`.

The [walkthrough](../tutorials/fr2-sample-agents.md) provides commands and source
reading paths. Yahya's walkthrough and Windows execution are pending verification.

## Existing examples and tutorial material

| Source | Work completed |
| --- | --- |
| Upstream README and `test/rand_env_test.py` | Reviewed setup and random-action loop; exercised a short non-GPS adaptation |
| `test/base_policy_test.py` | Executed original script to episode completion using SDL dummy display |
| Base policies README and attacker/defender source | Reviewed policy inputs and assignments; exercised 1v1 medium policies |
| `test/heuristic_test.py` and combined-policy source | Reviewed sample; exercised a short 2v2 hard-policy adaptation |
| MCTF training guide and `rl_test/train_3v3.py` | Reviewed training configuration and policy mapping; training execution deferred |

## Measured local results

The following are single demonstration runs, with blue/red counter order.
They provide execution evidence and are insufficient to estimate policy strength.

| Example | Configuration | Completion | Captures | Grabs | Tags |
| --- | --- | --- | --- | --- | --- |
| Random | 1v1, seed 7, 120 seconds, headless | 120 steps; time-limit truncation | 0 / 0 | 0 / 0 | 0 / 0 |
| Attacker/defender | 1v1, medium, seed 7, 120 seconds, headless | 120 steps; time-limit truncation | 0 / 0 | 0 / 0 | 0 / 1 |
| Combined heuristic | 2v2, hard, `si` dynamics, seed 7, 120 seconds, offscreen | 120 steps; time-limit truncation | 0 / 0 | 0 / 0 | 0 / 0 |
| Attacker/defender GUI | 1v1, medium, seed 7, 12 seconds | 12 steps; time-limit truncation; GUI launch passed | 0 / 0 | 0 / 0 | 0 / 0 |

The original upstream attacker/defender script exited successfully and reported
a final 0–0 score. Its configuration used 2v2, 600 simulated seconds, speedup
factor 8, and `competition_easy` policies. It reported auto-detection warnings
for waypoint-string actions passed through the declared discrete action space.

The local demos validate discrete actions and finite observations. The combined
demo uses 2v2 because an initial 1v1 check emitted empty-teammate statistic
warnings. No captures occurred in the recorded runs; successful capture and
trained-policy performance remain later validation targets.

## Optional MOOS import correction

FR-1 verified the simulator directly. FR-2 found that importing the existing
policies transitively imports the hardware bridge and failed with:

```text
ModuleNotFoundError: No module named 'pymoos'
```

`patches/pyquaticus-optional-moos.patch` makes a missing pymoos import optional
at module load and raises an explicit dependency error when constructing the
hardware bridge. Other import failures propagate. Policy code and bridge
operation with an installed pymoos package are otherwise unchanged by the patch;
hardware operation has not been verified.

Checks confirmed that all three sample policy classes import, the demos execute,
and hardware-bridge construction without pymoos raises the expected error.
The setup script applies this patch on every platform; the dependency-marker
patch and SciPy snapshot remain specific to ARM macOS.
An offline setup-script rerun passed with both patches already applied and
reconfirmed dependency compatibility and the FR-1 startup check. The combined
demo's final rendered frame was visually inspected.

## Verification limits

RL training, GPS-map examples, keyboard control, and hardware operation were
not executed. Shared-interface work is outside the current scope. Windows and
other teammate environments need independent verification.
