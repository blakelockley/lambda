from ltypes import Definition, Function, Application


def print_debug(expr, *, indent=0, increment=2):

    if isinstance(expr, Definition):
        print(" " * indent + "Definition:")
        print_debug(expr.name, indent=indent + increment)
        print_debug(expr.func, indent=indent + increment)

    elif isinstance(expr, Function):
        print(" " * indent + "Function:")
        print_debug(expr.symbol, indent=indent + increment)
        print_debug(expr.expr, indent=indent + increment)

    elif isinstance(expr, Application):
        print(" " * indent + "Application:")
        print_debug(expr.expr_1, indent=indent + increment)
        print_debug(expr.expr_2, indent=indent + increment)

    else:
        print(" " * indent + repr(expr))
