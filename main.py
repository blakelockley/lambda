import sys
from src.repl import run_repl
from src.levaluator import evaluate_file

if __name__ == "__main__":
    args = sys.argv

    if "-c" in args and len(args) >= 3:
        filename = args[2]
        evaluate_file(filename)

    else:
        run_repl(sys.argv)
