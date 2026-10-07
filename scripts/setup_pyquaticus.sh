#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"
command -v uv >/dev/null || { echo "Install uv before running this script." >&2; exit 1; }

export UV_CACHE_DIR="$PROJECT_ROOT/.local/uv-cache"
export UV_PYTHON_INSTALL_DIR="$PROJECT_ROOT/.local/python"
UPSTREAM="$PROJECT_ROOT/.local/pyquaticus"
REVISION=475d670650ec5d49691ba707cd1054c4e45d8053

uv python install --no-bin 3.10.20
if [[ ! -d "$UPSTREAM" ]]; then
    git clone --depth 1 --branch mctf2026 \
        https://github.com/mit-ll-trusted-autonomy/pyquaticus.git "$UPSTREAM"
    if [[ "$(git -C "$UPSTREAM" rev-parse HEAD)" != "$REVISION" ]]; then
        git -C "$UPSTREAM" fetch --depth 1 origin "$REVISION"
        git -C "$UPSTREAM" checkout --detach "$REVISION"
    fi
fi
if [[ "$(git -C "$UPSTREAM" rev-parse HEAD)" != "$REVISION" ]]; then
    echo "Existing upstream checkout has a different revision; inspect it before proceeding." >&2
    exit 1
fi

INSTALL_ARGS=()
if [[ "$(uname -s)" == Darwin && "$(uname -m)" == arm64 ]]; then
    PATCH="$PROJECT_ROOT/patches/pyquaticus-macos-arm64.patch"
    if ! git -C "$UPSTREAM" apply --reverse --check "$PATCH" 2>/dev/null; then
        git -C "$UPSTREAM" apply --check "$PATCH"
        git -C "$UPSTREAM" apply "$PATCH"
    fi
    INSTALL_ARGS=(-r "$PROJECT_ROOT/requirements/macos-arm64-py310.txt")
fi

POLICY_PATCH="$PROJECT_ROOT/patches/pyquaticus-optional-moos.patch"
if ! git -C "$UPSTREAM" apply --reverse --check "$POLICY_PATCH" 2>/dev/null; then
    git -C "$UPSTREAM" apply --check "$POLICY_PATCH"
    git -C "$UPSTREAM" apply "$POLICY_PATCH"
fi

if [[ ! -d .venv ]]; then
    uv venv --python 3.10.20 .venv
fi
uv pip install --python .venv/bin/python "${INSTALL_ARGS[@]}" -e "$UPSTREAM"
uv pip check --python .venv/bin/python
.venv/bin/python scripts/check_pyquaticus.py
