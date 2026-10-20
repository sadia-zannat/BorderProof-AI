"""Verify SHA-256 hashes of all shipped release files, excluding the manifest itself."""
from __future__ import annotations
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'SOURCE_MANIFEST_SHA256.txt'

def release_files():
    files = []
    for item in ROOT.rglob('*'):
        if not item.is_file():
            continue
        rel = item.relative_to(ROOT)
        if any(part in {'.git', 'runtime', '.pytest_cache', '__pycache__', 'node_modules', '.next', '.venv', '.hypothesis'} for part in rel.parts):
            continue
        if item.name in {'SOURCE_MANIFEST_SHA256.txt', '.env', '.env.local'} or item.suffix in {'.pyc', '.pyo', '.tsbuildinfo'} or item.name.endswith('.sqlite3'):
            continue
        files.append(rel.as_posix())
    return sorted(files)

def main():
    entries = {}
    for line in MANIFEST.read_text(encoding='utf-8').splitlines():
        if not line.strip() or line.startswith('#'):
            continue
        digest, rel = line.split('  ', 1)
        if rel in entries:
            raise SystemExit(f'DUPLICATE ENTRY {rel}')
        entries[rel] = digest
    expected = set(release_files())
    if expected != entries.keys():
        raise SystemExit(f'FILE SET MISMATCH: extra={sorted(entries.keys()-expected)} missing={sorted(expected-entries.keys())}')
    for rel, digest in entries.items():
        observed = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        if observed != digest:
            raise SystemExit(f'HASH MISMATCH {rel}')
    print(f'PASS source manifest: {len(entries)} entries, all SHA-256 hashes verified')

if __name__ == '__main__':
    main()
