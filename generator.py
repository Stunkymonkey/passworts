#!/usr/bin/env python3

import random
import os.path
from collections import defaultdict
import pickle

import calc

n = 3


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


def text_import(dict_path, source):
    try:
        with open(dict_path + source + ".pickle", "rb") as handle:
            counts = pickle.load(handle)
    except FileNotFoundError as e:
        raise SystemExit("Could not open text file: " + str(e))
    return counts


def words_import(dict_path):
    try:
        with open(dict_path + "words.txt", "r", encoding="ISO-8859-1") as f:
            words = f.read()
    except FileNotFoundError as e:
        raise SystemExit("Could not open words file: " + str(e))
    return words


def dd():
    return defaultdict(int)


def generate(pw_lenght, randomLenght):
    # print ("reading...")
    source = "text.txt"
    source = source.split(".")[0]
    dict_path = os.path.join(os.path.abspath(".") + r"/dict/")
    words = words_import(dict_path)

    counts = defaultdict(dd)
    if os.path.isfile(dict_path + source + ".pickle"):
        counts = text_import(dict_path, source)
    else:
        calc.calculate(source + ".txt")
        counts = text_import(dict_path, source)

    # print(counts)
    # print(type(counts))

    # print("counts")
    # print(counts)

    # print ("generating...")
    for i in range(50000):
        madeup_word = makeup(counts, n).lower()
        # break
        if (madeup_word not in words.lower() and madeup_word.isalpha()):
            if bool(randomLenght):
                return madeup_word
            elif (not bool(randomLenght) and len(madeup_word) == pw_lenght):
                return madeup_word
        print("           " + str(i + 1) + "-crap:       " + madeup_word)
    print("Sorry this one took to long")
    return ("Sorry this one took to long")

if __name__ == '__main__':
    for i in range(1):
        print(generate(8, False))
