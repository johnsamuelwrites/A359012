# A359012
Experiments on the integer sequence [A359012](https://oeis.org/A359012)

A359012 consists of a sequence of numbers k that are a substring of xPy where k=concatenation(x,y) and xPy is the number of permutations.

If x,y,k are natural numbers and k is formed by the concatenation of the digits of x followed by those of y, i.e., k = concatenation(x,y), then k belongs to A359012, if xPy contains the number k.


The first eight numbers are given below:
|k|x|y|permutations|
|-|-|-|-|
|318|31|8|318073392000|
|557|55|7|1022755734000|
|692|69|2|4692|
|729|72|9|30885807297945600|
|2226|222|6|111822261510960|
|2437|243|7|45853567243767360|
|2776|277|6|427763435299200|
|3209|320|9|31408938532094015692800|

## Repository Contents
- [`A359012.py`](./A359012.py): brute-force generators for the sequence and an annotated length table.
- [`main.py`](./main.py): exports the sequence data to CSV files.
- [`A359012.csv`](./A359012.csv): generated terms and their witnessing permutation values below `10^4`.
- [`A359012_length.csv`](./A359012_length.csv): the same search with digit-length annotations.
- [`analyze_sequence.py`](./analyze_sequence.py): computes a small mathematical summary and writes [`ANALYSIS.md`](./ANALYSIS.md).
- [`tests/test_a359012.py`](./tests/test_a359012.py): regression tests for known terms and basic generator behavior.

## Observed Properties Below 10000
Using the current brute-force search bound `10 <= k < 10^4`, the repository finds 33 terms.

- The sequence is sparse in this range.
- Four terms have 3 digits and twenty-nine have 4 digits.
- Balanced splits are common: `(len(x), len(y)) = (2, 2)` occurs 21 times.
- Only one current witness is a prefix match inside `xPy` (`318`); the others are internal substring hits.
- 32 of the 33 witness values `xPy` end in `0`.
- Repeated-digit terms are slightly more common than all-distinct-digit terms in the current data.

See [`ANALYSIS.md`](./ANALYSIS.md) for the generated summary.

## Reproduce
Generate the CSV files:

```bash
python main.py
```

Generate the analysis summary:

```bash
python analyze_sequence.py
```

Run the tests:

```bash
pytest -q
```

## Possible Next Questions
- How does the counting function grow with the search bound?
- Does the dominance of balanced splits persist for larger ranges?
- Can the trailing-zero bias be explained directly from the arithmetic of `xPy`?
- Are there infinite families of terms with repeated digits or special endings?

## Author
- John Samuel

## Archives and Releases
- [Zenodo](https://doi.org/10.5281/zenodo.7513671)
- [Release Notes](RELEASE.md)

## Licence
All code are released under GPLv3+ licence. The associated documentation and other content are released under [CC-BY-SA](http://creativecommons.org/licenses/by-sa/4.0/).
