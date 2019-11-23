import pytest
from ..src.ltypes import Definition, DefinitionCall, Symbol, Function, Application
from ..src.lparser import parse_expression
from ..src.lreducer import reduce_expression
from ..src.lexceptions import ParserError


def test_parse_definition_symbol():
    text = r"name = a"
    defn = parse_expression(text)

    excepted = Definition("name", Symbol("a"))
    assert defn == excepted


def test_parse_definition_function():
    text = r"name = \x.x"
    defn = parse_expression(text)

    excepted = Definition("name", Function(Symbol("x"), Symbol("x")))
    assert defn == excepted


def test_parse_definition_application():
    text = r"name = (\x.x)a"
    defn = parse_expression(text)

    excepted = Definition(
        "name", Application(Function(Symbol("x"), Symbol("x")), Symbol("a"))
    )
    assert defn == excepted


def test_parse_definition_call():
    text = r"name = (\x.x)($name)"
    defn = parse_expression(text)

    excepted = Definition(
        "name", Application(Function(Symbol("x"), Symbol("x")), DefinitionCall("name"))
    )
    assert defn == excepted


def test_parse_definition_call_func():
    text = r"name = (\x.($name)x)"
    defn = parse_expression(text)

    excepted = Definition(
        "name", Function(Symbol("x"), Application(DefinitionCall("name"), Symbol("x")))
    )
    assert defn == excepted


def test_parse_definition_call_invalid_func():
    text = r"name = (\x($name).x)"

    with pytest.raises(ParserError):
        defn = parse_expression(text)


def test_evaluate_definition():
    text = r"name = \x.x"
    defn = parse_expression(text)

    expected_definition = Definition("name", Function(Symbol("x"), Symbol("x")))

    assert defn == expected_definition

    defns = {defn.name: defn}
    text = r"($name)a"

    expr = parse_expression(text)
    result = reduce_expression(expr, definitions=defns)

    assert result == Symbol("a")
