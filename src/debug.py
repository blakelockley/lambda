from .ltypes import Function, Application


def print_debug(expr, *, indent=0, increment=2):

    if isinstance(expr, Function):
        print(" " * indent + "Function:")
        print_debug(expr.symbol, indent=indent + increment)
        print_debug(expr.expr, indent=indent + increment)

    elif isinstance(expr, Application):
        print(" " * indent + "Application:")
        print_debug(expr.expr_1, indent=indent + increment)
        print_debug(expr.expr_2, indent=indent + increment)

    else:
        print(" " * indent + repr(expr))


def assert_comparison(actual, expected, *, expected_result=True):

    actual_result = actual == expected

    if actual_result != expected_result:

        if expected_result is True:  # verbose
            print("* Actual")
            print_debug(actual)

            print()  # blank line
            print("* Expected")
            print_debug(expected)

            raise AssertionError(f"Compared expressions are not equal.")

        else:
            print("* Expression")
            print_debug(actual)

            raise AssertionError(f"Compared expressions are equal (unexpected).")
