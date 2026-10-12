#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
sdk="${1:-$root/.runtime/avm-sdk-linux-x86_64}"
optimizer="${2:-$root/.runtime/binaryen-version_133/bin/wasm-opt}"
sdk="$(cd "$sdk" && pwd)"
cd "$root"
mkdir -p evidence
rustc --version
cargo fmt -p avm-revenue-core -p avm-revenue-vault -p avm-revenue-receiver -p avm-revenue-audit -p avm-revenue-tests -- --check
cargo clippy --workspace --all-targets --offline -- -D warnings 2>&1 | tee evidence/clippy-native.txt
cargo test --workspace --offline 2>&1 | tee evidence/native-tests.txt
bash scripts/build.sh "$sdk" "$optimizer"
for contract in vault receiver audit; do
  cargo clippy -p "avm-revenue-$contract" --target wasm32-unknown-unknown --offline -- -D warnings 2>&1 | tee "evidence/clippy-wasm-$contract.txt"
done
cargo run -p avm-revenue-tests --bin batch_probe --offline > evidence/batch-probe.csv
python3 scripts/e2e.py --sdk "$sdk"
python3 scripts/verify_artifacts.py
echo "All revenue hub checks passed."
