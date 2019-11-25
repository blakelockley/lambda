from typing import Iterator
from .ltypes import Definition
from .lparser import parse_expression
from .lanalyser import analyse_definitions
from .lreducer import reduce_expression, generate_reduced_expressions
from .debug import print_debug

WELCOME_MESSAGE = """* Welcome to the lambda REPL!
* Hint: You can use '\\' to represent to lambda character (λ)."""

REPL_PROMPT = ">>> "
EXIT_COMMANDS = set(["exit", "quit", "q"])


def print_expr(expr):
    output = str(expr).replace("\\", "λ")  # Revert slashes for printing
    print(output)


def run_repl(args):
    print(WELCOME_MESSAGE)

    # Store definitions
    defns = {}

    # Proccess switches in args
    verbose = any([True for opt in args if opt in ("-v", "--verbose")])

    # Set reducer based on verbose switch
    reducer = reduce_expression
    if verbose:
        print("* Running in verbose mode.")
        reducer = generate_reduced_expressions

    # Loop
    while True:

        # Read
        line = input(REPL_PROMPT)
        line = line.strip()
        line = line.replace("λ", "\\")  # Replace λ with substitued lambda characted

        if line == "":
            continue

        if line in EXIT_COMMANDS:
            break

        try:
            # Evaluate
            expr = parse_expression(line)
            expr = analyse_definitions(expr, defns)
            reduced = reducer(expr)

            # Store definition
            if isinstance(expr, Definition):
                defns[expr.name] = expr

            # Print
            elif isinstance(reduced, Iterator):
                for expr in reduced:
                    print_expr(expr)

            else:
                print_expr(reduced)

        except Exception as e:
            print(f"{e.__class__.__name__}: {e}")
