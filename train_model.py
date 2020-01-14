# -*- coding: utf-8 -*-
"""Train an AddOne model and pickle saves it in -d

Usage:
  train_model.py -d directory -c corpus
  train_model.py -h | --help

Options:
  -c <file>     Corpus location
  -d <file>     Directory for trained data
  -h --help     Show this screen.
"""
from docopt import docopt
from nltk.corpus import PlaintextCorpusReader
from nltk.data import LazyLoader
import pickle

from model.ngram import NGram, InterpolatedNGram, AddOneNGram

if __name__ == '__main__':
    opts = docopt(__doc__)
    corpus_directory = opts['-c']
    location = opts['-d']

    corpus = PlaintextCorpusReader(corpus_directory, '.*\.txt', sent_tokenizer=LazyLoader('tokenizers/punkt/spanish.pickle'), encoding="utf8")
    sents = corpus.sents()

    model = AddOneNGram(3, sents)

    # save it
    filename = location + "model"
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()

