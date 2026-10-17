#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
sdk="${1:-$root/.runtime/avm-sdk-linux-x86_64}"
optimizer="${2:-$root/.runtime/binaryen-version_133/bin/wasm-opt}"
sdk="$(cd "$sdk" && pwd)"
cd "$root"
mkdir -p evidence
rustc --version
python3 scripts/runtime_info.py --sdk "$sdk"
cargo fmt -p avm-revenue-core -p avm-revenue-vault -p avm-revenue-receiver -p avm-revenue-audit -p avm-revenue-tests -- --check
cargo clippy --workspace --all-targets --locked --offline -- -D warnings 2>&1 | tee evidence/clippy-native.txt
cargo test --workspace --locked --offline 2>&1 | tee evidence/native-tests.txt
bash scripts/build.sh "$sdk" "$optimizer"
for contract in vault receiver audit; do
  cargo clippy -p "avm-revenue-$contract" --target wasm32-unknown-unknown --locked --offline -- -D warnings 2>&1 | tee "evidence/clippy-wasm-$contract.txt"
done
cargo run -p avm-revenue-tests --bin batch_probe --locked --offline > evidence/batch-probe.csv
python3 scripts/e2e.py --sdk "$sdk"
bash scripts/check_state_limits.sh "$sdk"
python3 scripts/verify_artifacts.py
python3 scripts/summarize.py
echo "All revenue hub checks passed."
