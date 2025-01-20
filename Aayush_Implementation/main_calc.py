from parser import *
from ast_class import *

if __name__ == "__main__":
    expr = "if {2 < 3} then { if {4>5} then {10 + 10} else {100+100} end } else {1 + 2 + 2} end"
    ast = parse(expr)
    result = e(ast)
    print(result)