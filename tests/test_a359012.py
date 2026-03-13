#
# SPDX-FileCopyrightText: 2023 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import csv
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from A359012 import (
    annotate_sequence_for_csv,
    annotate_sequence_with_lengths,
    generate_sequence_A359012,
    generate_sequence_A359012_lengths,
    is_prime,
    write_sequence_lengths_to_file,
    write_sequence_to_file,
)

# All 33 known members of A359012 below 10 000, in ascending order.
KNOWN_TERMS_BELOW_10000 = [
    "318", "557", "692", "729",
    "2226", "2437", "2776", "3209",
    "4436", "5336", "5549", "5718",
    "5956", "6068", "6141", "6353",
    "6958", "7045", "7046", "7338",
    "7345", "7643", "7865", "8261",
    "8409", "9153", "9178", "9242",
    "9544", "9569", "9664", "9894",
    "9999",
]


# ---------------------------------------------------------------------------
# Basic / regression tests (original)
# ---------------------------------------------------------------------------

def test_known_terms_below_1000_match_current_dataset():
    sequence = generate_sequence_A359012(1000)
    terms = [row[0] for row in sequence]

    assert terms == ["318", "557", "692", "729"]


def test_known_term_has_expected_split_and_contains_substring():
    sequence = generate_sequence_A359012(1000)
    row = next(item for item in sequence if item[0] == "692")

    assert row[1] == "69"
    assert row[2] == "2"
    assert row[3] == str(math.perm(69, 2))
    assert "692" in row[3]


def test_non_term_is_not_in_small_search_window():
    terms = {row[0] for row in generate_sequence_A359012(500)}

    assert "317" not in terms
    assert "500" not in terms


def test_length_variant_tracks_digit_lengths():
    sequence = generate_sequence_A359012_lengths(1000)
    row = next(item for item in sequence if item[0] == "729")

    assert row == ("729", 3, "72", 2, "9", 1, str(math.perm(72, 9)), 17)


def test_length_annotations_are_derived_from_base_sequence():
    base_sequence = generate_sequence_A359012(1000)
    assert annotate_sequence_with_lengths(base_sequence) == generate_sequence_A359012_lengths(1000)


def test_csv_annotations_include_position_and_ratios():
    row = next(item for item in annotate_sequence_for_csv(generate_sequence_A359012(1000)) if item[0] == "692")
    # Columns: k, |k|, x, |x|, y, |y|, perm, |perm|, pos, depth, ratio,
    #          num_witnesses, gap_prev, digit_sum, k_mod_9, is_prime, trailing_zero
    # gap_prev for 692 = 692 - 557 = 135; digit_sum = 6+9+2 = 17; 692%9 = 8; not prime; 4692 ends in '2'
    assert row == ("692", 3, "69", 2, "2", 1, "4692", 4, 1, 0.25, 1.33, 1, 135, 17, 8, 0, 0)


# ---------------------------------------------------------------------------
# Full sequence completeness
# ---------------------------------------------------------------------------

def test_full_sequence_below_10000_matches_known_terms():
    terms = [row[0] for row in generate_sequence_A359012(10000)]
    assert terms == KNOWN_TERMS_BELOW_10000


def test_full_sequence_has_33_terms():
    assert len(generate_sequence_A359012(10000)) == 33


# ---------------------------------------------------------------------------
# Core definitional properties — every term must satisfy all three
# ---------------------------------------------------------------------------

def test_every_term_k_is_substring_of_its_permutation():
    for k, x, y, perm_str in generate_sequence_A359012(10000):
        assert k in perm_str, f"{k}: not found in P({x},{y})"


def test_every_term_satisfies_concatenation_constraint():
    for k, x, y, _ in generate_sequence_A359012(10000):
        assert k == x + y, f"concat({x!r}, {y!r}) != {k!r}"


def test_every_permutation_value_matches_math_perm():
    for k, x, y, perm_str in generate_sequence_A359012(10000):
        assert perm_str == str(math.perm(int(x), int(y))), f"wrong perm for {k}"


def test_x_is_at_least_as_large_as_y_for_every_term():
    # P(x, y) requires x >= y; all witnessed terms must satisfy this.
    for k, x, y, _ in generate_sequence_A359012(10000):
        assert int(x) >= int(y), f"{k}: int({x!r}) < int({y!r})"


# ---------------------------------------------------------------------------
# Trailing-zero bias
# ---------------------------------------------------------------------------

def test_trailing_zero_bias_all_except_692():
    """32 of 33 permutation values end in '0'; the lone exception is 692."""
    sequence = generate_sequence_A359012(10000)
    non_zero = [k for k, _, _, perm in sequence if not perm.endswith("0")]
    assert non_zero == ["692"]


def test_692_permutation_ends_in_2():
    # P(69, 2) = 69 * 68 = 4692 — a small, non-zero-ending value.
    assert math.perm(69, 2) == 4692


# ---------------------------------------------------------------------------
# Permutation magnitude
# ---------------------------------------------------------------------------

def test_smallest_witness_permutation_is_for_692():
    sequence = generate_sequence_A359012(10000)
    by_perm_len = {k: len(perm) for k, _, _, perm in sequence}
    min_len = min(by_perm_len.values())
    assert by_perm_len["692"] == min_len


def test_692_permutation_has_4_digits():
    assert len(str(math.perm(69, 2))) == 4


def test_largest_witness_permutation_is_for_9999():
    sequence = generate_sequence_A359012(10000)
    by_perm_len = {k: len(perm) for k, _, _, perm in sequence}
    max_len = max(by_perm_len.values())
    assert by_perm_len["9999"] == max_len


def test_9999_permutation_has_156_digits():
    # P(99, 99) = 99!
    assert len(str(math.factorial(99))) == 156


# ---------------------------------------------------------------------------
# Special structure of individual terms
# ---------------------------------------------------------------------------

def test_9999_is_the_factorial_case():
    """When x == y, P(x, y) = x!  The only such term below 10 000 is 9999."""
    sequence = generate_sequence_A359012(10000)
    row = next(item for item in sequence if item[0] == "9999")
    k, x, y, perm_str = row
    assert k == "9999"
    assert x == y == "99"
    assert perm_str == str(math.factorial(99))


def test_9999_is_only_term_where_split_is_equal_length_and_equal_value():
    sequence = generate_sequence_A359012(10000)
    equal_splits = [k for k, x, y, _ in sequence if x == y]
    assert equal_splits == ["9999"]


def test_7045_and_7046_are_consecutive_members():
    """Two consecutive integers are both in the sequence."""
    terms = [row[0] for row in generate_sequence_A359012(10000)]
    idx_7045 = terms.index("7045")
    assert terms[idx_7045 + 1] == "7046"


def test_only_palindrome_below_10000_is_9999():
    sequence = generate_sequence_A359012(10000)
    palindromes = [k for k, _, _, _ in sequence if k == k[::-1]]
    assert palindromes == ["9999"]


# ---------------------------------------------------------------------------
# Substring placement inside the permutation value
# ---------------------------------------------------------------------------

def test_318_is_the_only_prefix_hit():
    """k appears at position 0 in P(x, y) only for 318."""
    sequence = generate_sequence_A359012(10000)
    prefix_hits = [k for k, _, _, perm in sequence if perm.startswith(k)]
    assert prefix_hits == ["318"]


def test_692_is_the_only_suffix_hit():
    """P(69, 2) = 4692, which ends with '692', making it the lone suffix hit."""
    sequence = generate_sequence_A359012(10000)
    suffix_hits = [k for k, _, _, perm in sequence if perm.endswith(k)]
    assert suffix_hits == ["692"]


def test_most_hits_are_strictly_internal():
    sequence = generate_sequence_A359012(10000)
    internal = [
        k for k, _, _, perm in sequence
        if not perm.startswith(k) and not perm.endswith(k)
    ]
    # 31 of 33 are internal (all except 318 and 9999)
    assert len(internal) == 31


# ---------------------------------------------------------------------------
# Length-annotated variant — internal consistency
# ---------------------------------------------------------------------------

def test_length_variant_all_digit_lengths_are_consistent():
    for k, len_k, x, len_x, y, len_y, perm, len_perm in generate_sequence_A359012_lengths(10000):
        assert len(k) == len_k
        assert len(x) == len_x
        assert len(y) == len_y
        assert len(perm) == len_perm
        assert k == x + y


def test_length_variant_count_matches_basic_variant():
    assert len(generate_sequence_A359012_lengths(10000)) == len(generate_sequence_A359012(10000))


# ---------------------------------------------------------------------------
# File I/O tests
# ---------------------------------------------------------------------------

def test_write_sequence_to_file_produces_correct_csv(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    sequence = generate_sequence_A359012(1000)
    write_sequence_to_file(sequence)

    # Filter blank rows produced by the Windows \r\r\n artefact in the source writer
    rows = [r for r in csv.reader((tmp_path / "A359012.csv").open()) if r]
    assert rows[0] == [
        "k",
        "|k|",
        "x",
        "|x|",
        "y",
        "|y|",
        "permutations",
        "|permutations|",
        "position_of_k",
        "relative_depth",
        "expansion_ratio",
        "num_witnesses",
        "gap_prev",
        "digit_sum",
        "k_mod_9",
        "is_prime",
        "trailing_zero",
    ]
    assert len(rows) - 1 == len(sequence)
    for row, expected in zip(rows[1:], annotate_sequence_for_csv(sequence)):
        assert row == [str(value) for value in expected]


def test_write_sequence_lengths_to_file_produces_correct_csv(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    sequence = generate_sequence_A359012_lengths(1000)
    write_sequence_lengths_to_file(sequence)

    rows = [r for r in csv.reader((tmp_path / "A359012_length.csv").open()) if r]
    assert rows[0] == ["k", "|k|", "x", "|x|", "y", "|y|", "permutations", "|permutations|"]
    assert len(rows) - 1 == len(sequence)


# ---------------------------------------------------------------------------
# is_prime helper
# ---------------------------------------------------------------------------

def test_is_prime_returns_false_for_small_non_primes():
    assert not is_prime(0)
    assert not is_prime(1)
    assert not is_prime(4)
    assert not is_prime(9)


def test_is_prime_returns_true_for_small_primes():
    assert is_prime(2)
    assert is_prime(3)
    assert is_prime(5)
    assert is_prime(7)
    assert is_prime(11)


def test_is_prime_557_is_prime():
    assert is_prime(557)


def test_is_prime_318_and_692_are_not_prime():
    assert not is_prime(318)   # 318 = 2 * 3 * 53
    assert not is_prime(692)   # 692 = 4 * 173


# ---------------------------------------------------------------------------
# New CSV columns: gap_prev, digit_sum, k_mod_9, is_prime, trailing_zero,
#                  num_witnesses
# ---------------------------------------------------------------------------

def test_csv_gap_prev_first_term_is_zero():
    """The lowest-k term in any search window has gap_prev = 0."""
    annotated = annotate_sequence_for_csv(generate_sequence_A359012(1000))
    first_row = annotated[0]   # 318 is the smallest term below 1000
    gap_prev = first_row[12]
    assert gap_prev == 0


def test_csv_gap_prev_matches_difference_between_successive_unique_terms():
    """557 - 318 = 239; 692 - 557 = 135; 729 - 692 = 37."""
    annotated = annotate_sequence_for_csv(generate_sequence_A359012(1000))
    by_k = {row[0]: row[12] for row in annotated}
    assert by_k["318"] == 0
    assert by_k["557"] == 239
    assert by_k["692"] == 135
    assert by_k["729"] == 37


def test_csv_digit_sum_column():
    """Digit sums: 318→12, 557→17, 692→17, 729→18."""
    annotated = annotate_sequence_for_csv(generate_sequence_A359012(1000))
    by_k = {row[0]: row[13] for row in annotated}
    assert by_k["318"] == 12
    assert by_k["557"] == 17
    assert by_k["692"] == 17
    assert by_k["729"] == 18


def test_csv_k_mod_9_equals_digit_sum_mod_9_for_every_term():
    """k % 9 equals (sum of digits of k) % 9 by casting-out-nines."""
    for row in annotate_sequence_for_csv(generate_sequence_A359012(10000)):
        k_mod_9 = row[14]
        digit_sum = row[13]
        assert k_mod_9 == digit_sum % 9


def test_csv_is_prime_column_identifies_557_as_prime():
    annotated = annotate_sequence_for_csv(generate_sequence_A359012(1000))
    by_k = {row[0]: row[15] for row in annotated}
    assert by_k["557"] == 1    # 557 is prime
    assert by_k["318"] == 0    # 318 = 2 * 3 * 53
    assert by_k["692"] == 0    # 692 = 4 * 173
    assert by_k["729"] == 0    # 729 = 3^6


def test_csv_trailing_zero_column_matches_perm_suffix():
    """trailing_zero == 1 iff the permutation string ends in '0'."""
    for row in annotate_sequence_for_csv(generate_sequence_A359012(1000)):
        perm_str = row[6]
        trailing_zero = row[16]
        assert trailing_zero == (1 if perm_str.endswith("0") else 0)


def test_csv_trailing_zero_is_zero_for_692():
    """P(69, 2) = 4692 does not end in 0."""
    annotated = annotate_sequence_for_csv(generate_sequence_A359012(1000))
    row_692 = next(r for r in annotated if r[0] == "692")
    assert row_692[16] == 0


def test_csv_num_witnesses_all_one_below_1000():
    """No k below 1000 has more than one valid (x, y) split."""
    for row in annotate_sequence_for_csv(generate_sequence_A359012(1000)):
        assert row[11] == 1


def test_multiple_witnesses_detected_if_present():
    """num_witnesses reflects how many splits witness the same k."""
    sequence = generate_sequence_A359012(10**6)
    annotated = annotate_sequence_for_csv(sequence)
    # Every annotated row's num_witnesses must be >= 1
    for row in annotated:
        assert row[11] >= 1
    # Terms with two witnesses appear in the sequence twice
    from collections import Counter
    k_counts = Counter(row[0] for row in annotated)
    for k, count in k_counts.items():
        rows_for_k = [r for r in annotated if r[0] == k]
        assert all(r[11] == count for r in rows_for_k)
