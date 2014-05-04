"""
analysing and generation of texts using markov models

(c) Thomas Waldmann, Felix Buehler MIT license

todo:
input for random output
web-integration
"""

print ("Welcome to Password-Generator\nwritten by Felix Buehler and Thomas Waldmann")

import random
import os.path
import sys
from collections import defaultdict

count = 0
lenght = 0
n = 3

def exit_prog():
    input ("\nPress Enter to quit: ")
    sys.exit()
    
def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def analyse(counts, text, n):
    """
    analyse text with n chars markov state, update the counts
    """
    text = '^' * n + text + '$' * n
    for i in range(len(text) - n):
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
    make up a word using the markov model of the original text
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

def password_count(count):
    while True:         # you really want that many passwords improve
        while True:
            try:
                count = int(input("How much passwords do you want? "))
                break
            except ValueError:
                print ("You have to enter a number")
        if count >= 1:
                if count <= 200:
                    return count
                else:
                    x = 0
                    while x == 0:
                        many_passwords = input("You really want that many passwords? (y/n) ")
                        if many_passwords.lower().strip() in "y yes".split():
                            x = 1
                            return count
                        elif many_passwords.lower().strip() in "n no".split():
                            x = 2
                        else:
                            print ("You have to enter yes or no!")
                            continue
        else:
            print ("You don't want to have no password")


def password_lenght(lenght):
    while True:
        plural = "password"
        if pw_count != 1:
            plural = "passwords"
        while True:
            try:
                lenght = int(input("How long should your " + plural + " be? "))
                break
            except ValueError:
                print ("You have to enter a number")
        if lenght > 3:
            if lenght <= 25:
                return lenght
            else:
                x = 0
                if plural == "password":
                    plural = "a password"
                while x == 0:
                    long_passwords = input("You really want " + plural + " that long? (hard to generate) (y/n) ")
                    if long_passwords.lower().strip() in "y yes".split():
                        x = 1
                    elif long_passwords.lower().strip() in "n no".split():
                        x = 2
                    else:
                        print ("You have to enter yes or no!")
                        continue
                if x == 1:
                    return lenght
                else:
                    continue
        else:
            print ("You don't want to have a password with less than four letters, because it is very insecure.")

try:
    text = set(open( os.path.abspath(".") + "/dict/text.txt").read().split())
except FileNotFoundError:
    print ("The dict/text.txt file was not found.")
    exit_prog()
try:
    words = open( os.path.abspath(".") + "/dict/words.txt").read()
except FileNotFoundError:
    print ("The dict/words.txt file was not found.")
    exit_prog()

pw_count = password_count(count)
pw_lenght = password_lenght(lenght)
print ("\nanalysing text...")
counts = defaultdict(lambda: defaultdict(int))
for word in text:
    counts = analyse(counts, word, n)
print ("calculating...")
counts = compute_prob(counts)

print ("generating...\n")
words_done = 0
for i in range(5000000):
    madeup_word = makeup(counts, n).lower()
    if madeup_word not in words.lower() and len(madeup_word) == pw_lenght and madeup_word.isalpha():
        print (madeup_word)
        words_done += 1
    #print ("           " + str(i+1) + "-crap:       " + madeup_word)
    elif words_done == int(pw_count):
        break
else:
    if words_done == 0:
        go_on = input("\nIt took too long to generate!!!\n(in 5 million generations there were no matches)\nTry it one more time with other settings.\nYou want to run the programm again? (y/n)")
    elif words_done <= pw_count:
        go_on = input("It was not possible to generate " + str(pw_count) + " passwords, because it took to long.\nYou want to run the programm again? (y/n)")
    if go_on.lower().strip() in "y yes".split():
        restart_program()
exit_prog()
