class Expression:
    pass


class Symbol(Expression):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Symbol({repr(self.name)})"

    def __str__(self):
        return self.name


class Function(Expression):
    def __init__(self, symbol, expr):
        self.symbol = symbol
        self.expr = expr

    def __repr__(self):
        return f"Function({repr(self.symbol)}, {repr(self.expr)})"

    def __str__(self):
        return f"\{self.symbol}. {self.expr})"


class Application(Expression):
    def __init__(self, expr_1, expr_2):
        self.expr_1 = expr_1
        self.expr_2 = expr_2

    def __repr__(self):
        return f"Application({repr(self.expr_1)}, {repr(self.expr_2)})"

    def __str__(self):
        return f"({self.expr_1}) ({self.expr_2})"


class Definition:
    def __init__(self, name, func):
        self.name = name
        self.func = func

    def __repr__(self):
        return f"Definition({repr(self.name)}, {repr(self.func)})"

    def __str__(self):
        return f"{self.name} = {self.func}"


class DefinitionCall(Expression):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"DefinitionCall({repr(self.name)})"

    def __str__(self):
        return f"{self.name}"

