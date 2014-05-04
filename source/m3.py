"""
analysing and generation of texts using markov models

(c) Thomas Waldmann, MIT license
"""

import random
from collections import defaultdict

text = open("m2.txt").read()


def analyse(counts, text, n):
    """
    analyse text with n chars markov state, update the counts
    """
    text = '^' * n + text + '$' * n
    for i in xrange(len(text) - n):
        st = i, text[i:i+n]
        next = text[i+n]
        counts[st][next] += 1
    return counts


def compute_prob(counts):
    """
    compute ranges in [0 .. 1) from the counts
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
    st = 0, '^' * n
    text = []
    while st[1] != '$' * n:
        d = counts[st]
        r = random.random()
        for next in d:
            if d[next] > r:
                break
        st = st[0] + 1, st[1][1:] + next
        text.append(next)
    return ''.join(text)[:-n]


n = 3

counts = defaultdict(lambda: defaultdict(int))

words = set(open("/usr/share/dict/words").read().split())

for word in words:
    counts = analyse(counts, word, n)

counts = compute_prob(counts)

for i in xrange(1000):
    madeup_word = makeup(counts, n)
    if madeup_word not in words:
        print madeup_word,

