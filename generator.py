#!/usr/bin/env python3
""" passworts cli for generating passwords"""
# import time

import pickle
import random
import bisect
from argparse import ArgumentParser
from collections import defaultdict
from pathlib import Path

import calc
from calc import LOOKUP_RANGE


def makeup(counts, lookup_lenght):
    """make up a word using the markov model of the original text"""
    previous_chars = 0, "^" * lookup_lenght
    text = []
    while previous_chars[1] != "$" * lookup_lenght:
        possible_chars = counts[previous_chars]
        random_char_propability = random.random()

        # find key of dict with first value larger then propability
        index = bisect.bisect(list(possible_chars.values()), random_char_propability)
        next_char = list(possible_chars.keys())[index]

        text.append(next_char)
        previous_chars = previous_chars[0] + 1, previous_chars[1][1:] + next_char
    return "".join(text)[:-lookup_lenght]


def text_import(text_path):
    """reads a file to analyse"""
    try:
        with open(text_path, "rb") as handle:
            counts = pickle.load(handle)
    except OSError as error:
        raise SystemExit("Could not open text file: " + str(error)) from error
    return counts


def words_import(words_path):
    """read words to prevent existing words"""
    try:
        with open(words_path, "r", encoding="utf-8") as word_file:
            words = word_file.read()
    except OSError as error:
        raise SystemExit("Could not open words file: " + str(error)) from error
    return words


def generate(pw_lenght, random_lenght, source):
    """generate word with limitations"""
    # print ("reading...")
    dict_path = Path(source)
    words = words_import(Path("./dict/words.txt"))

    if dict_path.with_suffix(".pkl").exists():
        counts = text_import(dict_path.with_suffix(".pkl"))
    else:
        calc.calculate(dict_path)
        counts = defaultdict(calc.integer_dict)
        counts = text_import(dict_path.with_suffix(".pkl"))

    # print ("generating...")
    for _ in range(50000):
        madeup_word = makeup(counts, LOOKUP_RANGE).lower()
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
