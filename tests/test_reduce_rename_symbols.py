from ..src.ltypes import Symbol, Function, Application
from ..src.lparser import parse_expression
from ..src.lreducer import rename_symbol
from ..src.debug import assert_comparison


def test_reduce_rename_symbol():
    expr = parse_expression(r"\x.x")
    renamed = rename_symbol(expr, Symbol("x"), Symbol("t"))

    # Next in line replacement symbol is always t
    expected = Function(Symbol("t"), Symbol("t"))

    assert_comparison(renamed, expected)


def test_reduce_rename_symbol_twice():
    expr = parse_expression(r"\xy.xy")
    renamed = rename_symbol(expr, Symbol("x"), Symbol("u"))
    renamed = rename_symbol(renamed, Symbol("y"), Symbol("v"))

    expected = Function(
        Symbol("u"), Function(Symbol("v"), Application(Symbol("u"), Symbol("v")))
    )

    assert_comparison(renamed, expected)


def test_reduce_rename_nested_renamed():
    expr = parse_expression(r"\x.x(\x.x)")
    renamed = rename_symbol(expr, Symbol("x"), Symbol("a"))

    excepted = Function(
        Symbol("a"), Application(Symbol("a"), Function(Symbol("a"), Symbol("a")))
    )

    assert_comparison(renamed, excepted)


def test_reduce_rename_nested_bound():
    expr = parse_expression(r"\x.x(\y.x)")
    renamed = rename_symbol(expr, Symbol("x"), Symbol("a"))

    excepted = Function(
        Symbol("a"), Application(Symbol("a"), Function(Symbol("y"), Symbol("a")))
    )

    assert_comparison(renamed, excepted)


def test_reduce_rename_nested_free():
    expr = parse_expression(r"\y.y(\y.xy)")
    renamed = rename_symbol(expr, Symbol("x"), Symbol("a"))

    excepted = Function(
        Symbol("y"),
        Application(
            Symbol("y"), Function(Symbol("y"), Application(Symbol("a"), Symbol("y")))
        ),
    )

    assert_comparison(renamed, excepted)
