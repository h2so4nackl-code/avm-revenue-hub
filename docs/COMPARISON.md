# Why this is a broader SDK example

This compares the earlier delivered `avm-bounty-escrow-v1.zip` with this project.
Both are local, unaudited SDK examples. Complexity and test count alone do not
prove production security or reward eligibility.

| Capability | Earlier Bounty Escrow | Revenue Hub |
| --- | --- | --- |
| Main use | One milestone bounty | Repeated revenue distribution to a fixed group |
| Beneficiaries | One worker and client refund receiver | Up to 16 distinct beneficiary destinations |
| Money authorization | Client approval of submitted delivery hash | Fixed ownership plus individual signed claims |
| Operational governance | No multisig proposal system | 2 of 3 votes, exact proposal binding, timelock, expiry |
| Revenue rounding | Fixed milestone amounts | Cumulative floor entitlements with carried dust |
| Pending transfers | One global transfer at a time | One per member; other members can continue |
| Receipt storage | History of at most 64 transfer attempts | Bounded latest native receipt metadata per member |
| Retry evidence | Failure and retry within the finite attempt budget | 100 failures then a successful retry in a native test |
| Batch execution | None | AccountBatch audit, partial rejection, coalesced state patches |
| Native project tests | 35 | 74 |
| Vendored SDK tests | 12 | 12 |
| Actual AVM application components | Escrow + receiver | Vault + receiver + audit (five deployed instances in demo) |
| Measured state patching | No batch measurement | 1 / 8 / 64 / 256-message output-size probes |
| Final local demo reconciliation | 1,000 = 700 paid + 300 refunded | 10,010 = 5,005 + 3,003 + 2,002, matching audit |

The new receipt design removes the earlier 64-attempt limit by using native
callback provenance and creation-LT boundaries rather than retaining every hash.
Its assurance is limited to the tested runtime and same-DApp routing view; it
does not authenticate arbitrary forged callback envelopes outside that trust model.
