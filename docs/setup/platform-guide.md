# PyQuaticus setup and platform compatibility

Use Python 3.10.20 and the pinned `mctf2026` revision
`475d670650ec5d49691ba707cd1054c4e45d8053` for the team's simulator work.
Installation adjustments and dependency snapshots depend on the operating
system and CPU architecture.

## Verification status

| Platform | Setup path | Status |
| --- | --- | --- |
| Apple Silicon macOS | Bash script; ARM macOS patch and dependency snapshot | Verified on macOS 27.0, ARM64 |
| Intel macOS | Bash script; upstream dependencies | Pending teammate verification |
| Native Windows | PowerShell commands below; upstream dependencies | Pending teammate verification |
| Windows with WSL | Bash script inside WSL; Linux dependencies | Pending teammate verification |
| Linux | Bash script; upstream dependencies | Pending teammate verification |

The verified macOS snapshot includes PyObjC packages and ARM macOS versions.
Use it only on Apple Silicon macOS. Generate separate snapshots after verifying
the other platforms. Different native dependencies are expected; keep the Python
version and PyQuaticus revision consistent.

## Apple Silicon macOS

Install Git and [uv](https://docs.astral.sh/uv/getting-started/installation/).
From the repository root:

```bash
bash scripts/setup_pyquaticus.sh
source .venv/bin/activate
python scripts/check_pyquaticus.py
python scripts/check_pyquaticus.py --render rgb_array
python scripts/check_pyquaticus.py --render human
```

The script applies `patches/pyquaticus-macos-arm64.patch` and installs the exact
runtime dependencies in `requirements/macos-arm64-py310.txt`. It stores Python,
the upstream checkout, and its cache under `.local`, and the environment under
`.venv`. Re-running the script recognizes an already-applied patch.

### Issue 1: pymoos installation fails

Observed failure:

```text
pymoos==2022.1 has no wheels with a matching platform tag
```

At the pinned revision, upstream requires this package on Linux and macOS.
The selected release has no matching distribution for ARM macOS. Its import is
in the MOOS bridge module; the basic simulator startup succeeds without it.

The tracked patch changes the requirement marker from:

```text
sys_platform == 'linux' or sys_platform == 'darwin'
```

to:

```text
sys_platform == 'linux' or (sys_platform == 'darwin' and platform_machine != 'arm64')
```

This adjustment excludes pymoos on ARM macOS. Linux and Intel macOS retain the
upstream dependency. The ARM macOS environment supports the verified simulation
workflow; MOOS hardware-bridge operation is unavailable.

### Issue 2: SciPy import fails on macOS 27

SciPy 1.15.3 installed successfully, then failed when PyQuaticus imported it:

```text
section '__DATA/__thread_bss' has a zero-fill section type, but offset field is not zero
```

The failure occurred while loading SciPy's PROPACK native library. A similar
failure appears in the [SciPy issue tracker](https://github.com/scipy/scipy/issues/25635).
SciPy 1.14.1 passed on our tested ARM macOS machine and is pinned in its snapshot.
This is a verified workaround for that environment. Other macOS versions and
architectures require their own checks.

If an existing ARM macOS environment has the failing version, run:

```bash
uv pip install --python .venv/bin/python -r requirements/macos-arm64-py310.txt
.venv/bin/python scripts/check_pyquaticus.py
```

### Issue 3: GUI startup fails inside a restricted shell

The desktop check initially reported unavailable macOS display services and:

```text
pygame.error: video system not initialized
```

On the tested machine, the GUI check passed when run with desktop access outside
the Codex shell sandbox. Run `--render human` from a local terminal with a
graphical session. The default check and `--render rgb_array` work headlessly.
Other occurrences of this error require investigation of the display session
and SDL configuration.

## Native Windows with PowerShell

FR-2 adds `patches/pyquaticus-optional-moos.patch`: sample policies import the
MOOS bridge even during simulation. This patch permits imports without pymoos
and reports an explicit dependency error if the hardware bridge is constructed.
The Bash setup script applies it automatically on every platform.

These instructions have been reviewed against the pinned source and uv CLI.
They still need execution on a teammate's Windows machine.

Install Git and uv using the
[official uv installation instructions](https://docs.astral.sh/uv/getting-started/installation/).
Open PowerShell in this repository's root. Use a fresh checkout/environment for
the first verification and stop if any command fails.

```powershell
$env:UV_CACHE_DIR = Join-Path $PWD.Path '.local\uv-cache'
$env:UV_PYTHON_INSTALL_DIR = Join-Path $PWD.Path '.local\python'
uv python install --no-bin 3.10.20

git clone --depth 1 --branch mctf2026 https://github.com/mit-ll-trusted-autonomy/pyquaticus.git .local/pyquaticus
git -C .local/pyquaticus fetch --depth 1 origin 475d670650ec5d49691ba707cd1054c4e45d8053
git -C .local/pyquaticus checkout --detach 475d670650ec5d49691ba707cd1054c4e45d8053
git -C .local/pyquaticus apply (Join-Path $PWD.Path 'patches/pyquaticus-optional-moos.patch')

uv venv --python 3.10.20 .venv
uv pip install --python .venv/Scripts/python.exe -e .local/pyquaticus
uv pip check --python .venv/Scripts/python.exe

.venv\Scripts\python.exe scripts/check_pyquaticus.py
.venv\Scripts\python.exe scripts/check_pyquaticus.py --render rgb_array
.venv\Scripts\python.exe scripts/check_pyquaticus.py --render human
```

These commands invoke the environment's interpreter directly, so activation
and PowerShell activation-script policy changes are unnecessary.

At the pinned revision, the pymoos requirement already has a platform marker
that excludes native Windows (`sys_platform == 'win32'`). The ARM macOS patch
does not apply to Windows. The
[MCTF installation page](https://www.mctf26.com/installation) suggests removing
pymoos for Windows; the pinned source achieves that exclusion through its marker.
Inspect the marker again if the team changes the upstream revision.

Once all checks pass, record the dependency snapshot:

```powershell
uv pip freeze --python .venv/Scripts/python.exe --exclude-editable | Set-Content -Encoding ascii requirements/windows-py310.txt
```

Record whether the Windows machine is x64 or ARM64. Snapshot names should include
the architecture if the team verifies multiple Windows architectures.

## WSL, Linux, and Intel macOS

Run `bash scripts/setup_pyquaticus.sh` in the target environment. These paths are
unverified by this change. The script installs upstream dependencies and applies
the patch/snapshot only when `uname` reports Darwin and ARM64.

WSL uses Linux dependency rules even though its host is Windows. The Linux
pymoos requirement remains active. Keep its Python environment inside WSL and
use `.venv/bin/python`; native Windows uses `.venv/Scripts/python.exe`.

Run the default and offscreen checks first. Desktop rendering needs a working
graphical session. If installation or imports fail, record the exact error and
platform before choosing a workaround.

## Team verification record

After setup, add the following to `docs/setup/fr1-verification.md`:

- Team member and verification date.
- OS version, CPU architecture, Python version, and upstream commit.
- Installation command and any platform adjustment.
- Results for dependency checking, headless execution, offscreen rendering,
  and GUI launch. Mark any skipped check explicitly.
- Dependency snapshot path and unresolved failures.

Expected startup output includes:

```text
PASS: import, 1v1 reset, 20 steps, episode completion; render=none
```

Successful verification on one platform does not establish another teammate's
installation status. FR-1's requirement for both owners remains pending Yahya's
independent result.
