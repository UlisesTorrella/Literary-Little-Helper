"""Generate Gibberish

Usage:
  litlithelp_sentence.py -d directory -n times
  litlithelp_sentence.py -h | --help

Options:
  -d <directory> where is the trained data
  -n <times>      how many
  -h --help      Show this screen.
"""
from docopt import docopt
import pickle
from reportlab import xrange
from model.generator import GrammarSensitiveGenerator


def title(n):
    for _ in xrange(n):
        print(generator.generate_sent())


if __name__ == "__main__":
    opts = docopt(__doc__)
    assert (isinstance(opts['-d'], type('')))

    location = opts['-d']
    # Pick up the trained model
    f = open(location + "model", 'rb')
    spanish_model = pickle.load(f)
    f.close()

    # Get the grammar
    f = open(location + "grammar", 'rb')
    spanish_grammar = pickle.load(f)
    f.close()

    # Don't forget about the tokens
    f = open(location + "tokenized", 'rb')
    spanish_tokens = pickle.load(f)
    f.close()

    # Generate

    generator = GrammarSensitiveGenerator(spanish_model, spanish_grammar, spanish_tokens)

    title(int(opts['-n']))
