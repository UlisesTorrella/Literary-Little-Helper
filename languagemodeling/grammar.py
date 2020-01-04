
class Symbol(object):
    # symbol is a String, and terminal a Boolean
    def __init__(self, symbol, terminal):
        self.symbol = symbol
        self.terminal = terminal
    def __eq__(self, other):
        return (self.symbol == other.symbol) and (self.terminal == other.terminal)
    def __hash__(self):
        return hash(tuple((self.symbol, self.terminal)))
    def __str__(self):
        return self.symbol
    def __repr__(self):
        return self.__str__()

class Production(object):
    # Ehere alpha and beta must be a list of symbols, N a non terminal
    # and right another list of symbols
    def __init__(self,  N, right, alpha = [], beta = []):
        assert(not N.terminal)
        self.alpha = [] + alpha
        self.N = N
        self.beta = [] + beta
        self.right = right
    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        alpha =  [str(element) for element in self.alpha]
        beta =  [str(element) for element in self.beta]
        right =  [str(element) for element in self.right]
        return str(alpha) + str(self.N) + str(beta) + " -> " + str(right)

    def __repr__(self):
        return self.__str__()

    def produce(self, N, alpha = [], beta = []):
        assert(self.isValid(alpha, N, beta))
        return alpha + self.right + beta
    # where i tells us where to find N to apply the production
    def producei(self, symbols, i = 0):
        return self.produce(alpha = symbols[:i], N = symbols[i], beta = symbols[i+1:])

    def isValid(self, alpha, N, beta):
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

    #nonterminal and terminal are sets containing Symbols
    #start must be in nonterminals
    def __init__(self, nonterminal, terminal, start):
        assert(start in nonterminal)
        assert((not n.terminal)for n in nonterminal)
        self.N = nonterminal
        self.T = terminal
        # we have dictionary of production to optimize searchs
        self.P = dict()
        for n in self.N:
            self.P[n] = set()
        self.S = start

    # takes alfa, beta, arrays of Symbols; N nonterminal;
    # result is an array of Symbols where terminal are Strings
    def addProduction(self,  N, right, alpha = [], beta = []):
        production = Production(N = N,right = right, alpha = alpha, beta = beta)
        self.P[N].add(production)
        return production

    # does list of words(Strings) contained in terminals
    def isTerminal(self, list):
        return set(list).issubset(self.T)

    # takes a nonterminal and it's context and produces a list only containing terminal symbols
    def getPossibleProductions(self, symbols):
        result = []
        for i, symbol in enumerate(symbols):
            if not symbol.terminal:
                for production in self.P[symbol]:
                    if production.isValid(symbols[:i], symbol, symbols[i+1:]):
                        result.append(production)
        return result
