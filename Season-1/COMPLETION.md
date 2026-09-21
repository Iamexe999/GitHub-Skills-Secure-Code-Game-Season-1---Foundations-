# Season 1: Foundations — verification

Run from the repository root:

```sh
python3 -m pip install flask bcrypt
python3 Season-1/verify.py
```

The runner uses a temporary copy and a fresh exercise database. It exits on any failure.
All original functionality tests are retained. The C exploit's output is checked because
its original program returns exit code zero even when privilege escalation succeeds.
C programs also run with UndefinedBehaviorSanitizer.

| Level | Fix | Verification |
|---|---|---|
| 1: Cyber Monday | Decimal arithmetic, separate totals, finite amounts, quantity and total limits | 5 functionality + 3 exploit + 3 regression tests |
| 2: Matrix | Lower and upper array bounds, complete integer parsing, account validation and ID allocation | Original tests and exploit + assertion-based capacity/bounds regression |
| 3: Social Network | Canonical paths constrained to the document root, including symlink resolution | 2 functionality + 2 exploit + 2 regression tests |
| 4: Data Bank | Parameter binding; arbitrary scripts replaced with a narrow read-only request parser | 6 functionality + 1 corrected exploit + 3 regression tests |
| 5: Locanda | secrets.choice, bcrypt salts, environment secret, salted password hashing | 2 functionality + 3 regression tests |

## Test correction and compatibility notes

`Level-4/hack.py` originally required a malicious string to produce exactly the response
for the legitimate symbol `MSFT`. Parameter binding correctly treats the entire string
as an unknown symbol. The revised assertion requires no returned rows, no script
execution marker, and an unchanged MSFT price. Additional regressions cover table
removal, boolean injection, unauthorized scripts, and fractional prices.

The Level 5 `MD5_hasher` name remains for the original API test, but its implementation
uses salted bcrypt over a SHA-256 prehash. It does not create or accept MD5 digests.
Existing MD5 passwords would require a reset. The training SECRET_KEY was removed
from active code; a real exposed key would also require rotation.

Path containment assumes the local filesystem is trusted while a file is opened;
it is not a replacement for per-user authorization or protection against concurrent
filesystem changes by a local attacker.

## Evidence

See the **Season 1 completed challenges** Actions run for independently rerun output.
`verification-output.txt` records the local run. CodeQL status is recorded after the
repository analysis finishes; intentionally vulnerable examples in other seasons and
reference solution files are outside this assignment.
