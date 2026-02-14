#!/usr/bin/env python3
"""
One-command prerelease automation for X4 ShipMatrix.

Flow:
1) Build main/updater executables
2) Stage release assets into releases/latest
3) Build installer
4) Create or update GitHub prerelease via gh CLI
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    print(f"\n{description}...")
    result = subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True, capture_output=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise RuntimeError(f"{description} failed (exit code {result.returncode})")
    if result.stdout.strip():
        print(result.stdout.strip())
    return result


def find_gh() -> str:
    gh = shutil.which("gh")
    if gh:
        return gh

    common = [
        Path(r"C:\Program Files\GitHub CLI\gh.exe"),
        Path.home() / "AppData" / "Local" / "Programs" / "GitHub CLI" / "gh.exe",
    ]
    for path in common:
        if path.exists():
            return str(path)

    raise FileNotFoundError(
        "GitHub CLI not found. Install it first: winget install --id GitHub.cli --exact --source winget"
    )


def detect_version_from_iss(iss_file: Path) -> str:
    content = iss_file.read_text(encoding="utf-8", errors="ignore")
    match = re.search(r'^\s*#define\s+MyAppVersion\s+"([^"]+)"', content, re.MULTILINE)
    if not match:
        raise ValueError(f"Could not detect MyAppVersion in {iss_file}")
    return match.group(1).strip()


def stage_assets(project_root: Path, version: str) -> list[Path]:
    build_scripts = project_root / "build_scripts"
    release_dir = project_root / "releases" / "latest"
    release_dir.mkdir(parents=True, exist_ok=True)

    source_to_dest = [
        (build_scripts / "dist" / "X4 ShipMatrix.exe", release_dir / "X4 ShipMatrix.exe"),
        (build_scripts / "dist" / "X4_Updater.exe", release_dir / "X4_Updater.exe"),
        (build_scripts / "README_USERS.txt", release_dir / "README_USERS.txt"),
        (release_dir / f"X4_ShipMatrix_v{version}_Setup.exe", release_dir / f"X4_ShipMatrix_v{version}_Setup.exe"),
    ]

    for src, dest in source_to_dest:
        if src == dest:
            if not src.exists():
                raise FileNotFoundError(f"Expected installer not found: {src}")
            continue
        if not src.exists():
            raise FileNotFoundError(f"Required asset not found: {src}")
        shutil.copy2(src, dest)

    assets = [
        release_dir / f"X4_ShipMatrix_v{version}_Setup.exe",
        release_dir / "X4 ShipMatrix.exe",
        release_dir / "X4_Updater.exe",
        release_dir / "README_USERS.txt",
    ]

    for asset in assets:
        if not asset.exists():
            raise FileNotFoundError(f"Missing staged asset: {asset}")

    return assets


def release_exists(gh: str, repo: str, tag: str, cwd: Path) -> bool:
    result = subprocess.run(
        [gh, "release", "view", tag, "--repo", repo],
        cwd=str(cwd),
        text=True,
        capture_output=True,
    )
    return result.returncode == 0


def build_default_notes(version: str) -> str:
    today = dt.date.today().isoformat()
    return (
        f"X4 ShipMatrix v{version} pre-release ({today})\n\n"
        "Assets included:\n"
        "- X4_ShipMatrix_v{version}_Setup.exe (installer)\n"
        "- X4 ShipMatrix.exe (standalone app)\n"
        "- X4_Updater.exe (optional updater)\n"
        "- README_USERS.txt\n"
    ).format(version=version)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build and publish GitHub prerelease in one command")
    parser.add_argument("--repo", default="jongreg288/X4_ShipMatrix", help="GitHub repo (owner/name)")
    parser.add_argument("--version", help="Version without v prefix (defaults to MyAppVersion in .iss)")
    parser.add_argument("--title", help="Release title (default: X4 ShipMatrix v<version>)")
    parser.add_argument("--notes", help="Release notes text")
    parser.add_argument("--notes-file", help="Path to release notes file")
    parser.add_argument("--skip-build", action="store_true", help="Skip build steps and publish existing assets")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    iss_file = project_root / "build_scripts" / "X4_ShipMatrix_Setup.iss"

    version = args.version or detect_version_from_iss(iss_file)
    tag = f"v{version}"
    title = args.title or f"X4 ShipMatrix v{version}"
    gh = find_gh()

    if args.notes and args.notes_file:
        raise ValueError("Use either --notes or --notes-file, not both")

    if not args.skip_build:
        run_command([sys.executable, "build_scripts/build_both.py"], "Building main and updater executables", cwd=project_root)
        run_command([sys.executable, "build_scripts/build_installer.py"], "Building installer executable", cwd=project_root)

    assets = stage_assets(project_root, version)

    run_command([gh, "auth", "status"], "Checking GitHub authentication", cwd=project_root)

    notes_args: list[str]
    if args.notes_file:
        notes_path = Path(args.notes_file)
        if not notes_path.is_absolute():
            notes_path = (project_root / notes_path).resolve()
        notes_args = ["--notes-file", str(notes_path)]
    else:
        notes_text = args.notes or build_default_notes(version)
        notes_args = ["--notes", notes_text]

    asset_args = [str(asset) for asset in assets]

    if release_exists(gh, args.repo, tag, project_root):
        run_command(
            [gh, "release", "upload", tag, *asset_args, "--clobber", "--repo", args.repo],
            f"Updating assets for existing release {tag}",
            cwd=project_root,
        )
        run_command(
            [gh, "release", "edit", tag, "--repo", args.repo, "--title", title, "--prerelease", *notes_args],
            f"Updating metadata for release {tag}",
            cwd=project_root,
        )
    else:
        run_command(
            [gh, "release", "create", tag, *asset_args, "--repo", args.repo, "--title", title, "--prerelease", *notes_args],
            f"Creating prerelease {tag}",
            cwd=project_root,
        )

    result = run_command(
        [gh, "release", "view", tag, "--repo", args.repo, "--json", "url", "--jq", ".url"],
        f"Fetching release URL for {tag}",
        cwd=project_root,
    )

    url = result.stdout.strip()
    print("\nPrerelease automation complete!")
    print(f"Release URL: {url}")
    print("Assets:")
    for asset in assets:
        print(f"- {asset}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"\nError: {exc}")
        raise SystemExit(1)
