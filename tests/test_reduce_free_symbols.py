from ..src.ltypes import Symbol, Function, Application
from ..src.lparser import parse_expression
from ..src.lreducer import find_free_variables
from ..src.debug import assert_comparison


def test_reduce_symbols_free_name_in_name():

    # <name> is free in <name>.
    # a -> [Symbol("a")]

    expr = parse_expression("a")
    frees = find_free_variables(expr)

    assert frees == [Symbol("a")]


def test_reduce_symbols_free_name_in_func():

    # <name> is free in λ<name1>.<exp> if the identifier <name>!=<name1> and <name> is free in <exp>.
    # λa.b -> [Symbol("b")]

    expr = parse_expression(r"\a.b")
    frees = find_free_variables(expr)

    assert frees == [Symbol("b")]


def test_reduce_symbols_free_name_in_appl():

    # <name> is free in E1E2 if <name> is free in E1 or if it is free in E2.
    # (λa.ac)(λb.b) -> [Symbol("c")]

    expr = parse_expression(r"(\a.ac)(\b.b)")
    frees = find_free_variables(expr)

    assert frees == [Symbol("c")]


def test_reduce_symbols_bound_name_in_appl():

    # <name> is bound in λ<name1>.<exp> if the identifier <name>=<name1> or if <name> is bound in <exp>.
    # λa.a -> []

    expr = parse_expression(r"(\a.ac)(\b.b)")
    frees = find_free_variables(expr)

    assert Symbol("a") not in frees


def test_reduce_symbols_bound_name_in_appl():

    # <name> is bound in E1E2 if <name> is bound in E1 or if it is bound in E2.

    # <name> is both bound and unbound the following expression:
    #   (λa.a)(λb.ba)

    expr = parse_expression(r"(\a.a)(\b.ba)")
    frees = find_free_variables(expr)

    assert Symbol("a") in frees

    expr = parse_expression(r"(\a.a)")
    frees = find_free_variables(expr)

    assert Symbol("a") not in frees

    expr = parse_expression(r"(\b.ba)")
    frees = find_free_variables(expr)

    assert Symbol("a") in frees

    assert False


def test_reduce_rename_symbols_find_free_basic():

    # λt.yt -> [Symbol("y")]

    expr = parse_expression(r"\t.yt")
    frees = find_free_variables(expr)

    assert frees == [Symbol("y")]


def test_reduce_rename_symbols_find_free_bound_other():

    # (λt.yt)(λy.yt) -> [Symbol("y"), Symbol("t")]

    expr = parse_expression(r"(\t.yt)(\y.yt)")
    frees = find_free_variables(expr)

    assert frees == [Symbol("y"), Symbol("t")]


def test_reduce_rename_symbols_find_free_none_nested():

    # λy.(λt.yt) -> \yt.yt -> []

    expr = parse_expression(r"\yt.(\t.yt)")
    frees = find_free_variables(expr)

    assert frees == []


def test_reduce_rename_symbols_find_free_deep_nested():

    # λxy.x(λt.yt(xa)) -> [Symbol("a")]

    expr = parse_expression(r"\xy.x(\t.yt(xa))")
    frees = find_free_variables(expr)

    assert frees == [Symbol("a")]

