from ..src.lparser import split_expression


def test_split_expression():
    text = "(a)(b)"
    expr_texts = split_expression(text)

    assert expr_texts == ["a", "b"]

    text = "a(b)"
    expr_texts = split_expression(text)

    assert expr_texts == ["a", "b"]

    text = "(a)b"
    expr_texts = split_expression(text)

    assert expr_texts == ["a", "b"]

    text = "(a)b(c)"
    expr_texts = split_expression(text)

    assert expr_texts == ["a", "b", "c"]

    text = "a(b)c"
    expr_texts = split_expression(text)

    assert expr_texts == ["a", "b", "c"]


def test_split_expression_double_parans():
    text = "((a))"
    expr_texts = split_expression(text)

    assert expr_texts == ["(a)"]


def test_split_expression_func():
    text = r"\x.(\y.y)"
    expr_texts = split_expression(text)

    assert expr_texts == [r"\x.(\y.y)"]
