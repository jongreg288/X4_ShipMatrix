#!/usr/bin/env python3
"""Compatibility wrapper for archived legacy build_exe script."""

import subprocess
import sys
from pathlib import Path


def main() -> int:
    print("Compatibility wrapper: forwarding to build_scripts/legacy/build_exe.py")
    print("Preferred command: python build_scripts/release_prerelease.py")
    print()

    legacy_script = Path(__file__).parent / "legacy" / "build_exe.py"
    command = [sys.executable, str(legacy_script), *sys.argv[1:]]
    return subprocess.call(command)


if __name__ == "__main__":
    raise SystemExit(main())