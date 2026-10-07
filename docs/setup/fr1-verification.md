# FR-1 PyQuaticus installation evidence

Verified October 7, 2026, on Akshith's development machine, branch
`ft-pyquaticus-setup`. This record covers installation and simulator startup.
Yahya's environment remains pending independent verification.

For platform-specific setup commands and the documented macOS failures, see
the [platform guide](platform-guide.md). Native Windows, WSL/Linux, and Intel
macOS are pending verification; their results should be recorded separately.

## Environment

| Item | Value |
| --- | --- |
| OS | macOS 27.0, build 26A428 |
| Architecture | ARM64 |
| Python | CPython 3.10.20, project-local uv runtime |
| Virtual environment | `.venv` |
| Upstream | `https://github.com/mit-ll-trusted-autonomy/pyquaticus.git` |
| Competition branch | `mctf2026` |
| Commit | `475d670650ec5d49691ba707cd1054c4e45d8053` |
| Installed PyQuaticus version | 0.1.0, editable install from pinned checkout |
| Dependency snapshot | `requirements/macos-arm64-py310.txt` |

Selected versions: NumPy 1.26.4, SciPy 1.14.1, PettingZoo 1.25.0,
Gymnasium 1.4.0, Pygame 2.4.0, and Contextily 1.6.2. The snapshot records all
45 installed runtime dependencies; PyQuaticus is installed separately from the
pinned source. Build-tool dependencies are resolved separately by uv.

## Compatibility adjustments

The first install failed because upstream requires `pymoos==2022.1` on macOS,
and that release has no matching ARM macOS distribution. Source inspection found
its import in `pyquaticus/moos_bridge/pyquaticus_moos_bridge.py`. The tracked
patch changes its dependency marker to exclude ARM macOS while retaining Linux
and other macOS architectures. Simulation startup passed with this adjustment.
Hardware bridge operation is outside this environment's verified capabilities.

The first import then failed with SciPy 1.15.3:

```text
section '__DATA/__thread_bss' has a zero-fill section type, but offset field is not zero
```

SciPy 1.14.1 passed on this machine and is pinned in the macOS snapshot.
A similar loader failure is documented in the
[SciPy issue tracker](https://github.com/scipy/scipy/issues/25635).

## Verification results

| Check | Result |
| --- | --- |
| `uv pip check --python .venv/bin/python` | All 46 installed packages compatible |
| `python scripts/check_pyquaticus.py` | Import, two-agent reset, 20 steps, episode completion passed |
| `python scripts/check_pyquaticus.py --render rgb_array` | Same lifecycle passed; 922 × 491 RGB frame saved and visually inspected |
| `python scripts/check_pyquaticus.py --render human` | Desktop rendering and same lifecycle passed outside the shell sandbox |
| `bash scripts/setup_pyquaticus.sh` | Existing-install rerun passed, including dependency and lifecycle checks |
| Fresh `.local/fr1-repro` virtual environment | Offline installation from the pinned snapshot and cached upstream build passed; startup check passed |

The desktop check initially failed inside the shell sandbox with unavailable
macOS display services. Running it with desktop access passed. Headless and
offscreen checks passed within the sandbox.

The smoke check uses the default non-GPS field, one agent per team, a two-second
episode limit, reset seed 7, and seeded random actions. It verifies simulator
startup and execution. It provides no trained-policy or capture-performance
evidence. At this revision, `env.render()` draws to a Pygame surface and returns
None; the offscreen check saves that surface directly.

## Teammate verification

Yahya should run the setup command and startup checks from the README, then add
the tested platform, versions, and results here. FR-1's requirement for both
owners remains open until those results are available. No teammate result is
inferred from Akshith's local checks.
