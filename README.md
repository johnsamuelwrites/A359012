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
- [`A359012.py`](./A359012.py): brute-force generator for the sequence plus helpers for derived annotations.
- [`main.py`](./main.py): exports the canonical sequence data to a single CSV file.
- [`A359012.csv`](./A359012.csv): the source dataset of generated terms, digit-length annotations, and row-level analysis fields below `10^6`.
- [`analyze_sequence.py`](./analyze_sequence.py): computes a compact mathematical summary from [`A359012.csv`](./A359012.csv) and writes [`ANALYSIS.md`](./ANALYSIS.md).
- [`index.html`](./index.html): an interactive D3-powered website for exploring the sequence visually.
- [`assets/site.js`](./assets/site.js) and [`assets/site.css`](./assets/site.css): the browser-side logic and styling for the website.
- [`assets/logo.svg`](./assets/logo.svg) and [`assets/favicon.svg`](./assets/favicon.svg): the visual identity for the site and browser tab.
- [`tests/test_a359012.py`](./tests/test_a359012.py): regression tests for known terms and basic generator behavior.

## Observed Properties Below 1000000
Using the current brute-force search bound `10 <= k < 10^6`, the repository finds 712 terms.

- The sequence is still sparse in this larger range: only 712 terms appear below one million.
- Term lengths are now distributed as 4 three-digit terms, 29 four-digit terms, 114 five-digit terms, and 565 six-digit terms.
- Balanced longer splits dominate the current data, especially `(3, 3)` with 391 cases and `(4, 2)` with 162 cases.
- Substring hits are overwhelmingly internal: 3 prefix hits, 1 suffix hit, and 708 strictly internal hits.
- 708 of the 712 witness values `xPy` end in `0`.
- Repeated-digit terms now dominate strongly: 572 terms have repeated digits, while 140 have all digits distinct.
- Palindromic terms do occur: `9999`, `29092`, `343343`, and `805508`.

See [`ANALYSIS.md`](./ANALYSIS.md) for the generated summary.

## Reproduce
Generate the CSV source:

```bash
python main.py
```

Generate the analysis summary from the CSV source:

```bash
python analyze_sequence.py
```

Preview the website locally:

```bash
python -m http.server
```

Then open `http://localhost:8000`.

Deploy the website with GitHub Pages:

- The workflow [`deploy-site.yml`](./.github/workflows/deploy-site.yml) publishes the static site on pushes to `main`.
- The deployment uploads `index.html`, `assets/`, `A359012.csv`, and supporting markdown files as the Pages artifact.

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
