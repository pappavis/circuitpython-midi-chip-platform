#!/usr/bin/env bash

set -euo pipefail

repository_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
staging_dir="${repository_root}/.mkdocs-source"

mkdir -p "${staging_dir}"

rsync -a --delete \
  --exclude='.git/' \
  --exclude='.mkdocs-source/' \
  --exclude='.pytest_cache/' \
  --exclude='.venv/' \
  --exclude='build/' \
  --exclude='device/' \
  --exclude='dist/' \
  --exclude='site/' \
  --exclude='src/' \
  --exclude='tests/' \
  --include='outputs/' \
  --include='outputs/CHATOD-20260714-MCP-CP-MVP-001/' \
  --include='outputs/CHATOD-20260714-MCP-CP-MVP-001/circuitpython_midi_chip_platform_mvp_kanban_v0.1.0.xlsx' \
  --exclude='outputs/***' \
  --include='*/' \
  --include='*.md' \
  --include='LICENSE' \
  --include='assets/***' \
  --exclude='*' \
  "${repository_root}/" "${staging_dir}/"

if [[ -x "${repository_root}/.venv/bin/mkdocs" ]]; then
  mkdocs_command="${repository_root}/.venv/bin/mkdocs"
elif command -v mkdocs >/dev/null 2>&1; then
  mkdocs_command="$(command -v mkdocs)"
else
  echo "MkDocs is missing. Install the documentation extra with: python -m pip install -e '.[docs]'" >&2
  exit 1
fi

"${mkdocs_command}" build --clean --config-file "${repository_root}/mkdocs.yml"
