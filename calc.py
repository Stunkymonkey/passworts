#!/usr/bin/env python3

import os.path
from collections import defaultdict

import pickle

n = 3


def analyse(counts, text, n):
    # analyse text with n chars markov state, update the counts

    text = '^' * n + text + '$' * n
    for i in range(len(text) - n):
        st = i, text[i:i + n]
        next = text[i + n]
        counts[st][next] += 1
    return counts


def compute_prob(counts):
    # compute ranges in [0 .. 1) from the counts

    for c1 in counts:
        total = float(sum(counts[c1][c2] for c2 in counts[c1]))
        base = 0.0
        for c2 in counts[c1]:
            prob = counts[c1][c2] / total
            base = base + prob
            counts[c1][c2] = base
    return counts


def text_import(dict_path):
    # import text to analyse

    try:
        with open(dict_path + "text.txt", "r", encoding="ISO-8859-1") as f:
            text = set(f.read().split())
    except (FileNotFoundError):
        print("The dict/text.txt file was not found.")
        # return ("The dict/text.txt file was not found.")
    return text


def calculate():
    print ("reading...")
    dict_path = os.path.join(os.path.abspath(".") + r"/dict/")
    text = text_import(dict_path)
    print ("analysing text...")
    counts = defaultdict(lambda: defaultdict(int))

    for word in text:
        counts = analyse(counts, word, n)

    print ("calculating...")
    print (type(counts))
    counts = compute_prob(counts)

    print (type(counts))
    # print (counts)

    # save to file

    with open((dict_path + 'filename.pickle'), 'wb') as handle:
        pickle.dump(dict(counts), handle)
    print ("finish")

if __name__ == '__main__':
    calculate()
