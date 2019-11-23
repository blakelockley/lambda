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
        symbols = [self.symbol]
        expr = self.expr

        while isinstance(expr, Function):
            symbols.append(expr.symbol)
            expr = expr.expr

        symbol_str = str().join(map(str, symbols))
        return f"\\{symbol_str}.{expr}"

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
        a = str(self.expr_1)
        if not isinstance(self.expr_1, Symbol):
            a = f"({a})"

        b = str(self.expr_2)
        if not isinstance(self.expr_2, Symbol):
            b = f"({b})"

        return f"{a}{b}"

    def __eq__(self, other):
        if not isinstance(other, Application):
            return False

        return self.expr_1 == other.expr_1 and self.expr_2 == other.expr_2


class Definition(Expression):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def __repr__(self):
        return f"Definition({repr(self.name)}, {repr(self.expr)})"

    def __str__(self):
        return f"{self.name} = {self.expr}"

    def __eq__(self, other):
        if not isinstance(other, Definition):
            return False

        return self.name == other.name and self.expr == other.expr


class DefinitionCall(Expression):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"DefinitionCall({repr(self.name)})"

    def __str__(self):
        return f"{self.name}"

    def __eq__(self, other):
        if not isinstance(other, DefinitionCall):
            return False

        return self.name == other.name
