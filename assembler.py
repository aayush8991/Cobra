from tree import *
from lexer import *

HALT, NOP, PUSH, POP, ADD, SUB, MUL, NEG = range(8)

def do_codegen(t: AST, code):
    match t:
        case IntToken(v): 
            code.append(PUSH)
            code.append(int(v))
        case BinOp("+", l, r):
            do_codegen(l, code)
            do_codegen(r, code)
            code.append(ADD)
            code.append(0)
        case BinOp("-", l, r):
            do_codegen(l, code)
            do_codegen(r, code)
            code.append(SUB)
            code.append(0)
        case BinOp("*", l, r):
            do_codegen(l, code)
            do_codegen(r, code)
            code.append(MUL)
            code.append(0)
    return code

def codegen(t):
    c = do_codegen(t, bytearray())
    c.append(HALT)
    return c

expr_cg = BinOp ("*", BinOp("+", IntToken("2"), IntToken("3"), IntToken("5")))