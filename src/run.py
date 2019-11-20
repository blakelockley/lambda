from .lparser import parse_expression
from .lreducer import reduce_expression
from .debug import print_debug


if __name__ == "__main__":

    text = "(\\xy.x)a"  # -> \y.a

    expr = parse_expression(text)
    print(repr(expr))

    reduced = reduce_expression(expr)

    print(repr(reduced))
