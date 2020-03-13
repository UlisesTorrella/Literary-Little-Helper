import re
from collections import defaultdict
import random
import operator
from math import ceil

from reportlab import xrange

from statistics.syllable_per_word import get_mean_syllable
from utils.spanish_syllables import how_many_syllables_sent, how_many_syllables_word
from .grammar import Grammar
from .symbol import Symbol


class GrammarSensitiveGenerator(object):

    def __init__(self, model, grammar, tokens):
        """
        :type tokens: set of string to Symbol
        :type grammar: object of model.grammar.Grammar
        :type model: object of model.ngram.LanguageModel
        """
        self._n = model._n
        self.model = model
        self.grammar = grammar
        self.tokens = tokens
        # compute the probabilities
        probs = defaultdict(dict)
        count = model._count.copy()
        count.pop(())
        count.pop(('<s>',)) # no queremos que exista prob de empezar una nueva oracion
        for gram in count:
            gram = list(gram)
            last_word = gram.pop()
            if last_word in tokens.keys():
                probs[tokens[last_word]].setdefault(tuple(gram), {}).update({last_word : model.cond_prob(last_word, gram)})

        self._probs = dict(probs)

        #        for key, value in self._probs.items():
        #            print(sum(value.values()))
                # sort in descending order for efficient sampling
        self._sorted_probs = defaultdict(dict)
        for tok in self._probs.keys():
            for key, value in self._probs[tok].items():
                self._sorted_probs[tok].setdefault(key, {})
                self._sorted_probs[tok][key] = sorted(value.items(), key=operator.itemgetter(1), reverse=True)

    def generate_sent(self):
        """Randomly generate a sentence.
        returns string
        """
        n = self._n
        s = self.grammar.get_start()
        grammar = self.grammar
        word = "<s>"
        sentence = [word]
        alpha = [s]
        product = [1, 2, 3]
        i = 0
        while len(product) > 1:
            product = random.choice(grammar.get_possible_productions(alpha))\
                .produce()
            word = self.generate_word(tuple(sentence[i:i + n - 1]), product[0])
            # get rid of the old non terminal, and replace it by the new product
            alpha = alpha[:-1] + product
            sentence.append(word)
            i += 1
        return ' '.join(sentence[1:])

    '''
    # Brute forcing conditions, it may be impossible or highly improbable, should be time catched
    def generate_sent_restricted(self, conditions):
        """
        Randomly generate a sentence of given syllables that matches array of conditions
                In case is not possible, returns -1
        :type conditions: List of RegEx
        """
        sent = self.generate_sent()
        while not conditions.are_all_attained(sent):
            print(sent)
            sent = self.generate_sent()
        return sent
    '''

    def get_word_that_matches(self, regex):
        r = random.choice(tuple(self.model.vocabulary()))
        i = 0
        while re.match(regex, r, re.IGNORECASE) is None and i < self.model.V():
            r = random.choice(tuple(self.model.vocabulary()))
            i += 1
        return r

    def generate_verse(self, syllables, rhyme=".*", attempts=10, persistence=10):
        """
        Generate a verse of given syllables and rhyme
        :param attempts: how many times will we try to rhyme
        :param syllables: Amount of syllables
        :param rhyme: regex for last word
        :param persistence: how many times it will try to find a verse matching both rhyme and syllable
        :return: string
        """
        n = self._n
        s = self.grammar.get_start()
        grammar = self.grammar
        # as many attempts as we are allowed (attempts as words that rhyme that we will try to put in a sentence with
        # given amount of syllables
        for _ in xrange(attempts):
            # get me any word that rhymes and it will be the last
            word = self.get_word_that_matches(rhyme)
            # what's its token?
            token = self.tokens[word]
            # estimate the amount of words we will need to match the required syllables
            w = ceil(syllables/get_mean_syllable(self.model))
            # around that much of words we will generate (it's clumsy)
            # we need to do this to choose how deep into our grammar to look for the token we have, the token can be
            # anywhere, it's useless to look for it in depth 1 given that the words has less than x syllables
            #### in case of i=4 we will try sentences of lenght 3, 4, 5 and 6
            for i in range(w-1, w+2):
                # we get a list of all the possible productions that get will us to 'word''s token, given it's context
                # [token] means we are looking for producctions that return only token, and no NonTerminals
                # grammar.non_terminals_hierarchy[i] comes as "the nonterminal for i depth"
                possibilities = grammar.get_possible_produced([token], grammar.non_terminals_hierarchy[i])
                if not possibilities:
                    # if it's empty then we have a token that can't be the last one
                    break
                # any of those productions, we pick it's context alpha, as we ignore beta in this program. [:-1] because
                # we already have that one
                sentence_tokens = random.choice(possibilities).alpha[:-1]
                patience = persistence
                # let's match token to word, attempting to satisfy the syllables condition.
                # until we lose our patience as a poet
                while patience > 0:
                    sentence = ["<s>"]
                    for token in sentence_tokens:
                        sentence.append(self.generate_word(tuple(sentence[i:i + n - 1]), token))
                    sentence.append(word)
                    # does it comply with the requested sentences?
                    if how_many_syllables_sent(' '.join(sentence[1:])) != syllables:
                        patience -= 1
                    else:
                        return ' '.join(sentence[1:])
        return -1

    def generate_word_restricted(self, regex, prev_tokens=None, token=None):
        """Randomly generate a token, given prev_tokens.

        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        returns -1 if it's impossible to match the regex
        """
        assert isinstance(token, Symbol)
        if token == Symbol('ε', True):
            return "</s>"
        x = random.choice(list(self._sorted_probs[token.symbol].keys()))
        if prev_tokens not in self._sorted_probs[token.symbol].keys():
            options = self._sorted_probs[token.symbol][x]
        else:
            options = self._sorted_probs[token.symbol][prev_tokens]
        for option in options:
            if re.match(regex, option[0]) is not None:
                return option[0]
        return -1

    def generate_word(self, prev_tokens=None, token=None):
        """Randomly generate a token, given prev_tokens.

        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        assert isinstance(token, Symbol)
        if token == Symbol('ε', True):
            return "</s>"
        r = random.random()
        i = 0
        x = random.choice(list(self._sorted_probs[token].keys()))
        if prev_tokens not in self._sorted_probs[token].keys():
            word, prob = self._sorted_probs[token][x][0]
            l = len(self._sorted_probs[token][x]) # Para que addone no se pase
        else:
            word, prob = self._sorted_probs[token][prev_tokens][0]
            l = len(self._sorted_probs[token][prev_tokens])  # Para que addone no se pase
        acum = prob
        '''
        sea una acumulada discreta escalonada tenemos algo asi
         [0] [1]         [2]        r              [3]    [4][5]             [6]     [7]   [8]
        0|----|-----------|-------------------------|------|--|---------------|-------|-----|1
        por eso hay mas chances de que r caiga en la posicion de mayor probabilidad
        y por eso lo ordenamos
        '''
        while r > acum:  # Buscamos en la funcion acumulada nuestro valor random
            i += 1
            i = i % l
            if prev_tokens not in self._sorted_probs[token].keys():
                word, prob = self._sorted_probs[token][x][i]
            else:
                word, prob = self._sorted_probs[token][prev_tokens][i]
            acum += prob
        return word
