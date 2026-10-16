#!/usr/bin/env bash
# ==============================================================================
# IG Growth Prompts - POSIX Setup & Launcher (macOS / Linux)
# ==============================================================================
set -euo pipefail

echo "==> Checking Python installation..."
if ! command -v python3 &>/dev/null; then
    echo "Error: python3 is not installed. Please install Python 3.10 or higher." >&2
    exit 1
fi

PYTHON_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "==> Detected Python $PYTHON_VER"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

echo "==> Installing igprompts package locally (pip install -e .)..."
python3 -m pip install --quiet -e .

echo "==> Setup completed successfully!"
echo "    Run 'igprompts --help' or 'python3 -m igprompts gui' to start."
