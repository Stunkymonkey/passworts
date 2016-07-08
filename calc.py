#!/usr/bin/env python3

import os.path
from collections import defaultdict
import pickle

n = 3


def analyse(counts, text, n):
    """analyse text with n chars markov state, update the counts"""

    text = '^' * n + text + '$' * n
    for i in range(len(text) - n):
        st = i, text[i:i + n]
        next = text[i + n]
        counts[st][next] += 1
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


def text_import(dict_path, source):
    """reads a file to analyse"""

    try:
        with open(dict_path + source, "r", encoding="ISO-8859-1") as f:
            text = set(f.read().split())
    except (FileNotFoundError):
        print("The dict/text.txt file was not found.")
        # return ("The dict/text.txt file was not found.")
    return text


def dd():
    return defaultdict(int)


def calculate(source):
    print("reading...")
    dict_path = os.path.join(os.path.abspath(".") + r"/dict/")
    text = text_import(dict_path, source)
    source = source.split(".")[0]
    print("analysing text...")
    counts = defaultdict(dd)

    for word in text:
        counts = analyse(counts, word, n)

    print("calculating...")
    counts = compute_prob(counts)

    # print(type(counts))
    # print(counts)

    # save to file
    print("write...")
    with open((dict_path + source + '.pickle'), 'wb') as handle:
        pickle.dump(counts, handle)

    print("checking file...")
    with open((dict_path + source + '.pickle'), 'rb') as handle:
        written = pickle.load(handle)

    if written == counts:
        print("Calucation was sucessfull")
    else:
        print("Something went wrong")


if __name__ == '__main__':
    calculate("text.txt")
