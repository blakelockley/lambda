from typing import Tuple, List
from .ltypes import Expression, Application, Function, Symbol
from .lexceptions import ReducerError

Bindings = Tuple[List[Symbol], List[Symbol]]


def find_variable_bindings(expr, *, _func_symbols=[]) -> Bindings:

    # Free
    # <name> is free in <name>.
    # <name> is free in λ<name1>.<exp> if the identifier <name>=<name1> and <name> is free in <exp>.
    # <name> is free in E1E2 if <name> is free in E1 or if it is free in E2.

    # Bound
    # <name> is bound in λ<name1>.<exp> if the identifier <name>=<name1> or if <name> is bound in <exp>.
    # <name> is bound in E1E2 if <name> is bound in E1 or if it is bound in E2.

    func_symbols = _func_symbols.copy()

    free_symbols = []
    bound_symbols = []

    if isinstance(expr, Symbol):
        symbol = expr
        if symbol not in func_symbols:
            free_symbols.append(symbol)

    elif isinstance(expr, Function):
        func = expr
        func_symbols.append(func.symbol)

        frees, bounds = find_variable_bindings(func.expr, _func_symbols=func_symbols)
        free_symbols.extend(frees)
        bound_symbols.extend([func.symbol] + bounds)

    elif isinstance(expr, Application):
        appl = expr

        bindings_1 = find_variable_bindings(appl.expr_1, _func_symbols=func_symbols)
        bindings_2 = find_variable_bindings(appl.expr_2, _func_symbols=func_symbols)

        frees, bounds = bindings_1
        free_symbols.extend(frees)
        bound_symbols.extend(bounds)

        frees, bounds = bindings_2
        free_symbols.extend(frees)
        bound_symbols.extend(bounds)

    else:
        raise ReducerError(
            f"Unable to find free vairables for expression {expr} of invalid type {expr.__class__}."
        )

    return (free_symbols, bound_symbols)


def replace_symbol(
    target: Symbol, expr: Expression, new_expr: Expression
) -> Expression:

    # Symbol
    if isinstance(expr, Symbol):
        symbol = expr
        return new_expr if (symbol == target) else symbol

    # Function
    if isinstance(expr, Function):
        func = expr

        # If a function contains this target as its bound symbol end replacing
        #   TODO: Ensure all symbols are unique for this to be correct
        if func.symbol == target:
            return expr

        # Transverse further to find and replace symbol
        else:
            body_expr = replace_symbol(target, func.expr, new_expr)
            return Function(func.symbol, body_expr)

    # Application
    if isinstance(expr, Application):
        appl = expr
        expr_1 = replace_symbol(target, appl.expr_1, new_expr)
        expr_2 = replace_symbol(target, appl.expr_2, new_expr)

        return Application(expr_1, expr_2)

    raise ReducerError(f"Unable to replace {target} in {expr}.")


def reduce_expression_iteration(expr: Expression) -> Expression:

    # Application
    if isinstance(expr, Application):
        lhs = expr.expr_1
        rhs = expr.expr_2

        if isinstance(lhs, Function):
            symbol = lhs.symbol
            return replace_symbol(symbol, lhs.expr, rhs)

        reduced_rhs = reduce_expression_iteration(rhs)
        reduced_lhs = reduce_expression_iteration(lhs)
        return Application(reduced_lhs, reduced_rhs)

    # Function
    if isinstance(expr, Function):
        return Function(expr.symbol, reduce_expression_iteration(expr.expr))

    # Symbol (Leaf)
    if isinstance(expr, Symbol):
        return expr

    raise ReducerError(f"Unable to reduce expression: {expr}.")


def reduce_expression(expr: Expression) -> Expression:

    reduced = reduce_expression_iteration(expr)
    while reduced != expr:
        expr = reduced
        reduced = reduce_expression_iteration(expr)

    return reduced
