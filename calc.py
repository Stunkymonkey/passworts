#!/usr/bin/env python3
""" passworts module for pre-calculations"""

import pickle
import sys
from argparse import ArgumentParser
from collections import defaultdict
from pathlib import Path

# lookup range (lower more difficult to pronounce, higher easier)
LOOKUP_RANGE = 3


def integer_dict():
    """
    these lines are required, because pickle does not store the data type
    https://stackoverflow.com/questions/27732354/unable-to-load-files-using-pickle-and-multipile-modules
    """
    return defaultdict(int)


def analyse(counts, text, lookup_lenght):
    """analyse text with n chars markov state, update the counts"""

    text = "^" * lookup_lenght + text + "$" * lookup_lenght
    for index in range(len(text) - lookup_lenght):
        substring = index, text[index : index + lookup_lenght]
        next_char = text[index + lookup_lenght]
        counts[substring][next_char] += 1
    return counts


def compute_prob(counts):
    """compute ranges in [0 .. 1) of the given words"""

    for char1 in counts:
        total = float(sum(counts[char1][char2] for char2 in counts[char1]))
        base = 0.0
        for char2 in counts[char1]:
            prob = counts[char1][char2] / total
            base = base + prob
            counts[char1][char2] = base
    return counts


def text_import(text_path):
    """reads a file to analyse"""

    try:
        with open(text_path, "r", encoding="ISO-8859-1") as handle:
            text = set(handle.read().split())
    except OSError as error:
        raise SystemExit("Could not open text file: " + str(error)) from error
    return text


def calculate(text_path):
    """precalculate the propabilities"""
    print("reading...")
    text = text_import(text_path)
    print("analysing text...")
    counts = defaultdict(integer_dict)

    for word in text:
        counts = analyse(counts, word, LOOKUP_RANGE)

    print("calculating...")
    counts = compute_prob(counts)

    # save to file
    print("write...")
    with open(text_path.with_suffix(".pkl"), "wb") as handle:
        pickle.dump(counts, handle)

    print("checking file...")
    with open(text_path.with_suffix(".pkl"), "rb") as handle:
        written = pickle.load(handle)

    if written == counts:
        print("Calucation was sucessfull")
    else:
        print("Something went wrong")
        sys.exit(1)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-f", "--file", type=Path, dest="filename", help="Name of the input file"
    )
    args = parser.parse_args()

    calculate(args.filename)
