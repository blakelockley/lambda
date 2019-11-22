from ..src.ltypes import Symbol, Function, Application
from ..src.lparser import parse_expression
from ..src.lreducer import reduce_expression
from ..src.debug import assert_comparison


def test_evaluate_succ_one():
    text = r"(\wyx.y(wyx))(\sz.sz)"
    expected = r"\yx.y(yx)"

    expr = parse_expression(text)
    result = reduce_expression(expr)
    actual = str(result)

    assert expected == actual

def test_evaluate_add_two_one():
    text = r"(\sz.s(sz))(\wyx.y(wyx))(\sz.sz)"
    expected = r"\yx.y(y(yx))"

    expr = parse_expression(text)
    result = reduce_expression(expr)
    actual = str(result)

    assert expected == actual
