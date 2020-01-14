# -*- coding: utf-8 -*-

import pickle
from model.grammar import Grammar
from model.symbol import Symbol
import random

f = open("Spanish/spanish.grammar", 'rb')
grammar = pickle.load(f)
f.close()

for a, p in grammar.P.items():
    for f in p:
        print(str(f))
'''
s = grammar.get_start()
empty_alpha = [Symbol("<s>", True)]
empty_beta = [Symbol("</s>", True)]
product = random.choice(grammar.get_possible_productions(empty_alpha + [s] + empty_beta))
sentence_beg = []
sentence_end = []
while len(product.right) > 1:
    print(product.right)
    sentence_beg.append(product.right[0])
    sentence_end.append(product.right[-1:])
    product = random.choice(grammar.get_possible_productions(product.right))

print(product.right)
sentence_end.reverse()
print(sentence_beg + sentence_end)
'''

