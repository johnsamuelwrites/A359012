#
# SPDX-FileCopyrightText: 2023 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Functions to generate the integer sequence A359012 and write a sequence to a CSV file

import math
import csv


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
    with open("A359012.csv", "w") as A359012_csv_file:
        header = ["k", "x", "y", "permutations"]

        writer = csv.writer(A359012_csv_file, delimiter=",")
        writer.writerow(header)
        writer.writerows(sequence)


def generate_sequence_A359012_lengths(maximum: int):
    A359012_lengths = []

    for num in range(10, maximum):
        k = str(num)
        length = len(k)

        # To calculate xPy, x should >= y
        for count in range(math.ceil(length / 2), length):
            x = k[:count]
            y = k[-(length - count) :]

            perm_str = str(math.perm(int(x), int(y)))
            if k in perm_str:
                A359012_lengths.append(
                    (k, len(k), x, len(x), y, len(y), perm_str, len(perm_str))
                )
    return A359012_lengths


def write_sequence_lengths_to_file(sequence: list):
    with open("A359012_length.csv", "w") as A359012_csv_file:
        header = ["k", "|k|", "x", "|x|", "y", "|y|", "permutations", "|permutations|"]

        writer = csv.writer(A359012_csv_file, delimiter=",")
        writer.writerow(header)
        writer.writerows(sequence)
