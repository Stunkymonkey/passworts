#!/usr/bin/env python3

from pathlib import Path
from collections import defaultdict
import pickle
from argparse import ArgumentParser
import sys

n = 3


def dd():
    return defaultdict(int)


def analyse(counts, text, n):
    """analyse text with n chars markov state, update the counts"""

    text = "^" * n + text + "$" * n
    for i in range(len(text) - n):
        st = i, text[i : i + n]
        next_char = text[i + n]
        counts[st][next_char] += 1
    return counts


def compute_prob(counts):
    """compute ranges in [0 .. 1) of the given words"""

    for c1 in counts:
        total = float(sum(counts[c1][c2] for c2 in counts[c1]))
        base = 0.0
        for c2 in counts[c1]:
            prob = counts[c1][c2] / total
            base = base + prob
            counts[c1][c2] = base
    return counts


def text_import(text_path):
    """reads a file to analyse"""

    try:
        with open(text_path, "r", encoding="ISO-8859-1") as handle:
            text = set(handle.read().split())
    except OSError as e:
        raise SystemExit("Could not open text file: " + str(e)) from e
    return text


def calculate(text_path):
    print("reading...")
    text = text_import(text_path)
    print("analysing text...")
    counts = defaultdict(dd)

    for word in text:
        counts = analyse(counts, word, n)

    print("calculating...")
    counts = compute_prob(counts)

    # save to file
    print("write...")
    with open(text_path.with_suffix('.pkl'), "wb") as handle:
        pickle.dump(counts, handle)

    print("checking file...")
    with open(text_path.with_suffix('.pkl'), "rb") as handle:
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
