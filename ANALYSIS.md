# A359012 Analysis

Search bound: terms `k` with `10 <= k < 10000`
Terms found: 33

## Terms

318, 557, 692, 729, 2226, 2437, 2776, 3209, 4436, 5336, 5549, 5718, 5956, 6068, 6141, 6353, 6958, 7045, 7046, 7338, 7345, 7643, 7865, 8261, 8409, 9153, 9178, 9242, 9544, 9569, 9664, 9894, 9999

## Observed Properties

- Sparsity: only 33 terms appear below 10000.
- Term lengths: 3-digit terms: 4, 4-digit terms: 29.
- Split types `(len(x), len(y))`: (2, 1): 4, (2, 2): 21, (3, 1): 8.
- `y` digit lengths: 1-digit cases: 12, 2-digit cases: 21.
- Substring placement in `xPy`: 1 prefix hits, 1 suffix hits, 31 strictly internal hits.
- Trailing-zero bias: 32 of 33 permutation values end in `0`.
- Digit repetition: 17 terms have repeated digits; 16 have all digits distinct.
- Palindromes: 9999.
- Smallest permutation length: 4 digits (term(s): 692).
- Largest permutation length: 156 digits (term(s): 9999).
- Repeated `y` values: 8 (4), 9 (3), 36 (2), 45 (2), 53 (2), 6 (2), 7 (2).

## Conjecture Starters

- The sequence appears sparse, so estimating its counting function may be interesting.
- Balanced splits seem favored: `(2, 2)` dominates the current search window.
- Most witnesses are internal substrings rather than prefix or suffix matches.
- Decimal trailing-zero structure in `xPy` may strongly influence where matches can occur.
