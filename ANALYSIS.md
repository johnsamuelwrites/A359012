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

| k | x | y | |P(x,y)| | position of k | relative depth | expansion ratio |
| --- | --- | --- | --- | --- | --- | --- |
| 318 | 31 | 8 | 12 | 0 | 0.000 | 4.0 |
| 557 | 55 | 7 | 13 | 5 | 0.385 | 4.33 |
| 692 | 69 | 2 | 4 | 1 | 0.250 | 1.33 |
| 729 | 72 | 9 | 17 | 7 | 0.412 | 5.67 |
| 2226 | 222 | 6 | 15 | 4 | 0.267 | 3.75 |
| 2437 | 243 | 7 | 17 | 8 | 0.471 | 4.25 |
| 2776 | 277 | 6 | 15 | 1 | 0.067 | 3.75 |
| 3209 | 320 | 9 | 23 | 9 | 0.391 | 5.75 |
| 4436 | 44 | 36 | 50 | 11 | 0.220 | 12.5 |
| 5336 | 53 | 36 | 56 | 41 | 0.732 | 14.0 |
| 5549 | 55 | 49 | 71 | 35 | 0.493 | 17.75 |
| 5718 | 571 | 8 | 23 | 3 | 0.130 | 5.75 |
| 5956 | 59 | 56 | 80 | 16 | 0.200 | 20.0 |
| 6068 | 606 | 8 | 23 | 6 | 0.261 | 5.75 |
| 6141 | 61 | 41 | 66 | 48 | 0.727 | 16.5 |

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

## Multiple Witnesses

- Unique k values in the sequence: 712 (total rows including duplicate splits: 712).
- k values with more than one valid (x, y) split: none in this range.

## Non-Trailing-Zero Outliers

- 708 of 712 witness values end in `0`; 4 do not.
- k=692: P(69,2) = 4692 (ends in `2`)
- k=55383: P(5538,3) = 169755383616 (ends in `6`)
- k=218244: P(21824,4) = 226786921824465024 (ends in `4`)
- k=723293: P(72329,3) = 378372329359224 (ends in `4`)
- Trailing zeros in xPy arise from paired factors of 2 and 5 in the falling factorial product.
  Exceptions occur when y is small enough that no factor of 5 appears in x*(x-1)*...*(x-y+1).

## Prime Terms

- Prime k values: 57 of 712 unique terms (8.0%).
- Primes: 557, 2437, 3209, 6353, 7643, 10889, 26893, 29989, 32233, 40427, 50329, 60397, 75787, 76369, 96289, 177887, 296183, 342757, 356171, 412619 ...

## Gap Analysis

- Gaps between consecutive unique terms: min = 1, max = 26763, average = 1402.4.
- Five largest gaps (from, to, size):
  - 191481 → 218244: gap 26763
  - 142152 → 158776: gap 16624
  - 311794 → 326046: gap 14252
  - 267684 → 279394: gap 11710
  - 180046 → 191481: gap 11435

## Digit Sum and Residues

- Digit sums range from 9 to 47.
- Distribution of (digit sum) mod 9 across unique k values:
  - 0: 72 terms
  - 1: 80 terms
  - 2: 60 terms
  - 3: 81 terms
  - 4: 71 terms
  - 5: 77 terms
  - 6: 77 terms
  - 7: 100 terms
  - 8: 94 terms
- Note: digit_sum ≡ k (mod 9) by casting-out-nines, so this also describes k mod 9.

## Counting Function and Density

- Cumulative term counts at decade boundaries (unique k):
  - below 10^2: 0 terms
  - below 10^3: 4 terms
  - below 10^4: 33 terms
  - below 10^5: 147 terms
  - below 10^6: 712 terms
- Power-law fit to log-log data: count(N) ≈ C · N^α,  estimated α ≈ 0.74.
- α < 1 confirms the sequence is sub-linear (sparser than a fixed proportion of integers).
- Probabilistic model: for a balanced d-digit split, |P(x,y)| ≈ (d/2)·log10(d/2) digits by
  Stirling, so the expected match probability is ~10^(-(d/2)) per candidate — consistent with
  the observed rapid growth as digit length increases.

## Relative Depth Distribution

- Histogram of where k lands inside P(x,y) (10 equal bins over [0, 1]):
  - [0.0, 0.1): 78 terms
  - [0.1, 0.2): 69 terms
  - [0.2, 0.3): 85 terms
  - [0.3, 0.4): 83 terms
  - [0.4, 0.5): 94 terms
  - [0.5, 0.6): 69 terms
  - [0.6, 0.7): 78 terms
  - [0.7, 0.8): 92 terms
  - [0.8, 0.9): 61 terms
  - [0.9, 1.0): 3 terms
- A uniform distribution would place ~10% of terms in each bin.
- Deviations indicate structural biases in where k appears within its witness.
