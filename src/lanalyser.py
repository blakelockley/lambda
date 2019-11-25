from typing import Dict
from .lexceptions import AnalyserError
from .ltypes import (
    Expression,
    Symbol,
    Function,
    Application,
    Definition,
    DefinitionCall,
)


def analyse_definitions(expr: Expression, defns: Dict[str, Definition]) -> Expression:
    """
    Replace DefinitionCall occurances with their Definition expressions.
    """

    # Symbol
    if isinstance(expr, Symbol):
        return expr

    # Function
    if isinstance(expr, Function):
        func = expr

        body_expr = analyse_definitions(func.expr, defns)
        return Function(func.symbol, body_expr)

    # Application
    if isinstance(expr, Application):
        appl = expr
        expr_1 = analyse_definitions(appl.expr_1, defns)
        expr_2 = analyse_definitions(appl.expr_2, defns)

        return Application(expr_1, expr_2)

    # Definition Call
    #   Access definitions mapping and replace with corresponding expression
    if isinstance(expr, DefinitionCall):
        call = expr
        defn = defns.get(call.name)

        if defn is None:
            raise AnalyserError(f"Definition '{call.name}' does not exist.")

        return analyse_definitions(defn.expr, defns)

    # Definition
    if isinstance(expr, Definition):
        defn = expr
        return Definition(defn.name, analyse_definitions(defn.expr, defns))

    raise AnalyserError(f"Unable to analyze definitions for '{expr}'.")
