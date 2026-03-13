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
    assert row == ("692", 3, "69", 2, "2", 1, "4692", 4, 1, 0.25, 1.33)


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
