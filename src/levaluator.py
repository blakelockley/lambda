from .ltypes import Definition
from .lparser import parse_expression
from .lreducer import reduce_expression
from .lanalyser import analyse_definitions


def evaluate_source(source: str, defns={}):

    defns = defns.copy()
    lines = source.splitlines()

    last_expr = None

    for n, line in enumerate(lines, 1):
        line = line.strip()
        line = line.replace("λ", "\\")  # Replace λ with substitued lambda characted

        if len(line) == 0:
            continue

        try:
            expr = parse_expression(line)
            expr = analyse_definitions(expr, defns)
            reduced = reduce_expression(expr)

            if isinstance(expr, Definition):
                defn = expr
                defns[defn.name] = defn

            else:
                print(str(reduced))

            last_expr = reduced

        except Exception as e:
            print(f"On line {n} the following exception occured:")
            print(f"{e.__class__.__name__}: {e}")

    return last_expr


def evaluate_file(filename, defns={}):
    with open(filename) as f:
        return evaluate_source(f.read(), defns)
