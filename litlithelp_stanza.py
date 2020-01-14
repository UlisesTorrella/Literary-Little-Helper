"""Generate Gibberish

Usage:
  litlithelp_stanza.py -s syllables -r rhyme -d directory
  litlithelp_stanza.py -h | --help

Options:
  -r <rhyme>     asonante, consonante
  -s <syllables> syllables for each verse
  -d <directory> where is the trained data
  -h --help      Show this screen.
"""
from docopt import docopt
import pickle
from model.generator import GrammarSensitiveGenerator


def consonante(s):
    first_verse = generator.generate_verse(syllables=s, attempts=1000)
    if first_verse == -1:
        print("no pude")
        return -1
    print(first_verse)
    second_verse = generator.generate_verse(syllables=s, attempts=1000)
    if second_verse == -1:
        print("no pude")
        return -1
    print(second_verse)
    third_verse = generator.generate_verse(syllables=s, attempts=1000)
    if third_verse == -1:
        print("no pude")
        return -1
    print(third_verse)
    forth_verse = generator.generate_verse(syllables=s, attempts=1000, rhyme=".*" + second_verse[-3:] + "$")
    if forth_verse == -1:
        print("no pude")
        return -1
    print(forth_verse)


vowels = {'a', 'e', 'i', 'o', 'u', 'á', 'é', 'í', 'ó', 'ú',
          'A', 'E', 'I', 'O', 'U', 'Á', 'É', 'Í', 'Ó', 'Ú'}


def asonante(s):
    first_verse = generator.generate_verse(syllables=s, attempts=1000)
    if first_verse == -1:
        print("no pude")
        return -1
    print(first_verse)
    second_verse = generator.generate_verse(syllables=s, attempts=1000)
    if second_verse == -1:
        print("no pude")
        return -1
    print(second_verse)
    third_verse = generator.generate_verse(syllables=s, attempts=1000)
    if third_verse == -1:
        print("no pude")
        return -1
    print(third_verse)
    forth_verse = generator.generate_verse(syllables=s, attempts=1000,
                                           rhyme=".*" + '[^aeiouAEIOUáéíóúÁÉÍÓÚ]'.join([q if q in vowels else ''
                                                                                        for q in second_verse]
                                                                                       [-3:]) + "$")
    if forth_verse == -1:
        print("no pude")
        return -1
    print(forth_verse)


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

    syllables = int(opts['-s'])
    if opts['-r'] == "asonante":
        asonante(syllables)
    elif opts['-r'] == "consonante":
        consonante(syllables)
