"""
make up words from dict files and a markov-like model

(c) Thomas Waldmann, MIT license
"""

import random
import sys
from collections import defaultdict


def from_dictfile(fname):
    """
    yield words from a words file (1 word per line)
    """
    with open(fname) as f:
        for word in f:
            yield word.strip()


def from_textfile(fname, punctuation=""".,:;!?"'()[]{}"""):
    """
    yield words from text file, strip punctuation
    """
    with open(fname) as f:
        for word in f.read().split():
            word = word.strip(punctuation)
            if word:
                yield word


def build_model(n, words):
    """
    from words, build a markov-like mapping: state --> next

    state: a n-tuple of the last n tokens (characters)
    next: a list of tokens (characters) seen as next after this state

    Note: it would be enough to count the "next tokens", but we are lazy.
    """
    model = defaultdict(list)
    for word in words:
        state = (None, ) * n  # n-tuple of None
        for t_next in word:
            model[state].append(t_next)
            state = state[1:] + (t_next, )
        model[state].append(None)  # Mark the end
    return model


def makeup_words(n, model):
    """
    using a model, make up words matching that model (real as well as unreal words)

    Note: this is a infinite generator
    """
    while True:
        state = (None, ) * n
        word = []
        while True:
            t_next = random.choice(model[state])
            if t_next is None:
                yield ''.join(word)
                break
            word.append(t_next)
            state = state[1:] + (t_next, )


if __name__ == '__main__':

    real_words = set(from_dictfile("/usr/share/dict/words"))

    n = 3
    model = build_model(n, real_words)
    for counter, word in zip(range(1, 100), makeup_words(n, model)):
        print counter, word, "(real)" if word in real_words else "(made up)"

