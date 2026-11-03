# Tested environment

Local validation date: 2026-11-03. Full reproduction is validated in a newly created virtual environment after installing requirements.txt; the private delivery report records the actual checks.

- Operating system: Windows, AMD64.
- Python: 3.14.6.
- Backend: Matplotlib Agg (no display required).
- Font: DejaVu Sans shipped with Matplotlib; no standalone font file is included.
- CPU only; no GPU, container engine, model/API account or parent-project input is required.

## Installed test versions

|Package|Version|
|---|---|
|contourpy|1.4.0|
|cycler|0.12.1|
|fonttools|4.68.0|
|kiwisolver|1.5.1|
|matplotlib|3.11.0|
|numpy|2.5.1|
|packaging|26.3|
|pillow|13.0.0|
|pyparsing|3.3.3|
|python-dateutil|4.0.0|
|tzdata|2026.6|

requirements.txt pins the direct plotting dependencies (NumPy and Matplotlib) and the transitive versions resolved in the clean test environment. None of these distributions is vendored.

Analysis-only mode uses the standard library. Full plotting needs the packages in requirements.txt. Python 3.14.6 on Windows is the validated combination; Linux/macOS and other Python versions were not tested. Commands in the README describe the platform-specific interpreter paths without claiming additional validation.

UTF-8 is used for the Chinese anchor and result tables. The runner sets UTF-8 child-process output, disables bytecode cache generation and preserves source/reference files. SVG/PDF dates are suppressed, but only result data and table content are compared across runs; cross-platform rendering is not promised to be byte-identical.
