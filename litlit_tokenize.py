# -*- coding: utf-8 -*-
"""Go word by word of given model's vocabulary tokenizing it with the SpanishTokenizer, and store it. (it's the
 most time consuming script)
    Todo: Make it possible to choose different tokenizers

Usage:
  litlit_tokenize.py -n name -d directory
  litlit_tokenize.py -h | --help

Options:
  -n <file>     Name of the training corpus
  -d <file>     Directory for trained data
  -h --help     Show this screen.
"""
from docopt import docopt
from model.symbol import Symbol
from tokenizer.spanish.spanish import SpanishTokenizer
import pickle

if __name__ == '__main__':
    opts = docopt(__doc__)
    location = opts['-d'] + opts['-n'] + '.'

    f = open(location + "model", 'rb')
    model = pickle.load(f)
    f.close()


    # Dictionary of words and it's token for later use
    tokenized = dict()
    notfound = set()

    tokenizer = SpanishTokenizer()
    found = 0.0
    error = 0
    voc = model.vocabulary()
    voc_size = model.V()

    for word in voc:
        token = tokenizer.tokenize(word)
        if token != word:
            print(str((float(found + error) / voc_size) * 100) + "%")
            tokenized[word] = Symbol(token, True)
            found += 1
        else:
            notfound.add(word)
            tokenized[word] = Symbol(word, True)
            print(word)
            error += 1

    print("found: " + str(found))
    print("error: " + str(error))
    # I'm getting a 0.78 rate
    print("success rate = " + str(found/voc_size))

    # save the dictionary
    filename = location + "tokenized"
    f = open(filename, 'wb')
    pickle.dump(tokenized, f)
    f.close()

    # save not found words
    filename = location + "notfound"
    f = open(filename, 'wb')
    pickle.dump(notfound, f)
    f.close()
