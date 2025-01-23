from dataclasses import dataclass
from lexer import IntToken, FloatToken, StringToken, BoolToken

# Abstract Syntax Tree classes
class AST:
    pass

@dataclass
class BinOp(AST):
    op: str
    left: AST
    right: AST
    _fields = ('op', 'left', 'right')

@dataclass
class Number(AST):
    v: IntToken | FloatToken | StringToken
    _fields = ('val',)

@dataclass
class If(AST):
    c: AST
    t: AST
    e: AST

def e(tree: AST) -> IntToken | FloatToken | StringToken | BoolToken :
    match tree:
        case Number(v):
            return v
        case BinOp("+", l, r):
            left = e(l)
            right = e(r)
            if isinstance(left, (IntToken, FloatToken)) and isinstance(right, (IntToken, FloatToken)):
                if isinstance(left, FloatToken) or isinstance(right, FloatToken):
                    return FloatToken(left.v + right.v)
                return IntToken(left.v + right.v)
            elif isinstance(left, StringToken) and isinstance(right, StringToken):
                return StringToken(left.v + right.v)
            else:
                raise TypeError(f"Invalid operation: {type(left).__name__} + {type(right).__name__}")
        case BinOp("*", l, r):
            left = e(l)
            right = e(r)
            if isinstance(left, StringToken) and isinstance(right, IntToken):
                return StringToken(left.v * right.v)
            elif isinstance(left, IntToken) and isinstance(right, StringToken):
                return StringToken(right.v * left.v)
            elif isinstance(left, (IntToken, FloatToken)) and isinstance(right, (IntToken, FloatToken)):
                if isinstance(left, FloatToken) or isinstance(right, FloatToken):
                    return FloatToken(left.v * right.v)
                return IntToken(left.v * right.v)
            else:
                raise TypeError(f"Invalid operation: {type(left).__name__} * {type(right).__name__}")
        case BinOp("-", l, r):
            left = e(l)
            right = e(r)
            if isinstance(left, (IntToken, FloatToken)) and isinstance(right, (IntToken, FloatToken)):
                if isinstance(left, FloatToken) or isinstance(right, FloatToken):
                    return FloatToken(left.v - right.v)
                return IntToken(left.v - right.v)
            else:
                raise TypeError(f"Invalid operation: {type(left).__name__} - {type(right).__name__}")
        case BinOp("/", l, r):
            left = e(l)
            right = e(r)
            if isinstance(left, (IntToken, FloatToken)) and isinstance(right, (IntToken, FloatToken)):
                if right.v == 0:
                    raise ZeroDivisionError("Division by zero")
                return FloatToken(left.v / right.v)
            else:
                raise TypeError(f"Invalid operation: {type(left).__name__} / {type(right).__name__}")
        case BinOp("^", l, r):
            left = e(l)
            right = e(r)
            if isinstance(left, (IntToken, FloatToken)) and isinstance(right, (IntToken, FloatToken)):
                if isinstance(left, FloatToken) or isinstance(right, FloatToken):
                    return FloatToken(left.v ** right.v)
                return IntToken(left.v ** right.v)
            else:
                raise TypeError(f"Invalid operation: {type(left).__name__} ^ {type(right).__name__}")
        case BinOp("<", l, r): return BoolToken(e(l) < e(r))
        case If(cond, then, else_):
            if e(cond):
                return e(then)
            else:
                return e(else_)
        case _:
            raise ValueError("Unknown AST node")

