from nltk.tokenize import WordPunctTokenizer
import re

vocal_cerrada = "[iuIU]"
vocal_cerrada_tonica = "[íúÍÚ]"
vocal_abierta = "[aeoAEO]"
vocal_abierta_tonica = "[áéóÁÉÓ]"
hiato = "(" + vocal_abierta + "h*" + vocal_abierta + "|" + vocal_abierta +\
        "h*" + vocal_cerrada_tonica + "|" + vocal_cerrada_tonica + "h*" + vocal_abierta + ")"
diptongo = "(" + vocal_cerrada + "h*" + vocal_cerrada + "|" + vocal_abierta +\
        "h*" + vocal_cerrada + "|" + vocal_cerrada + "h*" + vocal_abierta + "|" + vocal_cerrada + "h*" \
           + vocal_abierta_tonica + ")"
vowels = "[aeiouAEIOUáéíóúÁÉÍÓÚyY]"


def how_many_syllables_sent(sentence):
    """
    :param sentence: string containing a sentence in spanish
    :return: the approximate amount of syllables in sentence
    """
    tokenizer = WordPunctTokenizer()
    words = tokenizer.tokenize(sentence)
    res = 0
    for word in words:
        res = res + how_many_syllables_word(word)
    return res


def how_many_syllables_word(word):
    if re.search(hiato, word) is None and re.search(diptongo, word) is None:
        # Solo es la cantidad de vocales en la palabra
        return len(re.findall(vowels, word))
    else:
        if re.search(diptongo, word) is None:
            # es hiato
            return len(re.findall(vowels, word))
        else:
            # es diptongo
            return len(re.findall(vowels, word)) - len(re.findall(diptongo, word))

