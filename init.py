# -*- coding: utf-8 -*-

from nltk.corpus import PlaintextCorpusReader
from nltk.data import LazyLoader
from languagemodeling.ngram import NGram
from languagemodeling.ngram_generator import NGramGenerator
from languagemodeling.grammar import Grammar, Symbol, Production

corpus_spanish = "corpus/spanish"
corpus_english = "corpus/english"

#spanish = PlaintextCorpusReader(corpus_spanish, '.*\.txt', sent_tokenizer=LazyLoader('tokenizers/punkt/spanish.pickle'), encoding="utf8")
#english = PlaintextCorpusReader(corpus_english, '.*\.txt')
#spanish_sents = spanish.sents()
#english_sents = english.sents()

#spanish_model = NGram(3, spanish_sents)
#english_model = Ngram(3, english_sents)

#spanish_generator = NGramGenerator(spanish_model)

#for i in range(10):
#    print(' '.join(spanish_generator.generate_sent()))

terminals = set()
a = Symbol("a", True)
terminals.add(a)
b = Symbol("b", True)
terminals.add(b)
nonterminals = set()
xA = Symbol("A", False)
nonterminals.add(xA)
s = Symbol("S", False)
nonterminals.add(s)
grammar = Grammar(nonterminals, terminals, s)
from math import floor
p = grammar.addProduction(N = s, right=[a,s,b])
e = grammar.addProduction(N = s, right=[])

print(grammar.getPossibleProductions([s]))
