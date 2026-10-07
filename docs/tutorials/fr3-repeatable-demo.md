# FR-3 Repeatable sample-agent demonstration

The demo runs blue's upstream `BaseAttacker` against red's `BaseDefender` in
1v1. Both use `medium` mode. It demonstrates agent movement, a defender tag,
and episode completion with a saved configuration and recording.

## Run the demonstration

Complete setup using the [platform guide](../setup/platform-guide.md).
From the repository root on macOS/Linux:

```bash
source .venv/bin/activate
python scripts/run_sample_agents.py --config configs/fr3-demo.json --output runs/fr3/first
```

Native Windows PowerShell:

```powershell
.venv\Scripts\python.exe scripts/run_sample_agents.py --config configs/fr3-demo.json --output runs/fr3/first
```

The saved configuration uses offscreen rendering, so recording needs no desktop
window. For a live demonstration, override rendering:

```bash
python scripts/run_sample_agents.py --config configs/fr3-demo.json --render human --output runs/fr3/live
```

Use `.venv\Scripts\python.exe` in place of `python` on Windows. A live demo
requires a graphical session. Command-line settings override the JSON defaults.

## Configuration

| Setting | Value |
| --- | --- |
| Saved configuration | `configs/fr3-demo.json` |
| Team size | One blue, one red |
| Assignments | `agent_0`: BaseAttacker; `agent_1`: BaseDefender |
| Policy mode | Medium |
| Action space | Discrete |
| Field | Default non-GPS field, 160 × 80 meters |
| Dynamics | Upstream default `heron` |
| Reset seed | 7 |
| Episode limit | 120 simulated seconds |
| Simulation speedup | 10 |
| Rendering | Offscreen RGB surface with agent IDs |
| Recording | MP4, 10 FPS; 12 seconds for the full episode |

The MP4 includes one frame per outer simulation step and presents the episode
at 10 times simulated-time speed. Its final time-limit result is stored in the
summary. The full input game configuration, including defaults from the pinned
revision, is saved alongside the recording. Automatic geometry values remain
marked `auto` in that input configuration and are resolved by the pinned source.

## Output artifacts

| File | Contents |
| --- | --- |
| `demo.mp4` | Recorded movement, sampled once per outer step |
| `frame.png` | Final uncompressed Pygame surface |
| `summary.json` | Input configuration, assignments, counters, steps, and end reason |
| `trajectory.json` | Per-step actions, positions, capture totals, and tag totals |
| `metadata.json` | Upstream commit, actual upstream-diff hash, runner hash, patch hashes, Python and installed package versions |

The video uses even dimensions with black padding when needed by the MPEG
encoder. Output directories are gitignored. Reusing a directory replaces
matching artifact files; use a separate directory for each comparison run.

## Check repeatability

Run the same saved configuration again into another directory:

```bash
python scripts/run_sample_agents.py --config configs/fr3-demo.json --output runs/fr3/repeat
python -c "from pathlib import Path; a=Path('runs/fr3/first'); b=Path('runs/fr3/repeat'); assert all((a/name).read_bytes()==(b/name).read_bytes() for name in ('trajectory.json','summary.json')); print('PASS: trajectories and summaries match')"
```

On Windows, use `.venv\Scripts\python.exe` for both commands. Compare metadata
when sharing results across machines. Exact trajectory equality was verified
on the tested macOS environment. Cross-platform numerical or rendering equality
requires independent measurement.

## What to show at the checkpoint

1. Open the MP4, or launch the live demo.
2. Identify blue's attacker and red's defender using agent IDs.
3. Explain that the existing policies use simulator global state through `info`.
4. Show the summary: 120 steps, time-limit truncation, blue/red tags 0/1,
   and captures 0/0 in the verified run.
5. Show the saved configuration and the matching repeat-run evidence.

This demonstrates heuristic execution and reproducibility. Successful flag
capture and learned-policy performance are later validation targets.

See [FR-3 verification evidence](../setup/fr3-verification.md).
