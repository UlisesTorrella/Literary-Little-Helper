from collections import defaultdict
from random import random
import operator


class NGramGenerator(object):

    def __init__(self, model):
        """
        model -- n-gram model.
        """
        self._n = model._n

        # compute the probabilities
        probs = defaultdict(dict)
        count = model._count.copy()
###        model._count[()] = 14 Algun dia sacarse la duda
        count.pop(())
        count.pop(('<s>',)) # no queremos que exista prob de empezar una nueva oracion
        for gram in count:
            gram = list(gram)
            lastword = gram.pop()
            probs[tuple(gram)].update({ lastword : model.cond_prob(lastword, gram) })

        self._probs = dict(probs)
#        for key, value in self._probs.items():
#            print(sum(value.values()))
        # sort in descending order for efficient sampling
        self._sorted_probs = sorted_probs = {}
        for key, value in self._probs.items():
            self._sorted_probs[key] = sorted(value.items(), key=operator.itemgetter(1))

    def generate_sent(self):
        """Randomly generate a sentence."""
        word = "<s>"
        sentence = [word]
        i = 0
        n = self._n
        while word != "</s>":
            word = self.generate_token(tuple(sentence[i:i+n-1]))
            sentence.append(word)
            i += 1
        return sentence[1:len(sentence)-1]

    def generate_token(self, prev_tokens=None):
        """Randomly generate a token, given prev_tokens.

        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        r = random()
        i = 0
        word, prob = self._sorted_probs[prev_tokens][0]
        acum = prob
        '''
        sea una acumulada discreta escalonada tenemos algo asi
         [0] [1]         [2]        r              [3]    [4][5]             [6]     [7]   [8]
        0|----|-----------|-------------------------|------|--|---------------|-------|-----|1
        por eso hay mas chances de que r caiga en la posicion de mayor probabilidad
        y por eso lo ordenamos
        '''
        l = len(self._sorted_probs[prev_tokens] ) # Para que addone no se pase
        while r>acum: ## Buscamos en la funcion acumulada nuestro valor random
            i+=1
            i = i%l
            word, prob = self._sorted_probs[prev_tokens][i]
            acum += prob
        return word
