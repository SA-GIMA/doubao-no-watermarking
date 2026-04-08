$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

python -m pip install pyinstaller pywebview

pyinstaller `
  --noconfirm `
  --clean `
  --windowed `
  --name "doubao-no-watermarking" `
  --add-data "src/desktop_app/ui;src/desktop_app/ui" `
  --add-data "legal;legal" `
  src/desktop_app/launcher.py
