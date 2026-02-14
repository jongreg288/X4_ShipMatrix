# Build and Release Workflow

This document defines the canonical build and release flow for this repository.

## Canonical entrypoint

Run from project root:

```powershell
python build_scripts/release_prerelease.py
```

What this does:
- Builds `X4 ShipMatrix.exe`
- Builds `X4_Updater.exe`
- Builds installer `X4_ShipMatrix_v<version>_Setup.exe`
- Stages assets in `releases/latest`
- Creates or updates GitHub prerelease `v<version>`

Optional flags:

```powershell
python build_scripts/release_prerelease.py --skip-build
python build_scripts/release_prerelease.py --notes-file release_notes.md
python build_scripts/release_prerelease.py --version 0.2.2
```

## Script status map

### Primary (use these)
- `build_scripts/release_prerelease.py` (single-command release pipeline)
- `build_scripts/build_both.py` (build app + updater only)
- `build_scripts/build_installer.py` (installer only)

### Legacy (supported, not preferred)
- `build_scripts/build.py`
- `build_scripts/build_exe.py`
- `build_scripts/prepare_installer_files.py`

Legacy implementations are archived in `build_scripts/legacy/`, while the original script paths are compatibility wrappers.
New workflows should use the primary scripts above.

## Folder intent

- `src/`: runtime application code
- `build_scripts/`: packaging and release tooling
- `docs/`: project and release documentation
- `releases/latest/`: staged binaries for GitHub release upload
