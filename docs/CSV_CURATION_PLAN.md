# CSV Curation Plan

This is a lightweight plan for future CSV edits (for example, excluding Khaak or selected Xenon entries).

## Goal

Keep runtime CSV files as the single source for end-user data while supporting controlled exclusions.

## Suggested workflow

1. Edit source CSV files in `data/csv_cache/`.
2. Keep an exclusion list in version control (for example, by ship id or faction).
3. Run a validation pass to confirm:
   - expected factions are excluded,
   - required ship/prop rows still exist,
   - no empty required columns.
4. Rebuild and republish with:

```powershell
python build_scripts/release_prerelease.py
```

## Suggested checks

- `ships.csv`: verify no rows where faction is excluded.
- `engines.csv`, `shields.csv`, `weapons.csv`, `turrets.csv`: ensure not empty.
- Optional: keep row count baselines and alert when count drops unexpectedly.

## Notes

This repo now runs in CSV-first mode, so CSV changes directly affect released runtime behavior.
