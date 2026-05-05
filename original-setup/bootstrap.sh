#!/usr/bin/env bash
set -euo pipefail

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found on PATH" >&2
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT_DIR/.venv"

REQS_FILE="$ROOT_DIR/requirements.txt"
if [ ! -f "$REQS_FILE" ]; then
  echo "requirements.txt not found at $REQS_FILE" >&2
  exit 1
fi

if [ ! -f "$VENV_DIR/bin/activate" ]; then
  python3 -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

python -m pip install --upgrade pip
python -m pip install -r "$REQS_FILE"

echo "OK: virtualenv ready at $VENV_DIR"
