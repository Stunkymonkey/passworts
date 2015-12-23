#!/usr/bin/env python3

import random
import os.path
from collections import defaultdict

import dill

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


def makeup(counts, n):
    # make up a word using the markov model of the original text

    st = 0, '^' * n
    text = []
    while st[1] != '$' * n:
        d = counts[st]
        r = random.random()
        # TODO RNG test here
        for next in d:
            if d[next] > r:
                break
        st = st[0] + 1, st[1][1:] + next
        text.append(next)
    return ''.join(text)[:-n]

"""
def text_import(dict_path):
    try:
        with open(dict_path + "text.txt", "r", encoding="ISO-8859-1") as f:
            text = set(f.read().split())
    except (FileNotFoundError):
        print("The dict/text.txt file was not found.")
        # return ("The dict/text.txt file was not found.")
    return text
"""


def text_import(dict_path, source):
    try:
        with open(dict_path + source + ".dill", "rb") as handle:
            counts = dill.load(handle)
    except (FileNotFoundError):
        print("The dict/text.txt file was not found.")
        # return ("The dict/text.txt file was not found.")
    return counts


def words_import(dict_path):
    try:
        with open(dict_path + "words.txt", "r", encoding="ISO-8859-1") as f:
            words = f.read()
    except (FileNotFoundError):
        print("The dict/words.txt file was not found.")
        # return ("The dict/words.txt file was not found.")
    return words


def generate(pw_lenght, randomLenght):
    # print ("reading...")
    source = "text.txt"
    source = source.split(".")[0]
    dict_path = os.path.join(os.path.abspath(".") + r"/dict/")
    words = words_import(dict_path)

    """
    text = text_import(dict_path)
    print ("analysing text...")
    counts = defaultdict(lambda: defaultdict(int))

    for word in text:
        counts = analyse(counts, word, n)
    print ("calculating...")
    counts = compute_prob(counts)
    """
    counts = defaultdict(lambda: defaultdict(int))
    counts = text_import(dict_path, source)
    # print(counts)
    print(type(counts))

    # print ("generating...")
    for i in range(500000):
        madeup_word = makeup(counts, n).lower()
        # break
        if (madeup_word not in words.lower() and madeup_word.isalpha() and
                bool(randomLenght)):
            return madeup_word
        elif (madeup_word not in words.lower() and madeup_word.isalpha() and
                not bool(randomLenght) and len(madeup_word) == pw_lenght):
            return madeup_word
        print("           " + str(i+1) + "-crap:       " + madeup_word)
    print("Sorry this one took to long")
    return ("Sorry this one took to long")

if __name__ == '__main__':
    for i in range(20):
        print(generate(8, False))
