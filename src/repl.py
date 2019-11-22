from .lparser import parse_expression
from .lreducer import reduce_expression
from .debug import print_debug

WELCOME_MESSAGE = """* Welcome to the lambda REPL!
* Hint: You can use '\\' to represent to lambda character (λ)."""

REPL_PROMPT = ">>> "
EXIT_COMMANDS = set(["exit", "quit", "q"])


def run_repl(args):
    print(WELCOME_MESSAGE)

    # Loop
    while True:

        # Read
        line = input(REPL_PROMPT)
        line = line.replace("λ", "\\")  # Replace λ with substitued lambda characted

        if line in EXIT_COMMANDS:
            break

        try:
            # Evaluate
            expr = parse_expression(line)
            reduced = reduce_expression(expr)

            # Print
            output = str(reduced).replace("\\", "λ")  # Revert slashes for printing
            print(output)

        except Exception as e:
            print(f"{e.__class__.__name__}: {e}")

