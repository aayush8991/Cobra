from dataclasses import dataclass

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

expr_t1 = BinOp("+", Number("2"), BinOp("*", Number("3"), Number("5")))
# print(expr_t1)

def e(tree: AST) -> int:
    match tree:
        case Number(v): return int(v)
        case BinOp("+", l, r): return e(l) + e(r)
        case BinOp("-", l, r): return e(l) - e(r)
        case BinOp("*", l, r): return e(l) * e(r)
        case _: raise ValueError("Unsupported AST node")

# print(e(expr_t1))

class Token:
    pass

@dataclass
class NumberToken(Token):
    v: str

@dataclass
class OperatorToken(Token):
    o: str

from collections.abc import Iterator
def lex(s: str) -> Iterator[Token]:
    i = 0
    while True:
        while i < len(s) and s[i].isspace():
            i = i + 1

        if i >= len(s):
            return

        if s[i].isdigit():
            t = s[i]
            i = i + 1
            while i < len(s) and s[i].isdigit():
                t = t + s[i]
                i = i + 1
            yield NumberToken(t)
        else:
            match t := s[i]:
                case '+' | '*' | '-':
                    i = i + 1
                    yield OperatorToken(t)

# for t in lex("2 + 3*5"):
#     print(t)

from collections.abc import Iterator
def parse(s: str) -> AST:
    from more_itertools import peekable
    t = peekable(lex(s))

    def parse_add():
        ast = parse_sub()
        while True:
            match t.peek(None):
                case OperatorToken('+'):
                    next(t)
                    ast = BinOp('+', ast, parse_sub())
                case _:
                    if ast is not None:
                        return ast
                    else:
                        raise ValueError("Invalid syntax")
    def parse_sub():
        ast = parse_mul()
        while True:
            match t.peek(None):
                case OperatorToken('-'):
                    next(t)
                    ast = BinOp('-', ast, parse_mul())
                case _:
                    return ast

    def parse_mul():
        ast = parse_atom()
        while True:
            match t.peek(None):
                case OperatorToken('*'):
                    next(t)
                    ast = BinOp("*", ast, parse_atom())
                case _:
                    return ast

    def parse_atom():
        match t.peek(None):
            case NumberToken(v):
                next(t)
                return Number(v)
            case _:
                raise ValueError("Invalid syntax")

    result = parse_add()
    if result is None:
        raise ValueError("Invalid syntax")
    return result

# print(parse("2+3*5"))

print(e(parse("2 - 1 * 1 + 5")))