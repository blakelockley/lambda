class Expression:
    pass


class Symbol(Expression):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Symbol({repr(self.name)})"

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if not isinstance(other, Symbol):
            return False

        return self.name == other.name


class Function(Expression):
    def __init__(self, symbol, expr):
        self.symbol = symbol
        self.expr = expr

    def __repr__(self):
        return f"Function({repr(self.symbol)}, {repr(self.expr)})"

    def __str__(self):
        return f"\\{self.symbol}. {self.expr})"

    def __eq__(self, other):
        if not isinstance(other, Function):
            return False

        # TODO: Implement true equivalence independant of variable name
        #   e.g. \x.xy == \s.sz (True)
        return self.symbol == other.symbol and self.expr == other.expr


class Application(Expression):
    def __init__(self, expr_1, expr_2):
        self.expr_1 = expr_1
        self.expr_2 = expr_2

    def __repr__(self):
        return f"Application({repr(self.expr_1)}, {repr(self.expr_2)})"

    def __str__(self):
        return f"({self.expr_1}) ({self.expr_2})"

    def __eq__(self, other):
        if not isinstance(other, Application):
            return False

        return self.expr_1 == other.expr_1 and self.expr_2 == other.expr_2


class Definition:
    def __init__(self, name, func):
        self.name = name
        self.func = func

    def __repr__(self):
        return f"Definition({repr(self.name)}, {repr(self.func)})"

    def __str__(self):
        return f"{self.name} = {self.func}"

    def __eq__(self, other):
        return self.name == other.name and self.func == other.func


class DefinitionCall(Expression):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"DefinitionCall({repr(self.name)})"

    def __str__(self):
        return f"{self.name}"

    def __eq__(self):
        return self.name == other.name
