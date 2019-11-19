from parser import parse
from debug import print_debug

text_I = r"I = \x.xy"
text_0 = r"0 = \s.(\z.z)"
text_1 = r"1 = \sz.s(z)"
text_S = r"S = \w.(\y.(\x.y(wyx)))"

text = text_S

defns = parse(text)

print(text)
for defn in defns.values():
    print(repr(defn))
    print_debug(defn)
