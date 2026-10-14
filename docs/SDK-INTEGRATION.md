# Proposed SDK-suite integration

Keep the SDK's existing fixtures unchanged. Add the three contract packages as
separate reference applications with the native suite, output-size probe, and
real stand journey. Dependency paths may be adjusted to the SDK's own crate;
canonical ABI metadata, generated IDs, and wire layouts must remain consistent.

Suggested gate:

1. Pin source SDK, published runtime, Rust 1.93.0, and Binaryen 133.
2. Run the native SDK and application tests.
3. Build with the official reproducibility check and deterministic optimization.
4. Validate ABI IDs, exports, lack of host imports, and artifact hashes.
5. Execute the application journey with actual WASM in the packaged stand.
6. Require correct contract statuses, member accounting, matching receiver/audit
   totals, empty queue, and replay roots/fees/count matching the final snapshot.
7. Retain the batch-size CSV without treating output bytes as FUEL measurements.

The additional coverage includes arithmetic at u128 boundaries, deposit-fragmentation
equivalence, partial audit-batch failures, duplicate semantic reports, operation
timelocks, approval replay, and independent pending beneficiary payments.

## Submission description

AVM Revenue Hub is a three-contract Rust SDK reference application: a 2-of-3
governed revenue vault, bound payout receivers, and an AccountBatch receipt ledger.
It demonstrates fixed-share cumulative accounting, independent beneficiary claims,
native failure/refund/retry handling, exact-proposal votes with timelock and expiry,
and narrow coalesced audit patches. The project includes 74 application regression
tests, pinned SDK/tooling, reproducible build and optimization evidence, actual AVM
execution, and reconciled journal replay. It is proposed as an SDK-suite example;
its asset, routing, callback, and audit-delivery limits are documented.

## SDK 0.2.0

See [the standalone compatibility result](SDK-020.md). In-tree integration must
use the current SDK path dependency and reviewed lock, without RUSTC_WRAPPER.
The existing upstream integration PR is #10. Its approval and validation
are separate from these standalone checks.
