from tree import AST, BinOp, If
from lexer import *
from more_itertools import peekable

def parse(s: str) -> AST:
    t = peekable(lex(s))
    
    def expect(what: Token):
        if t.peek(None) == what:
            next(t)
            return
        raise ParseError
    
    def parse_braced_expr():
        expect(OperatorToken('{'))
        expr = parse_if()
        expect(OperatorToken('}'))
        return expr

    def parse_if():
        match t.peek(None):
            case KeywordToken("if"):
                next(t)
                cond = parse_braced_expr()
                expect(KeywordToken("then"))
                then = parse_braced_expr()
                expect(KeywordToken("else"))
                else_ = parse_braced_expr()
                expect(KeywordToken("end"))
                return If(cond, then, else_)
            case _:
                return parse_cmp()

    def parse_cmp():
        l = parse_sub()
        if t.peek(None) == OperatorToken('<'):
            next(t)
            r = parse_sub()
            return BinOp('<', l, r)
        elif t.peek(None) == OperatorToken('>'):
            next(t)
            r = parse_sub()
            return BinOp('>', l, r)
        elif t.peek(None) == OperatorToken('=='):
            next(t)
            r = parse_sub()
            return BinOp('==', l, r)
        else:
            return l

    def parse_sub():
        ast = parse_add()
        while True:
            match t.peek(None):
                case OperatorToken('-'):
                    next(t)
                    ast = BinOp('-', ast, parse_add())
                case _:
                    return ast
                    
    def parse_add():
        ast = parse_mul()
        while True:
            match t.peek(None):
                case OperatorToken('+'):
                    next(t)
                    ast = BinOp('+', ast, parse_mul())
                case _:
                    return ast

    def parse_mul():
        ast = parse_div()
        while True:
            match t.peek(None):
                case OperatorToken('*'):
                    next(t)
                    ast = BinOp("*", ast, parse_div())
                case _:
                    return ast
    
    def parse_div():
        ast = parse_pow()
        match t.peek(None):
            case OperatorToken('/'):
                next(t)
                ast = BinOp("/", ast, parse_div())
        return ast
    
    def parse_pow():
        ast = parse_atom()
        match t.peek(None):
            case OperatorToken('^'):
                next(t)
                ast = BinOp("^", ast, parse_pow())
        return ast

    def parse_atom():
        match t.peek(None):
            case IntToken(v):
                next(t)
                return IntToken(v)
            case FloatToken(v):
                next(t)
                return FloatToken(v)
            case StringToken(v):
                next(t)
                return StringToken(v)
            case OperatorToken('('):
                next(t)
                expr = parse_sub()  # Parse the expression inside the parentheses
                match t.peek(None):
                    case OperatorToken(')'):
                        next(t)
                        return expr
                    case _:
                        raise ValueError("Missing closing parenthesis")
            case _:
                raise ValueError("Unexpected token in expression")

    result = parse_if()
    if result is None:
        raise ValueError("Invalid syntax")
    return result