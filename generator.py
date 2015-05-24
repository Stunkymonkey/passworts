#!/usr/bin/env python3

import random
import os.path
from collections import defaultdict

# import pickle

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


def text_import(dict_path):
    try:
        with open(dict_path + "text.txt", "r") as f:
            text = set(f.read().split())
    except (FileNotFoundError):
        print("The dict/text.txt file was not found.")
        # return ("The dict/text.txt file was not found.")
    return text


def words_import(dict_path):
    try:
        with open(dict_path + "words.txt", "r") as f:
            words = f.read()
    except (FileNotFoundError):
        print("The dict/words.txt file was not found.")
        # return ("The dict/words.txt file was not found.")
    return words


"""
def text_import(dict_path):
    try:
        with open(dict_path + "filename.pickle", "rb") as handle:
            counts = pickle.load(handle)
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
"""


def generate(pw_lenght, random):
    # print ("reading...")
    dict_path = os.path.join(os.path.abspath(".") + r"/dict/")
    # print (counts)
    text = text_import(dict_path)
    words = words_import(dict_path)

    # print ("analysing text...")
    counts = defaultdict(lambda: defaultdict(int))

    for word in text:
        counts = analyse(counts, word, n)
    # print ("calculating...")
    counts = compute_prob(counts)

    # print ("generating...")
    for i in range(500000):
        madeup_word = makeup(counts, n).lower()
        # break
        if (madeup_word not in words.lower() and madeup_word.isalpha() and
                bool(random) == False and len(madeup_word) == pw_lenght):
            return madeup_word
        elif (madeup_word not in words.lower() and madeup_word.isalpha() and
              bool(random) == True):
            return madeup_word
        # print ("           " + str(i+1) + "-crap:       " + madeup_word)
    print ("Sorry this one took to long")
    return ("Sorry this one took to long")

if __name__ == '__main__':
    generate(8, False)
