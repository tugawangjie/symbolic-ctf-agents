# FR-3 Demonstration verification

Verified October 7, 2026, on Akshith's macOS 27.0 ARM64 environment using
Python 3.10.20 and the pinned PyQuaticus revision with both tracked patches.
Teammate and Windows reproduction remain pending.

## Executed commands

```bash
.venv/bin/python scripts/run_sample_agents.py --config configs/fr3-demo.json --output runs/fr3/first
.venv/bin/python scripts/run_sample_agents.py --config configs/fr3-demo.json --output runs/fr3/repeat
cmp runs/fr3/first/trajectory.json runs/fr3/repeat/trajectory.json
cmp runs/fr3/first/summary.json runs/fr3/repeat/summary.json
```

Both runs completed 120 steps and 120 simulated seconds with time-limit
truncation. Their summaries and per-step action/position/counter traces matched
byte for byte. Final blue/red counters were captures 0/0, grabs 0/0, and tags
0/1. Policies were the upstream medium attacker and defender.

## Recording validation

OpenCV decoded every frame of both generated MP4s successfully: 120 frames,
10 FPS, 922 × 492 pixels, and 12 seconds each. A decoded mid-episode frame was
visually inspected and showed the field and labeled agents. The underlying
Pygame surface is 922 × 491 pixels; recording pads the bottom row to preserve
the complete field with an even MPEG dimension.

An initial encoding check detected that the encoder cropped an odd-height
surface. The runner now pads to even dimensions, and both recordings were
regenerated and revalidated.

## Limits

- Repeatability is measured for this configuration on one machine.
- Video encoding and cross-platform numerical equality are unverified.
- The recorded episode demonstrates a tag and zero captures.
- The policies use global state and are heuristic; no training occurred.
- Shared-interface work remains deferred.

The [demo guide](../tutorials/fr3-repeatable-demo.md) provides macOS/Linux and
Windows commands, configuration details, artifact descriptions, and a checkpoint
presentation sequence.
