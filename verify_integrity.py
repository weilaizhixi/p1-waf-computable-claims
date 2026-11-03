"""Verify the v1.0.0 payload and exact file set using standard-library SHA-256."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOCAL_DIRS = {'.git', '.venv', 'outputs', '__pycache__'}


def main():
    checksums = {}
    for line in (ROOT / 'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
        digest, name = line.split('  ', 1)
        p = Path(name)
        if p.is_absolute() or '..' in p.parts or name in checksums:
            raise ValueError('Invalid or duplicate checksum path: ' + name)
        checksums[name] = digest
    manifest = json.loads((ROOT / 'FILE_MANIFEST.json').read_text(encoding='utf-8'))
    entries = {row['path']: row for row in manifest['files']}
    if len(entries) != len(manifest['files']):
        raise ValueError('Duplicate manifest paths')
    expected = set(entries) | {'FILE_MANIFEST.json'}
    if set(checksums) != expected:
        raise ValueError('Checksum/manifest coverage mismatch')
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()
              and not any(part in LOCAL_DIRS for part in p.relative_to(ROOT).parts)}
    if actual != expected | {'SHA256SUMS.txt'}:
        raise ValueError('Unexpected/missing payload files: ' + repr(sorted(actual ^ (expected | {'SHA256SUMS.txt'}))))
    for name, expected_hash in checksums.items():
        p = ROOT / name
        if p.is_symlink():
            raise ValueError('Symlinks are not allowed: ' + name)
        raw = p.read_bytes()
        if hashlib.sha256(raw).hexdigest() != expected_hash:
            raise ValueError('SHA-256 mismatch: ' + name)
        if name in entries and (len(raw) != entries[name]['bytes'] or expected_hash != entries[name]['sha256']):
            raise ValueError('Manifest mismatch: ' + name)
    print('INTEGRITY PASS: ' + str(len(checksums)) + ' SHA-256 checks; exact payload file set verified.')


if __name__ == '__main__':
    main()
