"""
analysing and generation of texts using markov models

(c) Thomas Waldmann, MIT license
"""

import random
from collections import defaultdict

text = open("dict/text.txt").read()


def analyse(counts, text, n):
    """
    analyse text with n chars markov state, update the counts
    """
    text = '^' * n + text + '$' * n
    for i in list(range(len(text) - n)):
        st = text[i:i+n]
        next = text[i+n]
        counts[st][next] += 1
    return counts


def compute_prob(counts):
    """
    compute probabilities from the counts
    """
    for c1 in counts:
        total = float(sum(counts[c1][c2] for c2 in counts[c1]))
        base = 0.0
        for c2 in counts[c1]:
            prob = counts[c1][c2] / total
            base = base + prob
            counts[c1][c2] = base
    return counts


def makeup(counts, n):
    """
    make up a text using the markov model of the original text
    """
    st = '^' * n
    text = []
    while st != '$' * n:
        d = counts[st]
        r = random.random()
        for next in d:
            if d[next] > r:
                break
        st = st[1:] + next
        text.append(next)
    return ''.join(text)


n = 3

counts = defaultdict(lambda: defaultdict(int))

counts = analyse(counts, text, n)

counts = compute_prob(counts)

print (makeup(counts, n))
input("Press ENTER to exit")