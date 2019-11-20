from ..src.lparser import parse_expression
from ..src.ltypes import Symbol, Function, Application


def test_common_true():
    text = r"\uv.u"
    expr = parse_expression(text)

    assert expr == Function(Symbol("u"), Function(Symbol("v"), Symbol("u"),))


def test_common_false():
    text = r"\uv.v"
    expr = parse_expression(text)

    assert expr == Function(Symbol("u"), Function(Symbol("v"), Symbol("v"),))


def test_common_true_false_true():
    text = r"(\uv.u)(\ab.b)(\xy.x)"
    expr = parse_expression(text)

    assert expr == Application(
        Application(
            Function(Symbol("u"), Function(Symbol("v"), Symbol("u"),)),
            Function(Symbol("a"), Function(Symbol("b"), Symbol("b"),)),
        ),
        Function(Symbol("x"), Function(Symbol("y"), Symbol("x"),)),
    )


def test_common_zero():
    text = r"\sz.z"
    expr = parse_expression(text)

    assert expr == Function(Symbol("s"), Function(Symbol("z"), Symbol("z")))


def test_common_one():
    text = r"\sz.s(z)"
    expr = parse_expression(text)

    assert expr == Function(
        Symbol("s"), Function(Symbol("z"), Application(Symbol("s"), Symbol("z")))
    )


def test_common_two():
    text = r"\sz.s(s(z))"
    expr = parse_expression(text)

    assert expr == Function(
        Symbol("s"),
        Function(
            Symbol("z"), Application(Symbol("s"), Application(Symbol("s"), Symbol("z")))
        ),
    )


def test_common_succ():
    text = r"\wyx.y(wyx)"
    expr = parse_expression(text)

    assert expr == Function(
        Symbol("w"),
        Function(
            Symbol("y"),
            Function(
                Symbol("x"),
                Application(
                    Symbol("y"),
                    Application(Application(Symbol("w"), Symbol("y"),), Symbol("x"),),
                ),
            ),
        ),
    )


def test_common_succ_one():
    text = r"(\wyx.y(wyx))\sz.s(z)"
    expr = parse_expression(text)

    assert expr == Application(
        Function(
            Symbol("w"),
            Function(
                Symbol("y"),
                Function(
                    Symbol("x"),
                    Application(
                        Symbol("y"),
                        Application(
                            Application(Symbol("w"), Symbol("y"),), Symbol("x"),
                        ),
                    ),
                ),
            ),
        ),
        Function(
            Symbol("s"), Function(Symbol("z"), Application(Symbol("s"), Symbol("z")))
        ),
    )
