from tree import *
from lexer import *
from more_itertools import peekable
from decimal import Decimal

def parse(s: str) -> AST:
    t = peekable(lex(s))
    def expect(what: Token):
        if t.peek(None) == what:
            next(t)
            return
        raise ParseError
    
    def parse_braced_expr():
        expect(OperatorToken('{'))
        expr = parse_let()
        expect(OperatorToken('}'))
        return expr

    def parse_let():
        match t.peek(None):
            case KeywordToken("let"):
                next(t)
                vt = next(t)
                expect(KeywordToken("be"))
                e = parse_let()
                expect(KeywordToken("in"))
                f = parse_let()
                expect(KeywordToken("end"))
                return Let(Var(vt.v), e, f)
            case _:
                return parse_fun()

    # def parse_fun():
    #     match t.peek(None):
    #         case KeywordToken("fun"):
    #             next(t)
    #             name = next(t)
    #             expect(OperatorToken('('))
    #             parameters = next(t)
    #             expect(OperatorToken(')'))
    #             expect(KeywordToken("is"))
    #             body = parse_braced_expr()
    #             expect(KeywordToken("in"))
    #             expr = parse_let()
    #             expect(KeywordToken("end"))
    #             return Fun(name.v, Var(parameters.v), body, expr)
    #         case _:
    #             return parse_if()
    def parse_fun():
        match t.peek(None):
            case KeywordToken("fun"):
                next(t)
                expect(OperatorToken('('))
                parameters = []
                while t.peek(None) != OperatorToken(')'):
                    parameters.append(Var(next(t).v))
                    if t.peek(None) == OperatorToken(','):
                        next(t)
                expect(OperatorToken(')'))  
                expect(KeywordToken("is"))
                body = parse_braced_expr()
                return Fun(parameters, body)
            case _:
                return parse_if()

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
                return parse_while()
            
    def parse_while():
        match t.peek(None):
            case KeywordToken("while"):
                next(t)
                cond = parse_braced_expr()
                expect(KeywordToken("do"))
                body_expr = []
                while t.peek(None) != KeywordToken("end"):
                    body_expr.append(parse_braced_expr())
    
                expect(KeywordToken("end"))
                return While(cond, body_expr)
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
        elif t.peek(None) == OperatorToken('!='):
            next(t)
            r = parse_sub()
            return BinOp('!=', l, r)
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
                expr = parse_let()  # Parse the expression inside the parentheses
                match t.peek(None):
                    case OperatorToken(')'):
                        next(t)
                        return expr
                    case _:
                        raise ValueError("Missing closing parenthesis")
            case OperatorToken('['):
                next(t)
                elements = []
                while t.peek(None) != OperatorToken(']'):
                    elements.append(parse_let())
                    if t.peek(None) == OperatorToken(','):
                        next(t)
                expect(OperatorToken(']'))
                return Array(elements)   
            case VariableToken(v):
                var_name = next(t).v
                if t.peek(None) == OperatorToken('['):
                    # Array indexing
                    array_var = Var(var_name)
                    expect(OperatorToken('['))
                    index = parse_let()
                    expect(OperatorToken(']'))
                    if t.peek(None) == OperatorToken(':='):
                        # Array assignment
                        expect(OperatorToken(':='))
                        value = parse_let()
                        return ArrayAssign(array_var, index, value)
                    return ArrayIndex(array_var, index)
                if t.peek(None) == OperatorToken('('):
                    expect(OperatorToken('('))
                    args = []
                    while t.peek(None) != OperatorToken(')'):
                        args.append(parse_let())
                        if t.peek(None) == OperatorToken(','):
                            next(t)
                    expect(OperatorToken(')'))
                    return Call(Var(var_name), args)
                elif t.peek(None) == OperatorToken(':='):
                    expect(OperatorToken(':='))
                    arg = parse_let()
                    return Assign(var_name, arg)
                return Var(var_name)
            case _:
                raise ValueError("Unexpected token in expression")

    result = parse_let()
    if result is None:
        raise ValueError("Invalid syntax")
    return result
