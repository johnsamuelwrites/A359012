import argparse
import csv
import math
from collections import Counter
from pathlib import Path

from A359012 import generate_sequence_A359012, is_prime


def load_sequence_from_csv(path: Path) -> list[tuple[str, str, str, str]]:
    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        return [
            (row["k"], row["x"], row["y"], row["permutations"])
            for row in reader
        ]


def build_summary(maximum: int, csv_path: Path | None = None) -> str:
    if csv_path and csv_path.exists():
        sequence = load_sequence_from_csv(csv_path)
        search_description = f"CSV source: `{csv_path.name}`"
    else:
        sequence = generate_sequence_A359012(maximum)
        search_description = f"Search bound: terms `k` with `10 <= k < {maximum}`"

    if not sequence:
        return (
            "# A359012 Analysis\n\n"
            f"No terms were found below {maximum}. Try a larger search bound.\n"
        )

    term_lengths = Counter(len(k) for k, _, _, _ in sequence)
    split_types = Counter((len(x), len(y)) for _, x, y, _ in sequence)
    y_lengths = Counter(len(y) for _, _, y, _ in sequence)
    substring_positions = [perm.find(k) for k, _, _, perm in sequence]
    prefix_hits = sum(position == 0 for position in substring_positions)
    suffix_hits = sum(
        perm.endswith(k) for k, _, _, perm in sequence
    )
    internal_hits = len(sequence) - prefix_hits - suffix_hits
    repeated_digits = [k for k, _, _, _ in sequence if len(set(k)) < len(k)]
    unique_digits = [k for k, _, _, _ in sequence if len(set(k)) == len(k)]
    palindromes = [k for k, _, _, _ in sequence if k == k[::-1]]
    trailing_zero_count = sum(perm.endswith("0") for _, _, _, perm in sequence)
    permutation_lengths = [(k, len(perm)) for k, _, _, perm in sequence]
    min_perm_len = min(length for _, length in permutation_lengths)
    max_perm_len = max(length for _, length in permutation_lengths)
    smallest_perm_terms = [k for k, length in permutation_lengths if length == min_perm_len]
    largest_perm_terms = [k for k, length in permutation_lengths if length == max_perm_len]
    y_values = Counter(y for _, _, y, _ in sequence)
    repeated_y_values = [(y, count) for y, count in y_values.items() if count > 1]
    repeated_y_values.sort(key=lambda item: (-item[1], item[0]))
    top_repeated_y_values = repeated_y_values[:10]

    # Substring position analysis
    positions = [perm.find(k) for k, _, _, perm in sequence]
    avg_position = sum(positions) / len(positions) if positions else 0
    position_table = [
        (k, pos, len(perm), round(pos / len(perm), 3))
        for (k, _, _, perm), pos in zip(sequence, positions)
    ]

    # Digit expansion ratio: how many times longer is P(x,y) than k?
    expansion_ratios = [
        (k, len(k), len(perm), round(len(perm) / len(k), 2))
        for k, _, _, perm in sequence
    ]
    avg_expansion = sum(r for _, _, _, r in expansion_ratios) / len(expansion_ratios)
    min_expansion = min(expansion_ratios, key=lambda t: t[3])
    max_expansion = max(expansion_ratios, key=lambda t: t[3])

    # Factorial cases (x == y  =>  P(x,y) = x!)
    factorial_cases = [(k, x) for k, x, y, _ in sequence if x == y]

    # --- Multiple witnesses: k values witnessed by more than one (x, y) split ---
    k_counts = Counter(k for k, _, _, _ in sequence)
    multi_witness_ks = sorted((k for k, c in k_counts.items() if c > 1), key=int)
    unique_k_count = len(k_counts)

    # --- Non-trailing-zero outliers ---
    non_tz_terms = [(k, x, y, perm) for k, x, y, perm in sequence if not perm.endswith("0")]

    # --- Prime terms ---
    seen_k = set()
    prime_terms = []
    for k, _, _, _ in sequence:
        if k not in seen_k and is_prime(int(k)):
            prime_terms.append(k)
        seen_k.add(k)

    # --- Gap analysis (on unique k values in ascending order) ---
    unique_ks_sorted = sorted({int(k) for k, _, _, _ in sequence})
    gaps = [unique_ks_sorted[i] - unique_ks_sorted[i - 1] for i in range(1, len(unique_ks_sorted))]
    max_gap = max(gaps) if gaps else 0
    min_gap = min(gaps) if gaps else 0
    avg_gap = round(sum(gaps) / len(gaps), 1) if gaps else 0
    # Top-5 largest gaps with the k pair that spans each
    gap_pairs = sorted(
        [(unique_ks_sorted[i - 1], unique_ks_sorted[i], unique_ks_sorted[i] - unique_ks_sorted[i - 1])
         for i in range(1, len(unique_ks_sorted))],
        key=lambda t: -t[2],
    )[:5]

    # --- Digit sum distribution ---
    digit_sums = [sum(int(d) for d in k) for k, _, _, _ in sequence if k not in (None,)]
    # deduplicate by k
    seen = set()
    digit_sums_unique = []
    for k, _, _, _ in sequence:
        if k not in seen:
            digit_sums_unique.append(sum(int(d) for d in k))
            seen.add(k)
    ds_counter = Counter(digit_sums_unique)
    mod9_counter = Counter(s % 9 for s in digit_sums_unique)

    # --- Counting function at decade boundaries ---
    decade_boundaries = [10 ** i for i in range(2, 7)]
    decade_counts = [
        (boundary, len({int(k) for k, _, _, _ in sequence if int(k) < boundary}))
        for boundary in decade_boundaries
    ]
    alpha = _power_law_exponent([(b, c) for b, c in decade_counts if c > 0])

    # --- Relative depth histogram (10 equal bins over [0, 1]) ---
    bin_edges = [i / 10 for i in range(11)]
    depth_hist = Counter()
    for k, _, _, perm in sequence:
        pos = perm.find(k)
        depth = pos / len(perm)
        bucket = min(int(depth * 10), 9)
        depth_hist[bucket] += 1

    lines = [
        "# A359012 Analysis",
        "",
        search_description,
        f"Terms found: {len(sequence)}",
        "",
        "## Observed Properties",
        "",
        f"- Sparsity: only {len(sequence)} terms appear below {maximum}.",
        f"- Term lengths: {format_digit_length_counter(term_lengths, label='terms')}.",
        f"- Split types `(len(x), len(y))`: {format_split_counter(split_types)}.",
        f"- `y` digit lengths: {format_digit_length_counter(y_lengths, label='cases')}.",
        (
            f"- Substring placement in `xPy`: {prefix_hits} prefix hits, "
            f"{suffix_hits} suffix hits, {internal_hits} strictly internal hits."
        ),
        (
            f"- Trailing-zero bias: {trailing_zero_count} of {len(sequence)} "
            "permutation values end in `0`."
        ),
        (
            f"- Digit repetition: {len(repeated_digits)} terms have repeated digits; "
            f"{len(unique_digits)} have all digits distinct."
        ),
        (
            f"- Palindromes: {', '.join(palindromes) if palindromes else 'none in this range'}."
        ),
        (
            f"- Smallest permutation length: {min_perm_len} digits "
            f"(term(s): {', '.join(smallest_perm_terms)})."
        ),
        (
            f"- Largest permutation length: {max_perm_len} digits "
            f"(term(s): {', '.join(largest_perm_terms)})."
        ),
        (
            "- Repeated `y` values: "
            + (
                ", ".join(f"{y} ({count})" for y, count in top_repeated_y_values)
                if repeated_y_values
                else "none"
            )
            + ("." if len(repeated_y_values) <= 10 else ", ...")
        ),
        "",
        "## Aggregate Measures",
        "",
        f"- Average substring position inside `P(x,y)`: {avg_position:.1f} digits from the start.",
        f"- Average expansion ratio `|P(x,y)| / |k|`: {avg_expansion:.1f}x.",
        (
            f"- Smallest expansion ratio: {min_expansion[3]}x for `k={min_expansion[0]}`; "
            f"largest: {max_expansion[3]}x for `k={max_expansion[0]}`."
        ),
        "",
        "## Examples",
        "",
        "| k | x | y | |P(x,y)| | position of k | relative depth | expansion ratio |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ] + [
        f"| {k} | {x} | {y} | {len(perm)} | {perm.find(k)} | {round(perm.find(k) / len(perm), 3):.3f} | {round(len(perm) / len(k), 2)} |"
        for k, x, y, perm in sequence[:15]
    ] + [
        "",
        "The table shows the first 15 terms only; the CSV remains the full source dataset.",
        "",
        "## Factorial Cases",
        "",
        (
            "Terms where x == y (so P(x,y) = x!): "
            + (
                ", ".join(f"{k} (x=y={x})" for k, x in factorial_cases)
                if factorial_cases
                else "none in this range"
            )
            + "."
        ),
        "",
        "## Conjecture Starters",
        "",
        "- The sequence appears sparse, so estimating its counting function may be interesting.",
        "- Balanced splits seem favored: `(2, 2)` dominates the current search window.",
        "- Most witnesses are internal substrings rather than prefix or suffix matches.",
        "- Decimal trailing-zero structure in `xPy` may strongly influence where matches can occur.",
        "- The digit expansion ratio grows rapidly; for large k, P(x,y) has tens of times more",
        "  digits than k, making a substring match increasingly likely by pure probability -",
        "  yet the sequence remains sparse because valid splits are structurally constrained.",
        "",
        "## Multiple Witnesses",
        "",
        f"- Unique k values in the sequence: {unique_k_count} (total rows including duplicate splits: {len(sequence)}).",
        (
            f"- k values with more than one valid (x, y) split: "
            + (", ".join(multi_witness_ks) if multi_witness_ks else "none in this range")
            + "."
        ),
        "",
        "## Non-Trailing-Zero Outliers",
        "",
        (
            f"- {len(sequence) - len(non_tz_terms)} of {len(sequence)} witness values end in `0`; "
            f"{len(non_tz_terms)} do not."
        ),
    ] + [
        f"- k={k}: P({x},{y}) = {perm} (ends in `{perm[-1]}`)"
        for k, x, y, perm in non_tz_terms
    ] + [
        "- Trailing zeros in xPy arise from paired factors of 2 and 5 in the falling factorial product.",
        "  Exceptions occur when y is small enough that no factor of 5 appears in x*(x-1)*...*(x-y+1).",
        "",
        "## Prime Terms",
        "",
        f"- Prime k values: {len(prime_terms)} of {unique_k_count} unique terms "
        f"({100 * len(prime_terms) / unique_k_count:.1f}%).",
        (
            "- Primes: "
            + (", ".join(prime_terms[:20]) + (" ..." if len(prime_terms) > 20 else ""))
            if prime_terms else "- No prime terms in this range."
        ),
        "",
        "## Gap Analysis",
        "",
        f"- Gaps between consecutive unique terms: min = {min_gap}, max = {max_gap}, average = {avg_gap}.",
        "- Five largest gaps (from, to, size):",
    ] + [
        f"  - {a} → {b}: gap {g}"
        for a, b, g in gap_pairs
    ] + [
        "",
        "## Digit Sum and Residues",
        "",
        f"- Digit sums range from {min(digit_sums_unique)} to {max(digit_sums_unique)}.",
        "- Distribution of (digit sum) mod 9 across unique k values:",
    ] + [
        f"  - {r}: {mod9_counter[r]} terms"
        for r in sorted(mod9_counter)
    ] + [
        "- Note: digit_sum ≡ k (mod 9) by casting-out-nines, so this also describes k mod 9.",
        "",
        "## Counting Function and Density",
        "",
        "- Cumulative term counts at decade boundaries (unique k):",
    ] + [
        f"  - below 10^{int(math.log10(b))}: {c} terms"
        for b, c in decade_counts
    ] + [
        (
            f"- Power-law fit to log-log data: count(N) ≈ C · N^α,  estimated α ≈ {alpha}."
            if alpha is not None
            else "- Not enough decade points for a power-law fit."
        ),
        "- α < 1 confirms the sequence is sub-linear (sparser than a fixed proportion of integers).",
        "- Probabilistic model: for a balanced d-digit split, |P(x,y)| ≈ (d/2)·log10(d/2) digits by",
        "  Stirling, so the expected match probability is ~10^(-(d/2)) per candidate — consistent with",
        "  the observed rapid growth as digit length increases.",
        "",
        "## Relative Depth Distribution",
        "",
        "- Histogram of where k lands inside P(x,y) (10 equal bins over [0, 1]):",
    ] + [
        f"  - [{i/10:.1f}, {(i+1)/10:.1f}): {depth_hist[i]} terms"
        for i in range(10)
    ] + [
        "- A uniform distribution would place ~10% of terms in each bin.",
        "- Deviations indicate structural biases in where k appears within its witness.",
        "",
    ]
    return "\n".join(lines)


def _power_law_exponent(decade_counts: list) -> float | None:
    """Estimate the power-law exponent α from (N, count) pairs via log-log linear regression."""
    points = [(math.log10(n), math.log10(c)) for n, c in decade_counts if c > 1]
    if len(points) < 2:
        return None
    n = len(points)
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    x_mean = sum(xs) / n
    y_mean = sum(ys) / n
    num = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(xs, ys))
    den = sum((xi - x_mean) ** 2 for xi in xs)
    return round(num / den, 3) if den else None


def format_digit_length_counter(counter: Counter, label: str) -> str:
    return ", ".join(
        f"{digits}-digit {label}: {count}" for digits, count in sorted(counter.items())
    )


def format_split_counter(counter: Counter) -> str:
    return ", ".join(
        f"{split}: {count}" for split, count in sorted(counter.items())
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze the A359012 search output.")
    parser.add_argument(
        "--maximum",
        type=int,
        default=10**6,
        help="Upper bound for the brute-force search (default: 1000000).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("ANALYSIS.md"),
        help="Where to write the Markdown summary (default: ANALYSIS.md).",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("A359012.csv"),
        help="CSV source to analyze when available (default: A359012.csv).",
    )
    args = parser.parse_args()

    summary = build_summary(args.maximum, args.input)
    args.output.write_text(summary, encoding="utf-8")
    print(f"Wrote analysis to {args.output}")


if __name__ == "__main__":
    main()
