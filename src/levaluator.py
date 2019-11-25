from .ltypes import Definition
from .lparser import parse_expression
from .lreducer import reduce_expression
from .lanalyser import analyse_definitions


def evaluate_file(filename, defns={}):

    with open(filename) as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            line = line.replace("λ", "\\")  # Replace λ with substitued lambda characted

            if len(line) == 0:
                continue

            expr = parse_expression(line)
            expr = analyse_definitions(expr, defns)
            reduced = reduce_expression(expr)

            if isinstance(expr, Definition):
                defn = expr
                defns[defn.name] = defn

            else:
                print(str(reduced))
