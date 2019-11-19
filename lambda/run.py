from parser import parse
from debug import print_debug

text_I = r"I = \x.xy"
text_0 = r"0 = \s.(\z.z)"
text_1 = r"1 = \sz.s(z)"
text_S = r"S = \w.(\y.(\x.y(wyx)))"
text_M = r"M = (\xyz.x(yz))(\sz.(sz))(\sz.(sz))"
text_A = r"A = (\x.x)y"
text_Z = r"Z = \xy.xyz"

text = text_M

defns = parse(text)

print(text)
for defn in defns.values():
    print(repr(defn))
    print_debug(defn)
