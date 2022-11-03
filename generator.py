#!/usr/bin/env python3

import random
from pathlib import Path
from collections import defaultdict
import pickle
from argparse import ArgumentParser

import calc

n = 3


def makeup(counts, n):
    """make up a word using the markov model of the original text"""
    st = 0, "^" * n
    text = []
    while st[1] != "$" * n:
        d = counts[st]
        r = random.random()
        for next_char in d:
            if d[next_char] > r:
                break
        st = st[0] + 1, st[1][1:] + next_char
        text.append(next_char)
    return "".join(text)[:-n]


def text_import(text_path):
    """reads a file to analyse"""

    try:
        with open(text_path, "rb") as handle:
            counts = pickle.load(handle)
    except OSError as e:
        raise SystemExit("Could not open text file: " + str(e)) from e
    return counts


def words_import(words_path):
    try:
        with open(words_path, "r", encoding="ISO-8859-1") as f:
            words = f.read()
    except OSError as e:
        raise SystemExit("Could not open words file: " + str(e)) from e
    return words


def dd():
    return defaultdict(int)


def generate(pw_lenght, random_lenght, source):
    # print ("reading...")
    dict_path = Path(source)
    words = words_import(Path("./dict/words.txt"))

    if dict_path.with_suffix('.pkl').exists():
        counts = text_import(dict_path.with_suffix('.pkl'))
    else:
        calc.calculate(dict_path)
        counts = defaultdict(dd)
        counts = text_import(dict_path.with_suffix('.pkl'))

    # print ("generating...")
    for _ in range(50000):
        madeup_word = makeup(counts, n).lower()
        # break
        if madeup_word not in words.lower() and madeup_word.isalpha():
            if bool(random_lenght):
                return madeup_word
            if not bool(random_lenght) and len(madeup_word) == pw_lenght:
                return madeup_word
        # print("           " + str(i + 1) + "-crap:       " + madeup_word)
    print("Sorry this one took to long")
    return "Sorry this one took to long"


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        type=Path,
        dest="filename",
        help="path of the input file",
        default=Path(__file__).absolute().parent / "dict" / "text.txt",
    )
    parser.add_argument(
        "-l",
        "--lenght",
        type=int,
        help="lenght of the password",
        default=8,
    )
    parser.add_argument(
        "-a",
        "--amount",
        type=int,
        help="amount of the passwords",
        default=1,
    )

    args = parser.parse_args()

    for i in range(args.amount):
        print(generate(args.lenght, False, str(args.filename)))
