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
