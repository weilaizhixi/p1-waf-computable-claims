# P1 aggregate-results reproducibility artifact

Version: **v1.0.0**. Prepared on **2026-11-03** for author review; no repository or public release has been created by this preparation.

This artifact accompanies the P1 study on auditing conclusions and evidence in Web Application Firewall (WAF) evaluation. It provides a small, self-contained route from archived aggregate results to checked tables and three English data figures. The input tables and some source comments remain in Chinese; English definitions are in [DATA_DICTIONARY.md](DATA_DICTIONARY.md).

**Rights and citation review remain pending.** See [LICENSE_REVIEW.md](LICENSE_REVIEW.md) and [CITATION.md](CITATION.md). No open-source or open-data license has been selected on the authors' behalf.

## Quick start

With Python available, run these commands from the repository root. On Windows, use `py -3` in place of `python` if needed.

```text
python -B verify_integrity.py
python -B run_reproduction.py --analysis-only --check-reference --output outputs/analysis
```

Analysis requires only the Python standard library. For tables and all three figures:

```text
python -m venv .venv
# Windows PowerShell:
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe -B run_reproduction.py --check-reference --output outputs/full
```

On Linux/macOS, use `.venv/bin/python` instead. That platform path is provided for convenience; the recorded release tests were run on Windows. Choose a new output directory for every run. Existing output directories are refused. No API credentials, model downloads, GPU, Docker, live WAF or paid model calls are required. Dependency installation needs access to a package index; reproduction itself reads local inputs.

See [REPRODUCING.md](REPRODUCING.md) for expected outputs and [ENVIRONMENT.md](ENVIRONMENT.md) for the tested environment.

## Results represented

|Material|Archived observation|
|---|---|
|Main answer classification|493 tasks, 5 route labels, 2 conditions: 4930 response cells|
|Disjoint partition|16 value discrepancies; 4 type-name substitutions; 2 missing-field cells; 747 format-only deviations; 4161 value-and-type-consistent cells|
|Direct/program contrast|48 paired tasks: 46 direct answers correct, 48 program-execution answers correct; 2 direct-wrong/program-correct pairs, 0 reverse pairs|
|Shared replay summary|12 applications, 213 candidate-rule cells: 213 measurement-valid, 211 satisfying the benign-response contract, 141 satisfying example conformance|

The 20 discrepancy cells are the 16 value discrepancies plus 4 type-name substitutions, across 19 tasks. The 2 missing-field cells are separate. The original 500-task analysis and the 484-task post hoc sensitivity remain descriptive. Route labels are archived request identifiers, not independently verified model identities or a model ranking. The prompt conditions were not randomly interleaved. Related inputs and repeated conditions must not be treated as independent observations.

This package reconstructs results **from aggregate inputs**. It does not rerun or independently validate the 5000 selected raw model answers, 681 source references, original instrument checks, changed-input program execution, or live WAF experiments. Those historical observations are described where needed in the anchor; they are not tests performed by this release. The 213-cell replay is shared with the companion deployment study, and example conformance is not a vulnerability-blocking rate.

The paired-task tile arrangement follows the existing H001–H048 ordering assumption: eight tasks per application in the reported application order. Only H007 and H019 are identified as discordant in the anchor. Other tile positions do not provide independently released task-level evidence.

## Contents

- `data/`: three unchanged aggregate CSVs and an exact extract of result sections A–J.
- `code/`: aggregate parsing, cross-checking and table/data generation.
- `plotting/`: three English figure scripts and their shared label/configuration files.
- `reference/`: frozen release-build outputs: 4 JSON files, 8 Markdown tables and 3 figures in PNG/SVG/PDF.
- `run_reproduction.py`, `verify_integrity.py`: safe output entry point and file verification.
- `FILE_MANIFEST.json`, `SHA256SUMS.txt`: file list, sizes and integrity metadata.

Expert blind-review records, reviewer identities, manuscripts, full project exports, raw request/response logs, credentials, budgets, third-party source trees, model weights and Git history are outside this release.

## Integrity and citation

Run `python -B verify_integrity.py` before reproduction. The manifest lists every content file except the manifest and checksum list themselves; the checksum list additionally authenticates the manifest and excludes itself. Its integrity is covered by the separately supplied release ZIP digest. This detects changes relative to the supplied digest; it does not establish authorship or a cryptographic signature.

Consult [CITATION.md](CITATION.md) before citing. Authors, final publication details and a public archive identifier must be supplied by the authors rather than inferred from local filenames.
