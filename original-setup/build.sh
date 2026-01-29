#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT_DIR/.venv"

if [ -f "$VENV_DIR/bin/activate" ]; then
  # shellcheck disable=SC1091
  source "$VENV_DIR/bin/activate"
  python "$ROOT_DIR/CVFoundry-Lite-Build.py" "$@"
  exit 0
fi

if command -v python >/dev/null 2>&1; then
  python "$ROOT_DIR/CVFoundry-Lite-Build.py" "$@"
  exit 0
fi

if command -v python3 >/dev/null 2>&1; then
  python3 "$ROOT_DIR/CVFoundry-Lite-Build.py" "$@"
  exit 0
fi

echo "No python interpreter found (expected 'python' or 'python3' on PATH)." >&2
exit 1
