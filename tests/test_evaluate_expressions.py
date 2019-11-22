from ..src.ltypes import Symbol, Function, Application
from ..src.lparser import parse_expression
from ..src.lreducer import reduce_expression
from ..src.debug import assert_comparison


def _evaluate_and_assert(text, expected):
    """
    Hellper function for boiler plate operations of the tests
    """

    expr = parse_expression(text)
    result = reduce_expression(expr)
    actual = str(result)

    assert expected == actual


def test_evaluate_succ_one():
    text = r"(\wyx.y(wyx))(\sz.sz)"
    expected = r"\yx.y(yx)"

    _evaluate_and_assert(text, expected)


def test_evaluate_add_two_one():
    text = r"(\sz.s(sz))(\wyx.y(wyx))(\sz.sz)"
    expected = r"\yx.y(y(yx))"

    _evaluate_and_assert(text, expected)


def test_evaluate_multiply():
    text = r"(\abc.a(bc))(\sz.s(sz))(\sz.s(sz))"
    expected = r"\cz.c(c(c(cz)))"

    _evaluate_and_assert(text, expected)


def test_evaluate_negate():
    text = r"(\x.x(\ab.b)(\ab.a))(\uv.u)"
    expected = r"\ab.b"

    _evaluate_and_assert(text, expected)


def test_evaluate_name_reused():
    text = r"(\xa.ax)(\a.a)b"
    expected = r"b(\a.a)"

    _evaluate_and_assert(text, expected)


def test_evaluate_subexpression_parans():
    text = r"((\xa.ax)(\a.a))b"
    expected = r"b(\a.a)"

    _evaluate_and_assert(text, expected)
