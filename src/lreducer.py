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


def find_variable_bindings(expr, *, _func_symbols=[], _defns={}) -> Bindings:

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

        frees, bounds = find_variable_bindings(
            func.expr, _func_symbols=func_symbols, _defns=_defns
        )
        free_symbols.extend(frees)
        bound_symbols.extend([func.symbol] + bounds)

    elif isinstance(expr, DefinitionCall):
        call = expr
        defn = _defns.get(call.name)

        frees, bounds = find_variable_bindings(
            defn.expr, _func_symbols=func_symbols, _defns=_defns
        )
        free_symbols.extend(frees)
        bound_symbols.extend(bounds)

    elif isinstance(expr, Application):
        appl = expr

        bindings_1 = find_variable_bindings(
            appl.expr_1, _func_symbols=func_symbols, _defns=_defns
        )
        bindings_2 = find_variable_bindings(
            appl.expr_2, _func_symbols=func_symbols, _defns=_defns
        )

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


def rename_symbol(expr, target_symbol, new_symbol, _defns={}):

    if isinstance(expr, Symbol):
        symbol = expr
        if symbol == target_symbol:
            return new_symbol

        return symbol

    elif isinstance(expr, Function):
        func = expr
        func_expr = rename_symbol(func.expr, target_symbol, new_symbol, _defns=_defns)

        if func.symbol == target_symbol:
            return Function(new_symbol, func_expr)

        return Function(func.symbol, func_expr)

    elif isinstance(expr, DefinitionCall):
        call = expr
        defn = _defns.get(call.name)

        return rename_symbol(defn, target_symbol, new_symbol, _defns=_defns)

    elif isinstance(expr, Application):
        appl = expr

        expr_1 = rename_symbol(appl.expr_1, target_symbol, new_symbol, _defns=_defns)
        expr_2 = rename_symbol(appl.expr_2, target_symbol, new_symbol, _defns=_defns)

        return Application(expr_1, expr_2)

    raise ReducerError(f"Unable to rename symbol for expression '{expr}'.")


def substitute(
    target: Symbol, expr: Expression, new_expr: Expression, _defns={}
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
            func_frees, func_bounds = find_variable_bindings(func, _defns=_defns)
            new_expr_frees, _ = find_variable_bindings(new_expr, _defns=_defns)

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

            body_expr = substitute(target, func.expr, new_expr)
            return Function(func.symbol, body_expr)

    # Definition Call
    if isinstance(expr, DefinitionCall):
        call = expr
        defn = _defns.get(call.name)

        return rename_symbol(target, defn, new_expr, _defns=_defns)

    # Application
    if isinstance(expr, Application):
        appl = expr
        expr_1 = substitute(target, appl.expr_1, new_expr, _defns=_defns)
        expr_2 = substitute(target, appl.expr_2, new_expr, _defns=_defns)

        return Application(expr_1, expr_2)

    raise ReducerError(f"Unable to replace '{target}' in '{expr}'.")


# Recursive helper function
def reduce(expr, defns={}):

    if isinstance(expr, Definition):
        defn = expr
        name = defn.name

        # Remove expression if it included in definitions table
        # NOTE: This means named recursion is unavaliable
        if name in defns:
            defns.pop(name)

        return Definition(name, reduce(defn.expr, defns=defns))

    # Application
    if isinstance(expr, Application):
        lhs = expr.expr_1
        rhs = expr.expr_2

        if isinstance(lhs, Function):
            symbol = lhs.symbol
            return substitute(symbol, lhs.expr, rhs, _defns=defns)

        reduced_rhs = reduce(rhs, defns=defns)
        reduced_lhs = reduce(lhs, defns=defns)
        return Application(reduced_lhs, reduced_rhs)

    # Function
    if isinstance(expr, Function):
        return Function(expr.symbol, reduce(expr.expr, defns=defns))

    # Definition Call
    if isinstance(expr, DefinitionCall):
        call = expr
        defn = defns.get(call.name)

        if defn is None:
            raise ReducerError(f"Call to definition '{call.name}' that does not exist.")

        return defn.expr

    # Symbol (Leaf)
    if isinstance(expr, Symbol):
        return expr

    raise ReducerError(f"Unable to reduce expression:\n    '{expr}'")


def reduce_expression(expr: Expression, definitions={}) -> Expression:
    """
    Reduce expression to simplest form
    """

    # Reduce and loop
    reduced = reduce(expr, defns=definitions)
    while reduced != expr:
        expr = reduced
        reduced = reduce(expr, defns=definitions)

    return expr


def generate_reduced_expressions(
    expr: Expression, definitions={}
) -> Iterator[Expression]:
    """
    Reduce expression by yeild each intermediate stage after reducing
    """

    # Reduce original expression
    reduced = reduce(expr, defns=definitions)

    # If original expression is already reduced, yeild expr as is
    if reduced == expr:
        yield expr

    # Continue to reduce and yield intermediate stages
    while reduced != expr:
        expr = reduced
        reduced = reduce(expr, defns=definitions)

        yield expr

