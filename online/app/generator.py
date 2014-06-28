#!/usr/bin/env python3

import random
import os.path
from collections import defaultdict

n = 3
cancel = False

def analyse(counts, text, n):
    #analyse text with n chars markov state, update the counts
    
    text = '^' * n + text + '$' * n
    for i in range(len(text) - n):
        st = i, text[i:i+n]
        next = text[i+n]
        counts[st][next] += 1
    return counts


def compute_prob(counts):
    #compute ranges in [0 .. 1) from the counts
    
    for c1 in counts:
        total = float(sum(counts[c1][c2] for c2 in counts[c1]))
        base = 0.0
        for c2 in counts[c1]:
            prob = counts[c1][c2] / total
            base = base + prob
            counts[c1][c2] = base
    return counts

def makeup(counts, n):
    #make up a word using the markov model of the original text
    
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

def stop():
	cancel = True

def text_import(dict_path):
    try:
        text = set(open( dict_path + "text.txt", 'r').read().split())
    except FileNotFoundError:
        print ("The dict/text.txt file was not found.")
        #return ("The dict/text.txt file was not found.")
    return text

def words_import(dict_path):
    try:
        words = open( dict_path + "words.txt", 'r').read()
    except FileNotFoundError:
        print ("The dict/words.txt file was not found.")
        #return ("The dict/words.txt file was not found.")
    return words

def generate(pw_lenght, pw_count):
    #print ("reading...")
    dict_path = os.path.join(os.path.abspath(".") + r"/app/dict/")
    text = text_import(dict_path)
    words = words_import(dict_path)
    #print ("analysing text...")
    counts = defaultdict(lambda: defaultdict(int))

    for word in text:
        counts = analyse(counts, word, n)

    #print ("calculating...")
    counts = compute_prob(counts)

    print ("generating...")
    words_done = 0
    finish_passwords = []
    for i in range(500000):
        madeup_word = makeup(counts, n).lower()
        #break
        if cancel == True:
        	return
        elif madeup_word not in words.lower() and len(madeup_word) == pw_lenght and madeup_word.isalpha():
            print (madeup_word)
            finish_passwords.append(madeup_word)
            words_done += 1
        #print ("           " + str(i+1) + "-crap:       " + madeup_word)
        elif words_done == int(pw_count):
            return(finish_passwords)
