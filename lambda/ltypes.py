class Expression:
    pass

class Name(Expression):
    def __init__(self, name):
        self.name = name

class Function(Expression):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class Application(Expression):
    def __init__(self, expr_1, expr_2):
        self.expr_1 = expr_1
        self.expr_2 = expr_2

class Definition:
    def __init__(self, symbol, func):
        self.symbol = symbol
        self.func = func

