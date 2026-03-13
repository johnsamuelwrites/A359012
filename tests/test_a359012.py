import math

from A359012 import generate_sequence_A359012, generate_sequence_A359012_lengths


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
