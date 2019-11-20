import re
from .ltypes import Symbol, Function, Application, Definition

# Expression
PAT_SYMBOL = re.compile(r"[a-z]")  # x
PAT_FUNCTION = re.compile(r"\\([a-z]+)\.(.+)")  # \x.<expr>

# Application
#   <expr><x|\x.<expr>|(<expr>)>
PAT_APPLICATION = re.compile(r"(.+)([a-z]|\\[a-z]+\..+|\(.+\))")

# Defintion
PAT_DEFINITION = re.compile(r"([A-Z0-9])\s*=\s*(.+)")  # S = <expr>

# Expressions
PAT_NESTED_PARANS = re.compile(r"\((.+)\)")


class ParserError(Exception):
    pass


def strip_parans(text: str):
    """Strip nested parans"""

    m = re.fullmatch(PAT_NESTED_PARANS, text)
    while m:
        text = m.group(1)
        m = re.fullmatch(PAT_NESTED_PARANS, text)

    return text


def split_expression(text: str):
    """
    Return a list of expr_text at the top level of 'text'.
    """

    if len(text) == 0:
        raise ParserError("Unable to split expressions from empty string.")

    result = []
    start = 0
    counter = 0

    for pos, char in enumerate(text):

        # If we find a top level function we can break the loop,
        #   the remainder of 'text' will be appended to result
        if char == "\\" and counter == 0:
            break

        elif char == "(":
            # Check of we finished parsing free text
            if counter == 0:
                # Check if valid free text
                if start != pos:
                    result.append(text[start:pos])

                # Record opening paran pos
                start = pos

            counter += 1

        elif char == ")":
            counter -= 1

            # Check if we finished parsing parans
            if counter == 0:
                expr_text = strip_parans(text[start + 1 : pos])

                if len(expr_text) == 0:
                    raise ParserError(f"Empty parans in snippet {line} are invalid.")

                result.append(expr_text)

                # Resest counter
                counter = 0
                start = pos + 1

    # Append trailing free text
    if start < len(text):
        expr_text = text[start:]
        result.append(expr_text)

    return result


def parse_expression(text: str):

    # Top-level (relative) expressions
    exprs = split_expression(text)

    # Update text with parans stripped
    if len(exprs) == 1:
        text = exprs[0]

    elif len(exprs) >= 2:
        # TODO: use deque
        expr = parse_expression(exprs.pop(0))

        while len(exprs) > 0:
            expr_2 = parse_expression(exprs.pop(0))
            expr = Application(expr, expr_2)

        return expr

    # Symbol
    m = re.fullmatch(PAT_SYMBOL, text)
    if m:
        return Symbol(text)

    # Function
    m = re.fullmatch(PAT_FUNCTION, text)
    if m:
        symbols, expr_text = m.groups()

        # Consume symbols in reverse order to build nested functions.
        symbols = list(symbols)

        expr = parse_expression(expr_text)
        func = Function(Symbol(symbols.pop()), expr)

        while len(symbols) > 0:
            func = Function(Symbol(symbols.pop()), func)

        return func

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
