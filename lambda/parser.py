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


def parse_expression(text: str):

    print("#", text)

    # Explict Expression (by parans)
    m = re.fullmatch(PAT_EXP_PARANS, text)
    if m:
        return parse_expression(m.group(1))

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
