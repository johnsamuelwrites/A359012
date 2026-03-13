import argparse
from collections import Counter
from pathlib import Path

from A359012 import generate_sequence_A359012


def build_summary(maximum: int) -> str:
    sequence = generate_sequence_A359012(maximum)

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

    lines = [
        "# A359012 Analysis",
        "",
        f"Search bound: terms `k` with `10 <= k < {maximum}`",
        f"Terms found: {len(sequence)}",
        "",
        "## Terms",
        "",
        ", ".join(k for k, _, _, _ in sequence),
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
                ", ".join(f"{y} ({count})" for y, count in repeated_y_values)
                if repeated_y_values
                else "none"
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
        default=10**4,
        help="Upper bound for the brute-force search (default: 10000).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("ANALYSIS.md"),
        help="Where to write the Markdown summary (default: ANALYSIS.md).",
    )
    args = parser.parse_args()

    summary = build_summary(args.maximum)
    args.output.write_text(summary, encoding="utf-8")
    print(f"Wrote analysis to {args.output}")


if __name__ == "__main__":
    main()
