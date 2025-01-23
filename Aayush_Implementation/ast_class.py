from dataclasses import dataclass
from decimal import Decimal, getcontext

getcontext().prec = 20

class AST:
    pass

@dataclass
class BinOp(AST):
    op: str
    left: AST
    right: AST

@dataclass
class Number(AST):
    val: str 

@dataclass
class If(AST):
    c: AST
    t: AST
    e: AST

def e(tree: AST) -> Decimal:
    match tree:
        case Number(v): return Decimal(v)
        case BinOp("+", l, r): return e(l) + e(r)
        case BinOp("-", l, r): return e(l) - e(r)
        case BinOp("*", l, r): return e(l) * e(r)
        case BinOp("/", l, r): return e(l) / e(r)
        case BinOp("^", l, r): return e(l) ** e(r)
        case BinOp("<", l, r): return e(l) < e(r)
        case BinOp(">", l, r): return e(l) > e(r)
        case BinOp("==", l, r): return e(l) <= e(r)
        case If(cond, then, else_):
            if e(cond):
                return e(then)
            else:
                return e(else_)
        case _: raise ValueError("Unsupported AST node")