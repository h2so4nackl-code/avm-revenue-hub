#!/usr/bin/env python3
"""Summarize fresh SDK 0.2.0 checks without replacing the full stand journal."""
import gzip
import hashlib
import json
from pathlib import Path
import re
import shutil
import tomllib

ROOT = Path(__file__).resolve().parents[1]
def write(path, value):
    path.write_text(json.dumps(value,indent=2)+'\n')
def run():
    runtime = json.loads((ROOT/'evidence/runtime-v020.json').read_text())
    journey_path = ROOT/'evidence/avm-e2e.json'
    journey = json.loads(journey_path.read_text())
    assert runtime['status'] == journey['status'] == 'PASS'
    state_limits = json.loads((ROOT/'evidence/state-limits-sdk020.json').read_text())
    guest_modes = json.loads((ROOT/'evidence/audit-guest-modes.json').read_text())
    assert state_limits['status'] == guest_modes['status'] == 'PASS'
    assert not state_limits['candidate_executed'] and not state_limits['mainnet_deployment']
    counts = [int(n) for n in re.findall(r'test result: ok\. (\d+) passed;', (ROOT/'evidence/native-tests.txt').read_text())]
    assert counts and 9 in counts and 4 in counts
    members = tomllib.loads((ROOT/'Cargo.toml').read_text())['workspace']['members']
    expected, project = next((count,name) for member,count,name in [
        ('contracts/escrow',35,'avm-bounty-escrow'),('contracts/vault',80,'avm-revenue-hub'),
        ('contracts/vesting',60,'avm-vesting-streams')] if member in members)
    assert sum(counts) == expected+13, counts
    keys = ['account_state_root','registry_root','accepted_input_count','cumulative_fee_shells']
    for key in keys:
        assert journey['inspect'][key] == journey['replay'][key],key
    assert journey['inspect']['queue']['message_count'] == 0
    compressed = gzip.compress(journey_path.read_bytes(),compresslevel=9,mtime=0)
    (ROOT/'evidence/avm-e2e.json.gz').write_bytes(compressed)
    summary = {key:value for key,value in journey.items() if key not in ['journal','inspect','replay','events']}
    summary['inspect'] = {key:journey['inspect'][key] for key in keys}
    summary['replay'] = {key:journey['replay'][key] for key in keys}
    summary['queue_message_count'] = 0
    summary['full_journal'] = 'avm-e2e.json.gz'
    write(ROOT/'evidence/avm-e2e-summary.json',summary)
    artifacts = json.loads((ROOT/'evidence/artifacts.json').read_text())
    assert artifacts['status'] == 'PASS'
    assert guest_modes['wasm_sha256'] == artifacts['contracts']['audit']['sha256']['contract.wasm']
    for contract in artifacts['contracts']:
        directory = ROOT/'contracts'/contract/'target'
        shutil.copyfile(directory/'avm-build-provenance.txt',ROOT/'evidence'/f'build-provenance-{contract}.txt')
    provenance = dict(sdk_repository='https://github.com/gosh-sh/avm-sdk',sdk_bundle_version='0.2.0',
                      guest_sdk_version='0.1.1',vendored_sdk_commit=runtime['sdk_commit'],
                      runtime_release_tag=runtime['release_tag'],runtime_sdk_commit=runtime['sdk_commit'],
                      runtime_source_commit=runtime['runtime_source_commit'],
                      runtime_archive_sha256='8728497cf1e476d3d770a09b19929f7c196f2637654642727432b4c285c85143',
                      rust_toolchain='1.93.0',target='wasm32-unknown-unknown',
                      profile_sha256=runtime['profile_sha256'],project_lock_sha256=runtime['project_lock_sha256'],
                      vendor_source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                                            for p in sorted((ROOT/'vendor').rglob('*')) if p.is_file() and p.name!='SHA256SUMS'})
    write(ROOT/'PROVENANCE.json',provenance)
    validation = dict(status='PASS',project=project,sdk_bundle_version='0.2.0',guest_sdk_version='0.1.1',
                      project_tests=expected,sdk_tests=13,total_tests=expected+13,
                      state_limits_evidence='state-limits-sdk020.json',
                      audit_guest_modes_evidence='audit-guest-modes.json',
                      audit_state_limits=journey['audit_state_limits'],
                      candidate_runtime_executed=False,
                      actual_avm_accounting=journey['accounting'],replay_roots_fees_and_count_match=True,
                      queue_message_count=0,fresh_local_stand=True,full_journal='avm-e2e.json.gz',
                      full_journal_sha256=hashlib.sha256(compressed).hexdigest(),
                      artifacts=artifacts['contracts'],runtime_scope='Published SDK 0.2.0 local stand; synthetic principal, same DApp',
                      mainnet_deployment=False,upstream_approval_claimed=False)
    write(ROOT/'evidence/VALIDATION.json',validation)
    print(f'SDK 0.2.0 summary PASS: {expected} application + 13 SDK = {expected+13} tests; actual AVM journey/replay PASS')
if __name__ == '__main__':
    run()
