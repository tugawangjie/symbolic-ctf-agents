# symbolic-ctf-agents

PyQuaticus and reinforcement-learning work for maritime capture the flag.
The current implementation covers FR-1 installation, FR-2 sample-agent execution,
and an FR-3 repeatable recorded demonstration.

## Setup

Prerequisites: Git, [uv](https://docs.astral.sh/uv/), and network access.
See the [platform setup and troubleshooting guide](docs/setup/platform-guide.md)
for Apple Silicon macOS, Intel macOS, native Windows PowerShell, and WSL/Linux.
The following commands use Bash on macOS/Linux. Native Windows users should
follow the PowerShell commands in that guide.

From the repository root:

```bash
bash scripts/setup_pyquaticus.sh
source .venv/bin/activate
```

The script downloads Python 3.10.20 into `.local/python`, checks out the pinned
PyQuaticus competition revision in `.local/pyquaticus`, installs it into `.venv`,
checks dependencies, and runs a two-second 1v1 startup check. These local
directories are gitignored.

Verified platform: macOS 27.0, Apple Silicon ARM64. The exact installed
dependencies are in `requirements/macos-arm64-py310.txt`. Other platforms use
upstream dependencies and require their own verification; the macOS requirements
contain platform-specific packages.

## Verify the simulator

Run from the repository root:

```bash
python scripts/check_pyquaticus.py
python scripts/check_pyquaticus.py --render rgb_array
python scripts/check_pyquaticus.py --render human
```

Each check resets one blue and one red agent, samples valid actions, checks for
finite observations, and runs until the two-second episode ends. The default
check is headless. `rgb_array` saves `runs/fr1/frame.png`; `human` briefly opens
the game window. Desktop rendering needs a graphical session.

These commands verify installation and simulator startup.

## Run sample agents

After setup, work through the
[FR-2 walkthrough](docs/tutorials/fr2-sample-agents.md):

```bash
python scripts/run_sample_agents.py --example random
python scripts/run_sample_agents.py --example attack-defend
python scripts/run_sample_agents.py --example combined --render rgb_array
python scripts/run_sample_agents.py --example attack-defend --render human --seconds 12
```

Random and attacker/defender demos use 1v1. The combined heuristic uses its
upstream 2v2 configuration. Outputs go under `runs/fr2/`; these examples use
existing heuristics and require no training dependencies. Windows interpreter
commands are included in the walkthrough.

See [FR-2 verification evidence](docs/setup/fr2-verification.md) for assignments,
measured results, and limitations.

## Record the checkpoint demo

```bash
python scripts/run_sample_agents.py --config configs/fr3-demo.json --output runs/fr3/first
```

This records a 12-second MP4 of the 120-second simulated 1v1 episode and saves
configuration, provenance, and trajectory evidence. See the
[FR-3 demo guide](docs/tutorials/fr3-repeatable-demo.md) for Windows commands,
live rendering, and repeatability checks.

## Compatibility and provenance

- Upstream branch: `mctf2026`, as specified by the
  [MCTF installation guide](https://www.mctf26.com/installation).
- Pinned commit: `475d670650ec5d49691ba707cd1054c4e45d8053`.
- Apple Silicon simulation uses `patches/pyquaticus-macos-arm64.patch` to omit
  `pymoos==2022.1`, which has no matching distribution for this platform. The
  Linux dependency is retained. The MOOS hardware bridge is unavailable in
  this macOS ARM environment.
- SciPy is pinned to 1.14.1 on macOS ARM. The initially resolved 1.15.3 wheel
  failed native-library loading on this machine; 1.14.1 passed verification.
- `patches/pyquaticus-optional-moos.patch` allows sample policies to import
  without pymoos. Constructing the hardware bridge still raises a dependency
  error when pymoos is unavailable. Setup applies this patch on every platform.
- RLlib and PyTorch training extras are deferred until the training task.

See [FR-1 verification evidence](docs/setup/fr1-verification.md) and the
[PRD](docs/prd/01-pyquaticus-setup-and-1v1-runner.md).
