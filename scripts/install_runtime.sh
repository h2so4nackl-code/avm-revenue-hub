#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
runtime_dir="${1:-$root/.runtime}"
tag="avm-dev-06e96ef71006-sdk-0748f4f0767a"
expected="8728497cf1e476d3d770a09b19929f7c196f2637654642727432b4c285c85143"
if [[ "$(uname -s)" != Linux || "$(uname -m)" != x86_64 ]]; then
  echo "SDK 0.2.0 requires Linux x86-64-v3, glibc >=2.39 (Windows: use WSL2)." >&2
  exit 2
fi
python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else "Python >=3.11 required")'
mkdir -p "$runtime_dir"
runtime_dir="$(cd "$runtime_dir" && pwd)"
if [[ -e "$runtime_dir/avm-sdk-linux-x86_64" && ! -L "$runtime_dir/avm-sdk-linux-x86_64" ]]; then
  echo "Use a fresh runtime directory; the existing historical bundle is retained." >&2
  exit 2
fi
download="$runtime_dir/downloads/$tag"
mkdir -p "$download"
archive="$download/avm-sdk-linux-x86_64.tar.gz"
if [[ ! -f "$archive" ]]; then
  curl -fL --retry 2 --max-time 180 \
    "https://github.com/gosh-sh/avm-sdk/releases/download/$tag/avm-sdk-linux-x86_64.tar.gz" \
    -o "$archive"
fi
printf '%s  %s\n' "$expected" "$archive" | sha256sum -c -
printf '%s  %s\n' "$expected" avm-sdk-linux-x86_64.tar.gz > "$archive.sha256"
# Upstream verifier from the immutable SDK commit checks the complete package
# and identity bindings before extraction and activation.
python3 "$root/vendor/sdk-release-verifier.py" install \
  --archive "$archive" --checksum "$archive.sha256" --tag "$tag" \
  --sdk-home "$runtime_dir/sdk" --bin-dir "$runtime_dir/bin"
ln -sfn "$runtime_dir/sdk/current" "$runtime_dir/avm-sdk-linux-x86_64"
echo "Verified SDK 0.2.0 ready: $runtime_dir/avm-sdk-linux-x86_64"
