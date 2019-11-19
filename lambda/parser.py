import re
from ltypes import Symbol, Function, Application, Definition

# Expression
PAT_SYMBOL = re.compile(r"[a-z]")  # x
PAT_FUNCTION = re.compile(r"\\([a-z]+)\.(.+)")  # \x.<expr>

# Application
#   <expr><x|\x.<expr>|(<expr>)>
PAT_APPLICATION = re.compile(r"(.+)([a-z]|\\[a-z]+\..+|\(.+\))")

# Defintion
PAT_DEFINITION = re.compile(r"([A-Z0-9])\s*=\s*(.+)")  # S = <expr>


class ParserError(Exception):
    pass


def match_parans(text: str):
    """
    Return a list of expr_text at the top level of 'text'.
    """

    # TODO: Have this split top level expressions

    if text[0] != "(":
        return []

    result = []
    start = 0
    counter = 0

    for pos, char in enumerate(text):

        if char == "(":
            counter += 1

        elif char == ")":
            counter -= 1

        if counter == 0:
            expr_text = text[start + 1 : pos]
            result.append(expr_text)

            # Resest counter
            counter = 0
            start = pos + 1

    return result


def parse_expression(text: str):

    # Top-level (relative) expressions
    exprs = match_parans(text)

    if len(exprs) >= 1:
        expr = parse_expression(exprs.pop())

        while len(exprs) > 0:
            expr_1 = parse_expression(exprs.pop())
            expr = Application(expr_1, expr)

        return expr

    # Symbol
    m = re.fullmatch(PAT_SYMBOL, text)
    if m:
        return Symbol(text)

    # Function
    m = re.fullmatch(PAT_FUNCTION, text)
    if m:
        symbol_text, expr_text = m.groups()

        symbol = Symbol(symbol_text)
        expr = parse_expression(expr_text)

        return Function(symbol, expr)

    # Application
    m = re.fullmatch(PAT_APPLICATION, text)
    if m:
        expr_1, expr_2 = map(parse_expression, m.groups())

        return Application(expr_1, expr_2)

    raise ParserError(f"Unable to parse expression: {text}")


def parse(source: str):

    definitions = {}

    lines = (line for line in source.split("\n") if len(line) > 0)
    for line in lines:
        m = re.fullmatch(PAT_DEFINITION, line)

        if not m:
            raise ParserError(
                "Top level statements must be named function definitions."
            )

        name, expr_text = m.groups()
        expr = parse_expression(expr_text)

        defn = Definition(name, expr)
        definitions[name] = defn

    return definitions
