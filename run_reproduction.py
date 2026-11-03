"""Rebuild P1 aggregate tables and figures into a new directory."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
RESULT_FILES = ['all_results.json', 'fig_partition_data.json', 'fig_exec_paired_data.json',
                'fig_replay_conditions_data.json']
TABLE_FILES = ['TABLE_corpus.md', 'TABLE_partition.md', 'TABLE_route_counts.md',
               'TABLE_cases.md', 'TABLE_sensitivity.md', 'TABLE_exec_control.md',
               'TABLE_discordant.md', 'TABLE_failure_chains.md']


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('outputs/run'),
                        help='New directory; relative paths are relative to the current working directory.')
    parser.add_argument('--analysis-only', action='store_true', help='Skip NumPy/Matplotlib plotting.')
    parser.add_argument('--check-reference', action='store_true', help='Compare result content with shipped reference outputs.')
    args = parser.parse_args()
    if sys.flags.optimize:
        parser.error('Do not use -O or PYTHONOPTIMIZE: research assertions must remain enabled.')
    output = args.output.resolve()
    if output.exists():
        parser.error('Output already exists. Choose a fresh directory; no outputs are overwritten.')
    for name in ('code', 'data', 'plotting', 'reference', '.git', '.venv'):
        protected = ROOT / name
        if output == protected or protected in output.parents:
            parser.error('Output must be outside protected source/reference directories.')
    output.mkdir(parents=True)
    env = dict(os.environ, P1_OUTPUT_DIR=str(output), PYTHONDONTWRITEBYTECODE='1',
               PYTHONIOENCODING='utf-8', MPLBACKEND='Agg')
    scripts = ['code/main.py', 'code/sanity_check.py']
    if not args.analysis_only:
        scripts += ['plotting/gen_fig_partition_en.py', 'plotting/gen_fig_exec_paired_en.py',
                    'plotting/gen_fig_replay_conditions_en.py']
    for script in scripts:
        subprocess.run([sys.executable, *(['-S'] if sys.flags.no_site else []), '-B', str(ROOT / script)], env=env, check=True)
    if args.check_reference:
        for name in RESULT_FILES:
            actual = json.loads((output / name).read_text(encoding='utf-8'))
            expected = json.loads((ROOT / 'reference' / name).read_text(encoding='utf-8'))
            # Only generation time changes. Anchor hash, counts, notes and checks remain compared.
            if name == 'all_results.json':
                actual.pop('generated_at', None)
                expected.pop('generated_at', None)
            if actual != expected:
                raise ValueError('Reference JSON mismatch: ' + name)
        for name in TABLE_FILES:
            if (output / name).read_bytes() != (ROOT / 'reference' / name).read_bytes():
                raise ValueError('Reference table mismatch: ' + name)
        print('REFERENCE COMPARISON PASS: 4 JSON results and 8 tables.')
    print('REPRODUCTION PASS' + (' (analysis only)' if args.analysis_only else ' (analysis and 3 figures)'))


if __name__ == '__main__':
    main()
