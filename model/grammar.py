class Production(object):
    # here alpha and beta must be a list of symbols, N a non terminal
    # and right another list of symbols
    def __init__(self, N, right, alpha=[], beta=[]):
        assert(not N.terminal)
        self.alpha = [] + alpha
        self.N = N
        self.beta = [] + beta
        self.right = right
    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        alpha = [str(element) for element in self.alpha]
        beta = [str(element) for element in self.beta]
        right = [element.symbol for element in self.right]
        return str(alpha) + str(self.N) + str(beta) + " -> " + str(right)

    def __repr__(self):
        return self.__str__()

    def produce(self):
        return self.right

    def left(self):
        return self.alpha + [self.N] + self.beta

    def is_valid(self, alpha, N, beta):
        if self.N != N:
            return False
        validAlpha= False
        validBeta = False
        if len(self.alpha)>len(alpha):
            return False
        else:
            if len(alpha)>len(self.alpha):
                if(alpha[len(alpha) - len(self.alpha):] == self.alpha):
                    validAlpha = True
            else:
                if self.alpha == alpha:
                    validAlpha = True

        if len(self.beta)>len(beta):
            return False
        else:
            if len(beta)>len(self.beta):
                if(beta[:len(self.beta)] == self.beta):
                    validBeta = True
            else:
                if self.beta == beta:
                    validBeta = True

        return validAlpha and validBeta

#    def degenerate(self, symbols):
        #TODO


class Grammar(object):
    # TODO make Grammar Ngrammable
    # nonterminal and terminal are sets containing Symbols
    # start must be in nonterminals
    def __init__(self, nonterminal, terminal, start):
        assert(start in nonterminal)
        assert((not n.terminal)for n in nonterminal)
        self.N = nonterminal
        self.T = terminal
        # we have dictionary of production to optimize searches
        self.P = dict()
        for n in self.N:
            self.P[n] = set()
        self.S = start
        self.non_terminals_hierarchy = [self.S]

    def __str__(self):
        r = ""
        for i, l in self.P.items():
            for p in l:
                r += str(p) + "\n"
        return r

    # Takes a production and adds it to the P set
    def add_production(self, production):
        self.P[production.N].add(production)
        return production

    # does list of Symbols contained in terminals
    def is_terminal(self, list):
        return set(list).issubset(self.T)

    # takes a non terminal and it's context and produces a list only containing terminal symbols
    def get_possible_productions(self, symbols):
        result = []
        for i, symbol in enumerate(symbols):
            if not symbol.terminal:
                for production in self.P[symbol]:
                    if production.is_valid(symbols[:i], symbol, symbols[i + 1:]):
                        result.append(production)
        return result

    def add_terminal(self, symbol):
        assert symbol.terminal
        self.T.add(symbol)

    def add_non_terminal(self, symbol):
        assert not symbol.terminal
        self.N.add(symbol)
        self.P[symbol] = set()

    def get_start(self):
        return self.S

    def get_possible_produced(self, symbols, nonterminal):
        result = []
        for production in self.P[nonterminal]:
            if production.right == symbols:
                result.append(production)
        return result
