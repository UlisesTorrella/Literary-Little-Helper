# -*- coding: utf-8 -*-
"""Takes a portion of the corpus to train a context sensitive grammar.
Uses tokenization in -d

Usage:
  train_grammar.py -n name -d directory -c corpus
  train_grammar.py -h | --help

Options:
  -c <file>     Corpus location
  -n <file>     Name of the training corpus
  -d <file>     Directory for trained data
  -h --help     Show this screen.
"""
from docopt import docopt
from nltk.corpus import PlaintextCorpusReader
from nltk.data import LazyLoader
from model.grammar import Grammar, Production
from model.symbol import Symbol
import pickle

if __name__ == '__main__':
    opts = docopt(__doc__)
    print("TRAIN GRAMMAR: ")
    # Get the corpus
    corpus = opts['-c']
    location = opts['-d'] + opts['-n'] + '.'

    print("getting corpus from: " + corpus)
    model = PlaintextCorpusReader(corpus, '.*\.txt', sent_tokenizer=LazyLoader('tokenizers/punkt/spanish.pickle'), encoding="utf8")


    # Create grammar
    terminals = set()
    epsilon = Symbol("ε", True)
    terminals.add(epsilon) ## epsilon terminal
    non_terminals = set()
    s = Symbol("S", False)  # Starting non terminal
    non_terminals.add(s)
    grammar = Grammar(non_terminals, terminals, s)
    # This is only to tell me how advanced the process is
    count = 0.0
    len_fileids = len(model.fileids())

    # Get the tokenized corpus
    tokens_location = location + "tokenized"
    print("getting tokens from: " + tokens_location)
    f = open(tokens_location, 'rb')
    tokens = pickle.load(f)
    f.close()

    # Train the grammar model with a context of -+1
    for fileid in model.fileids():
        spanish_sents = model.sents(fileid)
        print(str((count / len_fileids) * 100) + "%")
        count += 1
        # Between training with the entire corpus or just bits I get a small difference of productions, so it's not worth it
        fro = 0.55 * len(spanish_sents)
        to = 0.6 * len(spanish_sents)
        for sent in spanish_sents[int(fro):int(to)]:
            tokenized_sentence = []
            for word in sent:
                ts = tokens[word]
                tokenized_sentence.append(ts)
                grammar.add_terminal(ts)

            i = 0
            for terminal in tokenized_sentence[:-1]:
                # if this is the longest we have generated so far, we will need new non terminals (All the k = i part is
                # just to be sure it wont throw NullPointerException, the difference should never be greater than 1)
                k = len(grammar.non_terminals_hierarchy)
                while i >= len(grammar.non_terminals_hierarchy)-1:
                    new_nt = Symbol("A" + str(k), False)
                    grammar.non_terminals_hierarchy.append(new_nt)
                    grammar.add_non_terminal(new_nt)
                    k += 1

                p = Production(N=grammar.non_terminals_hierarchy[i], right=[tokenized_sentence[i],
                                                                            grammar.non_terminals_hierarchy[i+1]],
                               alpha=tokenized_sentence[:i])
                grammar.add_production(p)
                i += 1
            p = Production(N=grammar.non_terminals_hierarchy[i], right=[tokenized_sentence[i]],

                           alpha=tokenized_sentence[:i])
            grammar.add_production(p)


    # save it
    filename = location + "grammar"
    f = open(filename, 'wb')
    pickle.dump(grammar, f)
    f.close()
