#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://docs.python.org/3/library/collections.html
from collections import defaultdict
import math



class LanguageModel(object):

    def sent_prob(self, sent):
        """Probability of a sentence. Warning: subject to underflow problems.

        sent -- the sentence as a list of tokens.
        """
        n = self._n
        sent.insert(0, '<s>')
        sent.append('</s>')
        prob = 1
        for i in range(len(sent)-n):
            segment = sent[i:i+n]
            cond=self.cond_prob(segment.pop(), segment)
            prob = prob*cond
        return prob

    def sent_log_prob(self, sent):
        """Log-probability of a sentence.

        sent -- the sentence as a list of tokens.
        """
        n = self._n
        sent.insert(0, '<s>')
        sent.append('</s>')
        prob = 0
        for i in range(len(sent)-n):
            segment = sent[i:i+n]
            cond=self.cond_prob(segment.pop(), segment)
            if cond == 0.0:
                return -float("inf")
            prob = prob+math.log(cond,2)
        return prob

    def log_prob(self, sents):
        """Log-probability of a list of sentences.

        sents -- the sentences.
        """
        log_prob = 0
        for sent in sents:
            log_prob += self.sent_log_prob(sent)
        return log_prob

    def cross_entropy(self, sents):
        """Cross-entropy of a list of sentences.

        sents -- the sentences.
        """
        return (-1)*self.log_prob(sents)/len(self._count)

    def perplexity(self, sents):
        """Perplexity of a list of sentences.

        sents -- the sentences.
        """
        return 2**self.cross_entropy(sents)


class NGram(LanguageModel):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
        assert n > 0
        self._n = n

        count = defaultdict(int)
        while(n>=0):
            for sent in sents:
                s = sent[:] ## En una oracio auxiliar agrego el item de start y end para contarlos
                s.insert(0, "<s>")
                s.append("</s>")
                for i in range(len(s)-n+1):
                    count[tuple(s[i:i+n])] += 1
            n -= 1
        count[()] = count[()]-count[('<s>',)]-count[('</s>',)] # Pero no quiero que <s> y </s> sean considerados por ()
        self._count = count

    def count(self, tokens):
        """Count for an n-gram or (n-1)-gram.

        tokens -- the n-gram or (n-1)-gram tuple.
        """
        return self._count.get(tuple(tokens), 0)

    def cond_prob(self, token, prev_tokens=()):
        """Conditional probability of a token.

        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        assert len(prev_tokens)<self._n
        if (self.count(prev_tokens) == 0):
            return 0.0
        return float(self.count(list(prev_tokens) + [token]))/float(self.count(prev_tokens))



class AddOneNGram(NGram):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
        # call superclass to compute counts
        super(AddOneNGram, self).__init__(n, sents)

        # compute vocabulary
        self._voc = voc = set()
        for sent in sents:
            voc = voc.union(set(sent))
        voc.add('</s>')
        self._voc = voc
        self._V = len(voc)  # vocabulary size

    def V(self):
        """Size of the vocabulary.
        """
        return self._V

    def cond_prob(self, token, prev_tokens=()):
        """Conditional probability of a token.

        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        return float(self.count(list(prev_tokens) + [token]) + 1)/float(self.count(prev_tokens) + self._V)

class InterpolatedNGram(NGram):


    def __init__(self, n, sents, gamma=None, addone=True):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        gamma -- interpolation hyper-parameter (if not given, estimate using
            held-out data).
        addone -- whether to use addone smoothing (default: True).
        """
        assert n > 0
        self._n = n

        if gamma is not None:
            # everything is training data
            train_sents = sents
        else:
            # 90% training, 10% held-out
            m = int(0.45 * len(sents))
            l = int(0.65 * len(sents))
            train_sents = sents[:m] + sents[l:]
            held_out_sents = sents[m:l]

        print('Computing counts...')
        count = defaultdict(int)
        while(n>=0):
            for sent in train_sents:
                s = sent[:] ## En una oracion auxiliar agrego el item de start y end para contarlos
                s.insert(0, "<s>")
                s.append("</s>")
                for i in range(len(s)-n+1):
                    count[tuple(s[i:i+n])] += 1
            n -= 1
        count[()] = count[()]-count[('<s>',)]-count[('</s>',)] # Pero no quiero que <s> y </s> sean considerados por ()
        self._count = count
        # WORKed HERE!!
        # COMPUTE COUNTS FOR ALL K-GRAMS WITH K <= N

        # compute vocabulary size for add-one in the last step
        self._addone = addone
        if addone:
            print('Computing vocabulary...')
            self._voc = voc = set()
            for sent in sents:
                voc = voc.union(set(sent))
            voc.add('</s>')
            self._voc = voc
            self._V = len(voc)

        # compute gamma if not given
        if gamma is not None:
            self._gamma = gamma
        else:
            print('Computing gamma...')
            self._gamma = gamma = 1
            p = self.log_prob(held_out_sents)
            new_gamma = 2
            streak = 1
            growing = True
            turns = 0
            while(turns<15):
                self._gamma = new_gamma
                np = self.log_prob(held_out_sents)
                gamma = new_gamma
                if(np>p):
                    if growing:
                        streak += 1
                    else:
                        turns +=1
                        streak = 0
                        growing = True
                    new_gamma = new_gamma + 2**streak
                else:
                    if growing:
                        turns += 1
                        streak = 0
                        growing = False
                    else:
                        streak += 1
                    new_gamma = new_gamma - 2**streak
                p = np
            self._gamma = new_gamma
            print(self._gamma)

    def count(self, tokens):
        """Count for an k-gram for k <= n.

        tokens -- the k-gram tuple.
        """
        return self._count[tuple(tokens)]

    def sub_cond_prob(self, token, prev_tokens=()):
        """Conditional probability of a token.

        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        assert len(prev_tokens)<self._n
        if (self.count(prev_tokens) == 0):
            return 0.0
        return float(self.count(list(prev_tokens) + [token]))/float(self.count(prev_tokens))

    def sub_cond_prob_addone(self, token, prev_tokens=()):
        """Conditional probability of a token.

        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        return float(self.count(list(prev_tokens) + [token]) + 1)/float(self.count(prev_tokens) + self._V)

    def cond_prob(self, token, prev_tokens=()):
        """Conditional probability of a token.

        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self._n
        lambdas = [0]*n
        res = 0
        for i in range(0,n-1):
            lambdas[i] = (1-sum(lambdas[:i]))*float(self.count(prev_tokens[i:]))/(float(self.count(prev_tokens[i:])) + self._gamma)
            res = res + lambdas[i]*self.sub_cond_prob(token, prev_tokens[i:])
        lambdas[n-1]= (1-sum(lambdas))
        assert(sum(lambdas)==1.0)
        if(self._addone):
            return float(res+lambdas[n-1]*self.sub_cond_prob_addone(token))
        else:
            return float(res+lambdas[n-1]*self.sub_cond_prob(token))


class BackOffNGram:

    def __init__(self, n, sents, beta=None, addone=True):
        """
        Back-off NGram model with discounting as described by Michael Collins.

        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        beta -- discounting hyper-parameter (if not given, estimate using
            held-out data).
        addone -- whether to use addone smoothing (default: True).
        """
        assert n > 0
        self._n = n

        # compute beta if not given
        if beta is not None:
            # everything is training data
            train_sents = sents
            self._beta = beta
        else:
            # 90% training, 10% held-out
            #m = int(0.45 * len(sents))
            #l = int(0.65 * len(sents))
            #train_sents = sents[:m] + sents[l:]
            #held_out_sents = sents[m:l]
            m = int(0.9 * len(sents))
            train_sents = sents[:m]
            held_out_sents = sents[m]
            print('Computing beta...')
            self._beta = gamma = 1
            p = self.log_prob(held_out_sents)
            new_beta = 2
            streak = 1
            growing = True
            turns = 0
            while(turns<15):
                self._beta = new_beta
                np = self.log_prob(held_out_sents)
                beta = new_beta
                if(np>p):
                    if growing:
                        streak += 1
                    else:
                        turns +=1
                        streak = 0
                        growing = True
                    new_beta = new_beta + 2**streak
                else:
                    if growing:
                        turns += 1
                        streak = 0
                        growing = False
                    else:
                        streak += 1
                    new_beta = new_beta - 2**streak
                p = np
            self._beta = new_beta
            print(self._beta)

        print('Computing counts...')
        count = defaultdict(int)
        while(n>=0):
            for sent in train_sents:
                s = sent[:] ## En una oracion auxiliar agrego el item de start y end para contarlos
                s.insert(0, "<s>")
                s.append("</s>")
                for i in range(len(s)-n+1):
                    count[tuple(s[i:i+n])] += 1
            n -= 1
        count[()] = count[()]-count[('<s>',)]-count[('</s>',)] # Pero no quiero que <s> y </s> sean considerados por ()
        self._count = count
        # WORKed HERE!!
        # COMPUTE COUNTS FOR ALL K-GRAMS WITH K <= N

        # compute vocabulary
        self._addone = addone
        print('Computing vocabulary...')
        self._voc = voc = set()
        for sent in sents:
            voc = voc.union(set(sent))
        voc.add('</s>')
        self._voc = voc
        self._V = len(voc)

    """
       Todos los metodos de NGram.
    """

    def A(self, tokens):
        """Set of words with counts > 0 for a k-gram with 0 < k < n.

        tokens -- the k-gram tuple.
        """


    def alpha(self, tokens):
        """Missing probability mass for a k-gram with 0 < k < n.

        tokens -- the k-gram tuple.
        """

    def denom(self, tokens):
        """Normalization factor for a k-gram with 0 < k < n.

        tokens -- the k-gram tuple.
        """
