# A359012 Analysis

CSV source: `A359012.csv`
Terms found: 712

## Observed Properties

- Sparsity: only 712 terms appear below 1000000.
- Term lengths: 3-digit terms: 4, 4-digit terms: 29, 5-digit terms: 114, 6-digit terms: 565.
- Split types `(len(x), len(y))`: (2, 1): 4, (2, 2): 21, (3, 1): 8, (3, 2): 103, (3, 3): 391, (4, 1): 11, (4, 2): 162, (5, 1): 12.
- `y` digit lengths: 1-digit cases: 35, 2-digit cases: 286, 3-digit cases: 391.
- Substring placement in `xPy`: 3 prefix hits, 1 suffix hits, 708 strictly internal hits.
- Trailing-zero bias: 708 of 712 permutation values end in `0`.
- Digit repetition: 572 terms have repeated digits; 140 have all digits distinct.
- Palindromes: 9999, 29092, 343343, 805508.
- Smallest permutation length: 4 digits (term(s): 692).
- Largest permutation length: 2506 digits (term(s): 981972).
- Repeated `y` values: 80 (11), 56 (8), 8 (8), 83 (8), 94 (8), 48 (7), 6 (7), 72 (7), 81 (7), 86 (7), ...

## Aggregate Measures

- Average substring position inside `P(x,y)`: 372.5 digits from the start.
- Average expansion ratio `|P(x,y)| / |k|`: 137.1x.
- Smallest expansion ratio: 1.33x for `k=692`; largest: 417.67x for `k=981972`.

## Examples

| k | x | y | |P(x,y)| | position of k |
| --- | --- | --- | --- | --- |
| 318 | 31 | 8 | 12 | 0 |
| 557 | 55 | 7 | 13 | 5 |
| 692 | 69 | 2 | 4 | 1 |
| 729 | 72 | 9 | 17 | 7 |
| 2226 | 222 | 6 | 15 | 4 |
| 2437 | 243 | 7 | 17 | 8 |
| 2776 | 277 | 6 | 15 | 1 |
| 3209 | 320 | 9 | 23 | 9 |
| 4436 | 44 | 36 | 50 | 11 |
| 5336 | 53 | 36 | 56 | 41 |
| 5549 | 55 | 49 | 71 | 35 |
| 5718 | 571 | 8 | 23 | 3 |
| 5956 | 59 | 56 | 80 | 16 |
| 6068 | 606 | 8 | 23 | 6 |
| 6141 | 61 | 41 | 66 | 48 |

The table shows the first 15 terms only; the CSV remains the full source dataset.

## Factorial Cases

Terms where x == y (so P(x,y) = x!): 9999 (x=y=99), 343343 (x=y=343).

## Conjecture Starters

- The sequence appears sparse, so estimating its counting function may be interesting.
- Balanced splits seem favored: `(2, 2)` dominates the current search window.
- Most witnesses are internal substrings rather than prefix or suffix matches.
- Decimal trailing-zero structure in `xPy` may strongly influence where matches can occur.
- The digit expansion ratio grows rapidly; for large k, P(x,y) has tens of times more
  digits than k, making a substring match increasingly likely by pure probability -
  yet the sequence remains sparse because valid splits are structurally constrained.
