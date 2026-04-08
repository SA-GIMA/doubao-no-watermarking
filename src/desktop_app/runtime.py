from __future__ import annotations

import sys
from pathlib import Path


def project_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)  # type: ignore[attr-defined]
    return Path(__file__).resolve().parents[2]


def ui_dir() -> Path:
    return project_root() / "src" / "desktop_app" / "ui"


def legal_dir() -> Path:
    return project_root() / "legal"
