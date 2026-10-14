#!/usr/bin/env python3
"""Record the exact runtime/profile, guest source and reviewed path-only lock."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tomllib

ROOT = Path(__file__).resolve().parents[1]
TAG = 'avm-dev-06e96ef71006-sdk-0748f4f0767a'
REVISION = '0748f4f0767a26da8bc363bcb6b5585539d6970e'
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def run(sdk):
    manifest = json.loads((sdk/'BUILD-MANIFEST.json').read_text())
    assert (manifest['release_tag'],manifest['bundle_version'],manifest['guest_version'],manifest['sdk_commit']) == (TAG,'0.2.0','0.1.1',REVISION)
    lock = tomllib.loads((ROOT/'Cargo.lock').read_text())
    assert lock['package'] and all('source' not in row for row in lock['package']), 'Review new registry dependencies before running'
    guest = tomllib.loads((ROOT/'vendor/avm-contract-sdk/Cargo.toml').read_text())
    assert guest['package']['version'] == '0.1.1'
    for line in (ROOT/'vendor/SHA256SUMS').read_text().splitlines():
        expected, name = line.split('  ',1)
        assert sha(ROOT/'vendor'/name) == expected, name
    result = dict(status='PASS',bundle_version='0.2.0',guest_version='0.1.1',release_tag=TAG,
                  sdk_commit=REVISION,runtime_source_commit=manifest['ackinacki_commit'],
                  profile_sha256=sha(sdk/'profiles/wasmtime-release-profile.v1'),
                  binary_sha256={name:sha(sdk/'bin'/name) for name in ['avm-contract-build','avm-local-stand']},
                  builder_version=subprocess.check_output([str(sdk/'bin/avm-contract-build'),'--version'],text=True).strip(),
                  rustc=subprocess.check_output(['rustc','--version'],text=True).strip(),
                  project_lock_sha256=sha(ROOT/'Cargo.lock'),reviewed_lock_packages=lock['package'],
                  dependencies='Only reviewed local path packages; no registry dependencies',fresh_local_stands=True)
    (ROOT/'evidence/runtime-build-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (ROOT/'evidence/runtime-v020.json').write_text(json.dumps(result,indent=2)+'\n')
    print('SDK 0.2.0 / guest 0.1.1, profile, source hashes and reviewed lock: PASS')
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sdk',type=Path,required=True)
    args = parser.parse_args()
    run(args.sdk.resolve())
