#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON_BIN:-python}"

"$PYTHON_BIN" -m pip install pyinstaller pywebview

"$PYTHON_BIN" -m PyInstaller \
  --noconfirm \
  --clean \
  --windowed \
  --name "doubao-no-watermarking" \
  --add-data "src/desktop_app/ui:src/desktop_app/ui" \
  --add-data "legal:legal" \
  src/desktop_app/launcher.py
