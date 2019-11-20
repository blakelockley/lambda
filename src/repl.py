from .lparser import parse_expression
from .lreducer import reduce_expression
from .debug import print_debug

WELCOME_MESSAGE = """* Welcome to the lambda REPL!
* Hint: You can use '\\' to represent to lambda character (λ).
"""

REPL_PROMPT = "λ "
EXIT_COMMANDS = set(["exit", "quit", "q"])


def run_repl(args):
    print(WELCOME_MESSAGE)

    while True:
        line = input(REPL_PROMPT)

        if line in EXIT_COMMANDS:
            break

        # Replace
        line = line.replace("λ", "\\")

        expr = parse_expression(line)
        reduced = reduce_expression(expr)

        output = str(reduced).replace("\\", "λ")
        print("--> ", output)
