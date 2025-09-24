#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ -d "${REPO_ROOT}/.venv" ]]; then
  # shellcheck disable=SC1091
  source "${REPO_ROOT}/.venv/bin/activate"
else
  echo "⚠️  A virtual environment (.venv) was not found."
  echo "    Create one with: python3 -m venv .venv"
  echo "    Then install dependencies: source .venv/bin/activate && pip install -r requirements.txt"
  echo
  echo "Continuing with the current Python environment..."
fi

python -m link_parser "$@"
