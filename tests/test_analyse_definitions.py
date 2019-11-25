import pytest
from ..src.ltypes import Definition, Symbol, Function, Application
from ..src.lparser import parse_expression
from ..src.lanalyser import analyse_definitions
from ..src.lexceptions import AnalyserError
from ..src.debug import assert_comparison


def test_analyse_definitions():
    defn = Definition("name", Symbol("a"))
    defns = {defn.name: defn}

    text = "$name"
    expr = parse_expression(text)

    result = analyse_definitions(expr, defns)
    expected = Symbol("a")

    assert_comparison(result, expected)


def test_analyse_definitions_func_body():
    defn = Definition("name", Symbol("a"))
    defns = {defn.name: defn}

    text = r"\x.($name)"
    expr = parse_expression(text)

    result = analyse_definitions(expr, defns)
    expected = Function(Symbol("x"), Symbol("a"))

    assert_comparison(result, expected)


def test_analyse_definitions_appl_func():
    defn = Definition("name", Function(Symbol("x"), Symbol("x")))
    defns = {defn.name: defn}

    text = r"$name(a)"
    expr = parse_expression(text)

    result = analyse_definitions(expr, defns)
    expected = Application(Function(Symbol("x"), Symbol("x")), Symbol("a"))

    assert_comparison(result, expected)


def test_analyse_definitions_appl_func_func():
    defn = Definition("name", Function(Symbol("x"), Symbol("x")))
    defns = {defn.name: defn}

    text = r"(\x.x)(\x.x)"
    expr = parse_expression(text)

    result = analyse_definitions(expr, defns)
    expected = Application(
        Function(Symbol("x"), Symbol("x")), Function(Symbol("x"), Symbol("x"))
    )

    assert_comparison(result, expected)


def test_analyse_definitions_raise_not_found():
    defns = {}

    text = r"$name"
    expr = parse_expression(text)

    with pytest.raises(AnalyserError):
        result = analyse_definitions(expr, defns)
