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

