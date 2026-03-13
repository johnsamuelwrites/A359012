#
# SPDX-FileCopyrightText: 2023 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Functions to generate the integer sequence A359012 and write a sequence to a CSV file

import csv
import math


def generate_sequence_A359012(maximum: int):
    A359012 = []

    for num in range(10, maximum):
        k = str(num)
        length = len(k)

        # To calculate xPy, x should >= y
        for count in range(math.ceil(length / 2), length):
            x = k[:count]
            y = k[-(length - count) :]

            perm_str = str(math.perm(int(x), int(y)))
            if k in perm_str:
                A359012.append((k, x, y, perm_str))
    return A359012


def write_sequence_to_file(sequence: list):
    with open("A359012.csv", "w", newline="") as A359012_csv_file:
        header = [
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

        writer = csv.writer(A359012_csv_file, delimiter=",")
        writer.writerow(header)
        writer.writerows(annotate_sequence_for_csv(sequence))


def annotate_sequence_with_lengths(sequence: list):
    return [
        (k, len(k), x, len(x), y, len(y), perm_str, len(perm_str))
        for k, x, y, perm_str in sequence
    ]


def annotate_sequence_for_csv(sequence: list):
    annotated_rows = []
    for k, x, y, perm_str in sequence:
        position = perm_str.find(k)
        perm_length = len(perm_str)
        relative_depth = round(position / perm_length, 3)
        expansion_ratio = round(perm_length / len(k), 2)
        annotated_rows.append(
            (
                k,
                len(k),
                x,
                len(x),
                y,
                len(y),
                perm_str,
                perm_length,
                position,
                relative_depth,
                expansion_ratio,
            )
        )
    return annotated_rows


def generate_sequence_A359012_lengths(maximum: int):
    return annotate_sequence_with_lengths(generate_sequence_A359012(maximum))


def write_sequence_lengths_to_file(sequence: list):
    with open("A359012_length.csv", "w", newline="") as A359012_csv_file:
        header = ["k", "|k|", "x", "|x|", "y", "|y|", "permutations", "|permutations|"]

        writer = csv.writer(A359012_csv_file, delimiter=",")
        writer.writerow(header)
        writer.writerows(sequence)
