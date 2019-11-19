import re
import ltypes


def parse(source: str):

    definition = re.compile(r"([a-zA-Z]\w+)\s*=\s*(.*)")
    function = re.compile(r"\\(.*)\.(.*)")

    lines = source.split("\n")
    for line in lines:
        m = definition.match(line)
        if m:
            symbol = m.group(1)
            expr = m.group(2)

