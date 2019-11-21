from ..src.ltypes import Symbol, Function, Application
from ..src.lreducer import reduce_expression
from ..src.debug import assert_comparison


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

    expr = Application(
        Function(
            Symbol("x"), Application(Function(Symbol("x"), Symbol("x")), Symbol("x"))
        ),
        Symbol("a"),
    )
    reduced = reduce_expression(expr)

    assert reduced == Symbol("a")


def test_reduce_function_reused_names_free():

    # Error:    (λx.(λy.xy))y -> (λy.yy)
    # Expected: (λx.(λy.xy))y -> (λt.yt) (where y is renamed t)

    expr = Application(
        Function(
            Symbol("x"), Function(Symbol("y"), Application(Symbol("x"), Symbol("y")))
        ),
        Symbol("y"),
    )

    reduced = reduce_expression(expr)

    error = Function(Symbol("y"), Application(Symbol("y"), Symbol("y")))
    expected = Function(Symbol("t"), Application(Symbol("y"), Symbol("t")))

    # Error
    assert_comparison(reduced, error, expected_result=False)

    # Expected
    assert_comparison(reduced, expected)

