from ..src.ltypes import Symbol, Function, Application
from ..src.lreducer import reduce_expression


def test_reduce_symbol():
    expr = Symbol("a")
    reduced = reduce_expression(expr)

    assert reduced == Symbol("a")


def test_reduce_function():
    expr = Function(Symbol("a"), Symbol("a"))
    reduced = reduce_expression(expr)

    assert reduced == Function(Symbol("a"), Symbol("a"))


def test_reduce_function_application():
    expr = Application(Function(Symbol("a"), Symbol("a")), Symbol("b"))
    reduced = reduce_expression(expr)

    assert reduced == Symbol("b")


def test_reduce_function_application_func():
    expr = Application(
        Function(Symbol("a"), Symbol("a")), Function(Symbol("x"), Symbol("x"))
    )
    reduced = reduce_expression(expr)

    assert reduced == Function(Symbol("x"), Symbol("x"))


def test_reduce_function_application_body():
    expr = Application(
        Function(Symbol("x"), Application(Symbol("y"), Symbol("x"))), Symbol("a")
    )
    reduced = reduce_expression(expr)

    assert reduced == Application(Symbol("y"), Symbol("a"))


def test_reduce_function_reused_names():

    # Reduce should not change the bound symbol in the nested function
    # (\x.(\x.x)x)a -> (\x.x)a

    expr = Application(
        Function(
            Symbol("x"), Application(Function(Symbol("x"), Symbol("x")), Symbol("x"))
        ),
        Symbol("a"),
    )
    reduced = reduce_expression(expr)

    assert reduced == Application(Function(Symbol("x"), Symbol("x")), Symbol("a"))
