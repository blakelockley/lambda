from ..src.lparser import parse_expression
from ..src.ltypes import Symbol, Function, Application


def test_symbol():
    text = r"x"
    expr = parse_expression(text)

    assert expr == Symbol('x')

def test_function_basic():
    text = r"\x.x"
    expr = parse_expression(text)

    assert expr == Function(Symbol('x'), Symbol('x'))

def test_function_body():
    text = r"\x.xy"
    expr = parse_expression(text)

    assert expr == Function(
        Symbol('x'),
        Application(Symbol('x'), Symbol('y'))
    )

def test_function_nested():
    text = r"\x.(\z.z)"
    expr = parse_expression(text)

    assert expr == Function(
        Symbol('x'),
        Function(
            Symbol('z'),
            Symbol('z')
        )
    )

def test_application():
    text = r"xy"
    expr = parse_expression(text)

    assert expr == Application(Symbol('x'), Symbol('y'))

def test_func_symbol_application():
    text = r"(\x.x)y"
    expr = parse_expression(text)

    assert expr == Application(
        Function(
            Symbol('x'),
            Symbol('x')
        ),
        Symbol('y')
    )

def test_func_func_application():
    text = r"(\x.x)(\y.y)"
    expr = parse_expression(text)

    assert expr == Application(
        Function(
            Symbol('x'),
            Symbol('x')
        ),
        Function(
            Symbol('y'),
            Symbol('y')
        )
    )

def test_func_func_no_parans_after():
    text = r"(\x.x)\y.y"
    expr = parse_expression(text)

    assert expr == Application(
        Function(
            Symbol('x'),
            Symbol('x')
        ),
        Function(
            Symbol('y'),
            Symbol('y')
        )
    )

def test_func_symbol__nested_func():
    text = r"\x.x(\y.y)"
    expr = parse_expression(text)

    assert expr == Application(
        Function(
            Symbol('x'),
            Application(
                Symbol('x'),
                Function(
                    Symbol('y'),
                    Symbol('y')
                )
            )
        )
    )

def test_func_nested_func_application():
    text = r"(\x.x)(\y.(\a.a)y)"
    expr = parse_expression(text)

    assert expr == Application(
        Function(
            Symbol('x'),
            Symbol('x')
        ),
        Function(
            Symbol('y'),
            Application(
                Function(
                    Symbol("a"),
                    Symbol("a")
                ),
                Symbol('y')
            )
        )
    )
