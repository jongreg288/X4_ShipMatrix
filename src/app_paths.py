"""Application path helpers for development and packaged runtime."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import List


def is_frozen() -> bool:
    return getattr(sys, "frozen", False) or hasattr(sys, "_MEIPASS")


def get_app_dir() -> Path:
    if is_frozen():
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


def get_user_data_root() -> Path:
    local_app_data = os.getenv("LOCALAPPDATA")
    base_dir = Path(local_app_data) if local_app_data else (Path.home() / "AppData" / "Local")
    return base_dir / "X4_ShipMatrix"


def get_data_dir() -> Path:
    return get_user_data_root() / "data"


def get_csv_cache_dir() -> Path:
    return get_data_dir() / "csv_cache"


def get_data_search_paths() -> List[Path]:
    app_dir = get_app_dir()
    paths: List[Path] = []

    if is_frozen():
        bundle_dir = Path(getattr(sys, "_MEIPASS", app_dir))
        paths.extend(
            [
                bundle_dir / "data",
                get_data_dir(),
                app_dir / "data",
                Path.cwd() / "data",
            ]
        )
    else:
        paths.extend(
            [
                app_dir / "data",
                app_dir / "build_scripts" / "data",
                get_data_dir(),
                Path.cwd() / "data",
            ]
        )

    deduped: List[Path] = []
    seen = set()
    for path in paths:
        resolved = str(path.resolve()) if path.exists() else str(path)
        if resolved not in seen:
            seen.add(resolved)
            deduped.append(path)

    return deduped


def has_xml_data() -> bool:
    for data_path in get_data_search_paths():
        if data_path.exists() and list(data_path.glob("**/*.xml")):
            return True
    return False
