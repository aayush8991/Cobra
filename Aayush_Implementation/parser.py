from collections.abc import Iterator
from more_itertools import peekable
from lexer import lex
from ast_class import *
from token_class import *

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
        l = parse_add()
        if t.peek(None) == OperatorToken('<'):
            next(t)
            r = parse_add()
            return BinOp('<', l, r)
        elif t.peek(None) == OperatorToken('>'):
            next(t)
            r = parse_add()
            return BinOp('>', l, r)
        elif t.peek(None) == OperatorToken('=='):
            next(t)
            r = parse_add()
            return BinOp('==', l, r)
        else:
            return l

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
        while True:
            match t.peek(None):
                case OperatorToken('/'):
                    next(t)
                    ast = BinOp('/', ast, parse_pow())
                case _:
                    return ast
                
    # def parse_pow():              # For left associativity
    #     ast = parse_atom()
    #     while True:             
    #         match t.peek(None):
    #             case OperatorToken('^'):
    #                 next(t)
    #                 ast = BinOp('^', ast, parse_atom())
    #             case _:
    #                 return ast

    def parse_pow():
        ast = parse_atom()  # Parse the left-hand side (base)
        match t.peek(None):
            case OperatorToken('^'):  # Check if the current token is '^'
                next(t)  # Consume the '^' operator
                # Recursively parse the right-hand side
                ast = BinOp('^', ast, parse_pow())  
        return ast


    def parse_atom():
        match t.peek(None):
            case NumberToken(v):
                next(t)
                return Number(v)
            case OperatorToken('('):    # If the next token is an opening bracket
                next(t)                 # Consume the '('
                ast = parse_add()       # Parse the expression inside the brackets
                match t.peek(None):
                    case OperatorToken(')'):    # Ensure there's a closing bracket
                        next(t)                 # Consume the ')'
                        return ast
                    case _:
                        raise ValueError("Expected closing bracket ')'")
            case _:
                raise ValueError("Invalid syntax")

    result = parse_if()
    if result is None:
        raise ValueError("Invalid syntax")
    return result