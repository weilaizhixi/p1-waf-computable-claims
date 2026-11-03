# Reproduction

## Inputs and scope

Run commands from the repository root unless an absolute script/output path is used. Analysis reads only `data/results_anchor_A-J.md` and the three CSVs in `data/`. Plotting additionally reads `plotting/chart_translation_map.json` and the generated figure JSON files. No parent-project files are needed.

The anchor retains the Chinese research tables, cases and qualifications without changing their numbers. It omits internal historical audit/cost sections K and L. The original aggregate calculation and classification logic is retained; release adaptations affect paths, output management, excluded metadata and font/output metadata only.

## Commands

```text
python -B verify_integrity.py
python -B run_reproduction.py --analysis-only --check-reference --output outputs/analysis
python -m pip install -r requirements.txt
python -B run_reproduction.py --check-reference --output outputs/full
```

A virtual environment is recommended for plotting; see the README. Use `py -3` on Windows if `python` is unavailable. Do not use `-O` or `PYTHONOPTIMIZE`, because research assertions must be enabled. The runner refuses optimized mode, existing output directories and outputs under protected source/reference directories. A failure may leave a partial output directory: inspect it and choose a new name for the next run.

The entry point works from other working directories too. Pass an absolute path to `run_reproduction.py`; relative `--output` paths are resolved from the caller's working directory. The runner controls `P1_OUTPUT_DIR` for its child scripts. Use the runner rather than invoking individual generation scripts, which are internal components and do not provide the same existing-output protection.

## Expected checks and files

A successful run reports **98 aggregate cross-checks, 0 failures**, then **8 output constraints**. With `--check-reference`, it compares the complete content of four JSON results and the exact bytes of eight tables to the shipped reference. Only `generated_at` in `all_results.json` is ignored. These are release-level checks of aggregate consistency, not historical experiment validation.

Both modes produce:

- `all_results.json`;
- `fig_partition_data.json`, `fig_exec_paired_data.json`, `fig_replay_conditions_data.json`;
- `TABLE_corpus.md`, `TABLE_partition.md`, `TABLE_route_counts.md`, `TABLE_cases.md`;
- `TABLE_sensitivity.md`, `TABLE_exec_control.md`, `TABLE_discordant.md`, `TABLE_failure_chains.md`.

Full mode also produces `fig_partition`, `fig_exec_paired` and `fig_replay_conditions`, each as PNG, SVG and PDF. The figures use DejaVu Sans supplied with Matplotlib. Small rendering differences across library/platform versions do not imply changed result data. The reference comparison checks figure JSON, not image bytes.

Key invariants are `4930 = 16 + 4 + 2 + 747 + 4161`, direct/program totals `48/46/48/2/0`, and replay totals `213/213/211/141`.

## Integrity coverage

The manifest covers all content files; it excludes `FILE_MANIFEST.json` and `SHA256SUMS.txt` to avoid recursive hashing. The checksum list covers content plus the manifest, excluding itself. The separate ZIP checksum covers the archive containing both metadata files. The verifier rejects missing/changed/unexpected files, apart from local `.git`, `.venv`, `outputs` and `__pycache__` directories. Do not upload those local directories.

Do not edit or regenerate the frozen `reference/` directory to make a failing run pass. Document any intended changes and rebuild the release integrity metadata before distributing a modified package.
