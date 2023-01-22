#
# SPDX-FileCopyrightText: 2023 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Generating the sequence and writing the sequence to a CSV file

from A359012 import (
    generate_sequence_A359012,
    generate_sequence_A359012_lengths,
    write_sequence_to_file,
    write_sequence_lengths_to_file,
)

maximum = 10**4
A359012 = generate_sequence_A359012(maximum)
write_sequence_to_file(A359012)

A359012_lengths = generate_sequence_A359012_lengths(maximum)
write_sequence_lengths_to_file(A359012_lengths)
