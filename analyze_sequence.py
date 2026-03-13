import argparse
import csv
from collections import Counter
from pathlib import Path

from A359012 import generate_sequence_A359012


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
    ]
    return "\n".join(lines)


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
