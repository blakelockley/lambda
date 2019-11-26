from typing import Tuple, List, Iterator
from .ltypes import (
    Expression,
    Application,
    Function,
    Symbol,
    Definition,
    DefinitionCall,
)
from .lexceptions import ReducerError

# Backup symbols to be used in renaming conflicting bound vs free symbols
#   It is deseriable to use uncommon symbols to avoid replacing already replaced symbols
# Common symbol collections:
#   - ab
#   - uv
#   - sz    (numbers)
#   - xyzw
#   - r     (recursion)
# The symbol 't' is often used for the renamed symbol
#   After this iterate through the alphabet natually, skipping reserved symbols
SYMBOL_BACKUPS = map(Symbol, "tcdefghijklmnopq")

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
            f"Unable to find free vairables for expression '{expr}' of invalid type {expr.__class__}."
        )

    return (free_symbols, bound_symbols)


def rename_symbol(expr, target_symbol, new_symbol):

    if isinstance(expr, Symbol):
        symbol = expr
        if symbol == target_symbol:
            return new_symbol

        return symbol

    elif isinstance(expr, Function):
        func = expr
        func_expr = rename_symbol(func.expr, target_symbol, new_symbol)

        if func.symbol == target_symbol:
            return Function(new_symbol, func_expr)

        return Function(func.symbol, func_expr)

    elif isinstance(expr, Application):
        appl = expr

        expr_1 = rename_symbol(appl.expr_1, target_symbol, new_symbol)
        expr_2 = rename_symbol(appl.expr_2, target_symbol, new_symbol)

        return Application(expr_1, expr_2)

    raise ReducerError(f"Unable to rename symbol for expression '{expr}'.")


def substitute(target: Symbol, expr: Expression, new_expr: Expression) -> Expression:

    # Symbol
    if isinstance(expr, Symbol):
        symbol = expr
        return new_expr if (symbol == target) else symbol

    # Function
    if isinstance(expr, Function):
        func = expr

        # If a function contains this target as its bound symbol stop replacing
        if func.symbol == target:
            return expr

        body_expr = substitute(target, func.expr, new_expr)
        return Function(func.symbol, body_expr)

    # Application
    if isinstance(expr, Application):
        appl = expr
        expr_1 = substitute(target, appl.expr_1, new_expr)
        expr_2 = substitute(target, appl.expr_2, new_expr)

        return Application(expr_1, expr_2)

    raise ReducerError(f"Unable to replace '{target}' in '{expr}'.")


# Recursive helper function
def reduce(expr):

    # Definition
    if isinstance(expr, Definition):
        defn = expr
        name = defn.name

        return Definition(name, reduce(defn.expr))

    # Application
    if isinstance(expr, Application):
        lhs = expr.expr_1
        rhs = expr.expr_2

        if isinstance(lhs, Function):
            func = lhs

            func_frees, func_bounds = find_variable_bindings(func)
            new_expr_frees, _ = find_variable_bindings(rhs)

            # Rename any symbols that will conflict
            renamable_symbols = [s for s in func_bounds if s in new_expr_frees]
            for s in renamable_symbols:
                func_symbols = func_frees + func_bounds

                new_symbol = next(
                    filter(lambda s: s not in func_symbols, SYMBOL_BACKUPS), None
                )

                if new_symbol is None:
                    raise ReducerError(
                        f"Unable to rename symbol '{s}' as all replacement symbols are exhausted."
                    )

                func = rename_symbol(func, s, new_symbol)

            symbol = func.symbol
            return substitute(symbol, func.expr, rhs)

        reduced_lhs = reduce(lhs)
        reduced_rhs = reduce(rhs)
        return Application(reduced_lhs, reduced_rhs)

    # Function
    if isinstance(expr, Function):
        return Function(expr.symbol, reduce(expr.expr))

    # Symbol (Leaf)
    if isinstance(expr, Symbol):
        return expr

    raise ReducerError(f"Unable to reduce expression:\n    '{expr}'")


def reduce_expression(expr: Expression) -> Expression:
    """
    Reduce expression to simplest form
    """

    # Reduce and loop
    reduced = reduce(expr)
    while reduced != expr:
        expr = reduced
        reduced = reduce(expr)

    return expr


def generate_reduced_expressions(expr: Expression) -> Iterator[Expression]:
    """
    Reduce expression by yeild each intermediate stage after reducing
    """

    # Reduce original expression
    reduced = reduce(expr)

    # If original expression is already reduced, yeild expr as is
    if reduced == expr:
        yield expr

    # Continue to reduce and yield intermediate stages
    while reduced != expr:
        expr = reduced
        reduced = reduce(expr)

        yield expr

