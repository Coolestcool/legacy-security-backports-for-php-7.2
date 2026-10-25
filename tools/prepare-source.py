#!/usr/bin/env python3
"""Validate vendor patches in temporary target-file copies; apply only on request."""
import argparse
import hashlib
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

REPO = Path(__file__).resolve().parents[1]


def prepare(source, apply=False):
    source = source.resolve(strict=True)
    header = (source / 'main/php_version.h').read_text()
    match = re.search(r'^#define\s+PHP_VERSION\s+"(7\.2\.34)"\s*$', header, re.M)
    if not match:
        raise ValueError('Expected exact PHP_VERSION 7.2.34')
    version = match.group(1)
    checksums = {}
    for line in (REPO / 'SHA256SUMS').read_text().splitlines():
        digest, name = line.split(None, 1)
        checksums[name.strip()] = digest
    for name, digest in checksums.items():
        if hashlib.sha256((REPO / name).read_bytes()).hexdigest() != digest:
            raise ValueError('Checksum mismatch: ' + name)
    names = ['php72-prerequisite-ZSTR_MAX_LEN.patch', 'php72-php2shell.patch']
    text = (source / 'Zend/zend_string.h').read_text()
    found = [bool(re.search(r'^\s*#\s*define\s+' + macro + r'\b', text, re.M)) for macro in ['ZSTR_MAX_OVERHEAD', 'ZSTR_MAX_LEN']]
    if any(found) and not all(found):
        raise ValueError('Partial ZSTR_MAX_LEN prerequisite; review source first')
    if all(found):
        names.pop(0)
    patches = [REPO / 'patches' / n for n in names]
    paths = set()
    for patch in patches:
        for name in re.findall(r'^\+\+\+ b/(\S+)$', patch.read_text(), re.M):
            p = Path(name)
            if p.is_absolute() or '..' in p.parts or '.git' in p.parts:
                raise ValueError('Unsafe patch target: ' + name)
            target = source / p
            if not target.is_file() or target.resolve() != target or not source in target.parents:
                raise ValueError('Missing or symlinked source target: ' + name)
            paths.add(p)
    if not paths:
        raise ValueError('No patch targets found')
    with tempfile.TemporaryDirectory(prefix='legacy-source-check-') as temp:
        staged = Path(temp)
        for relative in paths:
            target = staged / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / relative, target)
        for patch in patches:
            result = subprocess.run(['patch', '--batch', '--forward', '--fuzz=0', '-p1', '-i', str(patch)], cwd=staged, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            if result.returncode:
                raise ValueError(patch.name + ' rejected; input source left unchanged\n' + result.stdout)
        if apply:
            # The complete patch sequence has succeeded before any input source write.
            # This writes source files only; use a disposable backed-up working tree.
            for relative in sorted(paths):
                shutil.copyfile(staged / relative, source / relative)
    print(('APPLIED' if apply else 'CHECKED; source unchanged') + ': PHP ' + version + '; ' + ', '.join(names))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path, help='Disposable PHP 7.2.34 source working tree')
    parser.add_argument('--apply', action='store_true', help='Write patched files to the source tree after complete preflight')
    args = parser.parse_args()
    try:
        prepare(args.source, args.apply)
    except (OSError, ValueError) as exc:
        sys.exit('ERROR: ' + str(exc))
